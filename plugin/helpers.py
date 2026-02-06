from __future__ import annotations

import itertools
import os
import re
import subprocess
import threading
import time
from operator import itemgetter
from pathlib import Path
from typing import Any, Callable, Literal, Sequence, cast

import requests
import sublime
from LSP.plugin.core.protocol import Position as LspPosition
from LSP.plugin.core.protocol import Range as LspRange
from LSP.plugin.core.url import filename_to_uri
from more_itertools import duplicates_everseen, first_true
from wcmatch import glob

from .constants import COPILOT_WINDOW_SETTINGS_PREFIX, PACKAGE_NAME
from .log import log_error
from .settings import get_plugin_setting_dotted
from .types import (
    CopilotConversationTemplates,
    CopilotDocType,
    CopilotGitHubWebSearch,
    CopilotPayloadCompletion,
    CopilotPayloadPanelSolution,
    CopilotRequestConversationTurn,
    CopilotRequestConversationTurnReference,
    CopilotUserDefinedPromptTemplates,
)
from .utils import (
    all_views,
    all_windows,
    drop_falsy,
    erase_copilot_setting,
    erase_copilot_view_setting,
    get_copilot_setting,
    get_project_relative_path,
    get_view_language_id,
    set_copilot_setting,
)


class ActivityIndicator:
    def __init__(self, callback: Callable[[dict[str, Any]], None] | None = None) -> None:
        self.thread: threading.Thread | None = None
        self.animation = ["⣷", "⣯", "⣟", "⡿", "⢿", "⣻", "⣽", "⣾"]  # taken from Package Control
        self.animation_cycled = itertools.cycle(self.animation)
        self.callback = callback
        self.stop_event = threading.Event()

    def start(self) -> None:
        if not (self.thread and self.thread.is_alive()):
            self.stop_event.clear()
            self.thread = threading.Thread(target=self._run, daemon=True)
            self.thread.start()

    def stop(self) -> None:
        if self.thread:
            self.stop_event.set()
            self.thread.join()
            if self.callback:
                self.callback({"is_waiting": ""})

    def _run(self) -> None:
        while not self.stop_event.is_set():
            if self.callback:
                self.callback({"is_waiting": next(self.animation_cycled)})
            time.sleep(0.1)


class GithubInfo:
    AVATAR_PATH = Path(sublime.cache_path()) / f"{PACKAGE_NAME}/avatar.png"
    AVATAR_RESOURCE_URL = f"res://Cache/{PACKAGE_NAME}/avatar.png"

    @classmethod
    def get_avatar_img_src(cls) -> str:
        return cls.AVATAR_RESOURCE_URL if cls.AVATAR_PATH.is_file() else ""

    @classmethod
    def fetch_avatar(cls, username: str, *, size: int = 64) -> None:
        """If there is no cached avatar, fetches the avatar from GitHub and saves it to the cache."""
        if not username:
            log_error("No username provided for fetching avatar.")
            return

        cls.update_avatar(username, size=size)

    @classmethod
    def update_avatar(cls, username: str, *, size: int = 64) -> None:
        """Updates the avatar from GitHub and saves it to the cache directory."""
        if not username:
            cls.clear_avatar()
            return

        if (req := requests.get(f"https://github.com/{username}.png?size={size}")).ok:
            data = req.content
        # see https://github.com/TerminalFi/LSP-copilot/issues/218#issuecomment-2535522265
        elif req.status_code == 404:
            data = sublime.load_binary_resource(f"Packages/{PACKAGE_NAME}/plugin/assets/white-pixel.png")
        else:
            log_error(f'Failed to fetch avatar for "{username}" with status code {req.status_code}.')
            cls.clear_avatar()
            return

        cls.AVATAR_PATH.parent.mkdir(parents=True, exist_ok=True)
        cls.AVATAR_PATH.write_bytes(data)

    @classmethod
    def clear_avatar(cls) -> None:
        cls.AVATAR_PATH.unlink(missing_ok=True)


