import contextlib
import socket
import sublime
from ...protocol import DocumentSelector as DocumentSelector, DocumentUri as DocumentUri, FileOperationFilter as FileOperationFilter, ServerCapabilities as ServerCapabilities, TextDocumentSyncKind, TextDocumentSyncOptions as TextDocumentSyncOptions, URI as URI
from .collections import DottedDict as DottedDict
from .constants import LANGUAGE_IDENTIFIERS as LANGUAGE_IDENTIFIERS
from .file_watcher import FileWatcherEventType as FileWatcherEventType
from .logging import debug as debug, set_debug_logging as set_debug_logging
from .url import filename_to_uri as filename_to_uri, parse_uri as parse_uri
from _typeshed import Incomplete
from typing import Any, Callable, Generator, Iterable, TypeVar
from typing_extensions import TypedDict

TCP_CONNECT_TIMEOUT: int
FEATURES_TIMEOUT: int
WORKSPACE_DIAGNOSTICS_TIMEOUT: int
PANEL_FILE_REGEX: str
PANEL_LINE_REGEX: str

class FileWatcherConfig(TypedDict, total=False):
    patterns: list[str]
    events: list[FileWatcherEventType] | None
    ignores: list[str] | None

def basescope2languageid(base_scope: str) -> str: ...
@contextlib.contextmanager
def runtime(token: str) -> Generator[None, None, None]: ...
T = TypeVar('T')

def diff(old: Iterable[T], new: Iterable[T]) -> tuple[set[T], set[T]]:
    """
    Return a tuple of (added, removed) items
    """
def matches_pattern(path: str, patterns: Any) -> bool: ...
def sublime_pattern_to_glob(pattern: str, is_directory_pattern: bool, root_path: str | None = None) -> str:
    """
    Convert a Sublime Text pattern (http://www.sublimetext.com/docs/file_patterns.html)
    to a glob pattern that utilizes globstar extension.
    """
def debounced(f: Callable[[], Any], timeout_ms: int = 0, condition: Callable[[], bool] = ..., async_thread: bool = False) -> None:
    """
    Possibly run a function at a later point in time, either on the async thread or on the main thread.

    :param      f:             The function to possibly run. Its return type is discarded.
    :param      timeout_ms:    The time in milliseconds after which to possibly to run the function
    :param      condition:     The condition that must evaluate to True in order to run the function
    :param      async_thread:  If true, run the function on the async worker thread, otherwise run the function on the
                               main thread
    """

class SettingsRegistration:
    __slots__: Incomplete
    _settings: Incomplete
    def __init__(self, settings: sublime.Settings, on_change: Callable[[], None]) -> None: ...
    def __del__(self) -> None: ...

class DebouncerNonThreadSafe:
    """
    Debouncer for delaying execution of a function until specified timeout time.

    When calling `debounce()` multiple times, if the time span between calls is shorter than the specified `timeout_ms`,
    the callback function will only be called once, after `timeout_ms` since the last call.

    This implementation is not thread safe. You must ensure that `debounce()` is called from the same thread as
    was chosen during initialization through the `async_thread` argument.
    """
    _async_thread: Incomplete
    _current_id: int
    _next_id: int
    def __init__(self, async_thread: bool) -> None: ...
    def debounce(self, f: Callable[[], None], timeout_ms: int = 0, condition: Callable[[], bool] = ...) -> None:
        """
        Possibly run a function at a later point in time on the thread chosen during initialization.

        :param      f:             The function to possibly run
        :param      timeout_ms:    The time in milliseconds after which to possibly to run the function
        :param      condition:     The condition that must evaluate to True in order to run the function
        """
    def cancel_pending(self) -> None: ...

def read_dict_setting(settings_obj: sublime.Settings, key: str, default: dict) -> dict: ...
def read_list_setting(settings_obj: sublime.Settings, key: str, default: list) -> list: ...

