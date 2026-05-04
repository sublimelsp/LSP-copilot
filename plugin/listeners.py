from __future__ import annotations

import asyncio
import re
import threading
from collections.abc import Iterable
from typing import Any, final

import sublime
import sublime_plugin
from typing_extensions import override
from watchfiles import Change, awatch

from .client import CopilotPlugin
from .constants import PACKAGE_NAME
from .decorators import must_be_active_view
from .helpers import CopilotIgnore
from .ui import ViewCompletionManager, ViewPanelCompletionManager, WindowConversationManager
from .utils import all_windows, get_copilot_view_setting, get_session_setting, set_copilot_view_setting


class ViewEventListener(sublime_plugin.ViewEventListener):
    def __init__(self, view: sublime.View) -> None:
        super().__init__(view)

    @classmethod
    @override
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
        vcm.handle_text_change()

        if not self._is_saving and get_session_setting(session, "auto_ask_completions") and not vcm.is_waiting:
            plugin.request_get_completions(self.view)

    def on_activated_async(self) -> None:
        self.view.run_command("lsp_check_applicable", {"session_name": PACKAGE_NAME})
        _, session = CopilotPlugin.plugin_session(self.view)
        if session and CopilotPlugin.is_applicable(self.view, session.config):
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

    def on_load_project_async(self, window: sublime.Window) -> None:
        copilot_file_watcher.add_folders(window.folders())

    def on_new_project_async(self, window: sublime.Window) -> None:
        copilot_file_watcher.add_folders(window.folders())

    def on_new_window_async(self, window: sublime.Window) -> None:
        copilot_file_watcher.add_folders(window.folders())

    def on_pre_close_window_async(self, window: sublime.Window) -> None:
        copilot_file_watcher.remove_folders(window.folders())


@final
class CopilotFileWatcher:
    def __init__(self, folders: Iterable[str] | None = None) -> None:
        self._folders = set(folders or [])
        self._thread: threading.Thread | None = None
        self._stop_event: asyncio.Event | None = None

    def setup(self) -> None:
        self._stop_event = asyncio.Event()
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def cleanup(self) -> None:
        if self._stop_event is not None:
            self._stop_event.set()
        if self._thread is not None and self._thread.is_alive():
            self._thread.join(timeout=5)
        self._thread = None
        self._stop_event = None

    def _run(self) -> None:
        asyncio.run(self._awatch_loop())

    async def _awatch_loop(self) -> None:
        async for changes in awatch(
            *self._folders,
            recursive=False,
            stop_event=self._stop_event,
            rust_timeout=1000,
            yield_on_timeout=True,
        ):
            self._on_changes(changes)

    def _on_changes(self, changes: set[tuple[Change, str]]) -> None:
        for _change, path in changes:
            print(f"[😀] Detected change in: {_change = } ; {path = }")
            if not path.endswith(".copilotignore"):
                continue
            for window in all_windows():
                if any(path.startswith(folder) for folder in window.folders()):
                    sublime.set_timeout_async(lambda w=window: CopilotIgnore(w).load_patterns())
                    return

    def add_folders(self, folders: Iterable[str]) -> None:
        print(f"[😀 add_folders] Starting file watcher for folders: {self._folders}")
        changed = False
        for folder in folders:
            if folder not in self._folders:
                self._folders.add(folder)
                changed = True
        if changed:
            self._restart()

    def remove_folders(self, folders: list[str]) -> None:
        print(f"[😀 remove_folders] Starting file watcher for folders: {self._folders}")
        changed = False
        for folder in folders:
            if folder in self._folders:
                self._folders.remove(folder)
                changed = True
        if changed:
            self._restart()

    def _restart(self) -> None:
        self.cleanup()
        self.setup()


copilot_file_watcher = CopilotFileWatcher()
