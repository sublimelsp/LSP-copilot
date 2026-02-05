import sublime
import weakref
from ...protocol import ApplyWorkspaceEditParams as ApplyWorkspaceEditParams, ClientCapabilities as ClientCapabilities, CodeAction, Command, ConfigurationItem as ConfigurationItem, ConfigurationParams as ConfigurationParams, Diagnostic as Diagnostic, DiagnosticServerCancellationData as DiagnosticServerCancellationData, DidChangeWatchedFilesRegistrationOptions as DidChangeWatchedFilesRegistrationOptions, DidChangeWorkspaceFoldersParams as DidChangeWorkspaceFoldersParams, DocumentLink as DocumentLink, DocumentUri as DocumentUri, ExecuteCommandParams, FileEvent as FileEvent, FileSystemWatcher as FileSystemWatcher, GeneralClientCapabilities as GeneralClientCapabilities, InitializeParams as InitializeParams, InitializeResult as InitializeResult, LSPAny, Location as Location, LocationLink as LocationLink, LogMessageParams as LogMessageParams, PreviousResultId as PreviousResultId, ProgressParams as ProgressParams, ProgressToken as ProgressToken, PublishDiagnosticsParams as PublishDiagnosticsParams, Range as Range, RegistrationParams as RegistrationParams, ShowDocumentParams as ShowDocumentParams, ShowMessageParams as ShowMessageParams, ShowMessageRequestParams as ShowMessageRequestParams, SignatureHelpTriggerKind, TextDocumentClientCapabilities as TextDocumentClientCapabilities, TextDocumentSyncKind as TextDocumentSyncKind, TextEdit as TextEdit, UnregistrationParams as UnregistrationParams, WatchKind as WatchKind, WindowClientCapabilities as WindowClientCapabilities, WorkDoneProgressBegin, WorkDoneProgressCreateParams as WorkDoneProgressCreateParams, WorkspaceClientCapabilities as WorkspaceClientCapabilities, WorkspaceDiagnosticParams as WorkspaceDiagnosticParams, WorkspaceDiagnosticReport as WorkspaceDiagnosticReport, WorkspaceDocumentDiagnosticReport as WorkspaceDocumentDiagnosticReport, WorkspaceEdit as WorkspaceEdit, WorkspaceFullDocumentDiagnosticReport as WorkspaceFullDocumentDiagnosticReport
from ..diagnostics import DiagnosticsIdentifier as DiagnosticsIdentifier, DiagnosticsStorage as DiagnosticsStorage, WORKSPACE_DIAGNOSTICS_RETRIGGER_DELAY as WORKSPACE_DIAGNOSTICS_RETRIGGER_DELAY
from .active_request import ActiveRequest as ActiveRequest
from .collections import DottedDict as DottedDict
from .constants import MARKO_MD_PARSER_VERSION as MARKO_MD_PARSER_VERSION, RequestFlags as RequestFlags, SEMANTIC_TOKENS_MAP as SEMANTIC_TOKENS_MAP, ST_STORAGE_PATH as ST_STORAGE_PATH
from .edit import WorkspaceChanges as WorkspaceChanges, WorkspaceEditSummary as WorkspaceEditSummary, apply_text_edits as apply_text_edits, parse_workspace_edit as parse_workspace_edit
from .file_watcher import DEFAULT_WATCH_KIND as DEFAULT_WATCH_KIND, FileWatcher as FileWatcher, FileWatcherEvent as FileWatcherEvent, file_watcher_event_type_to_lsp_file_change_type as file_watcher_event_type_to_lsp_file_change_type, get_file_watcher_implementation as get_file_watcher_implementation, lsp_watch_kind_to_file_watcher_event_types as lsp_watch_kind_to_file_watcher_event_types
from .logging import debug as debug, exception_log as exception_log
from .open import center_selection as center_selection, open_externally as open_externally, open_file as open_file, open_resource as open_resource
from .progress import WindowProgressReporter as WindowProgressReporter
from .promise import PackagedTask as PackagedTask, Promise as Promise
from .protocol import Error as Error, JSONRPCMessage as JSONRPCMessage, Notification as Notification, Request as Request, ResolvedCodeLens as ResolvedCodeLens, Response as Response, ResponseError as ResponseError
from .settings import client_configs as client_configs, globalprefs as globalprefs, userprefs as userprefs
from .transports import Transport as Transport, TransportCallbacks as TransportCallbacks
from .types import Capabilities as Capabilities, ClientConfig as ClientConfig, ClientStates as ClientStates, DocumentSelector_ as DocumentSelector_, SemanticToken as SemanticToken, SettingsRegistration as SettingsRegistration, debounced as debounced, diff as diff, method_to_capability as method_to_capability, sublime_pattern_to_glob as sublime_pattern_to_glob
from .typing import StrEnum as StrEnum
from .url import filename_to_uri as filename_to_uri, normalize_uri as normalize_uri, parse_uri as parse_uri
from .version import __version__ as __version__
from .views import MarkdownLangMap as MarkdownLangMap, extract_variables as extract_variables, get_uri_and_range_from_location as get_uri_and_range_from_location, kind_contains_other_kind as kind_contains_other_kind, uri_from_view as uri_from_view
from .workspace import WorkspaceFolder as WorkspaceFolder, is_subpath_of as is_subpath_of
from _typeshed import Incomplete
from abc import ABCMeta, abstractmethod
from enum import IntEnum, IntFlag
from typing import Any, Callable, Generator, Literal, Protocol, TypeVar, overload
from typing_extensions import TypeAlias, TypeGuard
from weakref import WeakSet

