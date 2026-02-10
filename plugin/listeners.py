from __future__ import annotations

import re
from collections.abc import Iterable
from typing import Any

import sublime
import sublime_plugin
from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer
from watchdog.observers.api import ObservedWatch

from .client import CopilotPlugin
from .decorators import must_be_active_view
from .helpers import CopilotIgnore
from .ui import ViewCompletionManager, ViewPanelCompletionManager, WindowConversationManager
from .utils import all_windows, get_copilot_view_setting, get_session_setting, set_copilot_view_setting


class ViewEventListener(sublime_plugin.ViewEventListener):
    def __init__(self, view: sublime.View) -> None:
        super().__init__(view)

    @classmethod
    def applies_to_primary_view_only(cls) -> bool:
        # To fix "https://github.com/TerminalFi/LSP-copilot/issues/102",
        # let cloned views trigger their event listeners too.
        # But we guard some of event listeners only work for the activate view.
        return False

    @property
    def _is_modified(self) -> bool:
        return get_copilot_view_setting(self.view, "_is_modified", False)

    @_is_modified.setter
    def _is_modified(self, value: bool) -> None:
        set_copilot_view_setting(self.view, "_is_modified", value)

    @property
    def _is_saving(self) -> bool:
        return get_copilot_view_setting(self.view, "_is_saving", False)

    @_is_saving.setter
    def _is_saving(self, value: bool) -> None:
        set_copilot_view_setting(self.view, "_is_saving", value)

    @must_be_active_view()
    def on_modified_async(self) -> None:
        self._is_modified = True

        plugin, session = CopilotPlugin.plugin_session(self.view)
        if not plugin or not session:
            return

        vcm = ViewCompletionManager(self.view)
        if vcm.handle_text_change():
            return

        if not self._is_saving and get_session_setting(session, "auto_ask_completions") and not vcm.is_waiting:
            plugin.request_get_completions(self.view)

    def on_activated_async(self) -> None:
        _, session = CopilotPlugin.plugin_session(self.view)

        #        if (session and CopilotPlugin.should_ignore(self.view)) or (
        #            not session and not CopilotPlugin.should_ignore(self.view)
        #        ):
        # Hacky way to trigger adding and removing views from session
        #           prev_setting = self.view.settings().get("lsp_uri")
        #           self.view.settings().set("lsp_uri", "")
        #           sublime.set_timeout_async(lambda: self.view.settings().set("lsp_uri", prev_setting), 5)

        if session and not CopilotPlugin.should_ignore(self.view):
            if (window := self.view.window()) and self.view.name() != "Copilot Chat":
                WindowConversationManager(window).last_active_view_id = self.view.id()

    def on_deactivated_async(self) -> None:
        ViewCompletionManager(self.view).hide()

    def on_pre_close(self) -> None:
        # close corresponding panel completion
        ViewPanelCompletionManager(self.view).close()

    def on_close(self) -> None:
        ViewCompletionManager(self.view).handle_close()

    def on_query_context(self, key: str, operator: int, operand: Any, match_all: bool) -> bool | None:
        def test(value: Any) -> bool | None:
            if operator == sublime.OP_EQUAL:
                return value == operand
            if operator == sublime.OP_NOT_EQUAL:
                return value != operand
            return None

        if key == "copilot.has_signed_in":
            return test(CopilotPlugin.get_account_status().has_signed_in)

        if key == "copilot.is_authorized":
            return test(CopilotPlugin.get_account_status().is_authorized)

        if key == "copilot.is_on_completion":
            if not (
                (vcm := ViewCompletionManager(self.view)).is_visible
                and len(self.view.sel()) >= 1
                and vcm.current_completion
            ):
                return test(False)

            point = self.view.sel()[0].begin()
            line = self.view.line(point)
            beginning_of_line = self.view.substr(sublime.Region(line.begin(), point))

            return test(beginning_of_line.strip() != "" or not re.match(r"\s", vcm.current_completion["displayText"]))

        plugin, session = CopilotPlugin.plugin_session(self.view)
        if not plugin or not session:
            return None

        if key == "copilot.commit_completion_on_tab":
            return test(get_session_setting(session, "commit_completion_on_tab"))

        return None

    def on_post_text_command(self, command_name: str, args: dict[str, Any] | None) -> None:
        if command_name == "lsp_save":
            self._is_saving = True

        if command_name == "auto_complete":
            plugin, session = CopilotPlugin.plugin_session(self.view)
            if plugin and session and get_session_setting(session, "hook_to_auto_complete_command"):
                plugin.request_get_completions(self.view)

    def on_post_save_async(self) -> None:
        self._is_saving = False

    @must_be_active_view()
    def on_selection_modified_async(self) -> None:
        if not self._is_modified:
            ViewCompletionManager(self.view).handle_selection_change()

        self._is_modified = False


