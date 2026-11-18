# This file is maintained on https://github.com/jfcherng-sublime/ST-API-stubs
# ST version: 4136

from __future__ import annotations

import importlib.abc
import importlib.resources.abc
import io
import os
import threading
from importlib.machinery import ModuleSpec
from types import ModuleType
from typing import (
    Any,
    Callable,
    Dict,
    Generator,
    Generic,
    Iterable,
    Iterator,
    List,
    Sequence,
    Set,
    Tuple,
    Type,
    TypeVar,
    overload,
)

import sublime
from _sublime_types import AnyCallable, Completion, CompletionNormalized, EventDict, Point, T_AnyCallable

# ----- #
# types #
# ----- #

InputType = None | str | int | float | Dict[str, Any] | List[Any] | Tuple[Any, ...]
T_InputType = TypeVar("T_InputType", bound=InputType)

# -------- #
# ST codes #
# -------- #

api_ready: bool = False

deferred_plugin_loadeds: List[Callable[[], None]] = []

application_command_classes: List[Type] = []
window_command_classes: List[Type] = []
text_command_classes: List[Type] = []

view_event_listener_classes: List[Type] = []
view_event_listeners: Dict[int, List[ViewEventListener]] = {}

all_command_classes: List[List[Type]] = [application_command_classes, window_command_classes, text_command_classes]

all_callbacks: Dict[str, List[object]] = {
    "on_init": [],
    "on_new": [],
    "on_clone": [],
    "on_load": [],
    "on_revert": [],
    "on_reload": [],
    "on_pre_close": [],
    "on_close": [],
    "on_pre_save": [],
    "on_post_save": [],
    "on_pre_move": [],
    "on_post_move": [],
    "on_modified": [],
    "on_selection_modified": [],
    "on_activated": [],
    "on_deactivated": [],
    "on_query_context": [],
    "on_query_completions": [],
    "on_hover": [],
    "on_text_command": [],
    "on_window_command": [],
    "on_post_text_command": [],
    "on_post_window_command": [],
    "on_modified_async": [],
    "on_selection_modified_async": [],
    "on_pre_save_async": [],
    "on_post_save_async": [],
    "on_post_move_async": [],
    "on_activated_async": [],
    "on_deactivated_async": [],
    "on_new_async": [],
    "on_load_async": [],
    "on_revert_async": [],
    "on_reload_async": [],
    "on_clone_async": [],
    "on_new_buffer": [],
    "on_new_buffer_async": [],
    "on_close_buffer": [],
    "on_close_buffer_async": [],
    "on_new_project": [],
    "on_new_project_async": [],
    "on_load_project": [],
    "on_load_project_async": [],
    "on_pre_save_project": [],
    "on_post_save_project": [],
    "on_post_save_project_async": [],
    "on_pre_close_project": [],
    "on_new_window": [],
    "on_new_window_async": [],
    "on_pre_close_window": [],
    "on_exit": [],
}

pending_on_activated_async_lock: threading.Lock = threading.Lock()

pending_on_activated_async_callbacks: Dict[str, List[Type]] = {"EventListener": [], "ViewEventListener": []}

view_event_listener_excluded_callbacks: Set[str] = {
    "on_clone",
    "on_clone_async",
    "on_exit",
    "on_init",
    "on_load_project",
    "on_load_project_async",
    "on_new",
    "on_new_async",
    "on_new_buffer",
    "on_new_buffer_async",
    "on_associate_buffer",
    "on_associate_buffer_async",
    "on_close_buffer",
    "on_close_buffer_async",
    "on_new_project",
    "on_new_project_async",
    "on_new_window",
    "on_new_window_async",
    "on_post_save_project",
    "on_post_save_project_async",
    "on_post_window_command",
    "on_pre_close_project",
    "on_pre_close_window",
    "on_pre_save_project",
    "on_window_command",
}

text_change_listener_classes: List[Type] = []
text_change_listener_callbacks: Set[str] = {
    "on_text_changed",
    "on_text_changed_async",
    "on_revert",
    "on_revert_async",
    "on_reload",
    "on_reload_async",
}
text_change_listeners: Dict[int, List[TextChangeListener]] = {}

profile: Dict[str, Dict[str, Any]] = {}


def add_profiling(event_handler: T_AnyCallable) -> T_AnyCallable:
    """
    Decorator to measure blocking event handler methods. Also prevents
    exceptions from interrupting other events handlers.

    :param event_handler:
        The event handler method - must be an unbound method

    :return:
        The decorated method
    """
    ...