InitCallback: TypeAlias
P = TypeVar('P', bound=LSPAny)
R = TypeVar('R', bound=LSPAny)

class ViewStateActions(IntFlag):
    NONE = 0
    SAVE = 1
    CLOSE = 2

def is_workspace_full_document_diagnostic_report(report: WorkspaceDocumentDiagnosticReport) -> TypeGuard[WorkspaceFullDocumentDiagnosticReport]: ...
def is_diagnostic_server_cancellation_data(data: Any) -> TypeGuard[DiagnosticServerCancellationData]: ...
def get_semantic_tokens_map(custom_tokens_map: dict[str, str] | None) -> tuple[tuple[str, str], ...]: ...
def decode_semantic_token(types_legend: tuple[str, ...], modifiers_legend: tuple[str, ...], tokens_scope_map: tuple[tuple[str, str], ...], token_type_encoded: int, token_modifiers_encoded: int) -> tuple[str, list[str], str | None]:
    """
    This function converts the token type and token modifiers from encoded numbers into names, based on the legend from
    the server. It also returns the corresponding scope name, which will be used for the highlighting color, either
    derived from a predefined scope map if the token type is one of the types defined in the LSP specs, or from a scope
    for custom token types if it was added in the client configuration (will be `None` if no scope has been defined for
    the custom token type).
    """

class Manager(metaclass=ABCMeta):
    """
    A Manager is a container of Sessions.
    """
    @property
    @abstractmethod
    def window(self) -> sublime.Window:
        """
        Get the window associated with this manager.
        """
    @abstractmethod
    def get_session(self, config_name: str, file_path: str) -> Session | None:
        """
        Gets the session by name and file path.
        """
    @abstractmethod
    def get_project_path(self, file_path: str) -> str | None:
        """
        Get the project path for the given file.
        """
    @abstractmethod
    def should_ignore_diagnostics(self, uri: DocumentUri, configuration: ClientConfig) -> str | None:
        """
        Should the diagnostics for this URI be shown in the view? Return a reason why not
        """
    @abstractmethod
    def start_async(self, configuration: ClientConfig, initiating_view: sublime.View) -> None:
        """
        Start a new Session with the given configuration. The initiating view is the view that caused this method to
        be called.

        A normal flow of calls would be start -> on_post_initialize -> do language server things -> on_post_exit.
        However, it is possible that the subprocess cannot start, in which case on_post_initialize will never be called.
        """
    @abstractmethod
    def on_diagnostics_updated(self) -> None: ...
    @abstractmethod
    def on_post_exit_async(self, session: Session, exit_code: int, exception: Exception | None) -> None:
        """
        The given Session has stopped with the given exit code.
        """

def _int_enum_to_list(e: type[IntEnum]) -> list[int]: ...
def _str_enum_to_list(e: type[StrEnum]) -> list[str]: ...
def get_initialize_params(variables: dict[str, str], workspace_folders: list[WorkspaceFolder], config: ClientConfig) -> InitializeParams: ...

class SessionViewProtocol(Protocol):
    @property
    def session(self) -> Session: ...
    @property
    def view(self) -> sublime.View: ...
    @property
    def listener(self) -> weakref.ref[AbstractViewListener]: ...
    @property
    def session_buffer(self) -> SessionBufferProtocol: ...
    @property
    def active_requests(self) -> dict[int, ActiveRequest]: ...
    def get_uri(self) -> DocumentUri | None: ...
    def get_language_id(self) -> str | None: ...
    def get_view_for_group(self, group: int) -> sublime.View | None: ...
    def on_capability_added_async(self, registration_id: str, capability_path: str, options: dict[str, Any]) -> None: ...
    def on_capability_removed_async(self, registration_id: str, discarded_capabilities: dict[str, Any]) -> None: ...
    def has_capability_async(self, capability_path: str) -> bool: ...
    def shutdown_async(self) -> None: ...
    def present_diagnostics_async(self, is_view_visible: bool) -> None: ...
    def on_request_started_async(self, request_id: int, request: Request[Any, Any]) -> None: ...
    def on_request_finished_async(self, request_id: int) -> None: ...
    def on_request_progress(self, request_id: int, params: dict[str, Any]) -> None: ...
    def get_code_lenses_for_region(self, region: sublime.Region) -> list[Command]: ...
    def handle_code_lenses_async(self, code_lenses: list[ResolvedCodeLens]) -> None: ...
    def clear_code_lenses_async(self) -> None: ...
    def reset_show_definitions(self) -> None: ...
    def on_userprefs_changed_async(self) -> None: ...
    def get_request_flags(self) -> RequestFlags: ...

