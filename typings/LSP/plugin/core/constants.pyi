from ...protocol import CodeActionKind, CompletionItemKind, DiagnosticSeverity, DocumentHighlightKind, MessageType, SymbolKind
from .typing import StrEnum as StrEnum
from _typeshed import Incomplete
from enum import IntFlag

SublimeKind = tuple[int, str, str]
ST_CACHE_PATH: Incomplete
ST_INSTALLED_PACKAGES_PATH: Incomplete
ST_PACKAGES_PATH: Incomplete
ST_PLATFORM: Incomplete
ST_VERSION: Incomplete
ST_STORAGE_PATH: Incomplete
MARKO_MD_PARSER_VERSION: str | None

class RequestFlags(IntFlag):
    """
    A bitflag that indicates how some of the requests are prioritized between the sessions.
    This is used for multi-session configurations, where the best session is selected for each of the relevant features
    below and the corresponding request is made only by that one session.
    """
    NONE = 0
    DOCUMENT_COLOR = 1
    INLAY_HINT = 2
    SEMANTIC_TOKENS = 4

class RegionKey(StrEnum):
    """ Key names for use with the `View.add_regions` method. """
    CODE_ACTION = 'lsp_code_action'
    DOCUMENT_LINK = 'lsp_document_link'
    HOVER_HIGHLIGHT = 'lsp_hover_highlight'
    REFERENCE_HIGHLIGHT = 'lsp_reference_highlight'

CODE_LENS_ENABLED_KEY: str
HOVER_ENABLED_KEY: str
SHOW_DEFINITIONS_KEY: str
DOCUMENT_LINK_FLAGS: Incomplete
REGIONS_INITIALIZE_FLAGS: Incomplete
SEMANTIC_TOKEN_FLAGS: Incomplete
KIND_ARRAY: Incomplete
KIND_BOOLEAN: Incomplete
KIND_CLASS: Incomplete
KIND_COLOR: Incomplete
KIND_CONSTANT: Incomplete
KIND_CONSTRUCTOR: Incomplete
KIND_ENUM: Incomplete
KIND_ENUMMEMBER: Incomplete
KIND_EVENT: Incomplete
KIND_FIELD: Incomplete
KIND_FILE: Incomplete
KIND_FOLDER: Incomplete
KIND_FUNCTION: Incomplete
KIND_INTERFACE: Incomplete
KIND_KEY: Incomplete
KIND_KEYWORD: Incomplete
KIND_METHOD: Incomplete
KIND_MODULE: Incomplete
KIND_NAMESPACE: Incomplete
KIND_NULL: Incomplete
KIND_NUMBER: Incomplete
KIND_OBJECT: Incomplete
KIND_OPERATOR: Incomplete
KIND_PACKAGE: Incomplete
KIND_PROPERTY: Incomplete
KIND_REFERENCE: Incomplete
KIND_SNIPPET: Incomplete
KIND_STRING: Incomplete
KIND_STRUCT: Incomplete
KIND_TEXT: Incomplete
KIND_TYPEPARAMETER: Incomplete
KIND_UNIT: Incomplete
KIND_VALUE: Incomplete
KIND_VARIABLE: Incomplete
KIND_ERROR: Incomplete
KIND_WARNING: Incomplete
KIND_INFORMATION: Incomplete
KIND_HINT: Incomplete
KIND_QUICKFIX: Incomplete
KIND_REFACTOR: Incomplete
KIND_SOURCE: Incomplete
COMPLETION_KINDS: dict[CompletionItemKind, SublimeKind]
SYMBOL_KINDS: dict[SymbolKind, SublimeKind]
DIAGNOSTIC_KINDS: dict[DiagnosticSeverity, SublimeKind]
CODE_ACTION_KINDS: dict[CodeActionKind, SublimeKind]
DOCUMENT_HIGHLIGHT_KIND_NAMES: dict[DocumentHighlightKind, str]
MESSAGE_TYPE_LEVELS: dict[MessageType, str]
SUBLIME_KIND_SCOPES: dict[SublimeKind, str]
DOCUMENT_HIGHLIGHT_KIND_SCOPES: dict[DocumentHighlightKind, str]
LANGUAGE_IDENTIFIERS: dict[str, str]
SEMANTIC_TOKENS_MAP: Incomplete