class Settings:
    diagnostics_additional_delay_auto_complete_ms: Incomplete
    diagnostics_delay_ms: Incomplete
    diagnostics_gutter_marker: Incomplete
    diagnostics_highlight_style: Incomplete
    diagnostics_panel_include_severity_level: Incomplete
    disabled_capabilities: Incomplete
    document_highlight_style: Incomplete
    hover_highlight_style: Incomplete
    inhibit_snippet_completions: Incomplete
    inhibit_word_completions: Incomplete
    initially_folded: Incomplete
    link_highlight_style: Incomplete
    completion_insert_mode: Incomplete
    log_debug: Incomplete
    log_max_size: Incomplete
    log_server: Incomplete
    lsp_code_actions_on_save: Incomplete
    lsp_format_on_paste: Incomplete
    lsp_format_on_save: Incomplete
    on_save_task_timeout_ms: Incomplete
    only_show_lsp_completions: Incomplete
    popup_max_characters_height: Incomplete
    popup_max_characters_width: Incomplete
    refactoring_auto_save: Incomplete
    semantic_highlighting: Incomplete
    show_code_actions: Incomplete
    show_code_lens: Incomplete
    show_inlay_hints: Incomplete
    inlay_hints_max_length: Incomplete
    show_diagnostics_in_hover: Incomplete
    show_code_actions_in_hover: Incomplete
    show_diagnostics_annotations_severity_level: Incomplete
    show_diagnostics_count_in_view_status: Incomplete
    show_multiline_diagnostics_highlights: Incomplete
    show_multiline_document_highlights: Incomplete
    show_diagnostics_in_view_status: Incomplete
    show_diagnostics_panel_on_save: Incomplete
    show_diagnostics_severity_level: Incomplete
    show_references_in_quick_panel: Incomplete
    show_symbol_action_links: Incomplete
    show_view_status: Incomplete
    def __init__(self, s: sublime.Settings) -> None: ...
    def update(self, s: sublime.Settings) -> None: ...
    def highlight_style_region_flags(self, style_str: str) -> tuple[sublime.RegionFlags, sublime.RegionFlags]: ...
    @staticmethod
    def _style_str_to_flag(style_str: str) -> sublime.RegionFlags | None: ...
    def diagnostics_highlight_style_flags(self) -> list[sublime.RegionFlags | None]:
        """Returns flags for highlighting diagnostics on single lines per severity"""

class SemanticToken:
    __slots__: Incomplete
    modifiers: Incomplete
    region: Incomplete
    type: Incomplete
    def __init__(self, region: sublime.Region, type: str, modifiers: list[str]) -> None: ...

class ClientStates:
    STARTING: int
    READY: int
    STOPPING: int

class DocumentFilter_:
    '''
    A document filter denotes a document through properties like language, scheme or pattern. An example is a filter
    that applies to TypeScript files on disk. Another example is a filter that applies to JSON files with name
    package.json:

        { "language": "typescript", scheme: "file" }
        { "language": "json", "pattern": "**/package.json" }

    Sublime Text doesn\'t understand what a language ID is, so we have to maintain a global translation map from language
    IDs to selectors. Sublime Text also has no support for patterns. We use the wcmatch library for this.
    '''
    __slots__: Incomplete
    scheme: Incomplete
    pattern: Incomplete
    language: Incomplete
    def __init__(self, language: str | None = None, scheme: str | None = None, pattern: str | None = None) -> None: ...
    def __call__(self, view: sublime.View) -> bool:
        """Does this filter match the view? An empty filter matches any view."""

class DocumentSelector_:
    """
    A DocumentSelector is a list of DocumentFilters. A view matches a DocumentSelector if and only if any one of its
    filters matches against the view.
    """
    __slots__: Incomplete
    filters: Incomplete
    def __init__(self, document_selector: DocumentSelector) -> None: ...
    def __bool__(self) -> bool: ...
    def matches(self, view: sublime.View) -> bool:
        """Does this selector match the view? A selector with no filters matches all views."""

def match_file_operation_filters(filters: list[FileOperationFilter], uri: URI) -> bool: ...

_METHOD_TO_CAPABILITY_EXCEPTIONS: dict[str, tuple[str, str | None]]

def method_to_capability(method: str) -> tuple[str, str]:
    """
    Given a method, returns the corresponding capability path, and the associated path to stash the registration key.

    Examples:

        textDocument/definition --> (definitionProvider, definitionProvider.id)
        textDocument/references --> (referencesProvider, referencesProvider.id)
        textDocument/didOpen --> (textDocumentSync.didOpen, textDocumentSync.didOpen.id)
    """
def normalize_text_sync(textsync: TextDocumentSyncOptions | TextDocumentSyncKind | None) -> dict[str, Any]:
    """
    Brings legacy text sync capabilities to the most modern format
    """