class EventListener(sublime_plugin.EventListener):
    def on_window_command(
        self,
        window: sublime.Window,
        command_name: str,
        args: dict[str, Any] | None,
    ) -> tuple[str, dict[str, Any] | None] | None:
        sheet = window.active_sheet()

        # if the user tries to close panel completion via Ctrl+W
        if (
            isinstance(sheet, sublime.HtmlSheet)
            and command_name in {"close", "close_file"}
            and (vcm := ViewPanelCompletionManager.from_sheet_id(sheet.id()))
        ):
            vcm.close()
            return "noop", None

        return None

    def on_new_window(self, window: sublime.Window) -> None:
        copilot_ignore_observer.add_folders(window.folders())

    def on_pre_close_window(self, window: sublime.Window) -> None:
        copilot_ignore_observer.remove_folders(window.folders())


class CopilotIgnoreHandler(FileSystemEventHandler):
    def __init__(self) -> None:
        self.filename = ".copilotignore"

    def on_modified(self, event: FileSystemEvent) -> None:
        if not event.is_directory and event.src_path.endswith(self.filename):
            self.update_window_patterns(event.src_path)

    def on_created(self, event: FileSystemEvent) -> None:
        if not event.is_directory and event.src_path.endswith(self.filename):
            self.update_window_patterns(event.src_path)

    def update_window_patterns(self, path: str) -> None:
        for window in all_windows():
            if not self._best_matched_folder(path, window.folders()):
                continue
            # Update patterns for specific window and folder
            CopilotIgnore(window).load_patterns()
            return

    def _best_matched_folder(self, path: str, folders: list[str]) -> str | None:
        matching_folder = None
        for folder in folders:
            if path.startswith(folder) and (matching_folder is None or len(folder) > len(matching_folder)):
                matching_folder = folder
        return matching_folder


class CopilotIgnoreObserver:
    def __init__(self, folders: Iterable[str] | None = None) -> None:
        self.observer = Observer()
        self._event_handler = CopilotIgnoreHandler()
        self._folders = list(folders or [])
        self._scheduler: dict[str, ObservedWatch] = {}

    def setup(self) -> None:
        self.add_folders(self._folders)
        self.observer.start()

    def cleanup(self) -> None:
        self.observer.stop()
        self.observer.join()

    def add_folders(self, folders: Iterable[str]) -> None:
        for folder in folders:
            self.add_folder(folder)

    def add_folder(self, folder: str) -> None:
        if folder not in self._folders:
            self._folders.append(folder)
        observer = self.observer.schedule(self._event_handler, folder, recursive=False)
        self._scheduler[folder] = observer

    def remove_folders(self, folders: list[str]) -> None:
        for folder in folders:
            self.remove_folder(folder)

    def remove_folder(self, folder: str) -> None:
        if folder in self._folders:
            self._folders.remove(folder)
            self.observer.unschedule(self._scheduler[folder])


copilot_ignore_observer = CopilotIgnoreObserver()