def trap_exceptions(event_handler: T_AnyCallable) -> T_AnyCallable:
    """
    Decorator to prevent exceptions from interrupting other events handlers.

    :param event_handler:
        The event handler method - must be an unbound method

    :return:
        The decorated method
    """
    ...


def decorate_handler(cls: Type, method_name: str) -> None:
    """
    Decorates an event handler method with exception trapping, and in the case
    of blocking calls, profiling.

    :param cls:
        The class object to decorate

    :param method_name:
        A unicode string of the name of the method to decorate
    """
    ...


def unload_module(module: ModuleType) -> None:
    ...


def unload_plugin(modulename: str) -> None:
    ...


def reload_plugin(modulename: str) -> None:
    ...


def load_module(m: ModuleType) -> None:
    ...


def synthesize_on_activated_async() -> None:
    ...


def _instantiation_error(cls: Type, e: Exception) -> None:
    ...


def notify_application_commands() -> None:
    ...


def create_application_commands() -> List[Tuple[ApplicationCommand, str]]:
    ...


def create_window_commands(window_id: int) -> List[Tuple[WindowCommand, str]]:
    ...


def create_text_commands(view_id: int) -> List[Tuple[TextCommand, str]]:
    ...


def on_api_ready() -> None:
    ...


def is_view_event_listener_applicable(cls: Type[ViewEventListener], view: sublime.View) -> bool:
    ...


def create_view_event_listeners(classes: Iterable[Type[ViewEventListener]], view: sublime.View) -> None:
    ...


def check_view_event_listeners(view: sublime.View) -> None:
    ...


def attach_view(view: sublime.View) -> None:
    ...


check_all_view_event_listeners_scheduled: bool = False


def check_all_view_event_listeners() -> None:
    ...


def detach_view(view: sublime.View) -> None:
    ...


def find_view_event_listener(view: sublime.View, cls: Type) -> None | ViewEventListener:
    """Find the view event listener object, whose class is `cls`, for the `view`."""
    ...


def attach_buffer(buf: sublime.Buffer) -> None:
    ...


def check_text_change_listeners(buf: sublime.Buffer) -> None:
    ...


def detach_buffer(buf: sublime.Buffer) -> None:
    ...


def plugin_module_for_obj(obj: object) -> str:
    ...


def el_callbacks(name: str, listener_only: bool = False) -> Generator[Type | str, None, None]:
    ...


def vel_callbacks(v: sublime.View, name: str, listener_only: bool = False) -> Generator[Type | str, None, None]:
    ...


def run_view_callbacks(
    name: str,
    view_id: int,
    *args: Any,
    el_only: bool = False,
) -> None:
    ...


def run_window_callbacks(name: str, window_id: int, *args: Any) -> None:
    ...


def on_init(module: str) -> None:
    """
    Trigger the on_init() methods on EventListener and ViewEventListener
    objects. This is method that allows event listeners to run something
    once per view, even if the view is done loading before the listener
    starts listening.

    :param module:
        A unicode string of the name of a plugin module to filter listeners by
    """
    ...


def on_new(view_id: int) -> None:
    ...


def on_new_async(view_id: int) -> None:
    ...


def on_new_buffer(buffer_id: int) -> None:
    ...


def on_new_buffer_async(buffer_id: int) -> None:
    ...


def on_associate_buffer(buffer_id: int) -> None:
    ...


def on_associate_buffer_async(buffer_id: int) -> None:
    ...


def on_close_buffer(buffer_id: int) -> None:
    ...


def on_close_buffer_async(buffer_id: int) -> None:
    ...


def on_clone(view_id: int) -> None:
    ...


def on_clone_async(view_id: int) -> None:
    ...


class Summary:
    max: float
    sum: float
    count: int

    def __init__(self) -> None:
        ...

    def record(self, x: float) -> None:
        ...


def get_profiling_data() -> List[Tuple[str, str, int, float, float]]:
    ...


def on_load(view_id: int) -> None:
    ...


def on_load_async(view_id: int) -> None:
    ...


def on_revert(view_id: int) -> None:
    ...


def on_revert_async(view_id: int) -> None:
    ...


def on_reload(view_id: int) -> None:
    ...


def on_reload_async(view_id: int) -> None:
    ...


def on_pre_close(view_id: int) -> None:
    ...


def on_close(view_id: int) -> None:
    ...


def on_pre_save(view_id: int) -> None:
    ...


def on_pre_save_async(view_id: int) -> None:
    ...