class CopilotIgnore:
    def __init__(self, window: sublime.Window) -> None:
        self.window = window
        self.patterns: dict[str, list[str]] = {}
        self.load_patterns()

    @classmethod
    def cleanup(cls) -> None:
        for window in all_windows():
            erase_copilot_setting(window, COPILOT_WINDOW_SETTINGS_PREFIX, "copilotignore.patterns")
        for view in all_views():
            erase_copilot_view_setting(view, "is_copilot_ignored")

    def unload_patterns(self) -> None:
        self.patterns.clear()
        erase_copilot_setting(self.window, COPILOT_WINDOW_SETTINGS_PREFIX, "copilotignore.patterns")

    def load_patterns(self) -> None:
        self.patterns.clear()

        # Load workspace patterns
        for folder in self.window.folders():
            self.add_patterns_from_file(os.path.join(folder, ".copilotignore"), folder)

        set_copilot_setting(self.window, COPILOT_WINDOW_SETTINGS_PREFIX, "copilotignore.patterns", self.patterns)

    def read_ignore_patterns(self, file_path: str) -> list[str]:
        if os.path.isfile(file_path):
            with open(file_path, encoding="utf-8") as f:
                return list(drop_falsy(map(str.strip, f)))
        return []

    def add_patterns_from_file(self, file_path: str, folder: str) -> None:
        if patterns := self.read_ignore_patterns(file_path):
            self.patterns[folder] = patterns

    def matches_any_pattern(self, file_path: str | Path) -> bool:
        file_path = Path(file_path)
        loaded_patterns: dict[str, list[str]] = get_copilot_setting(
            self.window,
            COPILOT_WINDOW_SETTINGS_PREFIX,
            "copilotignore.patterns",
            self.patterns,
        )
        for folder, patterns in loaded_patterns.items():
            try:
                relative_path = file_path.relative_to(folder).as_posix()
            except ValueError:
                continue
            if glob.globmatch(relative_path, patterns, flags=glob.GLOBSTAR):
                return True
        return False

    def trigger(self, view: sublime.View) -> bool:
        if self.patterns and (file := view.file_name()):
            return self.matches_any_pattern(file)
        return False


def st_point_to_lsp_position(point: int, view: sublime.View) -> LspPosition:
    row, col = view.rowcol_utf16(point)
    return {"line": row, "character": col}


def lsp_position_to_st_point(position: LspPosition, view: sublime.View) -> int:
    return view.text_point_utf16(position["line"], position["character"])


def st_region_to_lsp_range(region: sublime.Region, view: sublime.View) -> LspRange:
    return {
        "start": st_point_to_lsp_position(region.begin(), view),
        "end": st_point_to_lsp_position(region.end(), view),
    }


def lsp_range_to_st_region(range_: LspRange, view: sublime.View) -> sublime.Region:
    return sublime.Region(
        lsp_position_to_st_point(range_["start"], view),
        lsp_position_to_st_point(range_["end"], view),
    )


def prepare_code_review_request_doc(view: sublime.View):
    selection = view.sel()[0]
    file_path = view.file_name() or f"buffer:{view.buffer().id()}"
    return {
        "text": view.substr(sublime.Region(0, view.size())),
        "uri": file_path if file_path.startswith("buffer:") else filename_to_uri(file_path),
        "languageId": get_view_language_id(view),
        "selection": st_region_to_lsp_range(selection, view),
        "version": view.change_count(),
    }


def prepare_completion_request_doc(view: sublime.View) -> CopilotDocType | None:
    selection = view.sel()[0]
    file_path = view.file_name() or f"buffer:{view.buffer().id()}"
    return {
        "source": view.substr(sublime.Region(0, view.size())),
        "tabSize": cast(int, view.settings().get("tab_size")),
        "indentSize": 1,  # there is no such concept in ST
        "insertSpaces": cast(bool, view.settings().get("translate_tabs_to_spaces")),
        "path": file_path,
        "uri": file_path if file_path.startswith("buffer:") else filename_to_uri(file_path),
        "relativePath": get_project_relative_path(file_path),
        "languageId": get_view_language_id(view),
        "position": st_point_to_lsp_position(selection.begin(), view),
        # Buffer Version. Generally this is handled by LSP, but we need to handle it here
        # Will need to test getting the version from LSP
        "version": view.change_count(),
    }


def prepare_conversation_turn_request(
    conversation_id: str,
    window_id: int,
    message: str,
    view: sublime.View,
    views: list[sublime.View],
    source: Literal["panel", "inline"] = "panel",
) -> CopilotRequestConversationTurn | None:
    if not (doc := prepare_completion_request_doc(view)):
        return None

    # References can technicaly be across multiple files
    references: list[CopilotRequestConversationTurnReference | CopilotGitHubWebSearch] = []
    views.append(view)
    for view_ in views:
        if not (selection := view_.sel()[0]) or view_.substr(selection).isspace():
            continue

        file_path = view_.file_name()
        references.append({
            "type": "file",
            "status": "included",  # included, blocked, notfound, empty
            "uri": filename_to_uri(file_path) if file_path else f"buffer:{view_.buffer().id()}",
            "position": st_point_to_lsp_position(selection.begin(), view_),
            "range": st_region_to_lsp_range(selection, view_),
            "visibleRange": st_region_to_lsp_range(view_.visible_region(), view_),
            "selection": st_region_to_lsp_range(selection, view_),
            "openedAt": None,
            "activeAt": None,
        })

    return {
        "conversationId": conversation_id,
        "message": message,
        "workDoneToken": f"copilot_chat://{window_id}",
        "doc": doc,
        "computeSuggestions": True,
        "references": references,
        "source": source,
    }


