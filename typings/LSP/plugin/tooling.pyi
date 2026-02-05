import sublime
import sublime_plugin
from .core.css import css as css
from .core.logging import debug as debug
from .core.registry import windows as windows
from .core.sessions import get_plugin as get_plugin
from .core.transports import Transport as Transport, TransportCallbacks as TransportCallbacks, create_transport as create_transport
from .core.types import Capabilities as Capabilities, ClientConfig as ClientConfig
from .core.version import __version__ as __version__
from .core.views import extract_variables as extract_variables, make_command_link as make_command_link
from .core.workspace import ProjectFolders as ProjectFolders, sorted_workspace_folders as sorted_workspace_folders
from .session_buffer import SessionBuffer as SessionBuffer
from _typeshed import Incomplete
from typing import Any, Callable

def _translate_description(translations: dict[str, str] | None, descr: str) -> tuple[str, bool]:
    '''
    Translate a placeholder description like "%foo.bar.baz" into an English translation. The translation map is
    the first argument.
    '''
def _preprocess_properties(translations: dict[str, str] | None, properties: dict[str, Any]) -> None:
    '''
    Preprocess the server settings from a package.json file:

    - Replace description translation placeholders by their English translation
    - Discard the "scope" key
    - Removes key/values whose value is not a dict
    '''
def _enum_to_str(value: Any) -> str: ...

class BasePackageNameInputHandler(sublime_plugin.TextInputHandler):
    def initial_text(self) -> str: ...
    def preview(self, text: str) -> str: ...

class LspParseVscodePackageJson(sublime_plugin.ApplicationCommand):
    view: sublime.View | None
    def __init__(self) -> None: ...
    def writeline(self, contents: str, indent: int = 0) -> None: ...
    def writeline4(self, contents: str) -> None: ...
    def input(self, args: dict[str, Any]) -> sublime_plugin.CommandInputHandler | None: ...
    def run(self, base_package_name: str) -> None: ...

class LspTroubleshootServerCommand(sublime_plugin.WindowCommand):
    def run(self) -> None: ...
    def on_selected(self, selected_index: int, configs: list[ClientConfig], active_view: sublime.View) -> None: ...
    test_runner: ServerTestRunner | None
    def test_run_server_async(self, config: ClientConfig, window: sublime.Window, active_view: sublime.View, output_sheet: sublime.HtmlSheet) -> None: ...
    def update_sheet(self, config: ClientConfig, active_view: sublime.View | None, output_sheet: sublime.HtmlSheet, resolved_command: list[str], server_output: str, exit_code: int) -> None: ...
    def get_contents(self, config: ClientConfig, active_view: sublime.View | None, resolved_command: list[str], server_output: str, exit_code: int) -> str: ...
    def json_dump(self, contents: Any) -> str: ...
    def code_block(self, contents: str, lang: str = '') -> str: ...
    def read_resource(self, path: str) -> str | None: ...

class LspCopyToClipboardFromBase64Command(sublime_plugin.ApplicationCommand):
    def run(self, contents: str = '') -> None: ...

class LspDumpWindowConfigs(sublime_plugin.WindowCommand):
    """
    Very basic command to dump all of the window's resolved configurations.
    """
    def run(self) -> None: ...

class LspDumpBufferCapabilities(sublime_plugin.TextCommand):
    """
    Very basic command to dump the current view's static and dynamically registered capabilities.
    """
    def run(self, edit: sublime.Edit) -> None: ...

class ServerTestRunner(TransportCallbacks):
    """
    Used to start the server and collect any potential stderr output and the exit code.

    Server is automatically closed after defined timeout.
    """
    CLOSE_TIMEOUT_SEC: int
    _on_close: Incomplete
    _transport: Transport | None
    _resolved_command: list[str]
    _stderr_lines: list[str]
    def __init__(self, config: ClientConfig, window: sublime.Window, initiating_view: sublime.View, on_close: Callable[[list[str], str, int], None]) -> None: ...
    def force_close_transport(self) -> None: ...
    def on_payload(self, payload: dict[str, Any]) -> None: ...
    def on_stderr_message(self, message: str) -> None: ...
    def on_transport_close(self, exit_code: int, exception: Exception | None) -> None: ...

class LspOnDoubleClickCommand(sublime_plugin.TextCommand):
    click_count: int
    prev_command: str | None
    prev_args: dict[Any, Any] | None
    def run(self, edit: sublime.Edit, command: str, args: dict[Any, Any]) -> None: ...
    def reset(self) -> None: ...