def on_post_save(view_id: int) -> None:
    ...


def on_post_save_async(view_id: int) -> None:
    ...


def on_pre_move(view_id: int) -> None:
    ...


def on_post_move(view_id: int) -> None:
    ...


def on_post_move_async(view_id: int) -> None:
    ...


def on_modified(view_id: int) -> None:
    ...


def on_modified_async(view_id: int) -> None:
    ...


def on_selection_modified(view_id: int) -> None:
    ...


def on_selection_modified_async(view_id: int) -> None:
    ...


def on_activated(view_id: int) -> None:
    ...


def on_activated_async(view_id: int) -> None:
    ...


def on_deactivated(view_id: int) -> None:
    ...


def on_deactivated_async(view_id: int) -> None:
    ...


def on_query_context(
    view_id: int,
    key: str,
    operator: str,
    operand: Any,
    match_all: bool,
) -> None | bool:
    ...


def normalise_completion(c: sublime.CompletionItem | str | Sequence[str]) -> CompletionNormalized:
    ...


class MultiCompletionList:
    remaining_calls: int
    view_id: int
    req_id: int
    completions: List[CompletionNormalized]
    flags: int

    def __init__(self, num_completion_lists: int, view_id: int, req_id: int) -> None:
        ...

    def completions_ready(
        self,
        completions: Iterable[sublime.CompletionItem | str | Sequence[str]],
        flags: int,
    ) -> None:
        ...


def on_query_completions(
    view_id: int,
    req_id: int,
    prefix: str,
    locations: Sequence[Point],
) -> None | List[Completion] | Tuple[List[Completion], int]:
    ...


def on_hover(view_id: int, point: Point, hover_zone: int) -> None:
    ...


def on_text_command(
    view_id: int,
    name: str,
    args: None | Dict[str, Any],
) -> None | Tuple[str, None | Dict[str, Any]]:
    ...


def on_window_command(
    window_id: int,
    name: str,
    args: None | Dict[str, Any],
) -> None | Tuple[str, None | Dict[str, Any]]:
    ...


def on_post_text_command(view_id: int, name: str, args: None | Dict[str, Any]) -> None:
    ...


def on_post_window_command(window_id: int, name: str, args: None | Dict[str, Any]) -> None:
    ...


def on_new_project(window_id: int) -> None:
    ...


def on_new_project_async(window_id: int) -> None:
    ...


def on_load_project(window_id: int) -> None:
    ...


def on_load_project_async(window_id: int) -> None:
    ...


def on_pre_save_project(window_id: int) -> None:
    ...


def on_post_save_project(window_id: int) -> None:
    ...


def on_post_save_project_async(window_id: int) -> None:
    ...


def on_pre_close_project(window_id: int) -> None:
    ...


def on_new_window(window_id: int) -> None:
    ...


def on_new_window_async(window_id: int) -> None:
    ...


def on_pre_close_window(window_id: int) -> None:
    ...


def on_exit(log_path: str) -> None:
    ...


class CommandInputHandler(Generic[T_InputType]):
    def name(self) -> str:
        """
        The command argument name this input handler is editing.
        Defaults to `foo_bar` for an input handler named `FooBarInputHandler`.
        """
        ...

    def next_input(self, args: Dict[str, Any]) -> None | CommandInputHandler[InputType]:
        """
        Returns the next input after the user has completed this one.
        May return None to indicate no more input is required,
        or `sublime_plugin.BackInputHandler()` to indicate that
        the input handler should be poped off the stack instead.
        """
        ...

    def placeholder(self) -> str:
        """
        Placeholder text is shown in the text entry box before the user has entered anything.
        Empty by default.
        """
        ...

    def initial_text(self) -> str:
        """Initial text shown in the text entry box. Empty by default."""
        ...

    def initial_selection(
        self,
    ) -> List[Tuple[List[str | Tuple[str, T_InputType] | sublime.ListInputItem[T_InputType]], int]]:
        """A list of 2-element tuplues, defining the initially selected parts of the initial text."""
        ...

    def preview(self, arg: T_InputType) -> str | sublime.Html:
        """
        Called whenever the user changes the text in the entry box.
        The returned value (either plain text or HTML) will be shown in the preview area of the Command Palette.
        """
        ...

    def validate(self, arg: T_InputType) -> bool:
        """
        Called whenever the user presses enter in the text entry box.
        Return False to disallow the current value.
        """
        ...

    def cancel(self) -> None:
        """Called when the input handler is canceled, either by the user pressing backspace or escape."""
        ...

    @overload
    def confirm(self, arg: T_InputType) -> None:
        """Called when the input is accepted, after the user has pressed enter and the text has been validated."""
        ...

    @overload
    def confirm(self, arg: T_InputType, event: EventDict) -> None:
        """Called when the input is accepted, after the user has pressed enter and the text has been validated."""
        ...

    def create_input_handler_(self, args: Dict[str, Any]) -> None | CommandInputHandler[T_InputType]:
        ...

    def preview_(self, v: str) -> Tuple[str, int]:
        ...

    def validate_(self, v: str) -> bool:
        ...

    def cancel_(self) -> None:
        ...

    def confirm_(self, v: str) -> None:
        ...

    def want_event(self) -> bool:
        ...


