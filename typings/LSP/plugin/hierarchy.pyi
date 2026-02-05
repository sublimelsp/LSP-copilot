import sublime
import weakref
from ..protocol import CallHierarchyIncomingCall as CallHierarchyIncomingCall, CallHierarchyItem, CallHierarchyOutgoingCall as CallHierarchyOutgoingCall, CallHierarchyPrepareParams as CallHierarchyPrepareParams, Range as Range, TextDocumentPositionParams as TextDocumentPositionParams, TypeHierarchyItem, TypeHierarchyPrepareParams as TypeHierarchyPrepareParams
from .core.constants import SYMBOL_KINDS as SYMBOL_KINDS
from .core.paths import simple_path as simple_path
from .core.promise import Promise as Promise
from .core.protocol import Error as Error, Request as Request
from .core.registry import LspTextCommand as LspTextCommand, LspWindowCommand as LspWindowCommand, get_position as get_position
from .core.sessions import Session as Session
from .core.tree_view import TreeDataProvider as TreeDataProvider, TreeItem as TreeItem, new_tree_view_sheet as new_tree_view_sheet
from .core.views import make_command_link as make_command_link, text_document_position_params as text_document_position_params
from _typeshed import Incomplete
from abc import ABCMeta, abstractmethod
from typing import Any, Callable, TypedDict

HierarchyItem = CallHierarchyItem | TypeHierarchyItem

class HierarchyItemWrapper(TypedDict):
    item: HierarchyItem
    selectionRange: Range

class HierarchyDataProvider(TreeDataProvider):
    weaksession: Incomplete
    request: Incomplete
    request_handler: Incomplete
    root_elements: Incomplete
    session_name: Incomplete
    def __init__(self, weaksession: weakref.ref[Session], request: Callable[[Any], Request[Any, Any]], request_handler: Callable[[Any], Any], root_elements: list[HierarchyItemWrapper]) -> None: ...
    def get_children(self, element: HierarchyItemWrapper | None) -> Promise[list[HierarchyItemWrapper]]: ...
    def get_tree_item(self, element: HierarchyItemWrapper) -> TreeItem: ...

def make_data_provider(weaksession: weakref.ref[Session], sheet_name: str, direction: int, response: list[HierarchyItemWrapper]) -> HierarchyDataProvider: ...
def incoming_calls_handler(response: list[CallHierarchyIncomingCall] | None | Error) -> list[HierarchyItemWrapper]: ...
def outgoing_calls_handler(response: list[CallHierarchyOutgoingCall] | None | Error) -> list[HierarchyItemWrapper]: ...
def type_hierarchy_handler(response: list[TypeHierarchyItem] | None | Error) -> list[HierarchyItemWrapper]: ...
def to_hierarchy_data(item: CallHierarchyItem | TypeHierarchyItem, selection_range: Range | None = None) -> HierarchyItemWrapper: ...
def make_header(session_name: str, sheet_name: str, direction: int, root_elements: list[HierarchyItem]) -> str: ...

class LspHierarchyCommand(LspTextCommand, metaclass=ABCMeta):
    @classmethod
    @abstractmethod
    def request(cls, params: TextDocumentPositionParams, view: sublime.View) -> Request[Any, list[HierarchyItem] | None]:
        """ A function that generates the initial request when this command is invoked. """
    def is_visible(self, event: dict | None = None, point: int | None = None) -> bool: ...
    _window: Incomplete
    def run(self, edit: sublime.Edit, event: dict | None = None, point: int | None = None) -> None: ...
    def _handle_response_async(self, weaksession: weakref.ref[Session], response: list[HierarchyItem] | None) -> None: ...

class LspHierarchyToggleCommand(LspWindowCommand):
    def run(self, session_name: str, sheet_name: str, direction: int, root_elements: list[HierarchyItemWrapper]) -> None: ...

def open_first(window: sublime.Window, session_name: str, items: list[HierarchyItemWrapper]) -> None: ...

class LspCallHierarchyCommand(LspHierarchyCommand):
    capability: str
    @classmethod
    def request(cls, params: CallHierarchyPrepareParams, view: sublime.View) -> Request[CallHierarchyPrepareParams, list[CallHierarchyItem] | None]: ...

class LspTypeHierarchyCommand(LspHierarchyCommand):
    capability: str
    @classmethod
    def request(cls, params: TypeHierarchyPrepareParams, view: sublime.View) -> Request[TypeHierarchyPrepareParams, list[TypeHierarchyItem] | None]: ...