class SessionBufferProtocol(Protocol):
    @property
    def session(self) -> Session: ...
    @property
    def session_views(self) -> WeakSet[SessionViewProtocol]: ...
    @property
    def diagnostics(self) -> list[tuple[Diagnostic, sublime.Region]]: ...
    @property
    def last_synced_version(self) -> int: ...
    def get_uri(self) -> str | None: ...
    def get_language_id(self) -> str | None: ...
    def get_view_in_group(self, group: int = ...) -> sublime.View: ...
    def register_capability_async(self, registration_id: str, capability_path: str, registration_path: str, options: dict[str, Any], suppress_requests: bool) -> None: ...
    def unregister_capability_async(self, registration_id: str, capability_path: str, registration_path: str) -> None: ...
    def get_capability(self, capability_path: str) -> Any | None: ...
    def has_capability(self, capability_path: str) -> bool: ...
    def on_userprefs_changed_async(self) -> None: ...
    def on_diagnostics_async(self, raw_diagnostics: list[Diagnostic], version: int | None, visible_session_views: set[SessionViewProtocol]) -> None: ...
    def get_document_link_at_point(self, view: sublime.View, point: int) -> DocumentLink | None: ...
    def update_document_link(self, new_link: DocumentLink) -> None: ...
    def do_semantic_tokens_async(self, view: sublime.View) -> None: ...
    def set_semantic_tokens_pending_refresh(self, needs_refresh: bool = ...) -> None: ...
    def get_semantic_tokens(self) -> list[SemanticToken]: ...
    def evaluate_semantic_tokens_color_scheme_support(self, view: sublime.View) -> None: ...
    def do_inlay_hints_async(self, view: sublime.View) -> None: ...
    def set_inlay_hints_pending_refresh(self, needs_refresh: bool = ...) -> None: ...
    def remove_inlay_hint_phantom(self, phantom_uuid: str) -> None: ...
    def remove_all_inlay_hints(self) -> None: ...
    def do_document_diagnostic_async(self, view: sublime.View, version: int, *, forced_update: bool = ...) -> None: ...
    def set_document_diagnostic_pending_refresh(self, needs_refresh: bool = ...) -> None: ...
    def do_code_lenses_async(self, view: sublime.View) -> None: ...
    def set_code_lenses_pending_refresh(self, needs_refresh: bool = True) -> None: ...

class AbstractViewListener(metaclass=ABCMeta):
    TOTAL_ERRORS_AND_WARNINGS_STATUS_KEY: str
    view: Incomplete
    hover_provider_count: int
    @abstractmethod
    def session_async(self, capability: str, point: int | None = None) -> Session | None: ...
    @abstractmethod
    def sessions_async(self, capability: str | None = None) -> list[Session]: ...
    @abstractmethod
    def session_buffers_async(self, capability: str | None = None) -> list[SessionBufferProtocol]: ...
    @abstractmethod
    def session_views_async(self) -> list[SessionViewProtocol]: ...
    @abstractmethod
    def purge_changes_async(self) -> None: ...
    @abstractmethod
    def trigger_on_pre_save_async(self) -> None: ...
    @abstractmethod
    def on_session_initialized_async(self, session: Session) -> None: ...
    @abstractmethod
    def on_session_shutdown_async(self, session: Session) -> None: ...
    @abstractmethod
    def get_diagnostics_async(self, location: sublime.Region | int, max_diagnostic_severity_level: int = ...) -> list[tuple[SessionBufferProtocol, list[Diagnostic]]]: ...
    @abstractmethod
    def on_diagnostics_updated_async(self, is_view_visible: bool) -> None: ...
    @abstractmethod
    def get_language_id(self) -> str: ...
    @abstractmethod
    def get_uri(self) -> DocumentUri: ...
    @overload
    def do_signature_help_async(self, trigger_kind: Literal[SignatureHelpTriggerKind.TriggerCharacter], trigger_char: str) -> None: ...
    @overload
    def do_signature_help_async(self, trigger_kind: Literal[SignatureHelpTriggerKind.Invoked, SignatureHelpTriggerKind.ContentChange], trigger_char: None = None) -> None: ...
    @abstractmethod
    def navigate_signature_help(self, forward: bool) -> None: ...
    @abstractmethod
    def on_documentation_popup_toggle(self, *, opened: bool) -> None: ...
    @abstractmethod
    def on_post_move_window_async(self) -> None: ...
    @abstractmethod
    def get_request_flags(self, session: Session) -> RequestFlags: ...

