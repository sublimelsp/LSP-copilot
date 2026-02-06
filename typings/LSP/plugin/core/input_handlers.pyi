import sublime
import sublime_plugin
from .constants import ST_VERSION as ST_VERSION
from _typeshed import Incomplete
from abc import ABCMeta, abstractmethod
from typing import Any, Callable, final
from typing_extensions import ParamSpec

ListItemsReturn = list[str] | tuple[list[str], int] | list[tuple[str, Any]] | tuple[list[tuple[str, Any]], int] | list[sublime.ListInputItem] | tuple[list[sublime.ListInputItem], int]
P = ParamSpec('P')

def debounced(user_function: Callable[P, Any]) -> Callable[P, None]:
    """ A decorator which debounces the calls to a function.

    Note that the return value of the function will be discarded, so it only makes sense to use this decorator for
    functions that return None. The function will run on Sublime's main thread.
    """

class PreselectedListInputHandler(sublime_plugin.ListInputHandler, metaclass=ABCMeta):
    """ A ListInputHandler which can preselect a value.

    Subclasses of PreselectedListInputHandler must not implement the `list_items` method, but instead `get_list_items`,
    i.e. just prepend `get_` to the regular `list_items` method.

    To create an instance of PreselectedListInputHandler pass the window to the constructor, and optionally a second
    argument `initial_value` to preselect a value. Usually you then want to use the `next_input` method to push another
    InputHandler onto the input stack.

    Inspired by https://github.com/sublimehq/sublime_text/issues/5507.
    """
    _window: Incomplete
    _initial_value: Incomplete
    def __init__(self, window: sublime.Window, initial_value: str | sublime.ListInputItem | None = None) -> None: ...
    @final
    def list_items(self) -> ListItemsReturn: ...
    def _select_and_reset(self) -> None: ...
    @abstractmethod
    def get_list_items(self) -> ListItemsReturn: ...

class DynamicListInputHandler(sublime_plugin.ListInputHandler, metaclass=ABCMeta):
    """ A ListInputHandler which can update its items while typing in the input field.

    Subclasses of DynamicListInputHandler must not implement the `list_items` method, but can override
    `get_list_items` for the initial list items. The `on_modified` method will be called after a small delay (debounced)
    whenever changes were made to the input text. You can use this to call the `update` method with a list of
    `ListInputItem`s to update the list items.

    To create an instance of the derived class pass the command instance and the command arguments to the constructor,
    like this:

    def input(self, args):
        return MyDynamicListInputHandler(self, args)

    For now, the type of the command must be a WindowCommand, but maybe it can be generalized later if needed.
    This class will set and modify `_items` and '_text' attributes of the command, so make sure that those attribute
    names are not used in another way in the command's class.
    """
    command: Incomplete
    args: Incomplete
    text: Incomplete
    listener: sublime_plugin.TextChangeListener | None
    input_view: sublime.View | None
    def __init__(self, command: sublime_plugin.WindowCommand, args: dict[str, Any]) -> None: ...
    def _attach_listener(self) -> None: ...
    def _detach_listener(self) -> None: ...
    @final
    def list_items(self) -> list[sublime.ListInputItem]: ...
    def _select_first_row(self) -> None: ...
    def initial_text(self) -> str: ...
    def initial_selection(self) -> list[tuple[int, int]]: ...
    def validate(self, text: str) -> bool: ...
    def cancel(self) -> None: ...
    def confirm(self, text: str) -> None: ...
    def on_modified(self, text: str) -> None:
        """ Called after changes have been made to the input, with the text of the input field passed as argument. """
    def get_list_items(self) -> list[sublime.ListInputItem]:
        """ The list items which are initially shown. """
    def update(self, items: list[sublime.ListInputItem]) -> None:
        """ Call this method to update the list items. """

class InputListener(sublime_plugin.TextChangeListener):
    weakhandler: Incomplete
    def __init__(self, handler: DynamicListInputHandler) -> None: ...
    @classmethod
    def is_applicable(cls, buffer: sublime.Buffer) -> bool: ...
    @debounced
    def on_text_changed(self, changes: list[sublime.TextChange]) -> None: ...