class BackInputHandler(CommandInputHandler[None]):
    def name(self) -> str:
        """The command argument name this input handler is editing. Defaults to `_Back`."""
        ...


class TextInputHandler(CommandInputHandler[str]):
    """
    TextInputHandlers can be used to accept textual input in the Command Palette.
    Return a subclass of this from the `input()` method of a command.
    """

    def description(self, text: str) -> str:
        """
        The text to show in the Command Palette when this input handler is not at the top of the input handler stack.
        Defaults to the text the user entered.
        """
        ...

    def setup_(self, args: Dict[Any, Any]) -> Tuple[List[Any], Dict[str, str]]:
        ...

    def description_(self, v: str, text: str) -> str:
        ...


class ListInputHandler(CommandInputHandler[T_InputType], Generic[T_InputType]):
    """
    ListInputHandlers can be used to accept a choice input from a list items in the Command Palette.
    Return a subclass of this from the input() method of a command.
    """

    def list_items(
        self,
    ) -> (
        List[str | Tuple[str, T_InputType] | sublime.ListInputItem[T_InputType]]
        | Tuple[List[str | Tuple[str, T_InputType] | sublime.ListInputItem[T_InputType]], int]
    ):
        """
        The items to show in the list. If returning a list of `(str, value)` tuples,
        then the str will be shown to the user, while the value will be used as the command argument.

        Optionally return a tuple of `(list_items, selected_item_index)` to indicate an initial selection.
        """
        ...

    def description(self, v: str, text: str) -> str:
        """
        The text to show in the Command Palette when this input handler is not at the top of the input handler stack.
        Defaults to the text of the list item the user selected.
        """
        ...

    def setup_(self, args: Dict[Any, Any]) -> Tuple[List[Tuple[Any, ...]], Dict[str, str]]:
        ...

    def description_(self, v: str, text: str) -> str:
        ...