def preprocess_message_for_html(message: str) -> str:
    def _escape_html(text: str) -> str:
        return re.sub(r"<(.*?)>", r"&lt;\1&gt;", text)

    new_lines: list[str] = []
    inside_code_block = False
    inline_code_pattern = re.compile(r"`([^`]*)`")
    for line in message.split("\n"):
        if line.lstrip().startswith("```"):
            inside_code_block = not inside_code_block
            new_lines.append(line)
            continue
        if not inside_code_block:
            escaped_line = ""
            start = 0
            for match in inline_code_pattern.finditer(line):
                escaped_line += _escape_html(line[start : match.start()]) + match.group(0)
                start = match.end()
            escaped_line += _escape_html(line[start:])
            new_lines.append(escaped_line)
        else:
            new_lines.append(line)
    return "\n".join(new_lines)


def preprocess_chat_message(
    view: sublime.View,
    message: str,
    templates: Sequence[CopilotUserDefinedPromptTemplates] | None = None,
) -> tuple[bool, str]:
    from .template import load_string_template

    templates = templates or []
    user_template = first_true(templates, pred=lambda t: f"/{t['id']}" == message)

    if is_template := bool(user_template or CopilotConversationTemplates.has_value(message)):
        message += "\n\n{{ user_prompt }}\n\n{{ code }}"

    region = view.sel()[0]
    lang = get_view_language_id(view, region.begin())

    template = load_string_template(message)
    message = template.render(
        code=f"\n```{lang}\n{view.substr(region)}\n```\n",
        user_prompt="\n".join(user_template["prompt"]) if user_template else "",
    )

    return is_template, message


def preprocess_completions(view: sublime.View, completions: list[CopilotPayloadCompletion]) -> None:
    """Preprocess the `completions` from "getCompletions" request."""
    # in-place de-duplication
    duplicate_indexes = list(
        map(
            itemgetter(0),  # the index from enumerate
            duplicates_everseen(enumerate(completions), key=lambda pair: pair[1]["displayText"]),
        )
    )
    # delete from the end to avoid changing the index during iteration
    for index in reversed(duplicate_indexes):
        del completions[index]

    # inject extra information for convenience
    for completion in completions:
        completion["point"] = lsp_position_to_st_point(completion["position"], view)
        completion["region"] = lsp_range_to_st_region(completion["range"], view).to_tuple()


def preprocess_panel_completions(view: sublime.View, completions: Sequence[CopilotPayloadPanelSolution]) -> None:
    """Preprocess the `completions` from "getCompletionsCycling" request."""
    for completion in completions:
        completion["region"] = lsp_range_to_st_region(completion["range"], view).to_tuple()


def is_debug_mode() -> bool:
    return bool(get_plugin_setting_dotted("settings.debug", False))