class AbstractPlugin(metaclass=ABCMeta):
    '''
    Inherit from this class to handle non-standard requests and notifications.
    Given a request/notification, replace the non-alphabetic characters with an underscore, and prepend it with "m_".
    This will be the name of your method.
    For instance, to implement the non-standard eslint/openDoc request, define the Python method

        def m_eslint_openDoc(self, params, request_id):
            session = self.weaksession()
            if session:
                webbrowser.open_tab(params[\'url\'])
                session.send_response(Response(request_id, None))

    To handle the non-standard eslint/status notification, define the Python method

        def m_eslint_status(self, params):
            pass

    To understand how this works, see the __getattr__ method of the Session class.
    '''
    @classmethod
    @abstractmethod
    def name(cls) -> str:
        '''
        A human-friendly name. If your plugin is called "LSP-foobar", then this should return "foobar". If you also
        have your settings file called "LSP-foobar.sublime-settings", then you don\'t even need to re-implement the
        configuration method (see below).
        '''
    @classmethod
    def configuration(cls) -> tuple[sublime.Settings, str]:
        '''
        Return the Settings object that defines the "command", "languages", and optionally the "initializationOptions",
        "default_settings", "env" and "tcp_port" as the first element in the tuple, and the path to the base settings
        filename as the second element in the tuple.

        The second element in the tuple is used to handle "settings" overrides from users properly. For example, if your
        plugin is called LSP-foobar, you would return "Packages/LSP-foobar/LSP-foobar.sublime-settings".

        The "command", "initializationOptions" and "env" are subject to template string substitution. The following
        template strings are recognized:

        $file
        $file_base_name
        $file_extension
        $file_name
        $file_path
        $platform
        $project
        $project_base_name
        $project_extension
        $project_name
        $project_path

        These are just the values from window.extract_variables(). Additionally,

        $storage_path The path to the package storage (see AbstractPlugin.storage_path)
        $cache_path   sublime.cache_path()
        $temp_dir     tempfile.gettempdir()
        $home         os.path.expanduser(\'~\')
        $port         A random free TCP-port on localhost in case "tcp_port" is set to 0. This string template can only
                      be used in the "command"

        The "command" and "env" are expanded upon starting the subprocess of the Session. The "initializationOptions"
        are expanded upon doing the initialize request. "initializationOptions" does not expand $port.

        When you\'re managing your own server binary, you would typically place it in sublime.cache_path(). So your
        "command" should look like this: "command": ["$cache_path/LSP-foobar/server_binary", "--stdio"]
        '''
    @classmethod
    def is_applicable(cls, view: sublime.View, config: ClientConfig) -> bool:
        """
        Determine whether the server should run on the given view.

        The default implementation checks whether the URI scheme and the syntax scope match against the schemes and
        selector from the settings file. You can override this method for example to dynamically evaluate the applicable
        selector, or to ignore certain views even when those would match the static config. Please note that no document
        syncronization messages (textDocument/didOpen, textDocument/didChange, textDocument/didClose, etc.) are sent to
        the server for ignored views.

        This method is called when the view gets opened. To manually trigger this method again, run the
        `lsp_check_applicable` TextCommand for the given view and with a `session_name` keyword argument.

        :param      view:             The view
        :param      config:           The config
        """
    @classmethod
    def selector(cls, view: sublime.View, config: ClientConfig) -> str: ...
    @classmethod
    def additional_variables(cls) -> dict[str, str] | None:
        """
        In addition to the above variables, add more variables here to be expanded.
        """
    @classmethod
    def storage_path(cls) -> str:
        '''
        The storage path. Use this as your base directory to install server files. Its path is \'$DATA/Package Storage\'.
        You should have an additional subdirectory preferably the same name as your plugin. For instance:

        ```python
        from LSP.plugin import AbstractPlugin
        import os


        class MyPlugin(AbstractPlugin):

            @classmethod
            def name(cls) -> str:
                return "my-plugin"

            @classmethod
            def basedir(cls) -> str:
                # Do everything relative to this directory
                return os.path.join(cls.storage_path(), cls.name())
        ```
        '''
    @classmethod
    def needs_update_or_installation(cls) -> bool:
        """
        If this plugin manages its own server binary, then this is the place to check whether the binary needs
        an update, or whether it needs to be installed before starting the language server.
        """
    @classmethod
    def install_or_update(cls) -> None:
        """
        Do the actual update/installation of the server binary. This runs in a separate thread, so don't spawn threads
        yourself here.
        """
    @classmethod
    def can_start(cls, window: sublime.Window, initiating_view: sublime.View, workspace_folders: list[WorkspaceFolder], configuration: ClientConfig) -> str | None:
        """
        Determines ability to start. This is called after needs_update_or_installation and after install_or_update.
        So you may assume that if you're managing your server binary, then it is already installed when this
        classmethod is called.

        :param      window:             The window
        :param      initiating_view:    The initiating view
        :param      workspace_folders:  The workspace folders
        :param      configuration:      The configuration

        :returns:   A string describing the reason why we should not start a language server session, or None if we
                    should go ahead and start a session.
        """
    @classmethod
    def on_pre_start(cls, window: sublime.Window, initiating_view: sublime.View, workspace_folders: list[WorkspaceFolder], configuration: ClientConfig) -> str | None:
        '''
        Callback invoked just before the language server subprocess is started. This is the place to do last-minute
        adjustments to your "command" or "init_options" in the passed-in "configuration" argument, or change the
        order of the workspace folders. You can also choose to return a custom working directory, but consider that a
        language server should not care about the working directory.

        :param      window:             The window
        :param      initiating_view:    The initiating view
        :param      workspace_folders:  The workspace folders, you can modify these
        :param      configuration:      The configuration, you can modify this one

        :returns:   A desired working directory, or None if you don\'t care
        '''
    @classmethod
    def on_post_start(cls, window: sublime.Window, initiating_view: sublime.View, workspace_folders: list[WorkspaceFolder], configuration: ClientConfig) -> None:
        """
        Callback invoked when the subprocess was just started.

        :param      window:             The window
        :param      initiating_view:    The initiating view
        :param      workspace_folders:  The workspace folders
        :param      configuration:      The configuration
        """
    @classmethod
    def should_ignore(cls, view: sublime.View) -> bool: ...
    @classmethod
    def markdown_language_id_to_st_syntax_map(cls) -> MarkdownLangMap | None:
        """
        Override this method to tweak the syntax highlighting of code blocks in popups from your language server.
        The returned object should be a dictionary exactly in the form of mdpopup's language_map setting.

        See: https://facelessuser.github.io/sublime-markdown-popups/settings/#mdpopupssublime_user_lang_map

        :returns:   The markdown language map, or None
        """
    weaksession: Incomplete
    def __init__(self, weaksession: weakref.ref[Session]) -> None:
        """
        Constructs a new instance. Your instance is constructed after a response to the initialize request.

        :param      weaksession:  A weak reference to the Session. You can grab a strong reference through
                                  self.weaksession(), but don't hold on to that reference.
        """
    def on_settings_changed(self, settings: DottedDict) -> None:
        """
        Override this method to alter the settings that are returned to the server for the
        workspace/didChangeConfiguration notification and the workspace/configuration requests.

        :param      settings:      The settings that the server should receive.
        """
    def on_workspace_configuration(self, params: ConfigurationItem, configuration: Any) -> Any:
        """
        Override to augment configuration returned for the workspace/configuration request.

        :param      params:         A ConfigurationItem for which configuration is requested.
        :param      configuration:  The pre-resolved configuration for given params using the settings object or None.

        :returns: The resolved configuration for given params.
        """
    def on_pre_server_command(self, command: ExecuteCommandParams, done_callback: Callable[[], None]) -> bool:
        '''
        Intercept a command that is about to be sent to the language server.

        :param    command:        The payload containing a "command" and optionally "arguments".
        :param    done_callback:  The callback that you promise to invoke when you return true.

        :returns: True if *YOU* will handle this command plugin-side, false otherwise. You must invoke the
                  passed `done_callback` when you\'re done.
        '''
    def on_pre_send_request_async(self, request_id: int, request: Request[Any, Any]) -> None:
        """
        Notifies about a request that is about to be sent to the language server.
        This API is triggered on async thread.

        :param    request_id:  The request ID.
        :param    request:     The request object. The request params can be modified by the plugin.
        """
    def on_pre_send_notification_async(self, notification: Notification[Any]) -> None:
        """
        Notifies about a notification that is about to be sent to the language server.
        This API is triggered on async thread.

        :param    notification:  The notification object. The notification params can be modified by the plugin.
        """
    def on_server_response_async(self, method: str, response: Response[Any]) -> None:
        """
        Notifies about a response message that has been received from the language server.
        Only successful responses are passed to this method.

        :param    method:    The method of the request.
        :param    response:  The response object to the request. The response.result field can be modified by the
                             plugin, before it gets further handled by the LSP package.
        """
    def on_server_notification_async(self, notification: Notification[Any]) -> None:
        """
        Notifies about a notification message that has been received from the language server.

        :param    notification:  The notification object.
        """
    def on_open_uri_async(self, uri: DocumentUri, callback: Callable[[str | None, str, str], None]) -> bool:
        """
        Called when a language server reports to open an URI. If you know how to handle this URI, then return True and
        invoke the passed-in callback some time.

        The arguments of the provided callback work as follows:

        - The first argument is the title of the view that will be populated with the content of a new scratch view.
          If `None` is passed, no new view will be opened and the other arguments are ignored.
        - The second argument is the content of the view.
        - The third argument is the syntax to apply for the new view.
        """
    def on_session_buffer_changed_async(self, session_buffer: SessionBufferProtocol) -> None:
        """
        Called when the context of the session buffer has changed or a new buffer was opened.
        """
    def on_selection_modified_async(self, session_view: SessionViewProtocol) -> None:
        """
        Called after the selection has been modified in a view (debounced).
        """
    def on_session_end_async(self, exit_code: int | None, exception: Exception | None) -> None:
        """
        Notifies about the session ending (also if the session has crashed). Provides an opportunity to clean up
        any stored state or delete references to the session or plugin instance that would otherwise prevent the
        instance from being garbage-collected.

        If the session hasn't crashed, a shutdown message will be send immediately
        after this method returns. In this case exit_code and exception are None.
        If the session has crashed, the exit_code and an optional exception are provided.

        This API is triggered on async thread.
        """