class Command:
    def name(self) -> str:
        """
        The command argument name this input handler is editing.
        Defaults to `foo_bar` for an input handler named `FooBarInputHandler`.
        """
        ...

    def is_enabled_(self, args: Dict[str, Any]) -> bool:
        ...

    def is_enabled(self) -> bool:
        """
        Returns True if the command is able to be run at this time.
        The default implementation simply always returns True.
        """
        ...

    def is_visible_(self, args: Dict[str, Any]) -> bool:
        ...

    def is_visible(self) -> bool:
        """
        Returns True if the command should be shown in the menu at this time.
        The default implementation always returns True.
        """
        ...

    def is_checked_(self, args: Dict[str, Any]) -> bool:
        ...

    def is_checked(self) -> bool:
        """
        Returns True if a checkbox should be shown next to the menu item.
        The `.sublime-menu` file must have the "checkbox key set to true for this to be used.
        """
        ...

    def description_(self, args: Dict[str, Any]) -> str:
        ...

    def description(self) -> str:
        """
        Returns a description of the command with the given arguments.
        Used in the menus, and for Undo / Redo descriptions.
        Return None to get the default description.
        """
        ...

    def filter_args(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Returns the args after without the "event" entry"""
        ...

    def want_event(self) -> bool:
        """
        Return True to receive an event argument when the command is triggered by a mouse action.
        The event information allows commands to determine which portion of the view was clicked on.
        The default implementation returns False.
        """
        ...

    def input(self, args: Dict[str, Any]) -> None | CommandInputHandler[InputType]:
        """
        If this returns something other than `None`,
        the user will be prompted for an input before the command is run in the Command Palette.
        """
        ...

    def input_description(self) -> str:
        """
        Allows a custom name to be show to the left of the cursor in the input box,
        instead of the default one generated from the command name.
        """
        ...

    def create_input_handler_(self, args: Dict[str, Any]) -> None | CommandInputHandler[InputType]:
        ...


class ApplicationCommand(Command):
    """ApplicationCommands are instantiated once per application."""

    def run_(self, edit_token: int, args: Dict[str, Any]) -> None:
        ...

    run: AnyCallable


class WindowCommand(Command):
    """WindowCommands are instantiated once per window. The Window object may be retrieved via `self.window`"""

    window: sublime.Window

    def __init__(self, window: sublime.Window) -> None:
        ...

    def run_(self, edit_token: int, args: Dict[str, Any]) -> None:
        ...

    run: AnyCallable


class TextCommand(Command):
    """TextCommands are instantiated once per view. The View object may be retrieved via `self.view`"""

    view: sublime.View

    def __init__(self, view: sublime.View) -> None:
        ...

    def run_(self, edit_token: int, args: Dict[str, Any]) -> None:
        ...

    run: AnyCallable


class EventListener:
    pass


class ViewEventListener:
    """
    A class that provides similar event handling to EventListener, but bound to a specific view.
    Provides class method-based filtering to control what views objects are created for.

    The view is passed as a single parameter to the constructor.
    The default implementation makes the view available via `self.view`.
    """

    view: sublime.View

    @classmethod
    def is_applicable(cls, settings: sublime.Settings) -> bool:
        """
        Receives a Settings object and should return a bool
        indicating if this class applies to a view with those settings.
        """
        ...

    @classmethod
    def applies_to_primary_view_only(cls) -> bool:
        """
        Returns a bool indicating if this class applies only to the primary view for a file.
        A view is considered primary if it is the only, or first, view into a file.
        """
        ...

    def __init__(self, view: sublime.View) -> None:
        ...


class TextChangeListener:
    """
    Base implementation of a text change listener.

    An instance may be added to a view using `sublime.View.add_text_listener`.

    Has the following callbacks:

    on_text_changed(changes):
        Called when text is changed in a buffer.

        :param changes:
            A list of TextChange

    on_text_changed_async(changes):
        Async version of on_text_changed_async.

    on_revert():
        Called when the buffer is reverted.

        A revert does not trigger text changes. If the contents of the buffer
        are required here use View.substr()

    on_revert_async():
        Async version of on_revert_async.

    on_reload():
        Called when the buffer is reloaded.

        A reload does not trigger text changes. If the contents of the buffer
        are required here use View.substr()

    on_reload_async():
        Async version of on_reload_async.
    """

    __key: None | int
    buffer: None | sublime.Buffer

    @classmethod
    def is_applicable(cls, buffer: sublime.Buffer) -> bool:
        """
        Receives a Buffer object and should return a bool
        indicating if this class applies to a view with the Buffer.
        """
        ...

    def __init__(self) -> None:
        ...

    def detach(self) -> None:
        """
        Remove this listener from the buffer.

        Async callbacks may still be called after this, as they are queued separately.
        """
        ...

    def attach(self, buffer: sublime.Buffer) -> None:
        """Attach this listener to a buffer."""
        ...

    def is_attached(self) -> bool:
        """
        Check whether the listener is receiving events from a buffer.
        May not be called from __init__.
        """
        ...


class MultizipImporter(importlib.abc.MetaPathFinder):
    loaders: List[importlib.abc.Loader]

    def __init__(self) -> None:
        ...

    def _make_spec(self, loader: importlib.abc.Loader, fullname: str) -> ModuleSpec:
        """
        :param loader:
            The importlib.abc.Loader to create the ModuleSpec from

        :param fullname:
            A unicode string of the module name

        :return:
            An instance of importlib.machinery.ModuleSpec()
        """
        ...

    def find_spec(
        self,
        fullname: str,
        path: None | Sequence[bytes | str],
        target: None | Any = None,
    ) -> None | ModuleSpec:
        """
        :param fullname:
            A unicode string of the module name

        :param path:
            None or a list with a single unicode string of the __path__ of
            the parent module if importing a submodule

        :param target:
            Unused - extra info that importlib may provide?

        :return:
            An importlib.machinery.ModuleSpec() object
        """
        ...


class ZipResourceReader(importlib.resources.abc.ResourceReader):
    """
    Implements the resource reader interface introduced in Python 3.7
    """

    loader: ZipLoader
    fullname: str

    def __init__(self, loader: ZipLoader, fullname: str) -> None:
        """
        :param loader:
            The source ZipLoader() object

        :param fullname:
            A unicode string of the module name to load resources for
        """
        ...

    def open_resource(self, resource: bytes | str | os.PathLike[Any]) -> io.BytesIO:
        """
        :param resource:
            A unicode string of a resource name - should not contain a path
            separator

        :raises:
            FileNotFoundError - when the resource doesn't exist

        :return:
            An io.BytesIO() object
        """
        ...

    def resource_path(self, resource: bytes | str | os.PathLike[Any]) -> str:
        """
        :param resource:
            A unicode string of a resource name - should not contain a path
            separator

        :raises:
            FileNotFoundError - always, since there is no normal filesystem access
        """
        ...

    def is_resource(self, name: str) -> bool:
        """
        :param name:
            A unicode string of a file name to check if it is a resource

        :return:
            A boolean indicating if the file is a resource
        """
        ...

    def contents(self) -> Iterator[str]:
        """
        :return:
            A list of the resources for this module
        """
        ...


class ZipLoader(importlib.abc.InspectLoader):
    """
    A custom Python loader that handles loading .py and .pyc files from
    .sublime-package zip files, and supports overrides where a loose file in
    the Packages/ folder of the data dir may be loaded instead of a file in
    the .sublime-package file.
    """

    zippath: str
    name: str

    contents: Dict[str, str]
    filenames: Dict[str, str]
    packages: Set[str]
    resources: Dict[str, Dict[str, str]]
    refreshed: float

    def __init__(self, zippath: str) -> None:
        """
        :param zippath:
            A unicode string of the full filesystem path to the zip file
        """
        ...

    def _get_name_key(self, fullname: str) -> Tuple[None, None] | Tuple[str, str]:
        """
        Converts a module name into a pair of package name and key. The
        key is used to access the various data structures in this object.

        :param fullname:
            A unicode string of a module name

        :return:
            If the fullname is not a module in this package, (None, None),
            otherwise a 2-element tuple of unicode strings. The first element
            being the package name, and the second being a sub-module, e.g.
            ("Default", "indentation").
        """
        ...

    def has(self, fullname: str) -> bool:
        """
        Checks if the module is handled by this loader

        :param fullname:
            A unicode string of the module to check

        :return:
            A boolean if the module is handled by this loader
        """
        ...

    def get_resource_reader(self, fullname: str) -> None | importlib.resources.abc.ResourceReader:
        """
        :param fullname:
            A unicode string of the module name to get the resource reader for

        :return:
            None if the module is not a package, otherwise an object that
            implements the importlib.abc.ResourceReader() interface
        """
        ...

    def get_filename(self, fullname: str) -> str:
        """
        :param fullname:
            A unicode string of the module name

        :raises:
            ImportError - when the module has no file path

        :return:
            A unicode string of the file path to the module
        """
        ...

    def get_code(self, fullname: str) -> Any:
        """
        :param fullname:
            A unicode string of the module to get the code for

        :raises:
            ModuleNotFoundError - when the module is not part of this zip file
            ImportError - when there is an error loading the code

        :return:
            A code object for the module
        """
        ...

    def get_source(self, fullname: str) -> None | str:
        """
        :param fullname:
            A unicode string of the module to get the source for

        :raises:
            ModuleNotFoundError - when the module is not part of this zip file
            ImportError - when there is an error loading the source file

        :return:
            A unicode string of the source code, or None if there is no source
            for the module (i.e. a .pyc file)
        """
        ...

    def _load_source(self, fullname: str, path: str) -> str:
        """
        Loads the source code to the module

        :param fullname:
            A unicode string of the module name

        :param path:
            A filesystem path to the module - may be a path into s
            .sublime-package file

        :return:
            A unicode string
        """
        ...

    def is_package(self, fullname: str) -> bool:
        """
        :param fullname:
            A unicode string of the module to see if it is a package

        :return:
            A boolean if the module is a package
        """
        ...

    def _spec_info(self, fullname: str) -> Tuple[None, None] | Tuple[str, bool]:
        """
        :param fullname:
            A unicode string of the module that an
            importlib.machinery.ModuleSpec() object is going to be created for

        :return:
            A 2-element tuple of:
             - (None, None) if the loader does not know about the module
             - (unicode string, bool) of the origin and is_package params to
               pass to importlib.machinery.ModuleSpec()
        """
        ...

    def _scan_zip(self) -> None:
        """
        Rebuild the internal cached info about the contents of the zip
        """
        ...


override_path: None | str = None
multi_importer: MultizipImporter = MultizipImporter()


def update_compressed_packages(pkgs: Iterable[str]) -> None:
    ...


def set_override_path(path: str) -> None:
    ...
