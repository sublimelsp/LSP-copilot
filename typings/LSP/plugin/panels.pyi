import sublime
import sublime_plugin
from .core.panels import LOG_LINES_LIMIT_SETTING_NAME as LOG_LINES_LIMIT_SETTING_NAME, PanelName as PanelName
from .core.registry import windows as windows
from contextlib import contextmanager
from sublime_plugin import WindowCommand
from typing import Generator

@contextmanager
def mutable(view: sublime.View) -> Generator: ...
def clear_undo_stack(view: sublime.View) -> None: ...

class LspToggleServerPanelCommand(WindowCommand):
    def run(self) -> None: ...

class LspShowDiagnosticsPanelCommand(WindowCommand):
    def run(self) -> None: ...

class LspToggleLogPanelLinesLimitCommand(sublime_plugin.TextCommand):
    @classmethod
    def is_limit_enabled(cls, window: sublime.Window | None) -> bool: ...
    @classmethod
    def get_lines_limit(cls, window: sublime.Window | None) -> int: ...
    def is_checked(self) -> bool: ...
    def run(self, edit: sublime.Edit) -> None: ...

class LspClearPanelCommand(sublime_plugin.TextCommand):
    """
    A clear_panel command to clear the error panel.
    """
    def run(self, edit: sublime.Edit) -> None: ...

class LspUpdatePanelCommand(sublime_plugin.TextCommand):
    """
    A update_panel command to update the error panel with new text.
    """
    def run(self, edit: sublime.Edit, characters: str | None = '') -> None: ...

class LspUpdateLogPanelCommand(sublime_plugin.TextCommand):
    def run(self, edit: sublime.Edit) -> None: ...

class LspClearLogPanelCommand(sublime_plugin.TextCommand):
    def run(self, edit: sublime.Edit) -> None: ...