_plugins: dict[str, tuple[type[AbstractPlugin], SettingsRegistration]]

def _register_plugin_impl(plugin: type[AbstractPlugin], notify_listener: bool) -> None: ...
def register_plugin(plugin: type[AbstractPlugin], notify_listener: bool = True) -> None:
    """
    Register an LSP plugin in LSP.

    You should put a call to this function in your `plugin_loaded` callback. This way, when your package is disabled
    by a user and then re-enabled again by a user, the changes in state are picked up by LSP, and your language server
    will start for the relevant views.

    While your helper package may still work without calling `register_plugin` in `plugin_loaded`, the user will have a
    better experience when you do call this function.

    Your implementation should look something like this:

    ```python
    from LSP.plugin import register_plugin
    from LSP.plugin import unregister_plugin
    from LSP.plugin import AbstractPlugin


    class MyPlugin(AbstractPlugin):
        ...


    def plugin_loaded():
        register_plugin(MyPlugin)

    def plugin_unloaded():
        unregister_plugin(MyPlugin)
    ```

    If you need to install supplementary files (e.g. javascript source code that implements the actual server), do so
    in `AbstractPlugin.install_or_update` in a blocking manner, without the use of Python's `threading` module.
    """
def unregister_plugin(plugin: type[AbstractPlugin]) -> None:
    """
    Unregister an LSP plugin in LSP.

    You should put a call to this function in your `plugin_unloaded` callback. this way, when your package is disabled
    by a user, your language server is shut down for the views that it is attached to. This results in a good user
    experience.
    """
