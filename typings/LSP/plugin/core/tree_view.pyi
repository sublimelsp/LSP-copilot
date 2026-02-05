import sublime
from .constants import SublimeKind as SublimeKind
from .css import css as css
from .promise import Promise as Promise
from .registry import LspWindowCommand as LspWindowCommand, windows as windows
from _typeshed import Incomplete
from abc import ABCMeta, abstractmethod
from enum import IntEnum
from typing import TypeVar

T = TypeVar('T')
KIND_CLASS_NAMES: dict[int, str]

class TreeItemCollapsibleState(IntEnum):
    NONE = 1
    COLLAPSED = 2
    EXPANDED = 3

class TreeItem:
    label: Incomplete
    kind: Incomplete
    description: Incomplete
    tooltip: Incomplete
    command_url: Incomplete
    collapsible_state: Incomplete
    id: Incomplete
    def __init__(self, label: str, kind: SublimeKind = ..., description: str = '', tooltip: str = '', command_url: str = '') -> None: ...
    def html(self, sheet_name: str, indent_level: int) -> str: ...

class Node:
    __slots__: Incomplete
    element: Incomplete
    tree_item: Incomplete
    indent_level: Incomplete
    child_ids: list[str]
    is_resolved: bool
    def __init__(self, element: T, tree_item: TreeItem, indent_level: int = 0) -> None: ...

class TreeDataProvider(metaclass=ABCMeta):
    @abstractmethod
    def get_children(self, element: T | None) -> Promise[list[T]]:
        """ Implement this to return the children for the given element or root (if no element is passed). """
    @abstractmethod
    def get_tree_item(self, element: T) -> TreeItem:
        """ Implement this to return the UI representation (TreeItem) of the element that gets displayed in the
        TreeViewSheet. """

class TreeViewSheet(sublime.HtmlSheet):
    """ A special HtmlSheet which can render interactive tree data structures. """
    nodes: dict[str, Node]
    root_nodes: list[str]
    name: Incomplete
    data_provider: Incomplete
    header: Incomplete
    def __init__(self, id: int, name: str, data_provider: TreeDataProvider, header: str = '') -> None: ...
    def __repr__(self) -> str: ...
    def set_provider(self, data_provider: TreeDataProvider, header: str = '') -> None:
        """ Use this method if you want to render an entire new tree. This allows to reuse a single HtmlSheet, e.g. when
        using a feature consecutively on different symbols. """
    def _set_root_nodes(self, elements: list[T]) -> None: ...
    def _add_children(self, id: str, elements: list[T]) -> None: ...
    def expand_item(self, id: str) -> None: ...
    def collapse_item(self, id: str) -> None: ...
    def _update_contents(self) -> None: ...
    def _subtree_html(self, id: str) -> str: ...

def new_tree_view_sheet(window: sublime.Window, name: str, data_provider: TreeDataProvider, header: str = '', flags: sublime.NewFileFlags = ..., group: int = -1) -> TreeViewSheet | None:
    """
    Use this function to create a new TreeView in form of a special HtmlSheet (TreeViewSheet). Only one TreeViewSheet
    with the given name is allowed per window. If there already exists a TreeViewSheet with the same name, its content
    will be replaced with the new data. The header argument is allowed to contain minihtml markup.
    """
def toggle_tree_item(window: sublime.Window, name: str, id: str, expand: bool) -> None: ...

class LspExpandTreeItemCommand(LspWindowCommand):
    def run(self, name: str, id: str) -> None: ...

class LspCollapseTreeItemCommand(LspWindowCommand):
    def run(self, name: str, id: str) -> None: ...
