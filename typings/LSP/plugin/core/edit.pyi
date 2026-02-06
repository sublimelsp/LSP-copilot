import sublime
from ...protocol import AnnotatedTextEdit, Position as Position, TextEdit, WorkspaceEdit as WorkspaceEdit
from .logging import debug as debug
from .promise import Promise as Promise
from .protocol import UINT_MAX as UINT_MAX
from typing import TypedDict
from typing_extensions import NotRequired

WorkspaceChanges = dict[str, tuple[list[TextEdit | AnnotatedTextEdit], str | None, int | None]]

class WorkspaceEditSummary(TypedDict):
    total_changes: int
    edited_files: int
    created_files: NotRequired[int]
    renamed_files: NotRequired[int]
    deleted_files: NotRequired[int]

def parse_workspace_edit(workspace_edit: WorkspaceEdit, label: str | None = None) -> WorkspaceChanges: ...
def parse_range(range: Position) -> tuple[int, int]: ...
def apply_text_edits(view: sublime.View, edits: list[TextEdit] | None, *, label: str | None = None, process_placeholders: bool | None = False, required_view_version: int | None = None) -> Promise[sublime.View | None]: ...
def show_summary_message(window: sublime.Window, summary: WorkspaceEditSummary) -> None: ...
