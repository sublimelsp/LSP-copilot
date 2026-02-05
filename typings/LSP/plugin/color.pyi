import sublime
from ..protocol import ColorInformation as ColorInformation, ColorPresentation as ColorPresentation, ColorPresentationParams as ColorPresentationParams
from .core.edit import apply_text_edits as apply_text_edits
from .core.protocol import Request as Request
from .core.registry import LspTextCommand as LspTextCommand
from .core.views import range_to_region as range_to_region, text_document_identifier as text_document_identifier
from _typeshed import Incomplete

class LspColorPresentationCommand(LspTextCommand):
    capability: str
    _version: Incomplete
    _range: Incomplete
    def run(self, edit: sublime.Edit, color_information: ColorInformation) -> None: ...
    def want_event(self) -> bool: ...
    _filtered_response: list[ColorPresentation]
    def _handle_response_async(self, response: list[ColorPresentation]) -> None: ...
    def _on_select(self, index: int) -> None: ...
