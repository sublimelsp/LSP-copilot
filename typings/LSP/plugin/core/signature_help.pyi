import sublime
from ...protocol import SignatureHelp as SignatureHelp, SignatureInformation as SignatureInformation
from .logging import debug as debug
from .registry import LspTextCommand as LspTextCommand
from .views import FORMAT_MARKUP_CONTENT as FORMAT_MARKUP_CONTENT, FORMAT_STRING as FORMAT_STRING, MarkdownLangMap as MarkdownLangMap, minihtml as minihtml
from _typeshed import Incomplete

class LspSignatureHelpNavigateCommand(LspTextCommand):
    def want_event(self) -> bool: ...
    def run(self, _: sublime.Edit, forward: bool) -> None: ...

class LspSignatureHelpShowCommand(LspTextCommand):
    def want_event(self) -> bool: ...
    def run(self, _: sublime.Edit) -> None: ...

class SigHelp:
    """
    A quasi state-machine object that maintains which signature (a.k.a. overload) is active. The active signature is
    determined by what the end-user is doing.
    """
    _state: Incomplete
    _language_map: Incomplete
    _signatures: Incomplete
    _active_signature_index: Incomplete
    _active_parameter_index: Incomplete
    _function_color: str
    _active_parameter_color: str
    _active_parameter_bold: bool
    _active_parameter_underline: bool
    _inactive_parameter_color: str
    def __init__(self, state: SignatureHelp, language_map: MarkdownLangMap | None) -> None: ...
    @classmethod
    def from_lsp(cls, sighelp: SignatureHelp | None, language_map: MarkdownLangMap | None) -> SigHelp | None:
        """Create a SigHelp state object from a server's response to textDocument/signatureHelp."""
    def render(self, view: sublime.View) -> str:
        """Render the signature help content as minihtml."""
    def active_signature_help(self) -> SignatureHelp:
        """
        Extract the state out of this state machine to send back to the language server.
        """
    def has_multiple_signatures(self) -> bool:
        """Does the current signature help state contain more than one overload?"""
    def select_signature(self, forward: bool) -> None:
        """Increment or decrement the active overload; purely chosen by the end-user."""
    def _render_intro(self) -> str: ...
    def _render_label(self, signature: SignatureInformation) -> list[str]: ...
    def _render_docs(self, view: sublime.View, signature: SignatureInformation) -> list[str]: ...
    def _parameter_documentation(self, view: sublime.View, signature: SignatureInformation) -> str | None: ...
    def _signature_documentation(self, view: sublime.View, signature: SignatureInformation) -> str | None: ...
    def _function(self, content: str) -> str: ...
    def _parameter(self, content: str, active: bool) -> str: ...

def _wrap_with_color(content: str, color: str, bold: bool = False, underline: bool = False) -> str: ...