def get_plugin(name: str) -> type[AbstractPlugin] | None: ...

class Logger(metaclass=ABCMeta):
    @abstractmethod
    def stderr_message(self, message: str) -> None: ...
    @abstractmethod
    def outgoing_response(self, request_id: int | str, params: Any) -> None: ...
    @abstractmethod
    def outgoing_error_response(self, request_id: int | str, error: Error) -> None: ...
    @abstractmethod
    def outgoing_request(self, request_id: int, method: str, params: Any) -> None: ...
    @abstractmethod
    def outgoing_notification(self, method: str, params: Any) -> None: ...
    @abstractmethod
    def incoming_response(self, request_id: int | str, params: Any, is_error: bool) -> None: ...
    @abstractmethod
    def incoming_request(self, request_id: int | str, method: str, params: Any) -> None: ...
    @abstractmethod
    def incoming_notification(self, method: str, params: Any, unhandled: bool) -> None: ...

def print_to_status_bar(error: ResponseError) -> None: ...
def method2attr(method: str) -> str: ...

class _RegistrationData:
    __slots__: Incomplete
    registration_id: Incomplete
    registration_path: Incomplete
    capability_path: Incomplete
    selector: Incomplete
    options: Incomplete
    session_buffers: WeakSet[SessionBufferProtocol]
    def __init__(self, registration_id: str, capability_path: str, registration_path: str, options: dict[str, Any]) -> None: ...
    def __del__(self) -> None: ...
    def check_applicable(self, sb: SessionBufferProtocol, *, suppress_requests: bool = False) -> None: ...

_WORK_DONE_PROGRESS_PREFIX: str
_PARTIAL_RESULT_PROGRESS_PREFIX: str

