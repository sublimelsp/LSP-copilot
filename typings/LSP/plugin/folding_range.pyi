import sublime
from ..protocol import FoldingRange as FoldingRange, FoldingRangeParams as FoldingRangeParams, Range as Range
from .core.protocol import Request as Request, UINT_MAX as UINT_MAX
from .core.registry import LspTextCommand as LspTextCommand
from .core.views import range_to_region as range_to_region, text_document_identifier as text_document_identifier

def folding_range_to_range(folding_range: FoldingRange) -> Range: ...
def sorted_folding_ranges(folding_ranges: list[FoldingRange]) -> list[FoldingRange]: ...

class LspFoldCommand(LspTextCommand):
    '''A command to fold at the current caret position or at a given point.

    Optional command arguments:

    - `prefetch`:   Should usually be `false`, except for the built-in menu items under the "Edit" main menu, which
                    pre-run a request and cache the response to dynamically show or hide the item.
    - `hidden`:     Can be used for a hidden menu item with the purpose to run a request and store the response.
    - `strict`:     Allows to configure the folding behavior; `true` means to fold only when the caret is contained
                    within the folded region (like ST built-in `fold` command), and `false` will fold a region even if
                    the caret is anywhere else on the starting line.
    - `point`:      Can be used instead of the caret position, measured as character offset in the document.
    '''
    capability: str
    folding_ranges: list[FoldingRange]
    change_count: int
    folding_region: sublime.Region | None
    def is_visible(self, prefetch: bool = False, hidden: bool = False, strict: bool = True, event: dict | None = None, point: int | None = None) -> bool: ...
    def _handle_response_async(self, change_count: int, response: list[FoldingRange] | None) -> None: ...
    def description(self, prefetch: bool = False, hidden: bool = False, strict: bool = True, event: dict | None = None, point: int | None = None) -> str: ...
    def run(self, edit: sublime.Edit, prefetch: bool = False, hidden: bool = False, strict: bool = True, event: dict | None = None, point: int | None = None) -> None: ...
    def _handle_response_manual_async(self, point: int, strict: bool, response: list[FoldingRange] | None) -> None: ...

class LspFoldAllCommand(LspTextCommand):
    capability: str
    def run(self, edit: sublime.Edit, kind: str | None = None, event: dict | None = None) -> None: ...
    def _handle_response_async(self, kind: str | None, response: list[FoldingRange] | None) -> None: ...
