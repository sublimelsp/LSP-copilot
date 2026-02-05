import sublime
import sublime_plugin
from ..protocol import TextEdit as TextEdit, WorkspaceEdit as WorkspaceEdit
from .core.edit import WorkspaceChanges as WorkspaceChanges, parse_range as parse_range, parse_workspace_edit as parse_workspace_edit
from .core.logging import debug as debug
from .core.panels import PanelName as PanelName
from .core.promise import Promise as Promise
from .core.registry import LspWindowCommand as LspWindowCommand, windows as windows
from .core.sessions import Session as Session
from .core.url import parse_uri as parse_uri
from .core.views import get_line as get_line
from .core.windows import WindowManager as WindowManager
from _typeshed import Incomplete
from contextlib import contextmanager
from typing import Any, Callable, Generator, Iterable

TextEditTuple = tuple[tuple[int, int], tuple[int, int], str]
g_workspace_edit_panel_resolvers: dict[int, Callable[[bool], None]]
BUTTONS_TEMPLATE: str

@contextmanager
def temporary_setting(settings: sublime.Settings, key: str, val: Any) -> Generator[None, None, None]: ...

class LspApplyWorkspaceEditCommand(LspWindowCommand):
    def run(self, session_name: str, edit: WorkspaceEdit, label: str | None = None, is_refactoring: bool = False) -> None: ...

class LspApplyDocumentEditCommand(sublime_plugin.TextCommand):
    re_placeholder: Incomplete
    def description(self, **kwargs: dict[str, Any]) -> str | None: ...
    def run(self, edit: sublime.Edit, changes: list[TextEdit], label: str | None = None, required_view_version: int | None = None, process_placeholders: bool = False) -> None: ...
    def apply_change(self, region: sublime.Region, replacement: str, edit: sublime.Edit) -> None: ...
    def parse_snippet(self, replacement: str) -> tuple[str, tuple[int, int]] | None: ...

def _parse_text_edit(text_edit: TextEdit) -> TextEditTuple: ...
def _sort_by_application_order(changes: Iterable[TextEditTuple]) -> list[TextEditTuple]: ...
def prompt_for_workspace_edits(session: Session, response: WorkspaceEdit, label: str) -> Promise[bool]: ...
def _render_workspace_edit_panel(session: Session, changes_per_uri: WorkspaceChanges, label: str, total_changes: int, file_count: int, on_done: Callable[[bool], None]) -> None: ...
def utf16_to_code_points(s: str, col: int) -> int:
    """Convert a position from UTF-16 code units to Unicode code points, usable for string slicing."""

class LspConcludeWorkspaceEditPanelCommand(sublime_plugin.WindowCommand):
    def run(self, window_id: int, accept: bool) -> None: ...