class Session(TransportCallbacks):
    transport: Transport | None
    working_directory: str | None
    request_id: int
    _logger: Incomplete
    _response_handlers: dict[int, tuple[Request[Any, Any], Callable[[Any], None], Callable[[ResponseError], None]]]
    config: Incomplete
    config_status_message: str
    manager: Incomplete
    window: Incomplete
    state: Incomplete
    capabilities: Incomplete
    diagnostics: Incomplete
    diagnostics_result_ids: dict[tuple[DocumentUri, DiagnosticsIdentifier], str | None]
    workspace_diagnostics_pending_responses: dict[DiagnosticsIdentifier, int | None]
    exiting: bool
    _registrations: dict[str, _RegistrationData]
    _init_callback: InitCallback | None
    _initialize_error: tuple[int, Exception | None] | None
    _views_opened: int
    _workspace_folders: Incomplete
    _session_views: WeakSet[SessionViewProtocol]
    _session_buffers: WeakSet[SessionBufferProtocol]
    _progress: dict[ProgressToken, WindowProgressReporter | None]
    _watcher_impl: Incomplete
    _static_file_watchers: list[FileWatcher]
    _dynamic_file_watchers: dict[str, list[FileWatcher]]
    _plugin_class: Incomplete
    _plugin: AbstractPlugin | None
    _status_messages: dict[str, str]
    _semantic_tokens_map: Incomplete
    _is_executing_refactoring_command: bool
    _logged_unsupported_commands: set[str]
    def __init__(self, manager: Manager, logger: Logger, workspace_folders: list[WorkspaceFolder], config: ClientConfig, plugin_class: type[AbstractPlugin] | None) -> None: ...
    def __getattr__(self, name: str) -> Any:
        """
        If we don't have a request/notification handler, look up the request/notification handler in the plugin.
        """
    def get_workspace_folders(self) -> list[WorkspaceFolder]: ...
    def uses_plugin(self) -> bool: ...
    @property
    def plugin(self) -> AbstractPlugin | None: ...
    def register_session_view_async(self, sv: SessionViewProtocol) -> None: ...
    def unregister_session_view_async(self, sv: SessionViewProtocol) -> None: ...
    def session_views_async(self) -> Generator[SessionViewProtocol, None, None]:
        """
        It is only safe to iterate over this in the async thread
        """
    def session_view_for_view_async(self, view: sublime.View) -> SessionViewProtocol | None: ...
    def set_config_status_async(self, message: str) -> None:
        """
        Sets the message that is shown in parenthesis within the permanent language server status.

        :param message: The message
        """
    def _redraw_config_status_async(self) -> None: ...
    def set_window_status_async(self, key: str, message: str) -> None: ...
    def erase_window_status_async(self, key: str) -> None: ...
    def register_session_buffer_async(self, sb: SessionBufferProtocol) -> None: ...
    def _publish_diagnostics_to_session_buffer_async(self, sb: SessionBufferProtocol, diagnostics: list[Diagnostic], version: int | None = None) -> None: ...
    def unregister_session_buffer_async(self, sb: SessionBufferProtocol) -> None: ...
    def session_buffers_async(self) -> Generator[SessionBufferProtocol, None, None]:
        """
        It is only safe to iterate over this in the async thread
        """
    def get_session_buffer_for_uri_async(self, uri: DocumentUri) -> SessionBufferProtocol | None: ...
    def can_handle(self, view: sublime.View, scheme: str, capability: str | None, inside_workspace: bool) -> bool: ...
    def has_capability(self, capability: str, *, check_views: bool = False) -> bool:
        """
        Check whether this `Session` has the given `capability`. If `check_views` is set to `True`, this includes
        capabilities from dynamic registration restricted to certain views if at least one such view is open and matches
        the corresponding `DocumentSelector`.
        """
    def get_capability(self, capability: str) -> Any | None: ...
    def should_notify_did_open(self) -> bool: ...
    def text_sync_kind(self) -> TextDocumentSyncKind: ...
    def should_notify_did_change_workspace_folders(self) -> bool: ...
    def should_notify_will_save(self) -> bool: ...
    def should_notify_did_save(self) -> tuple[bool, bool]: ...
    def should_notify_did_close(self) -> bool: ...
    def on_file_event_async(self, events: list[FileWatcherEvent]) -> None: ...
    def on_userprefs_changed_async(self) -> None: ...
    def markdown_language_id_to_st_syntax_map(self) -> MarkdownLangMap | None: ...
    def handles_path(self, file_path: str | None, inside_workspace: bool) -> bool: ...
    def update_folders(self, folders: list[WorkspaceFolder]) -> None: ...
    def initialize_async(self, variables: dict[str, str], working_directory: str | None, transport: Transport, init_callback: InitCallback) -> None: ...
    def _handle_initialize_success(self, result: InitializeResult) -> None: ...
    def _handle_initialize_error(self, result: ResponseError) -> None: ...
    def _get_global_ignore_globs(self, root_path: str) -> list[str]: ...
    def call_manager(self, method: str, *args: Any) -> None: ...
    def on_stderr_message(self, message: str) -> None: ...
    def _supports_workspace_folders(self) -> bool: ...
    def _maybe_send_did_change_configuration(self) -> None: ...
    def _template_variables(self) -> dict[str, str]: ...
    def execute_command(self, command: ExecuteCommandParams, *, progress: bool = False, view: sublime.View | None = None, is_refactoring: bool = False) -> Promise[R | Error | None]:
        """Run a command from any thread. Your .then() continuations will run in Sublime's worker thread."""
    def _reset_is_executing_refactoring_command(self) -> None: ...
    def check_log_unsupported_command(self, command: str) -> None: ...
    def run_code_action_async(self, code_action: Command | CodeAction, progress: bool, view: sublime.View | None = None) -> Promise[None]: ...
    def try_open_uri_async(self, uri: DocumentUri, r: Range | None = None, flags: sublime.NewFileFlags = ..., group: int = -1) -> Promise[sublime.View | None] | None: ...
    def open_uri_async(self, uri: DocumentUri, r: Range | None = None, flags: sublime.NewFileFlags = ..., group: int = -1) -> Promise[sublime.View | None]: ...
    def _open_file_uri_async(self, uri: DocumentUri, r: Range | None = None, flags: sublime.NewFileFlags = ..., group: int = -1) -> Promise[sublime.View | None]: ...
    def _open_res_uri_async(self, uri: DocumentUri, r: Range | None = None, group: int = -1) -> Promise[sublime.View | None]: ...
    def _open_uri_with_plugin_async(self, plugin: AbstractPlugin, uri: DocumentUri, r: Range | None, flags: sublime.NewFileFlags, group: int) -> Promise[sublime.View | None] | None: ...
    def open_location_async(self, location: Location | LocationLink, flags: sublime.NewFileFlags = ..., group: int = -1) -> Promise[sublime.View | None]: ...
    def notify_plugin_on_session_buffer_change(self, session_buffer: SessionBufferProtocol) -> None: ...
    def _maybe_resolve_code_action(self, code_action: CodeAction, view: sublime.View | None) -> Promise[CodeAction | Error]: ...
    def _apply_code_action_async(self, code_action: CodeAction | Error | None, view: sublime.View | None) -> Promise[None]: ...
    def apply_workspace_edit_async(self, edit: WorkspaceEdit, *, label: str | None = None, is_refactoring: bool = False) -> Promise[WorkspaceEditSummary]:
        """
        Apply a WorkspaceEdit, and return a promise that resolves on the async thread again after the edits have been
        applied. The resolved promise contains a summary of the changes in the WorkspaceEdit.
        """
    def apply_parsed_workspace_edits(self, changes: WorkspaceChanges, is_refactoring: bool = False) -> Promise[WorkspaceEditSummary]: ...
    def _get_view_state_actions(self, uri: DocumentUri, auto_save: str) -> ViewStateActions:
        '''
        Determine the required actions for a view after applying a WorkspaceEdit, depending on the
        "refactoring_auto_save" user setting. Returns a bitwise combination of ViewStateActions.Save and
        ViewStateActions.Close, or 0 if no action is necessary.
        '''
    def _set_view_state(self, actions: ViewStateActions, view: sublime.View) -> Promise[None]: ...
    def _set_selected_sheets(self, sheets: list[sublime.Sheet]) -> None: ...
    def _set_focused_sheet(self, sheet: sublime.Sheet | None) -> None: ...
    def decode_semantic_token(self, types_legend: tuple[str, ...], modifiers_legend: tuple[str, ...], token_type_encoded: int, token_modifiers_encoded: int) -> tuple[str, list[str], str | None]: ...
    def session_views_by_visibility(self) -> tuple[set[SessionViewProtocol], set[SessionViewProtocol]]: ...
    def do_workspace_diagnostics_async(self) -> None: ...
    def _do_workspace_diagnostics_async(self, identifier: DiagnosticsIdentifier) -> None: ...
    def _on_workspace_diagnostics_async(self, identifier: DiagnosticsIdentifier, response: WorkspaceDiagnosticReport, *, reset_pending_response: bool = True) -> None: ...
    def _on_workspace_diagnostics_error_async(self, identifier: DiagnosticsIdentifier, error: ResponseError) -> None: ...
    def m_window_showMessageRequest(self, params: ShowMessageRequestParams, request_id: int | str) -> None:
        """handles the window/showMessageRequest request"""
    def m_window_showMessage(self, params: ShowMessageParams) -> None:
        """handles the window/showMessage notification"""
    def m_window_logMessage(self, params: LogMessageParams) -> None:
        """handles the window/logMessage notification"""
    def m_workspace_workspaceFolders(self, params: None, request_id: int | str) -> None:
        """handles the workspace/workspaceFolders request"""
    def m_workspace_configuration(self, params: ConfigurationParams, request_id: int | str) -> None:
        """handles the workspace/configuration request"""
    def m_workspace_applyEdit(self, params: ApplyWorkspaceEditParams, request_id: int | str) -> None:
        """handles the workspace/applyEdit request"""
    def m_workspace_codeLens_refresh(self, params: None, request_id: int | str) -> None:
        """handles the workspace/codeLens/refresh request"""
    def m_workspace_semanticTokens_refresh(self, params: None, request_id: int | str) -> None:
        """handles the workspace/semanticTokens/refresh request"""
    def m_workspace_inlayHint_refresh(self, params: None, request_id: int | str) -> None:
        """handles the workspace/inlayHint/refresh request"""
    def m_workspace_diagnostic_refresh(self, params: None, request_id: int | str) -> None:
        """handles the workspace/diagnostic/refresh request"""
    def m_textDocument_publishDiagnostics(self, params: PublishDiagnosticsParams) -> None:
        """handles the textDocument/publishDiagnostics notification"""
    def handle_diagnostics_async(self, uri: DocumentUri, identifier: DiagnosticsIdentifier, version: int | None, diagnostics: list[Diagnostic]) -> None: ...
    def m_client_registerCapability(self, params: RegistrationParams, request_id: int | str) -> None:
        """handles the client/registerCapability request"""
    def m_client_unregisterCapability(self, params: UnregistrationParams, request_id: int | str) -> None:
        """handles the client/unregisterCapability request"""
    def register_file_system_watchers(self, registration_id: str, watchers: list[FileSystemWatcher]) -> None: ...
    def unregister_file_system_watchers(self, registration_id: str) -> None: ...
    def m_window_showDocument(self, params: ShowDocumentParams, request_id: int | str) -> None:
        """handles the window/showDocument request"""
    def m_window_workDoneProgress_create(self, params: WorkDoneProgressCreateParams, request_id: int | str) -> None:
        """handles the window/workDoneProgress/create request"""
    def _invoke_views(self, request: Request[Any, Any], method: str, *args: Any) -> None: ...
    def _create_window_progress_reporter(self, token: ProgressToken, value: WorkDoneProgressBegin) -> None: ...
    def m___progress(self, params: ProgressParams) -> None:
        """handles the $/progress notification"""
    def end_async(self) -> None: ...
    def shutdown_session_view_async(self, session_view: SessionViewProtocol) -> None: ...
    def _handle_shutdown_result(self, _: Any) -> None: ...
    def on_transport_close(self, exit_code: int, exception: Exception | None) -> None: ...
    def send_request_async(self, request: Request[P, R], on_result: Callable[[R], None], on_error: Callable[[ResponseError], None] | None = None) -> int:
        """You must call this method from Sublime's worker thread. Callbacks will run in Sublime's worker thread."""
    def send_request(self, request: Request[P, R], on_result: Callable[[R], None], on_error: Callable[[ResponseError], None] | None = None) -> None:
        """You can call this method from any thread. Callbacks will run in Sublime's worker thread."""
    def send_request_task(self, request: Request[P, R]) -> Promise[R | Error]: ...
    def send_request_task_2(self, request: Request[P, R]) -> tuple[Promise[R | Error], int]: ...
    def cancel_request_async(self, request_id: int) -> None: ...
    def send_notification(self, notification: Notification[P]) -> None: ...
    def send_response(self, response: Response[P]) -> None: ...
    def send_error_response(self, request_id: int | str, error: Error) -> None: ...
    def exit(self) -> None: ...
    def send_payload(self, payload: JSONRPCMessage) -> None: ...
    def deduce_payload(self, payload: dict[str, Any]) -> tuple[Callable | None, Any, int | None, str | None, str | None]: ...
    def on_payload(self, payload: dict[str, Any]) -> None: ...
    def response_handler(self, response_id: int, response: dict[str, Any]) -> tuple[Callable[[ResponseError], None], str | None, Any, bool]: ...
    def _get_handler(self, method: str) -> Callable | None: ...
