import sublime
from ...protocol import DocumentUri as DocumentUri, Range as Range
from .constants import ST_PACKAGES_PATH as ST_PACKAGES_PATH, ST_PLATFORM as ST_PLATFORM, ST_VERSION as ST_VERSION
from .logging import exception_log as exception_log
from .promise import Promise as Promise, ResolveFunc as ResolveFunc
from .protocol import UINT_MAX as UINT_MAX
from .url import parse_uri as parse_uri
from .views import range_to_region as range_to_region
from _typeshed import Incomplete

opening_files: dict[str, tuple[Promise[sublime.View | None], ResolveFunc[sublime.View | None]]]
FRAGMENT_PATTERN: Incomplete

def lsp_range_from_uri_fragment(fragment: str) -> Range | None: ...
def open_file_uri(window: sublime.Window, uri: DocumentUri, flags: sublime.NewFileFlags = ..., group: int = -1) -> Promise[sublime.View | None]: ...
def _select_and_center(view: sublime.View | None, r: Range) -> sublime.View | None: ...
def _return_existing_view(flags: int, existing_view_group: int, active_group: int, specified_group: int) -> bool: ...
def _find_open_file(window: sublime.Window, fname: str, group: int = -1) -> sublime.View | None:
    """A replacement for Window.find_open_file that prefers the active view instead of the leftmost one."""
def open_file(window: sublime.Window, uri: DocumentUri, flags: sublime.NewFileFlags = ..., group: int = -1) -> Promise[sublime.View | None]:
    """
    Open a file asynchronously.
    It is only safe to call this function from the UI thread.
    The provided uri MUST be a file URI
    """
def open_resource(window: sublime.Window, uri: DocumentUri, group: int = -1) -> sublime.View | None:
    """
    Open a resource file.
    It is only safe to call this function from the UI thread.
    The provided uri MUST be a res URI
    """
def center_selection(view: sublime.View, r: Range) -> sublime.View: ...
def open_in_browser(uri: str) -> None: ...
def open_externally(uri: str, take_focus: bool) -> bool:
    '''
    A blocking function that invokes the OS\'s "open with default extension"
    '''