class Capabilities(DottedDict):
    """
    Maintains static and dynamic capabilities

    Static capabilities come from a response to the initialize request (from Client -> Server).
    Dynamic capabilities can be registered at any moment with client/registerCapability and client/unregisterCapability
    (from Server -> Client).
    """
    def register(self, registration_id: str, capability_path: str, registration_path: str, options: dict[str, Any]) -> None: ...
    def unregister(self, registration_id: str, capability_path: str, registration_path: str) -> dict[str, Any] | None: ...
    def assign(self, d: ServerCapabilities) -> None: ...
    def should_notify_did_open(self) -> bool: ...
    def text_sync_kind(self) -> TextDocumentSyncKind: ...
    def should_notify_did_change_workspace_folders(self) -> bool: ...
    def should_notify_will_save(self) -> bool: ...
    def should_notify_did_save(self) -> tuple[bool, bool]: ...
    def should_notify_did_close(self) -> bool: ...

def _translate_path(path: str, source: str, destination: str) -> tuple[str, bool]: ...

class PathMap:
    __slots__: Incomplete
    _local: Incomplete
    _remote: Incomplete
    def __init__(self, local: str, remote: str) -> None: ...
    @classmethod
    def parse(cls, json: Any) -> list[PathMap] | None: ...
    def __eq__(self, other: Any) -> bool: ...
    def map_from_local_to_remote(self, uri: str) -> tuple[str, bool]: ...
    def map_from_remote_to_local(self, uri: str) -> tuple[str, bool]: ...

class TransportConfig:
    __slots__: Incomplete
    name: Incomplete
    command: Incomplete
    tcp_port: Incomplete
    env: Incomplete
    listener_socket: Incomplete
    def __init__(self, name: str, command: list[str], tcp_port: int | None, env: dict[str, str], listener_socket: socket.socket | None) -> None: ...

class ClientConfig:
    name: Incomplete
    selector: Incomplete
    priority_selector: Incomplete
    schemes: list[str]
    command: Incomplete
    tcp_port: Incomplete
    auto_complete_selector: Incomplete
    enabled: Incomplete
    init_options: Incomplete
    settings: Incomplete
    env: Incomplete
    experimental_capabilities: Incomplete
    disabled_capabilities: Incomplete
    file_watcher: Incomplete
    path_maps: Incomplete
    status_key: Incomplete
    semantic_tokens: Incomplete
    diagnostics_mode: Incomplete
    def __init__(self, name: str, selector: str, priority_selector: str | None = None, schemes: list[str] | None = None, command: list[str] | None = None, binary_args: list[str] | None = None, tcp_port: int | None = None, auto_complete_selector: str | None = None, enabled: bool = True, init_options: DottedDict = ..., settings: DottedDict = ..., env: dict[str, str | list[str]] = {}, experimental_capabilities: dict[str, Any] | None = None, disabled_capabilities: DottedDict = ..., file_watcher: FileWatcherConfig = {}, semantic_tokens: dict[str, str] | None = None, diagnostics_mode: str = 'open_files', path_maps: list[PathMap] | None = None) -> None: ...
    @classmethod
    def from_sublime_settings(cls, name: str, s: sublime.Settings, file: str) -> ClientConfig: ...
    @classmethod
    def from_dict(cls, name: str, d: dict[str, Any]) -> ClientConfig: ...
    @classmethod
    def from_config(cls, src_config: ClientConfig, override: dict[str, Any]) -> ClientConfig: ...
    def resolve_transport_config(self, variables: dict[str, str]) -> TransportConfig: ...
    def set_view_status(self, view: sublime.View, message: str) -> None: ...
    def erase_view_status(self, view: sublime.View) -> None: ...
    def match_view(self, view: sublime.View, scheme: str) -> bool: ...
    def map_client_path_to_server_uri(self, path: str) -> str: ...
    def map_server_uri_to_client_path(self, uri: DocumentUri) -> str: ...
    def is_disabled_capability(self, capability_path: str) -> bool: ...
    def filter_out_disabled_capabilities(self, capability_path: str, options: dict[str, Any]) -> dict[str, Any]: ...
    def __repr__(self) -> str: ...
    def __eq__(self, other: Any) -> bool: ...

def _read_selector(config: sublime.Settings | dict[str, Any]) -> str: ...
def _read_priority_selector(config: sublime.Settings | dict[str, Any]) -> str: ...
def _find_free_port() -> int: ...
def _start_tcp_listener(tcp_port: int | None) -> socket.socket: ...