class GitHelper:
    """Helper class for Git operations used by Copilot commands."""

    @staticmethod
    def run_git_command(cmd: list[str], cwd: str | None = None) -> str | None:
        """Run a git command and return the output, or None if it fails."""
        try:
            result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=10, check=True)
            return result.stdout.strip()
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError):
            return None

    @staticmethod
    def get_git_repo_root(start_path: str) -> str | None:
        """Find the Git repository root starting from the given path."""
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--show-toplevel"],
                cwd=start_path,
                capture_output=True,
                text=True,
                timeout=5,
                check=True,
            )
            return result.stdout.strip()
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError):
            return None

    @staticmethod
    def get_git_changes(repo_root: str) -> list[str]:
        """Get actual diff content for staged and unstaged changes."""
        changes: list[str] = []

        # Get staged changes (actual diff content)
        staged_output = GitHelper.run_git_command(["git", "diff", "--cached"], repo_root)
        if staged_output:
            changes.append(f"=== STAGED CHANGES ===\n{staged_output}")

        # Get unstaged changes (actual diff content)
        unstaged_output = GitHelper.run_git_command(["git", "diff"], repo_root)
        if unstaged_output:
            changes.append(f"=== UNSTAGED CHANGES ===\n{unstaged_output}")

        # Get untracked files content (for small files)
        untracked_output = GitHelper.run_git_command(["git", "ls-files", "--others", "--exclude-standard"], repo_root)
        if untracked_output:
            untracked_files = [f.strip() for f in untracked_output.split("\n") if f.strip()]
            untracked_content: list[str] = []

            for file_path in untracked_files[:5]:  # Limit to first 5 untracked files
                full_path = Path(repo_root) / file_path
                try:
                    if full_path.is_file() and full_path.stat().st_size < 10000:  # Only read files < 10KB
                        content = full_path.read_text(encoding="utf-8", errors="ignore")
                        untracked_content.append(f"=== NEW FILE: {file_path} ===\n{content}")
                except (OSError, UnicodeDecodeError):
                    untracked_content.append(f"=== NEW FILE: {file_path} ===\n[Binary or unreadable file]")

            if untracked_content:
                changes.extend(untracked_content)

        return changes

    @staticmethod
    def get_current_user_email(repo_root: str) -> str | None:
        """Get the current Git user email."""
        return GitHelper.run_git_command(["git", "config", "user.email"], repo_root)

    @staticmethod
    def get_user_commits(repo_root: str, user_email: str | None, limit: int = 10) -> list[str]:
        """Get recent commits by the current user."""
        if not user_email:
            return []

        cmd = ["git", "log", f"--author={user_email}", f"--max-count={limit}", "--oneline", "--no-merges"]

        output = GitHelper.run_git_command(cmd, repo_root)
        if output:
            return [line.strip() for line in output.split("\n") if line.strip()]
        return []

    @staticmethod
    def get_recent_commits(repo_root: str, limit: int = 20) -> list[str]:
        """Get recent commits from all contributors."""
        cmd = ["git", "log", f"--max-count={limit}", "--oneline", "--no-merges"]

        output = GitHelper.run_git_command(cmd, repo_root)
        if output:
            return [line.strip() for line in output.split("\n") if line.strip()]
        return []

    @staticmethod
    def get_workspace_folder(view: sublime.View) -> str | None:
        """Get the workspace folder path."""
        if not (window := view.window()):
            return None

        # Try to get the project path
        if folders := window.folders():
            return folders[0]

        # Fallback to file directory
        if file_name := view.file_name():
            return str(Path(file_name).parent)

        return None

    @staticmethod
    def get_user_language() -> str | None:
        """Get user's language preference from Sublime Text settings."""
        # Try to get language from various Sublime Text settings
        settings = sublime.load_settings("Preferences.sublime-settings")

        # Check for explicit language setting
        if lang := settings.get("language"):
            return lang

        # Fallback to system locale
        try:
            import locale

            return locale.getdefaultlocale()[0]
        except Exception:
            return "en-US"

    @classmethod
    def gather_git_commit_data(cls, view: sublime.View) -> dict[str, Any] | None:
        """
        Gather all Git data needed for commit message generation.
        Returns None if not in a Git repository or if workspace folder not found.
        """
        # Get workspace folder
        workspace_folder = cls.get_workspace_folder(view)
        if not workspace_folder:
            return None

        # Find Git repository root
        repo_root = cls.get_git_repo_root(workspace_folder)
        if not repo_root:
            return None

        # Gather Git information
        changes = cls.get_git_changes(repo_root)
        user_email = cls.get_current_user_email(repo_root)
        user_commits = cls.get_user_commits(repo_root, user_email)
        recent_commits = cls.get_recent_commits(repo_root)
        user_language = cls.get_user_language()

        return {
            "changes": changes,
            "userCommits": user_commits,
            "recentCommits": recent_commits,
            "workspaceFolder": workspace_folder,
            "userLanguage": user_language,
        }


def prepare_conversation_edit_request(view: sublime.View) -> dict:
    """Prepare document information for edit conversation request."""
    if not (prepare_completion_request_doc(view)):
        return {}

    # Get the current selection
    selection = view.sel()[0]
    selection_start = selection.begin()
    selection_end = selection.end()

    # Get the line range for the selection
    selection_line_start = view.line(selection_start).begin()
    selection_line_end = view.line(selection_end).end()

    # Convert positions to LSP format (line, character)
    def point_to_lsp_position(point: int) -> dict:
        row, col = view.rowcol(point)
        return {"line": row, "character": col}

    return {
        "text": view.substr(sublime.Region(0, view.size())),
        "languageId": get_view_language_id(view),
        "selection": {
            "start": point_to_lsp_position(selection_start),
            "end": point_to_lsp_position(selection_end),
        },
        "range": {
            "start": point_to_lsp_position(selection_line_start),
            "end": point_to_lsp_position(selection_line_end),
        },
    }
