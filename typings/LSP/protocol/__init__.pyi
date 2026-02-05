from ..plugin.core.typing import StrEnum
from _typeshed import Incomplete
from enum import IntEnum, IntFlag
from typing import Any, Literal, Mapping, TypedDict
from typing_extensions import NotRequired

URI = str
DocumentUri = str
Uint = int
RegExp = str

class SemanticTokenTypes(StrEnum):
    """
    A set of predefined token types. This set is not fixed
    an clients can specify additional token types via the
    corresponding client capabilities.

    @since 3.16.0
    """
    Namespace: str
    Type: str
    Class: str
    Enum: str
    Interface: str
    Struct: str
    TypeParameter: str
    Parameter: str
    Variable: str
    Property: str
    EnumMember: str
    Event: str
    Function: str
    Method: str
    Macro: str
    Keyword: str
    Modifier: str
    Comment: str
    String: str
    Number: str
    Regexp: str
    Operator: str
    Decorator: str
    Label: str

class SemanticTokenModifiers(StrEnum):
    """
    A set of predefined token modifiers. This set is not fixed
    an clients can specify additional token types via the
    corresponding client capabilities.

    @since 3.16.0
    """
    Declaration: str
    Definition: str
    Readonly: str
    Static: str
    Deprecated: str
    Abstract: str
    Async: str
    Modification: str
    Documentation: str
    DefaultLibrary: str

class DocumentDiagnosticReportKind(StrEnum):
    """
    The document diagnostic report kinds.

    @since 3.17.0
    """
    Full: str
    Unchanged: str

class ErrorCodes(IntEnum):
    """Predefined error codes."""
    ParseError = -32700
    InvalidRequest = -32600
    MethodNotFound = -32601
    InvalidParams = -32602
    InternalError = -32603
    ServerNotInitialized = -32002
    UnknownErrorCode = -32001

class LSPErrorCodes(IntEnum):
    RequestFailed = -32803
    ServerCancelled = -32802
    ContentModified = -32801
    RequestCancelled = -32800

class FoldingRangeKind(StrEnum):
    """A set of predefined range kinds."""
    Comment: str
    Imports: str
    Region: str

class SymbolKind(IntEnum):
    """A symbol kind."""
    File = 1
    Module = 2
    Namespace = 3
    Package = 4
    Class = 5
    Method = 6
    Property = 7
    Field = 8
    Constructor = 9
    Enum = 10
    Interface = 11
    Function = 12
    Variable = 13
    Constant = 14
    String = 15
    Number = 16
    Boolean = 17
    Array = 18
    Object = 19
    Key = 20
    Null = 21
    EnumMember = 22
    Struct = 23
    Event = 24
    Operator = 25
    TypeParameter = 26

class SymbolTag(IntEnum):
    """
    Symbol tags are extra annotations that tweak the rendering of a symbol.

    @since 3.16
    """
    Deprecated = 1

class UniquenessLevel(StrEnum):
    """
    Moniker uniqueness level to define scope of the moniker.

    @since 3.16.0
    """
    Document: str
    Project: str
    Group: str
    Scheme: str
    Global: str

class MonikerKind(StrEnum):
    """
    The moniker kind.

    @since 3.16.0
    """
    Import: str
    Export: str
    Local: str

class InlayHintKind(IntEnum):
    """
    Inlay hint kinds.

    @since 3.17.0
    """
    Type = 1
    Parameter = 2

class MessageType(IntEnum):
    """The message type"""
    Error = 1
    Warning = 2
    Info = 3
    Log = 4
    Debug = 5

class TextDocumentSyncKind(IntEnum):
    """
    Defines how the host (editor) should sync
    document changes to the language server.
    """
    None_ = 0
    Full = 1
    Incremental = 2

class TextDocumentSaveReason(IntEnum):
    """Represents reasons why a text document is saved."""
    Manual = 1
    AfterDelay = 2
    FocusOut = 3

class CompletionItemKind(IntEnum):
    """The kind of a completion entry."""
    Text = 1
    Method = 2
    Function = 3
    Constructor = 4
    Field = 5
    Variable = 6
    Class = 7
    Interface = 8
    Module = 9
    Property = 10
    Unit = 11
    Value = 12
    Enum = 13
    Keyword = 14
    Snippet = 15
    Color = 16
    File = 17
    Reference = 18
    Folder = 19
    EnumMember = 20
    Constant = 21
    Struct = 22
    Event = 23
    Operator = 24
    TypeParameter = 25

class CompletionItemTag(IntEnum):
    """
    Completion item tags are extra annotations that tweak the rendering of a completion
    item.

    @since 3.15.0
    """
    Deprecated = 1

class InsertTextFormat(IntEnum):
    """
    Defines whether the insert text in a completion item should be interpreted as
    plain text or a snippet.
    """
    PlainText = 1
    Snippet = 2

class InsertTextMode(IntEnum):
    """
    How whitespace and indentation is handled during completion
    item insertion.

    @since 3.16.0
    """
    AsIs = 1
    AdjustIndentation = 2

class DocumentHighlightKind(IntEnum):
    """A document highlight kind."""
    Text = 1
    Read = 2
    Write = 3

class CodeActionKind(StrEnum):
    """A set of predefined code action kinds"""
    Empty: str
    QuickFix: str
    Refactor: str
    RefactorExtract: str
    RefactorInline: str
    RefactorMove: str
    RefactorRewrite: str
    Source: str
    SourceOrganizeImports: str
    SourceFixAll: str
    Notebook: str

class CodeActionTag(IntEnum):
    """
    Code action tags are extra annotations that tweak the behavior of a code action.

    @since 3.18.0 - proposed
    """
    LLMGenerated = 1

class TraceValue(StrEnum):
    Off: str
    Messages: str
    Verbose: str

class MarkupKind(StrEnum):
    """
    Describes the content type that a client supports in various
    result literals like `Hover`, `ParameterInfo` or `CompletionItem`.

    Please note that `MarkupKinds` must not start with a `$`. This kinds
    are reserved for internal usage.
    """
    PlainText: str
    Markdown: str

class LanguageKind(StrEnum):
    """
    Predefined Language kinds
    @since 3.18.0
    """
    ABAP: str
    WindowsBat: str
    BibTeX: str
    Clojure: str
    Coffeescript: str
    C: str
    CPP: str
    CSharp: str
    CSS: str
    D: str
    Delphi: str
    Diff: str
    Dart: str
    Dockerfile: str
    Elixir: str
    Erlang: str
    FSharp: str
    GitCommit: str
    GitRebase: str
    Go: str
    Groovy: str
    Handlebars: str
    Haskell: str
    HTML: str
    Ini: str
    Java: str
    JavaScript: str
    JavaScriptReact: str
    JSON: str
    LaTeX: str
    Less: str
    Lua: str
    Makefile: str
    Markdown: str
    ObjectiveC: str
    ObjectiveCPP: str
    Pascal: str
    Perl: str
    Perl6: str
    PHP: str
    Powershell: str
    Pug: str
    Python: str
    R: str
    Razor: str
    Ruby: str
    Rust: str
    SCSS: str
    SASS: str
    Scala: str
    ShaderLab: str
    ShellScript: str
    SQL: str
    Swift: str
    TypeScript: str
    TypeScriptReact: str
    TeX: str
    VisualBasic: str
    XML: str
    XSL: str
    YAML: str

class InlineCompletionTriggerKind(IntEnum):
    """
    Describes how an {@link InlineCompletionItemProvider inline completion provider} was triggered.

    @since 3.18.0
    @proposed
    """
    Invoked = 1
    Automatic = 2

class PositionEncodingKind(StrEnum):
    """
    A set of predefined position encoding kinds.

    @since 3.17.0
    """
    UTF8: str
    UTF16: str
    UTF32: str

class FileChangeType(IntEnum):
    """The file event type"""
    Created = 1
    Changed = 2
    Deleted = 3

class WatchKind(IntFlag):
    Create = 1
    Change = 2
    Delete = 4

class DiagnosticSeverity(IntEnum):
    """The diagnostic's severity."""
    Error = 1
    Warning = 2
    Information = 3
    Hint = 4

class DiagnosticTag(IntEnum):
    """
    The diagnostic tags.

    @since 3.15.0
    """
    Unnecessary = 1
    Deprecated = 2

class CompletionTriggerKind(IntEnum):
    """How a completion was triggered"""
    Invoked = 1
    TriggerCharacter = 2
    TriggerForIncompleteCompletions = 3

class ApplyKind(IntFlag):
    """
    Defines how values from a set of defaults and an individual item will be
    merged.

    @since 3.18.0
    """
    Replace = 1
    Merge = 2

class SignatureHelpTriggerKind(IntEnum):
    """
    How a signature help was triggered.

    @since 3.15.0
    """
    Invoked = 1
    TriggerCharacter = 2
    ContentChange = 3

class CodeActionTriggerKind(IntEnum):
    """
    The reason why code actions were requested.

    @since 3.17.0
    """
    Invoked = 1
    Automatic = 2

class FileOperationPatternKind(StrEnum):
    """
    A pattern kind describing if a glob pattern matches a file a folder or
    both.

    @since 3.16.0
    """
    File: str
    Folder: str

class NotebookCellKind(IntEnum):
    """
    A notebook cell kind.

    @since 3.17.0
    """
    Markup = 1
    Code = 2

class ResourceOperationKind(StrEnum):
    Create: str
    Rename: str
    Delete: str

class FailureHandlingKind(StrEnum):
    Abort: str
    Transactional: str
    TextOnlyTransactional: str
    Undo: str

class PrepareSupportDefaultBehavior(IntEnum):
    Identifier = 1

class TokenFormat(StrEnum):
    Relative: str

Definition: Incomplete
DefinitionLink: str
LSPArray: Incomplete
LSPAny: Incomplete
Declaration: Incomplete
DeclarationLink: str
InlineValue: Incomplete
DocumentDiagnosticReport: Incomplete
PrepareRenameResult: Incomplete
DocumentSelector: Incomplete
ProgressToken = int | str
ChangeAnnotationIdentifier = str
WorkspaceDocumentDiagnosticReport: Incomplete
TextDocumentContentChangeEvent: Incomplete
MarkedString: Incomplete
DocumentFilter: Incomplete
LSPObject = Mapping[str, Any]
GlobPattern: Incomplete
TextDocumentFilter: Incomplete
NotebookDocumentFilter: Incomplete
Pattern = str
RegularExpressionEngineKind = str

class ImplementationParams(TypedDict):
    textDocument: TextDocumentIdentifier
    position: Position
    workDoneToken: NotRequired['ProgressToken']
    partialResultToken: NotRequired['ProgressToken']

class Location(TypedDict):
    """
    Represents a location inside a resource, such as a line
    inside a text file.
    """
    uri: DocumentUri
    range: Range

class ImplementationRegistrationOptions(TypedDict):
    documentSelector: DocumentSelector | None
    id: NotRequired[str]

class TypeDefinitionParams(TypedDict):
    textDocument: TextDocumentIdentifier
    position: Position
    workDoneToken: NotRequired['ProgressToken']
    partialResultToken: NotRequired['ProgressToken']

class TypeDefinitionRegistrationOptions(TypedDict):
    documentSelector: DocumentSelector | None
    id: NotRequired[str]

class WorkspaceFolder(TypedDict):
    """A workspace folder inside a client."""
    uri: URI
    name: str

class DidChangeWorkspaceFoldersParams(TypedDict):
    """The parameters of a `workspace/didChangeWorkspaceFolders` notification."""
    event: WorkspaceFoldersChangeEvent

class ConfigurationParams(TypedDict):
    """The parameters of a configuration request."""
    items: list['ConfigurationItem']

class DocumentColorParams(TypedDict):
    """Parameters for a {@link DocumentColorRequest}."""
    textDocument: TextDocumentIdentifier
    workDoneToken: NotRequired['ProgressToken']
    partialResultToken: NotRequired['ProgressToken']

class ColorInformation(TypedDict):
    """Represents a color range from a document."""
    range: Range
    color: Color

class DocumentColorRegistrationOptions(TypedDict):
    documentSelector: DocumentSelector | None
    id: NotRequired[str]

class ColorPresentationParams(TypedDict):
    """Parameters for a {@link ColorPresentationRequest}."""
    textDocument: TextDocumentIdentifier
    color: Color
    range: Range
    workDoneToken: NotRequired['ProgressToken']
    partialResultToken: NotRequired['ProgressToken']

class ColorPresentation(TypedDict):
    label: str
    textEdit: NotRequired['TextEdit']
    additionalTextEdits: NotRequired[list['TextEdit']]

class WorkDoneProgressOptions(TypedDict):
    workDoneProgress: NotRequired[bool]

class TextDocumentRegistrationOptions(TypedDict):
    """General text document registration options."""
    documentSelector: DocumentSelector | None

class FoldingRangeParams(TypedDict):
    """Parameters for a {@link FoldingRangeRequest}."""
    textDocument: TextDocumentIdentifier
    workDoneToken: NotRequired['ProgressToken']
    partialResultToken: NotRequired['ProgressToken']

class FoldingRange(TypedDict):
    """
    Represents a folding range. To be valid, start and end line must be bigger than zero and smaller
    than the number of lines in the document. Clients are free to ignore invalid ranges.
    """
    startLine: Uint
    startCharacter: NotRequired[Uint]
    endLine: Uint
    endCharacter: NotRequired[Uint]
    kind: NotRequired['FoldingRangeKind']
    collapsedText: NotRequired[str]

class FoldingRangeRegistrationOptions(TypedDict):
    documentSelector: DocumentSelector | None
    id: NotRequired[str]

class DeclarationParams(TypedDict):
    textDocument: TextDocumentIdentifier
    position: Position
    workDoneToken: NotRequired['ProgressToken']
    partialResultToken: NotRequired['ProgressToken']

class DeclarationRegistrationOptions(TypedDict):
    documentSelector: DocumentSelector | None
    id: NotRequired[str]

class SelectionRangeParams(TypedDict):
    """A parameter literal used in selection range requests."""
    textDocument: TextDocumentIdentifier
    positions: list['Position']
    workDoneToken: NotRequired['ProgressToken']
    partialResultToken: NotRequired['ProgressToken']

class SelectionRange(TypedDict):
    """
    A selection range represents a part of a selection hierarchy. A selection range
    may have a parent selection range that contains it.
    """
    range: Range
    parent: NotRequired['SelectionRange']

class SelectionRangeRegistrationOptions(TypedDict):
    documentSelector: DocumentSelector | None
    id: NotRequired[str]

class WorkDoneProgressCreateParams(TypedDict):
    token: ProgressToken

class WorkDoneProgressCancelParams(TypedDict):
    token: ProgressToken

class CallHierarchyPrepareParams(TypedDict):
    """
    The parameter of a `textDocument/prepareCallHierarchy` request.

    @since 3.16.0
    """
    textDocument: TextDocumentIdentifier
    position: Position
    workDoneToken: NotRequired['ProgressToken']

class CallHierarchyItem(TypedDict):
    """
    Represents programming constructs like functions or constructors in the context
    of call hierarchy.

    @since 3.16.0
    """
    name: str
    kind: SymbolKind
    tags: NotRequired[list['SymbolTag']]
    detail: NotRequired[str]
    uri: DocumentUri
    range: Range
    selectionRange: Range
    data: NotRequired['LSPAny']

class CallHierarchyRegistrationOptions(TypedDict):
    """
    Call hierarchy options used during static or dynamic registration.

    @since 3.16.0
    """
    documentSelector: DocumentSelector | None
    id: NotRequired[str]

class CallHierarchyIncomingCallsParams(TypedDict):
    """
    The parameter of a `callHierarchy/incomingCalls` request.

    @since 3.16.0
    """
    item: CallHierarchyItem
    workDoneToken: NotRequired['ProgressToken']
    partialResultToken: NotRequired['ProgressToken']

CallHierarchyIncomingCall = TypedDict('CallHierarchyIncomingCall', {'from': 'CallHierarchyItem', 'fromRanges': list['Range']})

class CallHierarchyOutgoingCallsParams(TypedDict):
    """
    The parameter of a `callHierarchy/outgoingCalls` request.

    @since 3.16.0
    """
    item: CallHierarchyItem
    workDoneToken: NotRequired['ProgressToken']
    partialResultToken: NotRequired['ProgressToken']

class CallHierarchyOutgoingCall(TypedDict):
    """
    Represents an outgoing call, e.g. calling a getter from a method or a method from a constructor etc.

    @since 3.16.0
    """
    to: CallHierarchyItem
    fromRanges: list['Range']

class SemanticTokensParams(TypedDict):
    """@since 3.16.0"""
    textDocument: TextDocumentIdentifier
    workDoneToken: NotRequired['ProgressToken']
    partialResultToken: NotRequired['ProgressToken']

class SemanticTokens(TypedDict):
    """@since 3.16.0"""
    resultId: NotRequired[str]
    data: list[Uint]

class SemanticTokensPartialResult(TypedDict):
    """@since 3.16.0"""
    data: list[Uint]

class SemanticTokensRegistrationOptions(TypedDict):
    """@since 3.16.0"""
    documentSelector: DocumentSelector | None
    legend: SemanticTokensLegend
    range: NotRequired[bool | dict[str, LSPAny]]
    full: NotRequired[bool | SemanticTokensFullDelta]
    id: NotRequired[str]

class SemanticTokensDeltaParams(TypedDict):
    """@since 3.16.0"""
    textDocument: TextDocumentIdentifier
    previousResultId: str
    workDoneToken: NotRequired['ProgressToken']
    partialResultToken: NotRequired['ProgressToken']

class SemanticTokensDelta(TypedDict):
    """@since 3.16.0"""
    resultId: NotRequired[str]
    edits: list['SemanticTokensEdit']

class SemanticTokensDeltaPartialResult(TypedDict):
    """@since 3.16.0"""
    edits: list['SemanticTokensEdit']

class SemanticTokensRangeParams(TypedDict):
    """@since 3.16.0"""
    textDocument: TextDocumentIdentifier
    range: Range
    workDoneToken: NotRequired['ProgressToken']
    partialResultToken: NotRequired['ProgressToken']

class ShowDocumentParams(TypedDict):
    """
    Params to show a resource in the UI.

    @since 3.16.0
    """
    uri: URI
    external: NotRequired[bool]
    takeFocus: NotRequired[bool]
    selection: NotRequired['Range']

class ShowDocumentResult(TypedDict):
    """
    The result of a showDocument request.

    @since 3.16.0
    """
    success: bool

class LinkedEditingRangeParams(TypedDict):
    textDocument: TextDocumentIdentifier
    position: Position
    workDoneToken: NotRequired['ProgressToken']

class LinkedEditingRanges(TypedDict):
    """
    The result of a linked editing range request.

    @since 3.16.0
    """
    ranges: list['Range']
    wordPattern: NotRequired[str]

class LinkedEditingRangeRegistrationOptions(TypedDict):
    documentSelector: DocumentSelector | None
    id: NotRequired[str]

class CreateFilesParams(TypedDict):
    """
    The parameters sent in notifications/requests for user-initiated creation of
    files.

    @since 3.16.0
    """
    files: list['FileCreate']

class WorkspaceEdit(TypedDict):
    """
    A workspace edit represents changes to many resources managed in the workspace. The edit
    should either provide `changes` or `documentChanges`. If documentChanges are present
    they are preferred over `changes` if the client can handle versioned document edits.

    Since version 3.13.0 a workspace edit can contain resource operations as well. If resource
    operations are present clients need to execute the operations in the order in which they
    are provided. So a workspace edit for example can consist of the following two changes:
    (1) a create file a.txt and (2) a text document edit which insert text into file a.txt.

    An invalid sequence (e.g. (1) delete file a.txt and (2) insert text into file a.txt) will
    cause failure of the operation. How the client recovers from the failure is described by
    the client capability: `workspace.workspaceEdit.failureHandling`
    """
    changes: NotRequired[dict[DocumentUri, list['TextEdit']]]
    documentChanges: NotRequired[list[TextDocumentEdit | CreateFile | RenameFile | DeleteFile]]
    changeAnnotations: NotRequired[dict[ChangeAnnotationIdentifier, 'ChangeAnnotation']]

class FileOperationRegistrationOptions(TypedDict):
    """
    The options to register for file operations.

    @since 3.16.0
    """
    filters: list['FileOperationFilter']

class RenameFilesParams(TypedDict):
    """
    The parameters sent in notifications/requests for user-initiated renames of
    files.

    @since 3.16.0
    """
    files: list['FileRename']

class DeleteFilesParams(TypedDict):
    """
    The parameters sent in notifications/requests for user-initiated deletes of
    files.

    @since 3.16.0
    """
    files: list['FileDelete']

class MonikerParams(TypedDict):
    textDocument: TextDocumentIdentifier
    position: Position
    workDoneToken: NotRequired['ProgressToken']
    partialResultToken: NotRequired['ProgressToken']

class Moniker(TypedDict):
    """
    Moniker definition to match LSIF 0.5 moniker definition.

    @since 3.16.0
    """
    scheme: str
    identifier: str
    unique: UniquenessLevel
    kind: NotRequired['MonikerKind']

class MonikerRegistrationOptions(TypedDict):
    documentSelector: DocumentSelector | None

class TypeHierarchyPrepareParams(TypedDict):
    """
    The parameter of a `textDocument/prepareTypeHierarchy` request.

    @since 3.17.0
    """
    textDocument: TextDocumentIdentifier
    position: Position
    workDoneToken: NotRequired['ProgressToken']

class TypeHierarchyItem(TypedDict):
    """@since 3.17.0"""
    name: str
    kind: SymbolKind
    tags: NotRequired[list['SymbolTag']]
    detail: NotRequired[str]
    uri: DocumentUri
    range: Range
    selectionRange: Range
    data: NotRequired['LSPAny']

class TypeHierarchyRegistrationOptions(TypedDict):
    """
    Type hierarchy options used during static or dynamic registration.

    @since 3.17.0
    """
    documentSelector: DocumentSelector | None
    id: NotRequired[str]

class TypeHierarchySupertypesParams(TypedDict):
    """
    The parameter of a `typeHierarchy/supertypes` request.

    @since 3.17.0
    """
    item: TypeHierarchyItem
    workDoneToken: NotRequired['ProgressToken']
    partialResultToken: NotRequired['ProgressToken']

class TypeHierarchySubtypesParams(TypedDict):
    """
    The parameter of a `typeHierarchy/subtypes` request.

    @since 3.17.0
    """
    item: TypeHierarchyItem
    workDoneToken: NotRequired['ProgressToken']
    partialResultToken: NotRequired['ProgressToken']

class InlineValueParams(TypedDict):
    """
    A parameter literal used in inline value requests.

    @since 3.17.0
    """
    textDocument: TextDocumentIdentifier
    range: Range
    context: InlineValueContext
    workDoneToken: NotRequired['ProgressToken']

class InlineValueRegistrationOptions(TypedDict):
    """
    Inline value options used during static or dynamic registration.

    @since 3.17.0
    """
    documentSelector: DocumentSelector | None
    id: NotRequired[str]

class InlayHintParams(TypedDict):
    """
    A parameter literal used in inlay hint requests.

    @since 3.17.0
    """
    textDocument: TextDocumentIdentifier
    range: Range
    workDoneToken: NotRequired['ProgressToken']

class InlayHint(TypedDict):
    """
    Inlay hint information.

    @since 3.17.0
    """
    position: Position
    label: str | list['InlayHintLabelPart']
    kind: NotRequired['InlayHintKind']
    textEdits: NotRequired[list['TextEdit']]
    tooltip: NotRequired[str | MarkupContent]
    paddingLeft: NotRequired[bool]
    paddingRight: NotRequired[bool]
    data: NotRequired['LSPAny']

class InlayHintRegistrationOptions(TypedDict):
    """
    Inlay hint options used during static or dynamic registration.

    @since 3.17.0
    """
    resolveProvider: NotRequired[bool]
    documentSelector: DocumentSelector | None
    id: NotRequired[str]

class DocumentDiagnosticParams(TypedDict):
    """
    Parameters of the document diagnostic request.

    @since 3.17.0
    """
    textDocument: TextDocumentIdentifier
    identifier: NotRequired[str]
    previousResultId: NotRequired[str]
    workDoneToken: NotRequired['ProgressToken']
    partialResultToken: NotRequired['ProgressToken']

class DocumentDiagnosticReportPartialResult(TypedDict):
    """
    A partial result for a document diagnostic report.

    @since 3.17.0
    """
    relatedDocuments: dict[DocumentUri, FullDocumentDiagnosticReport | UnchangedDocumentDiagnosticReport]

class DiagnosticServerCancellationData(TypedDict):
    """
    Cancellation data returned from a diagnostic request.

    @since 3.17.0
    """
    retriggerRequest: bool

class DiagnosticRegistrationOptions(TypedDict):
    """
    Diagnostic registration options.

    @since 3.17.0
    """
    documentSelector: DocumentSelector | None
    identifier: NotRequired[str]
    interFileDependencies: bool
    workspaceDiagnostics: bool
    id: NotRequired[str]

class WorkspaceDiagnosticParams(TypedDict):
    """
    Parameters of the workspace diagnostic request.

    @since 3.17.0
    """
    identifier: NotRequired[str]
    previousResultIds: list['PreviousResultId']
    workDoneToken: NotRequired['ProgressToken']
    partialResultToken: NotRequired['ProgressToken']

class WorkspaceDiagnosticReport(TypedDict):
    """
    A workspace diagnostic report.

    @since 3.17.0
    """
    items: list['WorkspaceDocumentDiagnosticReport']

class WorkspaceDiagnosticReportPartialResult(TypedDict):
    """
    A partial result for a workspace diagnostic report.

    @since 3.17.0
    """
    items: list['WorkspaceDocumentDiagnosticReport']

class DidOpenNotebookDocumentParams(TypedDict):
    """
    The params sent in an open notebook document notification.

    @since 3.17.0
    """
    notebookDocument: NotebookDocument
    cellTextDocuments: list['TextDocumentItem']

class NotebookDocumentSyncRegistrationOptions(TypedDict):
    """
    Registration options specific to a notebook.

    @since 3.17.0
    """
    notebookSelector: list[NotebookDocumentFilterWithNotebook | NotebookDocumentFilterWithCells]
    save: NotRequired[bool]
    id: NotRequired[str]

class DidChangeNotebookDocumentParams(TypedDict):
    """
    The params sent in a change notebook document notification.

    @since 3.17.0
    """
    notebookDocument: VersionedNotebookDocumentIdentifier
    change: NotebookDocumentChangeEvent

class DidSaveNotebookDocumentParams(TypedDict):
    """
    The params sent in a save notebook document notification.

    @since 3.17.0
    """
    notebookDocument: NotebookDocumentIdentifier

class DidCloseNotebookDocumentParams(TypedDict):
    """
    The params sent in a close notebook document notification.

    @since 3.17.0
    """
    notebookDocument: NotebookDocumentIdentifier
    cellTextDocuments: list['TextDocumentIdentifier']

class InlineCompletionParams(TypedDict):
    """
    A parameter literal used in inline completion requests.

    @since 3.18.0
    @proposed
    """
    context: InlineCompletionContext
    textDocument: TextDocumentIdentifier
    position: Position
    workDoneToken: NotRequired['ProgressToken']

class InlineCompletionList(TypedDict):
    """
    Represents a collection of {@link InlineCompletionItem inline completion items} to be presented in the editor.

    @since 3.18.0
    @proposed
    """
    items: list['InlineCompletionItem']

class InlineCompletionItem(TypedDict):
    """
    An inline completion item represents a text snippet that is proposed inline to complete text that is being typed.

    @since 3.18.0
    @proposed
    """
    insertText: str | StringValue
    filterText: NotRequired[str]
    range: NotRequired['Range']
    command: NotRequired['Command']

class InlineCompletionRegistrationOptions(TypedDict):
    """
    Inline completion options used during static or dynamic registration.

    @since 3.18.0
    @proposed
    """
    documentSelector: DocumentSelector | None
    id: NotRequired[str]

class TextDocumentContentParams(TypedDict):
    """
    Parameters for the `workspace/textDocumentContent` request.

    @since 3.18.0
    @proposed
    """
    uri: DocumentUri

class TextDocumentContentResult(TypedDict):
    """
    Result of the `workspace/textDocumentContent` request.

    @since 3.18.0
    @proposed
    """
    text: str

class TextDocumentContentRegistrationOptions(TypedDict):
    """
    Text document content provider registration options.

    @since 3.18.0
    @proposed
    """
    schemes: list[str]
    id: NotRequired[str]

class TextDocumentContentRefreshParams(TypedDict):
    """
    Parameters for the `workspace/textDocumentContent/refresh` request.

    @since 3.18.0
    @proposed
    """
    uri: DocumentUri

class RegistrationParams(TypedDict):
    registrations: list['Registration']

class UnregistrationParams(TypedDict):
    unregisterations: list['Unregistration']

class InitializeParams(TypedDict):
    processId: int | None
    clientInfo: NotRequired['ClientInfo']
    locale: NotRequired[str]
    rootPath: NotRequired[str | None]
    rootUri: DocumentUri | None
    capabilities: ClientCapabilities
    initializationOptions: NotRequired['LSPAny']
    trace: NotRequired['TraceValue']
    workspaceFolders: NotRequired[list['WorkspaceFolder'] | None]

class InitializeResult(TypedDict):
    """The result returned from an initialize request."""
    capabilities: ServerCapabilities
    serverInfo: NotRequired['ServerInfo']

class InitializeError(TypedDict):
    """
    The data type of the ResponseError if the
    initialize request fails.
    """
    retry: bool

class InitializedParams(TypedDict): ...

class DidChangeConfigurationParams(TypedDict):
    """The parameters of a change configuration notification."""
    settings: LSPAny

class DidChangeConfigurationRegistrationOptions(TypedDict):
    section: NotRequired[str | list[str]]

class ShowMessageParams(TypedDict):
    """The parameters of a notification message."""
    type: MessageType
    message: str

class ShowMessageRequestParams(TypedDict):
    type: MessageType
    message: str
    actions: NotRequired[list['MessageActionItem']]

class MessageActionItem(TypedDict):
    title: str

class LogMessageParams(TypedDict):
    """The log message parameters."""
    type: MessageType
    message: str

class DidOpenTextDocumentParams(TypedDict):
    """The parameters sent in an open text document notification"""
    textDocument: TextDocumentItem

class DidChangeTextDocumentParams(TypedDict):
    """The change text document notification's parameters."""
    textDocument: VersionedTextDocumentIdentifier
    contentChanges: list['TextDocumentContentChangeEvent']

class TextDocumentChangeRegistrationOptions(TypedDict):
    """Describe options to be used when registered for text document change events."""
    syncKind: TextDocumentSyncKind
    documentSelector: DocumentSelector | None

class DidCloseTextDocumentParams(TypedDict):
    """The parameters sent in a close text document notification"""
    textDocument: TextDocumentIdentifier

class DidSaveTextDocumentParams(TypedDict):
    """The parameters sent in a save text document notification"""
    textDocument: TextDocumentIdentifier
    text: NotRequired[str]

class TextDocumentSaveRegistrationOptions(TypedDict):
    """Save registration options."""
    documentSelector: DocumentSelector | None
    includeText: NotRequired[bool]

class WillSaveTextDocumentParams(TypedDict):
    """The parameters sent in a will save text document notification."""
    textDocument: TextDocumentIdentifier
    reason: TextDocumentSaveReason

class TextEdit(TypedDict):
    """A text edit applicable to a text document."""
    range: Range
    newText: str

class DidChangeWatchedFilesParams(TypedDict):
    """The watched files change notification's parameters."""
    changes: list['FileEvent']

class DidChangeWatchedFilesRegistrationOptions(TypedDict):
    """Describe options to be used when registered for text document change events."""
    watchers: list['FileSystemWatcher']

class PublishDiagnosticsParams(TypedDict):
    """The publish diagnostic notification's parameters."""
    uri: DocumentUri
    version: NotRequired[int]
    diagnostics: list['Diagnostic']

class CompletionParams(TypedDict):
    """Completion parameters"""
    context: NotRequired['CompletionContext']
    textDocument: TextDocumentIdentifier
    position: Position
    workDoneToken: NotRequired['ProgressToken']
    partialResultToken: NotRequired['ProgressToken']

class CompletionItem(TypedDict):
    """
    A completion item represents a text snippet that is
    proposed to complete text that is being typed.
    """
    label: str
    labelDetails: NotRequired['CompletionItemLabelDetails']
    kind: NotRequired['CompletionItemKind']
    tags: NotRequired[list['CompletionItemTag']]
    detail: NotRequired[str]
    documentation: NotRequired[str | MarkupContent]
    deprecated: NotRequired[bool]
    preselect: NotRequired[bool]
    sortText: NotRequired[str]
    filterText: NotRequired[str]
    insertText: NotRequired[str]
    insertTextFormat: NotRequired['InsertTextFormat']
    insertTextMode: NotRequired['InsertTextMode']
    textEdit: NotRequired[TextEdit | InsertReplaceEdit]
    textEditText: NotRequired[str]
    additionalTextEdits: NotRequired[list['TextEdit']]
    commitCharacters: NotRequired[list[str]]
    command: NotRequired['Command']
    data: NotRequired['LSPAny']

class CompletionList(TypedDict):
    """
    Represents a collection of {@link CompletionItem completion items} to be presented
    in the editor.
    """
    isIncomplete: bool
    itemDefaults: NotRequired['CompletionItemDefaults']
    applyKind: NotRequired['CompletionItemApplyKinds']
    items: list['CompletionItem']

class CompletionRegistrationOptions(TypedDict):
    """Registration options for a {@link CompletionRequest}."""
    documentSelector: DocumentSelector | None
    triggerCharacters: NotRequired[list[str]]
    allCommitCharacters: NotRequired[list[str]]
    resolveProvider: NotRequired[bool]
    completionItem: NotRequired['ServerCompletionItemOptions']

class HoverParams(TypedDict):
    """Parameters for a {@link HoverRequest}."""
    textDocument: TextDocumentIdentifier
    position: Position
    workDoneToken: NotRequired['ProgressToken']

class Hover(TypedDict):
    """The result of a hover request."""
    contents: MarkupContent | MarkedString | list['MarkedString']
    range: NotRequired['Range']

class HoverRegistrationOptions(TypedDict):
    """Registration options for a {@link HoverRequest}."""
    documentSelector: DocumentSelector | None

class SignatureHelpParams(TypedDict):
    """Parameters for a {@link SignatureHelpRequest}."""
    context: NotRequired['SignatureHelpContext']
    textDocument: TextDocumentIdentifier
    position: Position
    workDoneToken: NotRequired['ProgressToken']

class SignatureHelp(TypedDict):
    """
    Signature help represents the signature of something
    callable. There can be multiple signature but only one
    active and only one active parameter.
    """
    signatures: list['SignatureInformation']
    activeSignature: NotRequired[Uint]
    activeParameter: NotRequired[Uint | None]

class SignatureHelpRegistrationOptions(TypedDict):
    """Registration options for a {@link SignatureHelpRequest}."""
    documentSelector: DocumentSelector | None
    triggerCharacters: NotRequired[list[str]]
    retriggerCharacters: NotRequired[list[str]]

class DefinitionParams(TypedDict):
    """Parameters for a {@link DefinitionRequest}."""
    textDocument: TextDocumentIdentifier
    position: Position
    workDoneToken: NotRequired['ProgressToken']
    partialResultToken: NotRequired['ProgressToken']

class DefinitionRegistrationOptions(TypedDict):
    """Registration options for a {@link DefinitionRequest}."""
    documentSelector: DocumentSelector | None

class ReferenceParams(TypedDict):
    """Parameters for a {@link ReferencesRequest}."""
    context: ReferenceContext
    textDocument: TextDocumentIdentifier
    position: Position
    workDoneToken: NotRequired['ProgressToken']
    partialResultToken: NotRequired['ProgressToken']

class ReferenceRegistrationOptions(TypedDict):
    """Registration options for a {@link ReferencesRequest}."""
    documentSelector: DocumentSelector | None

class DocumentHighlightParams(TypedDict):
    """Parameters for a {@link DocumentHighlightRequest}."""
    textDocument: TextDocumentIdentifier
    position: Position
    workDoneToken: NotRequired['ProgressToken']
    partialResultToken: NotRequired['ProgressToken']

class DocumentHighlight(TypedDict):
    """
    A document highlight is a range inside a text document which deserves
    special attention. Usually a document highlight is visualized by changing
    the background color of its range.
    """
    range: Range
    kind: NotRequired['DocumentHighlightKind']

class DocumentHighlightRegistrationOptions(TypedDict):
    """Registration options for a {@link DocumentHighlightRequest}."""
    documentSelector: DocumentSelector | None

class DocumentSymbolParams(TypedDict):
    """Parameters for a {@link DocumentSymbolRequest}."""
    textDocument: TextDocumentIdentifier
    workDoneToken: NotRequired['ProgressToken']
    partialResultToken: NotRequired['ProgressToken']

class SymbolInformation(TypedDict):
    """
    Represents information about programming constructs like variables, classes,
    interfaces etc.
    """
    deprecated: NotRequired[bool]
    location: Location
    name: str
    kind: SymbolKind
    tags: NotRequired[list['SymbolTag']]
    containerName: NotRequired[str]

class DocumentSymbol(TypedDict):
    """
    Represents programming constructs like variables, classes, interfaces etc.
    that appear in a document. Document symbols can be hierarchical and they
    have two ranges: one that encloses its definition and one that points to
    its most interesting range, e.g. the range of an identifier.
    """
    name: str
    detail: NotRequired[str]
    kind: SymbolKind
    tags: NotRequired[list['SymbolTag']]
    deprecated: NotRequired[bool]
    range: Range
    selectionRange: Range
    children: NotRequired[list['DocumentSymbol']]

class DocumentSymbolRegistrationOptions(TypedDict):
    """Registration options for a {@link DocumentSymbolRequest}."""
    documentSelector: DocumentSelector | None
    label: NotRequired[str]

class CodeActionParams(TypedDict):
    """The parameters of a {@link CodeActionRequest}."""
    textDocument: TextDocumentIdentifier
    range: Range
    context: CodeActionContext
    workDoneToken: NotRequired['ProgressToken']
    partialResultToken: NotRequired['ProgressToken']

class Command(TypedDict):
    """
    Represents a reference to a command. Provides a title which
    will be used to represent a command in the UI and, optionally,
    an array of arguments which will be passed to the command handler
    function when invoked.
    """
    title: str
    tooltip: NotRequired[str]
    command: str
    arguments: NotRequired[list['LSPAny']]

class CodeAction(TypedDict):
    """
    A code action represents a change that can be performed in code, e.g. to fix a problem or
    to refactor code.

    A CodeAction must set either `edit` and/or a `command`. If both are supplied, the `edit` is applied first, then the `command` is executed.
    """
    title: str
    kind: NotRequired['CodeActionKind']
    diagnostics: NotRequired[list['Diagnostic']]
    isPreferred: NotRequired[bool]
    disabled: NotRequired['CodeActionDisabled']
    edit: NotRequired['WorkspaceEdit']
    command: NotRequired['Command']
    data: NotRequired['LSPAny']
    tags: NotRequired[list['CodeActionTag']]

class CodeActionRegistrationOptions(TypedDict):
    """Registration options for a {@link CodeActionRequest}."""
    documentSelector: DocumentSelector | None
    codeActionKinds: NotRequired[list['CodeActionKind']]
    documentation: NotRequired[list['CodeActionKindDocumentation']]
    resolveProvider: NotRequired[bool]

class WorkspaceSymbolParams(TypedDict):
    """The parameters of a {@link WorkspaceSymbolRequest}."""
    query: str
    workDoneToken: NotRequired['ProgressToken']
    partialResultToken: NotRequired['ProgressToken']

class WorkspaceSymbol(TypedDict):
    """
    A special workspace symbol that supports locations without a range.

    See also SymbolInformation.

    @since 3.17.0
    """
    location: Location | LocationUriOnly
    data: NotRequired['LSPAny']
    name: str
    kind: SymbolKind
    tags: NotRequired[list['SymbolTag']]
    containerName: NotRequired[str]

class WorkspaceSymbolRegistrationOptions(TypedDict):
    """Registration options for a {@link WorkspaceSymbolRequest}."""
    resolveProvider: NotRequired[bool]

class CodeLensParams(TypedDict):
    """The parameters of a {@link CodeLensRequest}."""
    textDocument: TextDocumentIdentifier
    workDoneToken: NotRequired['ProgressToken']
    partialResultToken: NotRequired['ProgressToken']

class CodeLens(TypedDict):
    """
    A code lens represents a {@link Command command} that should be shown along with
    source text, like the number of references, a way to run tests, etc.

    A code lens is _unresolved_ when no command is associated to it. For performance
    reasons the creation of a code lens and resolving should be done in two stages.
    """
    range: Range
    command: NotRequired['Command']
    data: NotRequired['LSPAny']

class CodeLensRegistrationOptions(TypedDict):
    """Registration options for a {@link CodeLensRequest}."""
    documentSelector: DocumentSelector | None
    resolveProvider: NotRequired[bool]

class DocumentLinkParams(TypedDict):
    """The parameters of a {@link DocumentLinkRequest}."""
    textDocument: TextDocumentIdentifier
    workDoneToken: NotRequired['ProgressToken']
    partialResultToken: NotRequired['ProgressToken']

class DocumentLink(TypedDict):
    """
    A document link is a range in a text document that links to an internal or external resource, like another
    text document or a web site.
    """
    range: Range
    target: NotRequired[URI]
    tooltip: NotRequired[str]
    data: NotRequired['LSPAny']

class DocumentLinkRegistrationOptions(TypedDict):
    """Registration options for a {@link DocumentLinkRequest}."""
    documentSelector: DocumentSelector | None
    resolveProvider: NotRequired[bool]

class DocumentFormattingParams(TypedDict):
    """The parameters of a {@link DocumentFormattingRequest}."""
    textDocument: TextDocumentIdentifier
    options: FormattingOptions
    workDoneToken: NotRequired['ProgressToken']

class DocumentFormattingRegistrationOptions(TypedDict):
    """Registration options for a {@link DocumentFormattingRequest}."""
    documentSelector: DocumentSelector | None

class DocumentRangeFormattingParams(TypedDict):
    """The parameters of a {@link DocumentRangeFormattingRequest}."""
    textDocument: TextDocumentIdentifier
    range: Range
    options: FormattingOptions
    workDoneToken: NotRequired['ProgressToken']

class DocumentRangeFormattingRegistrationOptions(TypedDict):
    """Registration options for a {@link DocumentRangeFormattingRequest}."""
    documentSelector: DocumentSelector | None
    rangesSupport: NotRequired[bool]

class DocumentRangesFormattingParams(TypedDict):
    """
    The parameters of a {@link DocumentRangesFormattingRequest}.

    @since 3.18.0
    @proposed
    """
    textDocument: TextDocumentIdentifier
    ranges: list['Range']
    options: FormattingOptions
    workDoneToken: NotRequired['ProgressToken']

class DocumentOnTypeFormattingParams(TypedDict):
    """The parameters of a {@link DocumentOnTypeFormattingRequest}."""
    textDocument: TextDocumentIdentifier
    position: Position
    ch: str
    options: FormattingOptions

class DocumentOnTypeFormattingRegistrationOptions(TypedDict):
    """Registration options for a {@link DocumentOnTypeFormattingRequest}."""
    documentSelector: DocumentSelector | None
    firstTriggerCharacter: str
    moreTriggerCharacter: NotRequired[list[str]]

class RenameParams(TypedDict):
    """The parameters of a {@link RenameRequest}."""
    textDocument: TextDocumentIdentifier
    position: Position
    newName: str
    workDoneToken: NotRequired['ProgressToken']

class RenameRegistrationOptions(TypedDict):
    """Registration options for a {@link RenameRequest}."""
    documentSelector: DocumentSelector | None
    prepareProvider: NotRequired[bool]

class PrepareRenameParams(TypedDict):
    textDocument: TextDocumentIdentifier
    position: Position
    workDoneToken: NotRequired['ProgressToken']

class ExecuteCommandParams(TypedDict):
    """The parameters of a {@link ExecuteCommandRequest}."""
    command: str
    arguments: NotRequired[list['LSPAny']]
    workDoneToken: NotRequired['ProgressToken']

class ExecuteCommandRegistrationOptions(TypedDict):
    """Registration options for a {@link ExecuteCommandRequest}."""
    commands: list[str]

class ApplyWorkspaceEditParams(TypedDict):
    """The parameters passed via an apply workspace edit request."""
    label: NotRequired[str]
    edit: WorkspaceEdit
    metadata: NotRequired['WorkspaceEditMetadata']

class ApplyWorkspaceEditResult(TypedDict):
    """
    The result returned from the apply workspace edit request.

    @since 3.17 renamed from ApplyWorkspaceEditResponse
    """
    applied: bool
    failureReason: NotRequired[str]
    failedChange: NotRequired[Uint]

class WorkDoneProgressBegin(TypedDict):
    kind: Literal['begin']
    title: str
    cancellable: NotRequired[bool]
    message: NotRequired[str]
    percentage: NotRequired[Uint]

class WorkDoneProgressReport(TypedDict):
    kind: Literal['report']
    cancellable: NotRequired[bool]
    message: NotRequired[str]
    percentage: NotRequired[Uint]

class WorkDoneProgressEnd(TypedDict):
    kind: Literal['end']
    message: NotRequired[str]

class SetTraceParams(TypedDict):
    value: TraceValue

class LogTraceParams(TypedDict):
    message: str
    verbose: NotRequired[str]

class CancelParams(TypedDict):
    id: int | str

class ProgressParams(TypedDict):
    token: ProgressToken
    value: LSPAny

class TextDocumentPositionParams(TypedDict):
    """
    A parameter literal used in requests to pass a text document and a position inside that
    document.
    """
    textDocument: TextDocumentIdentifier
    position: Position

class WorkDoneProgressParams(TypedDict):
    workDoneToken: NotRequired['ProgressToken']

class PartialResultParams(TypedDict):
    partialResultToken: NotRequired['ProgressToken']

class LocationLink(TypedDict):
    """
    Represents the connection of two locations. Provides additional metadata over normal {@link Location locations},
    including an origin range.
    """
    originSelectionRange: NotRequired['Range']
    targetUri: DocumentUri
    targetRange: Range
    targetSelectionRange: Range

class Range(TypedDict):
    """
    A range in a text document expressed as (zero-based) start and end positions.

    If you want to specify a range that contains a line including the line ending
    character(s) then use an end position denoting the start of the next line.
    For example:
    ```ts
    {
        start: { line: 5, character: 23 }
        end : { line 6, character : 0 }
    }
    ```
    """
    start: Position
    end: Position

class ImplementationOptions(TypedDict):
    workDoneProgress: NotRequired[bool]

class StaticRegistrationOptions(TypedDict):
    """
    Static registration options to be returned in the initialize
    request.
    """
    id: NotRequired[str]

class TypeDefinitionOptions(TypedDict):
    workDoneProgress: NotRequired[bool]

class WorkspaceFoldersChangeEvent(TypedDict):
    """The workspace folder change event."""
    added: list['WorkspaceFolder']
    removed: list['WorkspaceFolder']

class ConfigurationItem(TypedDict):
    scopeUri: NotRequired[URI]
    section: NotRequired[str]

class TextDocumentIdentifier(TypedDict):
    """A literal to identify a text document in the client."""
    uri: DocumentUri

class Color(TypedDict):
    """Represents a color in RGBA space."""
    red: float
    green: float
    blue: float
    alpha: float

class DocumentColorOptions(TypedDict):
    workDoneProgress: NotRequired[bool]

class FoldingRangeOptions(TypedDict):
    workDoneProgress: NotRequired[bool]

class DeclarationOptions(TypedDict):
    workDoneProgress: NotRequired[bool]

class Position(TypedDict):
    """
    Position in a text document expressed as zero-based line and character
    offset. Prior to 3.17 the offsets were always based on a UTF-16 string
    representation. So a string of the form `a𐐀b` the character offset of the
    character `a` is 0, the character offset of `𐐀` is 1 and the character
    offset of b is 3 since `𐐀` is represented using two code units in UTF-16.
    Since 3.17 clients and servers can agree on a different string encoding
    representation (e.g. UTF-8). The client announces it's supported encoding
    via the client capability [`general.positionEncodings`](https://microsoft.github.io/language-server-protocol/specifications/specification-current/#clientCapabilities).
    The value is an array of position encodings the client supports, with
    decreasing preference (e.g. the encoding at index `0` is the most preferred
    one). To stay backwards compatible the only mandatory encoding is UTF-16
    represented via the string `utf-16`. The server can pick one of the
    encodings offered by the client and signals that encoding back to the
    client via the initialize result's property
    [`capabilities.positionEncoding`](https://microsoft.github.io/language-server-protocol/specifications/specification-current/#serverCapabilities). If the string value
    `utf-16` is missing from the client's capability `general.positionEncodings`
    servers can safely assume that the client supports UTF-16. If the server
    omits the position encoding in its initialize result the encoding defaults
    to the string value `utf-16`. Implementation considerations: since the
    conversion from one encoding into another requires the content of the
    file / line the conversion is best done where the file is read which is
    usually on the server side.

    Positions are line end character agnostic. So you can not specify a position
    that denotes `\\r|\\n` or `\\n|` where `|` represents the character offset.

    @since 3.17.0 - support for negotiated position encoding.
    """
    line: Uint
    character: Uint

class SelectionRangeOptions(TypedDict):
    workDoneProgress: NotRequired[bool]

class CallHierarchyOptions(TypedDict):
    """
    Call hierarchy options used during static registration.

    @since 3.16.0
    """
    workDoneProgress: NotRequired[bool]

class SemanticTokensOptions(TypedDict):
    """@since 3.16.0"""
    legend: SemanticTokensLegend
    range: NotRequired[bool | dict[str, LSPAny]]
    full: NotRequired[bool | SemanticTokensFullDelta]
    workDoneProgress: NotRequired[bool]

class SemanticTokensEdit(TypedDict):
    """@since 3.16.0"""
    start: Uint
    deleteCount: Uint
    data: NotRequired[list[Uint]]

class LinkedEditingRangeOptions(TypedDict):
    workDoneProgress: NotRequired[bool]

class FileCreate(TypedDict):
    """
    Represents information on a file/folder create.

    @since 3.16.0
    """
    uri: str

class TextDocumentEdit(TypedDict):
    """
    Describes textual changes on a text document. A TextDocumentEdit describes all changes
    on a document version Si and after they are applied move the document to version Si+1.
    So the creator of a TextDocumentEdit doesn't need to sort the array of edits or do any
    kind of ordering. However the edits must be non overlapping.
    """
    textDocument: OptionalVersionedTextDocumentIdentifier
    edits: list[TextEdit | AnnotatedTextEdit | SnippetTextEdit]

class CreateFile(TypedDict):
    """Create file operation."""
    kind: Literal['create']
    uri: DocumentUri
    options: NotRequired['CreateFileOptions']
    annotationId: NotRequired['ChangeAnnotationIdentifier']

class RenameFile(TypedDict):
    """Rename file operation"""
    kind: Literal['rename']
    oldUri: DocumentUri
    newUri: DocumentUri
    options: NotRequired['RenameFileOptions']
    annotationId: NotRequired['ChangeAnnotationIdentifier']

class DeleteFile(TypedDict):
    """Delete file operation"""
    kind: Literal['delete']
    uri: DocumentUri
    options: NotRequired['DeleteFileOptions']
    annotationId: NotRequired['ChangeAnnotationIdentifier']

class ChangeAnnotation(TypedDict):
    """
    Additional information that describes document changes.

    @since 3.16.0
    """
    label: str
    needsConfirmation: NotRequired[bool]
    description: NotRequired[str]

class FileOperationFilter(TypedDict):
    """
    A filter to describe in which file operation requests or notifications
    the server is interested in receiving.

    @since 3.16.0
    """
    scheme: NotRequired[str]
    pattern: FileOperationPattern

class FileRename(TypedDict):
    """
    Represents information on a file/folder rename.

    @since 3.16.0
    """
    oldUri: str
    newUri: str

class FileDelete(TypedDict):
    """
    Represents information on a file/folder delete.

    @since 3.16.0
    """
    uri: str

class MonikerOptions(TypedDict):
    workDoneProgress: NotRequired[bool]

class TypeHierarchyOptions(TypedDict):
    """
    Type hierarchy options used during static registration.

    @since 3.17.0
    """
    workDoneProgress: NotRequired[bool]

class InlineValueContext(TypedDict):
    """@since 3.17.0"""
    frameId: int
    stoppedLocation: Range

class InlineValueText(TypedDict):
    """
    Provide inline value as text.

    @since 3.17.0
    """
    range: Range
    text: str

class InlineValueVariableLookup(TypedDict):
    """
    Provide inline value through a variable lookup.
    If only a range is specified, the variable name will be extracted from the underlying document.
    An optional variable name can be used to override the extracted name.

    @since 3.17.0
    """
    range: Range
    variableName: NotRequired[str]
    caseSensitiveLookup: bool

class InlineValueEvaluatableExpression(TypedDict):
    """
    Provide an inline value through an expression evaluation.
    If only a range is specified, the expression will be extracted from the underlying document.
    An optional expression can be used to override the extracted expression.

    @since 3.17.0
    """
    range: Range
    expression: NotRequired[str]

class InlineValueOptions(TypedDict):
    """
    Inline value options used during static registration.

    @since 3.17.0
    """
    workDoneProgress: NotRequired[bool]

class InlayHintLabelPart(TypedDict):
    """
    An inlay hint label part allows for interactive and composite labels
    of inlay hints.

    @since 3.17.0
    """
    value: str
    tooltip: NotRequired[str | MarkupContent]
    location: NotRequired['Location']
    command: NotRequired['Command']

class MarkupContent(TypedDict):
    """
    A `MarkupContent` literal represents a string value which content is interpreted base on its
    kind flag. Currently the protocol supports `plaintext` and `markdown` as markup kinds.

    If the kind is `markdown` then the value can contain fenced code blocks like in GitHub issues.
    See https://help.github.com/articles/creating-and-highlighting-code-blocks/#syntax-highlighting

    Here is an example how such a string can be constructed using JavaScript / TypeScript:
    ```ts
    let markdown: MarkdownContent = {
     kind: MarkupKind.Markdown,
     value: [
       '# Header',
       'Some text',
       '```typescript',
       'someCode();',
       '```'
     ].join('\\n')
    };
    ```

    *Please Note* that clients might sanitize the return markdown. A client could decide to
    remove HTML from the markdown to avoid script execution.
    """
    kind: MarkupKind
    value: str

class InlayHintOptions(TypedDict):
    """
    Inlay hint options used during static registration.

    @since 3.17.0
    """
    resolveProvider: NotRequired[bool]
    workDoneProgress: NotRequired[bool]

class RelatedFullDocumentDiagnosticReport(TypedDict):
    """
    A full diagnostic report with a set of related documents.

    @since 3.17.0
    """
    relatedDocuments: NotRequired[dict[DocumentUri, FullDocumentDiagnosticReport | UnchangedDocumentDiagnosticReport]]
    kind: Literal['full']
    resultId: NotRequired[str]
    items: list['Diagnostic']

class RelatedUnchangedDocumentDiagnosticReport(TypedDict):
    """
    An unchanged diagnostic report with a set of related documents.

    @since 3.17.0
    """
    relatedDocuments: NotRequired[dict[DocumentUri, FullDocumentDiagnosticReport | UnchangedDocumentDiagnosticReport]]
    kind: Literal['unchanged']
    resultId: str

class FullDocumentDiagnosticReport(TypedDict):
    """
    A diagnostic report with a full set of problems.

    @since 3.17.0
    """
    kind: Literal['full']
    resultId: NotRequired[str]
    items: list['Diagnostic']

class UnchangedDocumentDiagnosticReport(TypedDict):
    """
    A diagnostic report indicating that the last returned
    report is still accurate.

    @since 3.17.0
    """
    kind: Literal['unchanged']
    resultId: str

class DiagnosticOptions(TypedDict):
    """
    Diagnostic options.

    @since 3.17.0
    """
    identifier: NotRequired[str]
    interFileDependencies: bool
    workspaceDiagnostics: bool
    workDoneProgress: NotRequired[bool]

class PreviousResultId(TypedDict):
    """
    A previous result id in a workspace pull request.

    @since 3.17.0
    """
    uri: DocumentUri
    value: str

class NotebookDocument(TypedDict):
    """
    A notebook document.

    @since 3.17.0
    """
    uri: URI
    notebookType: str
    version: int
    metadata: NotRequired['LSPObject']
    cells: list['NotebookCell']

class TextDocumentItem(TypedDict):
    """
    An item to transfer a text document from the client to the
    server.
    """
    uri: DocumentUri
    languageId: LanguageKind
    version: int
    text: str

class NotebookDocumentSyncOptions(TypedDict):
    """
    Options specific to a notebook plus its cells
    to be synced to the server.

    If a selector provides a notebook document
    filter but no cell selector all cells of a
    matching notebook document will be synced.

    If a selector provides no notebook document
    filter but only a cell selector all notebook
    document that contain at least one matching
    cell will be synced.

    @since 3.17.0
    """
    notebookSelector: list[NotebookDocumentFilterWithNotebook | NotebookDocumentFilterWithCells]
    save: NotRequired[bool]

class VersionedNotebookDocumentIdentifier(TypedDict):
    """
    A versioned notebook document identifier.

    @since 3.17.0
    """
    version: int
    uri: URI

class NotebookDocumentChangeEvent(TypedDict):
    """
    A change event for a notebook document.

    @since 3.17.0
    """
    metadata: NotRequired['LSPObject']
    cells: NotRequired['NotebookDocumentCellChanges']

class NotebookDocumentIdentifier(TypedDict):
    """
    A literal to identify a notebook document in the client.

    @since 3.17.0
    """
    uri: URI

class InlineCompletionContext(TypedDict):
    """
    Provides information about the context in which an inline completion was requested.

    @since 3.18.0
    @proposed
    """
    triggerKind: InlineCompletionTriggerKind
    selectedCompletionInfo: NotRequired['SelectedCompletionInfo']

class StringValue(TypedDict):
    """
    A string value used as a snippet is a template which allows to insert text
    and to control the editor cursor when insertion happens.

    A snippet can define tab stops and placeholders with `$1`, `$2`
    and `${3:foo}`. `$0` defines the final tab stop, it defaults to
    the end of the snippet. Variables are defined with `$name` and
    `${name:default value}`.

    @since 3.18.0
    @proposed
    """
    kind: Literal['snippet']
    value: str

class InlineCompletionOptions(TypedDict):
    """
    Inline completion options used during static registration.

    @since 3.18.0
    @proposed
    """
    workDoneProgress: NotRequired[bool]

class TextDocumentContentOptions(TypedDict):
    """
    Text document content provider options.

    @since 3.18.0
    @proposed
    """
    schemes: list[str]

class Registration(TypedDict):
    """General parameters to register for a notification or to register a provider."""
    id: str
    method: str
    registerOptions: NotRequired['LSPAny']

class Unregistration(TypedDict):
    """General parameters to unregister a request or notification."""
    id: str
    method: str

class WorkspaceFoldersInitializeParams(TypedDict):
    workspaceFolders: NotRequired[list['WorkspaceFolder'] | None]

class ServerCapabilities(TypedDict):
    """
    Defines the capabilities provided by a language
    server.
    """
    positionEncoding: NotRequired['PositionEncodingKind']
    textDocumentSync: NotRequired[TextDocumentSyncOptions | TextDocumentSyncKind]
    notebookDocumentSync: NotRequired[NotebookDocumentSyncOptions | NotebookDocumentSyncRegistrationOptions]
    completionProvider: NotRequired['CompletionOptions']
    hoverProvider: NotRequired[bool | HoverOptions]
    signatureHelpProvider: NotRequired['SignatureHelpOptions']
    declarationProvider: NotRequired[bool | DeclarationOptions | DeclarationRegistrationOptions]
    definitionProvider: NotRequired[bool | DefinitionOptions]
    typeDefinitionProvider: NotRequired[bool | TypeDefinitionOptions | TypeDefinitionRegistrationOptions]
    implementationProvider: NotRequired[bool | ImplementationOptions | ImplementationRegistrationOptions]
    referencesProvider: NotRequired[bool | ReferenceOptions]
    documentHighlightProvider: NotRequired[bool | DocumentHighlightOptions]
    documentSymbolProvider: NotRequired[bool | DocumentSymbolOptions]
    codeActionProvider: NotRequired[bool | CodeActionOptions]
    codeLensProvider: NotRequired['CodeLensOptions']
    documentLinkProvider: NotRequired['DocumentLinkOptions']
    colorProvider: NotRequired[bool | DocumentColorOptions | DocumentColorRegistrationOptions]
    workspaceSymbolProvider: NotRequired[bool | WorkspaceSymbolOptions]
    documentFormattingProvider: NotRequired[bool | DocumentFormattingOptions]
    documentRangeFormattingProvider: NotRequired[bool | DocumentRangeFormattingOptions]
    documentOnTypeFormattingProvider: NotRequired['DocumentOnTypeFormattingOptions']
    renameProvider: NotRequired[bool | RenameOptions]
    foldingRangeProvider: NotRequired[bool | FoldingRangeOptions | FoldingRangeRegistrationOptions]
    selectionRangeProvider: NotRequired[bool | SelectionRangeOptions | SelectionRangeRegistrationOptions]
    executeCommandProvider: NotRequired['ExecuteCommandOptions']
    callHierarchyProvider: NotRequired[bool | CallHierarchyOptions | CallHierarchyRegistrationOptions]
    linkedEditingRangeProvider: NotRequired[bool | LinkedEditingRangeOptions | LinkedEditingRangeRegistrationOptions]
    semanticTokensProvider: NotRequired[SemanticTokensOptions | SemanticTokensRegistrationOptions]
    monikerProvider: NotRequired[bool | MonikerOptions | MonikerRegistrationOptions]
    typeHierarchyProvider: NotRequired[bool | TypeHierarchyOptions | TypeHierarchyRegistrationOptions]
    inlineValueProvider: NotRequired[bool | InlineValueOptions | InlineValueRegistrationOptions]
    inlayHintProvider: NotRequired[bool | InlayHintOptions | InlayHintRegistrationOptions]
    diagnosticProvider: NotRequired[DiagnosticOptions | DiagnosticRegistrationOptions]
    inlineCompletionProvider: NotRequired[bool | InlineCompletionOptions]
    workspace: NotRequired['WorkspaceOptions']
    experimental: NotRequired['LSPAny']

class ServerInfo(TypedDict):
    """
    Information about the server

    @since 3.15.0
    @since 3.18.0 ServerInfo type name added.
    """
    name: str
    version: NotRequired[str]

class VersionedTextDocumentIdentifier(TypedDict):
    """A text document identifier to denote a specific version of a text document."""
    version: int
    uri: DocumentUri

class SaveOptions(TypedDict):
    """Save options."""
    includeText: NotRequired[bool]

class FileEvent(TypedDict):
    """An event describing a file change."""
    uri: DocumentUri
    type: FileChangeType

class FileSystemWatcher(TypedDict):
    globPattern: GlobPattern
    kind: NotRequired['WatchKind']

class Diagnostic(TypedDict):
    """
    Represents a diagnostic, such as a compiler error or warning. Diagnostic objects
    are only valid in the scope of a resource.
    """
    range: Range
    severity: NotRequired['DiagnosticSeverity']
    code: NotRequired[int | str]
    codeDescription: NotRequired['CodeDescription']
    source: NotRequired[str]
    message: str
    tags: NotRequired[list['DiagnosticTag']]
    relatedInformation: NotRequired[list['DiagnosticRelatedInformation']]
    data: NotRequired['LSPAny']

class CompletionContext(TypedDict):
    """Contains additional information about the context in which a completion request is triggered."""
    triggerKind: CompletionTriggerKind
    triggerCharacter: NotRequired[str]

class CompletionItemLabelDetails(TypedDict):
    """
    Additional details for a completion item label.

    @since 3.17.0
    """
    detail: NotRequired[str]
    description: NotRequired[str]

class InsertReplaceEdit(TypedDict):
    """
    A special text edit to provide an insert and a replace operation.

    @since 3.16.0
    """
    newText: str
    insert: Range
    replace: Range

class CompletionItemDefaults(TypedDict):
    """
    In many cases the items of an actual completion result share the same
    value for properties like `commitCharacters` or the range of a text
    edit. A completion list can therefore define item defaults which will
    be used if a completion item itself doesn't specify the value.

    If a completion list specifies a default value and a completion item
    also specifies a corresponding value, the rules for combining these are
    defined by `applyKinds` (if the client supports it), defaulting to
    ApplyKind.Replace.

    Servers are only allowed to return default values if the client
    signals support for this via the `completionList.itemDefaults`
    capability.

    @since 3.17.0
    """
    commitCharacters: NotRequired[list[str]]
    editRange: NotRequired[Range | EditRangeWithInsertReplace]
    insertTextFormat: NotRequired['InsertTextFormat']
    insertTextMode: NotRequired['InsertTextMode']
    data: NotRequired['LSPAny']

class CompletionItemApplyKinds(TypedDict):
    """
    Specifies how fields from a completion item should be combined with those
    from `completionList.itemDefaults`.

    If unspecified, all fields will be treated as ApplyKind.Replace.

    If a field's value is ApplyKind.Replace, the value from a completion item (if
    provided and not `null`) will always be used instead of the value from
    `completionItem.itemDefaults`.

    If a field's value is ApplyKind.Merge, the values will be merged using the rules
    defined against each field below.

    Servers are only allowed to return `applyKind` if the client
    signals support for this via the `completionList.applyKindSupport`
    capability.

    @since 3.18.0
    """
    commitCharacters: NotRequired['ApplyKind']
    data: NotRequired['ApplyKind']

class CompletionOptions(TypedDict):
    """Completion options."""
    triggerCharacters: NotRequired[list[str]]
    allCommitCharacters: NotRequired[list[str]]
    resolveProvider: NotRequired[bool]
    completionItem: NotRequired['ServerCompletionItemOptions']
    workDoneProgress: NotRequired[bool]

class HoverOptions(TypedDict):
    """Hover options."""
    workDoneProgress: NotRequired[bool]

class SignatureHelpContext(TypedDict):
    """
    Additional information about the context in which a signature help request was triggered.

    @since 3.15.0
    """
    triggerKind: SignatureHelpTriggerKind
    triggerCharacter: NotRequired[str]
    isRetrigger: bool
    activeSignatureHelp: NotRequired['SignatureHelp']

class SignatureInformation(TypedDict):
    """
    Represents the signature of something callable. A signature
    can have a label, like a function-name, a doc-comment, and
    a set of parameters.
    """
    label: str
    documentation: NotRequired[str | MarkupContent]
    parameters: NotRequired[list['ParameterInformation']]
    activeParameter: NotRequired[Uint | None]

class SignatureHelpOptions(TypedDict):
    """Server Capabilities for a {@link SignatureHelpRequest}."""
    triggerCharacters: NotRequired[list[str]]
    retriggerCharacters: NotRequired[list[str]]
    workDoneProgress: NotRequired[bool]

class DefinitionOptions(TypedDict):
    """Server Capabilities for a {@link DefinitionRequest}."""
    workDoneProgress: NotRequired[bool]

class ReferenceContext(TypedDict):
    """
    Value-object that contains additional information when
    requesting references.
    """
    includeDeclaration: bool

class ReferenceOptions(TypedDict):
    """Reference options."""
    workDoneProgress: NotRequired[bool]

class DocumentHighlightOptions(TypedDict):
    """Provider options for a {@link DocumentHighlightRequest}."""
    workDoneProgress: NotRequired[bool]

class BaseSymbolInformation(TypedDict):
    """A base for all symbol information."""
    name: str
    kind: SymbolKind
    tags: NotRequired[list['SymbolTag']]
    containerName: NotRequired[str]

class DocumentSymbolOptions(TypedDict):
    """Provider options for a {@link DocumentSymbolRequest}."""
    label: NotRequired[str]
    workDoneProgress: NotRequired[bool]

class CodeActionContext(TypedDict):
    """
    Contains additional diagnostic information about the context in which
    a {@link CodeActionProvider.provideCodeActions code action} is run.
    """
    diagnostics: list['Diagnostic']
    only: NotRequired[list['CodeActionKind']]
    triggerKind: NotRequired['CodeActionTriggerKind']

class CodeActionDisabled(TypedDict):
    """
    Captures why the code action is currently disabled.

    @since 3.18.0
    """
    reason: str

class CodeActionOptions(TypedDict):
    """Provider options for a {@link CodeActionRequest}."""
    codeActionKinds: NotRequired[list['CodeActionKind']]
    documentation: NotRequired[list['CodeActionKindDocumentation']]
    resolveProvider: NotRequired[bool]
    workDoneProgress: NotRequired[bool]

class LocationUriOnly(TypedDict):
    """
    Location with only uri and does not include range.

    @since 3.18.0
    """
    uri: DocumentUri

class WorkspaceSymbolOptions(TypedDict):
    """Server capabilities for a {@link WorkspaceSymbolRequest}."""
    resolveProvider: NotRequired[bool]
    workDoneProgress: NotRequired[bool]

class CodeLensOptions(TypedDict):
    """Code Lens provider options of a {@link CodeLensRequest}."""
    resolveProvider: NotRequired[bool]
    workDoneProgress: NotRequired[bool]

class DocumentLinkOptions(TypedDict):
    """Provider options for a {@link DocumentLinkRequest}."""
    resolveProvider: NotRequired[bool]
    workDoneProgress: NotRequired[bool]

class FormattingOptions(TypedDict):
    """Value-object describing what options formatting should use."""
    tabSize: Uint
    insertSpaces: bool
    trimTrailingWhitespace: NotRequired[bool]
    insertFinalNewline: NotRequired[bool]
    trimFinalNewlines: NotRequired[bool]

class DocumentFormattingOptions(TypedDict):
    """Provider options for a {@link DocumentFormattingRequest}."""
    workDoneProgress: NotRequired[bool]

class DocumentRangeFormattingOptions(TypedDict):
    """Provider options for a {@link DocumentRangeFormattingRequest}."""
    rangesSupport: NotRequired[bool]
    workDoneProgress: NotRequired[bool]

class DocumentOnTypeFormattingOptions(TypedDict):
    """Provider options for a {@link DocumentOnTypeFormattingRequest}."""
    firstTriggerCharacter: str
    moreTriggerCharacter: NotRequired[list[str]]

class RenameOptions(TypedDict):
    """Provider options for a {@link RenameRequest}."""
    prepareProvider: NotRequired[bool]
    workDoneProgress: NotRequired[bool]

class PrepareRenamePlaceholder(TypedDict):
    """@since 3.18.0"""
    range: Range
    placeholder: str

class PrepareRenameDefaultBehavior(TypedDict):
    """@since 3.18.0"""
    defaultBehavior: bool

class ExecuteCommandOptions(TypedDict):
    """The server capabilities of a {@link ExecuteCommandRequest}."""
    commands: list[str]
    workDoneProgress: NotRequired[bool]

class WorkspaceEditMetadata(TypedDict):
    """
    Additional data about a workspace edit.

    @since 3.18.0
    @proposed
    """
    isRefactoring: NotRequired[bool]

class SemanticTokensLegend(TypedDict):
    """@since 3.16.0"""
    tokenTypes: list[str]
    tokenModifiers: list[str]

class SemanticTokensFullDelta(TypedDict):
    """
    Semantic tokens options to support deltas for full documents

    @since 3.18.0
    """
    delta: NotRequired[bool]

class OptionalVersionedTextDocumentIdentifier(TypedDict):
    """A text document identifier to optionally denote a specific version of a text document."""
    version: int | None
    uri: DocumentUri

class AnnotatedTextEdit(TypedDict):
    """
    A special text edit with an additional change annotation.

    @since 3.16.0.
    """
    annotationId: ChangeAnnotationIdentifier
    range: Range
    newText: str

class SnippetTextEdit(TypedDict):
    """
    An interactive text edit.

    @since 3.18.0
    @proposed
    """
    range: Range
    snippet: StringValue
    annotationId: NotRequired['ChangeAnnotationIdentifier']

class ResourceOperation(TypedDict):
    """A generic resource operation."""
    kind: str
    annotationId: NotRequired['ChangeAnnotationIdentifier']

class CreateFileOptions(TypedDict):
    """Options to create a file."""
    overwrite: NotRequired[bool]
    ignoreIfExists: NotRequired[bool]

class RenameFileOptions(TypedDict):
    """Rename file options"""
    overwrite: NotRequired[bool]
    ignoreIfExists: NotRequired[bool]

class DeleteFileOptions(TypedDict):
    """Delete file options"""
    recursive: NotRequired[bool]
    ignoreIfNotExists: NotRequired[bool]

class FileOperationPattern(TypedDict):
    """
    A pattern to describe in which file operation requests or notifications
    the server is interested in receiving.

    @since 3.16.0
    """
    glob: str
    matches: NotRequired['FileOperationPatternKind']
    options: NotRequired['FileOperationPatternOptions']

class WorkspaceFullDocumentDiagnosticReport(TypedDict):
    """
    A full document diagnostic report for a workspace diagnostic result.

    @since 3.17.0
    """
    uri: DocumentUri
    version: int | None
    kind: Literal['full']
    resultId: NotRequired[str]
    items: list['Diagnostic']

class WorkspaceUnchangedDocumentDiagnosticReport(TypedDict):
    """
    An unchanged document diagnostic report for a workspace diagnostic result.

    @since 3.17.0
    """
    uri: DocumentUri
    version: int | None
    kind: Literal['unchanged']
    resultId: str

class NotebookCell(TypedDict):
    """
    A notebook cell.

    A cell's document URI must be unique across ALL notebook
    cells and can therefore be used to uniquely identify a
    notebook cell or the cell's text document.

    @since 3.17.0
    """
    kind: NotebookCellKind
    document: DocumentUri
    metadata: NotRequired['LSPObject']
    executionSummary: NotRequired['ExecutionSummary']

class NotebookDocumentFilterWithNotebook(TypedDict):
    """@since 3.18.0"""
    notebook: str | NotebookDocumentFilter
    cells: NotRequired[list['NotebookCellLanguage']]

class NotebookDocumentFilterWithCells(TypedDict):
    """@since 3.18.0"""
    notebook: NotRequired[str | NotebookDocumentFilter]
    cells: list['NotebookCellLanguage']

class NotebookDocumentCellChanges(TypedDict):
    """
    Cell changes to a notebook document.

    @since 3.18.0
    """
    structure: NotRequired['NotebookDocumentCellChangeStructure']
    data: NotRequired[list['NotebookCell']]
    textContent: NotRequired[list['NotebookDocumentCellContentChanges']]

class SelectedCompletionInfo(TypedDict):
    """
    Describes the currently selected completion item.

    @since 3.18.0
    @proposed
    """
    range: Range
    text: str

class ClientInfo(TypedDict):
    """
    Information about the client

    @since 3.15.0
    @since 3.18.0 ClientInfo type name added.
    """
    name: str
    version: NotRequired[str]

class ClientCapabilities(TypedDict):
    """Defines the capabilities provided by the client."""
    workspace: NotRequired['WorkspaceClientCapabilities']
    textDocument: NotRequired['TextDocumentClientCapabilities']
    notebookDocument: NotRequired['NotebookDocumentClientCapabilities']
    window: NotRequired['WindowClientCapabilities']
    general: NotRequired['GeneralClientCapabilities']
    experimental: NotRequired['LSPAny']

class TextDocumentSyncOptions(TypedDict):
    openClose: NotRequired[bool]
    change: NotRequired['TextDocumentSyncKind']
    willSave: NotRequired[bool]
    willSaveWaitUntil: NotRequired[bool]
    save: NotRequired[bool | SaveOptions]

class WorkspaceOptions(TypedDict):
    """
    Defines workspace specific capabilities of the server.

    @since 3.18.0
    """
    workspaceFolders: NotRequired['WorkspaceFoldersServerCapabilities']
    fileOperations: NotRequired['FileOperationOptions']
    textDocumentContent: NotRequired[TextDocumentContentOptions | TextDocumentContentRegistrationOptions]

class TextDocumentContentChangePartial(TypedDict):
    """@since 3.18.0"""
    range: Range
    rangeLength: NotRequired[Uint]
    text: str

class TextDocumentContentChangeWholeDocument(TypedDict):
    """@since 3.18.0"""
    text: str

class CodeDescription(TypedDict):
    """
    Structure to capture a description for an error code.

    @since 3.16.0
    """
    href: URI

class DiagnosticRelatedInformation(TypedDict):
    """
    Represents a related message and source code location for a diagnostic. This should be
    used to point to code locations that cause or related to a diagnostics, e.g when duplicating
    a symbol in a scope.
    """
    location: Location
    message: str

class EditRangeWithInsertReplace(TypedDict):
    """
    Edit range variant that includes ranges for insert and replace operations.

    @since 3.18.0
    """
    insert: Range
    replace: Range

class ServerCompletionItemOptions(TypedDict):
    """@since 3.18.0"""
    labelDetailsSupport: NotRequired[bool]

class MarkedStringWithLanguage(TypedDict):
    """
    @since 3.18.0
    @deprecated use MarkupContent instead.
    """
    language: str
    value: str

class ParameterInformation(TypedDict):
    """
    Represents a parameter of a callable-signature. A parameter can
    have a label and a doc-comment.
    """
    label: str | list[Uint]
    documentation: NotRequired[str | MarkupContent]

class CodeActionKindDocumentation(TypedDict):
    """
    Documentation for a class of code actions.

    @since 3.18.0
    @proposed
    """
    kind: CodeActionKind
    command: Command

class NotebookCellTextDocumentFilter(TypedDict):
    """
    A notebook cell text document filter denotes a cell text
    document by different properties.

    @since 3.17.0
    """
    notebook: str | NotebookDocumentFilter
    language: NotRequired[str]

class FileOperationPatternOptions(TypedDict):
    """
    Matching options for the file operation pattern.

    @since 3.16.0
    """
    ignoreCase: NotRequired[bool]

class ExecutionSummary(TypedDict):
    executionOrder: Uint
    success: NotRequired[bool]

class NotebookCellLanguage(TypedDict):
    """@since 3.18.0"""
    language: str

class NotebookDocumentCellChangeStructure(TypedDict):
    """
    Structural changes to cells in a notebook document.

    @since 3.18.0
    """
    array: NotebookCellArrayChange
    didOpen: NotRequired[list['TextDocumentItem']]
    didClose: NotRequired[list['TextDocumentIdentifier']]

class NotebookDocumentCellContentChanges(TypedDict):
    """
    Content changes to a cell in a notebook document.

    @since 3.18.0
    """
    document: VersionedTextDocumentIdentifier
    changes: list['TextDocumentContentChangeEvent']

class WorkspaceClientCapabilities(TypedDict):
    """Workspace specific client capabilities."""
    applyEdit: NotRequired[bool]
    workspaceEdit: NotRequired['WorkspaceEditClientCapabilities']
    didChangeConfiguration: NotRequired['DidChangeConfigurationClientCapabilities']
    didChangeWatchedFiles: NotRequired['DidChangeWatchedFilesClientCapabilities']
    symbol: NotRequired['WorkspaceSymbolClientCapabilities']
    executeCommand: NotRequired['ExecuteCommandClientCapabilities']
    workspaceFolders: NotRequired[bool]
    configuration: NotRequired[bool]
    semanticTokens: NotRequired['SemanticTokensWorkspaceClientCapabilities']
    codeLens: NotRequired['CodeLensWorkspaceClientCapabilities']
    fileOperations: NotRequired['FileOperationClientCapabilities']
    inlineValue: NotRequired['InlineValueWorkspaceClientCapabilities']
    inlayHint: NotRequired['InlayHintWorkspaceClientCapabilities']
    diagnostics: NotRequired['DiagnosticWorkspaceClientCapabilities']
    foldingRange: NotRequired['FoldingRangeWorkspaceClientCapabilities']
    textDocumentContent: NotRequired['TextDocumentContentClientCapabilities']

class TextDocumentClientCapabilities(TypedDict):
    """Text document specific client capabilities."""
    synchronization: NotRequired['TextDocumentSyncClientCapabilities']
    filters: NotRequired['TextDocumentFilterClientCapabilities']
    completion: NotRequired['CompletionClientCapabilities']
    hover: NotRequired['HoverClientCapabilities']
    signatureHelp: NotRequired['SignatureHelpClientCapabilities']
    declaration: NotRequired['DeclarationClientCapabilities']
    definition: NotRequired['DefinitionClientCapabilities']
    typeDefinition: NotRequired['TypeDefinitionClientCapabilities']
    implementation: NotRequired['ImplementationClientCapabilities']
    references: NotRequired['ReferenceClientCapabilities']
    documentHighlight: NotRequired['DocumentHighlightClientCapabilities']
    documentSymbol: NotRequired['DocumentSymbolClientCapabilities']
    codeAction: NotRequired['CodeActionClientCapabilities']
    codeLens: NotRequired['CodeLensClientCapabilities']
    documentLink: NotRequired['DocumentLinkClientCapabilities']
    colorProvider: NotRequired['DocumentColorClientCapabilities']
    formatting: NotRequired['DocumentFormattingClientCapabilities']
    rangeFormatting: NotRequired['DocumentRangeFormattingClientCapabilities']
    onTypeFormatting: NotRequired['DocumentOnTypeFormattingClientCapabilities']
    rename: NotRequired['RenameClientCapabilities']
    foldingRange: NotRequired['FoldingRangeClientCapabilities']
    selectionRange: NotRequired['SelectionRangeClientCapabilities']
    publishDiagnostics: NotRequired['PublishDiagnosticsClientCapabilities']
    callHierarchy: NotRequired['CallHierarchyClientCapabilities']
    semanticTokens: NotRequired['SemanticTokensClientCapabilities']
    linkedEditingRange: NotRequired['LinkedEditingRangeClientCapabilities']
    moniker: NotRequired['MonikerClientCapabilities']
    typeHierarchy: NotRequired['TypeHierarchyClientCapabilities']
    inlineValue: NotRequired['InlineValueClientCapabilities']
    inlayHint: NotRequired['InlayHintClientCapabilities']
    diagnostic: NotRequired['DiagnosticClientCapabilities']
    inlineCompletion: NotRequired['InlineCompletionClientCapabilities']

class NotebookDocumentClientCapabilities(TypedDict):
    """
    Capabilities specific to the notebook document support.

    @since 3.17.0
    """
    synchronization: NotebookDocumentSyncClientCapabilities

class WindowClientCapabilities(TypedDict):
    workDoneProgress: NotRequired[bool]
    showMessage: NotRequired['ShowMessageRequestClientCapabilities']
    showDocument: NotRequired['ShowDocumentClientCapabilities']

class GeneralClientCapabilities(TypedDict):
    """
    General client capabilities.

    @since 3.16.0
    """
    staleRequestSupport: NotRequired['StaleRequestSupportOptions']
    regularExpressions: NotRequired['RegularExpressionsClientCapabilities']
    markdown: NotRequired['MarkdownClientCapabilities']
    positionEncodings: NotRequired[list['PositionEncodingKind']]

class WorkspaceFoldersServerCapabilities(TypedDict):
    supported: NotRequired[bool]
    changeNotifications: NotRequired[str | bool]

class FileOperationOptions(TypedDict):
    """
    Options for notifications/requests for user operations on files.

    @since 3.16.0
    """
    didCreate: NotRequired['FileOperationRegistrationOptions']
    willCreate: NotRequired['FileOperationRegistrationOptions']
    didRename: NotRequired['FileOperationRegistrationOptions']
    willRename: NotRequired['FileOperationRegistrationOptions']
    didDelete: NotRequired['FileOperationRegistrationOptions']
    willDelete: NotRequired['FileOperationRegistrationOptions']

class RelativePattern(TypedDict):
    """
    A relative pattern is a helper to construct glob patterns that are matched
    relatively to a base URI. The common value for a `baseUri` is a workspace
    folder root, but it can be another absolute URI as well.

    @since 3.17.0
    """
    baseUri: WorkspaceFolder | URI
    pattern: Pattern

class TextDocumentFilterLanguage(TypedDict):
    """
    A document filter where `language` is required field.

    @since 3.18.0
    """
    language: str
    scheme: NotRequired[str]
    pattern: NotRequired['GlobPattern']

class TextDocumentFilterScheme(TypedDict):
    """
    A document filter where `scheme` is required field.

    @since 3.18.0
    """
    language: NotRequired[str]
    scheme: str
    pattern: NotRequired['GlobPattern']

class TextDocumentFilterPattern(TypedDict):
    """
    A document filter where `pattern` is required field.

    @since 3.18.0
    """
    language: NotRequired[str]
    scheme: NotRequired[str]
    pattern: GlobPattern

class NotebookDocumentFilterNotebookType(TypedDict):
    """
    A notebook document filter where `notebookType` is required field.

    @since 3.18.0
    """
    notebookType: str
    scheme: NotRequired[str]
    pattern: NotRequired['GlobPattern']

class NotebookDocumentFilterScheme(TypedDict):
    """
    A notebook document filter where `scheme` is required field.

    @since 3.18.0
    """
    notebookType: NotRequired[str]
    scheme: str
    pattern: NotRequired['GlobPattern']

class NotebookDocumentFilterPattern(TypedDict):
    """
    A notebook document filter where `pattern` is required field.

    @since 3.18.0
    """
    notebookType: NotRequired[str]
    scheme: NotRequired[str]
    pattern: GlobPattern

class NotebookCellArrayChange(TypedDict):
    """
    A change describing how to move a `NotebookCell`
    array from state S to S'.

    @since 3.17.0
    """
    start: Uint
    deleteCount: Uint
    cells: NotRequired[list['NotebookCell']]

class WorkspaceEditClientCapabilities(TypedDict):
    documentChanges: NotRequired[bool]
    resourceOperations: NotRequired[list['ResourceOperationKind']]
    failureHandling: NotRequired['FailureHandlingKind']
    normalizesLineEndings: NotRequired[bool]
    changeAnnotationSupport: NotRequired['ChangeAnnotationsSupportOptions']
    metadataSupport: NotRequired[bool]
    snippetEditSupport: NotRequired[bool]

class DidChangeConfigurationClientCapabilities(TypedDict):
    dynamicRegistration: NotRequired[bool]

class DidChangeWatchedFilesClientCapabilities(TypedDict):
    dynamicRegistration: NotRequired[bool]
    relativePatternSupport: NotRequired[bool]

class WorkspaceSymbolClientCapabilities(TypedDict):
    """Client capabilities for a {@link WorkspaceSymbolRequest}."""
    dynamicRegistration: NotRequired[bool]
    symbolKind: NotRequired['ClientSymbolKindOptions']
    tagSupport: NotRequired['ClientSymbolTagOptions']
    resolveSupport: NotRequired['ClientSymbolResolveOptions']

class ExecuteCommandClientCapabilities(TypedDict):
    """The client capabilities of a {@link ExecuteCommandRequest}."""
    dynamicRegistration: NotRequired[bool]

class SemanticTokensWorkspaceClientCapabilities(TypedDict):
    """@since 3.16.0"""
    refreshSupport: NotRequired[bool]

class CodeLensWorkspaceClientCapabilities(TypedDict):
    """@since 3.16.0"""
    refreshSupport: NotRequired[bool]

class FileOperationClientCapabilities(TypedDict):
    """
    Capabilities relating to events from file operations by the user in the client.

    These events do not come from the file system, they come from user operations
    like renaming a file in the UI.

    @since 3.16.0
    """
    dynamicRegistration: NotRequired[bool]
    didCreate: NotRequired[bool]
    willCreate: NotRequired[bool]
    didRename: NotRequired[bool]
    willRename: NotRequired[bool]
    didDelete: NotRequired[bool]
    willDelete: NotRequired[bool]

class InlineValueWorkspaceClientCapabilities(TypedDict):
    """
    Client workspace capabilities specific to inline values.

    @since 3.17.0
    """
    refreshSupport: NotRequired[bool]

class InlayHintWorkspaceClientCapabilities(TypedDict):
    """
    Client workspace capabilities specific to inlay hints.

    @since 3.17.0
    """
    refreshSupport: NotRequired[bool]

class DiagnosticWorkspaceClientCapabilities(TypedDict):
    """
    Workspace client capabilities specific to diagnostic pull requests.

    @since 3.17.0
    """
    refreshSupport: NotRequired[bool]

class FoldingRangeWorkspaceClientCapabilities(TypedDict):
    """
    Client workspace capabilities specific to folding ranges

    @since 3.18.0
    @proposed
    """
    refreshSupport: NotRequired[bool]

class TextDocumentContentClientCapabilities(TypedDict):
    """
    Client capabilities for a text document content provider.

    @since 3.18.0
    @proposed
    """
    dynamicRegistration: NotRequired[bool]

class TextDocumentSyncClientCapabilities(TypedDict):
    dynamicRegistration: NotRequired[bool]
    willSave: NotRequired[bool]
    willSaveWaitUntil: NotRequired[bool]
    didSave: NotRequired[bool]

class TextDocumentFilterClientCapabilities(TypedDict):
    relativePatternSupport: NotRequired[bool]

class CompletionClientCapabilities(TypedDict):
    """Completion client capabilities"""
    dynamicRegistration: NotRequired[bool]
    completionItem: NotRequired['ClientCompletionItemOptions']
    completionItemKind: NotRequired['ClientCompletionItemOptionsKind']
    insertTextMode: NotRequired['InsertTextMode']
    contextSupport: NotRequired[bool]
    completionList: NotRequired['CompletionListCapabilities']

class HoverClientCapabilities(TypedDict):
    dynamicRegistration: NotRequired[bool]
    contentFormat: NotRequired[list['MarkupKind']]

class SignatureHelpClientCapabilities(TypedDict):
    """Client Capabilities for a {@link SignatureHelpRequest}."""
    dynamicRegistration: NotRequired[bool]
    signatureInformation: NotRequired['ClientSignatureInformationOptions']
    contextSupport: NotRequired[bool]

class DeclarationClientCapabilities(TypedDict):
    """@since 3.14.0"""
    dynamicRegistration: NotRequired[bool]
    linkSupport: NotRequired[bool]

class DefinitionClientCapabilities(TypedDict):
    """Client Capabilities for a {@link DefinitionRequest}."""
    dynamicRegistration: NotRequired[bool]
    linkSupport: NotRequired[bool]

class TypeDefinitionClientCapabilities(TypedDict):
    """Since 3.6.0"""
    dynamicRegistration: NotRequired[bool]
    linkSupport: NotRequired[bool]

class ImplementationClientCapabilities(TypedDict):
    """@since 3.6.0"""
    dynamicRegistration: NotRequired[bool]
    linkSupport: NotRequired[bool]

class ReferenceClientCapabilities(TypedDict):
    """Client Capabilities for a {@link ReferencesRequest}."""
    dynamicRegistration: NotRequired[bool]

class DocumentHighlightClientCapabilities(TypedDict):
    """Client Capabilities for a {@link DocumentHighlightRequest}."""
    dynamicRegistration: NotRequired[bool]

class DocumentSymbolClientCapabilities(TypedDict):
    """Client Capabilities for a {@link DocumentSymbolRequest}."""
    dynamicRegistration: NotRequired[bool]
    symbolKind: NotRequired['ClientSymbolKindOptions']
    hierarchicalDocumentSymbolSupport: NotRequired[bool]
    tagSupport: NotRequired['ClientSymbolTagOptions']
    labelSupport: NotRequired[bool]

class CodeActionClientCapabilities(TypedDict):
    """The Client Capabilities of a {@link CodeActionRequest}."""
    dynamicRegistration: NotRequired[bool]
    codeActionLiteralSupport: NotRequired['ClientCodeActionLiteralOptions']
    isPreferredSupport: NotRequired[bool]
    disabledSupport: NotRequired[bool]
    dataSupport: NotRequired[bool]
    resolveSupport: NotRequired['ClientCodeActionResolveOptions']
    honorsChangeAnnotations: NotRequired[bool]
    documentationSupport: NotRequired[bool]
    tagSupport: NotRequired['CodeActionTagOptions']

class CodeLensClientCapabilities(TypedDict):
    """The client capabilities  of a {@link CodeLensRequest}."""
    dynamicRegistration: NotRequired[bool]
    resolveSupport: NotRequired['ClientCodeLensResolveOptions']

class DocumentLinkClientCapabilities(TypedDict):
    """The client capabilities of a {@link DocumentLinkRequest}."""
    dynamicRegistration: NotRequired[bool]
    tooltipSupport: NotRequired[bool]

class DocumentColorClientCapabilities(TypedDict):
    dynamicRegistration: NotRequired[bool]

class DocumentFormattingClientCapabilities(TypedDict):
    """Client capabilities of a {@link DocumentFormattingRequest}."""
    dynamicRegistration: NotRequired[bool]

class DocumentRangeFormattingClientCapabilities(TypedDict):
    """Client capabilities of a {@link DocumentRangeFormattingRequest}."""
    dynamicRegistration: NotRequired[bool]
    rangesSupport: NotRequired[bool]

class DocumentOnTypeFormattingClientCapabilities(TypedDict):
    """Client capabilities of a {@link DocumentOnTypeFormattingRequest}."""
    dynamicRegistration: NotRequired[bool]

class RenameClientCapabilities(TypedDict):
    dynamicRegistration: NotRequired[bool]
    prepareSupport: NotRequired[bool]
    prepareSupportDefaultBehavior: NotRequired['PrepareSupportDefaultBehavior']
    honorsChangeAnnotations: NotRequired[bool]

class FoldingRangeClientCapabilities(TypedDict):
    dynamicRegistration: NotRequired[bool]
    rangeLimit: NotRequired[Uint]
    lineFoldingOnly: NotRequired[bool]
    foldingRangeKind: NotRequired['ClientFoldingRangeKindOptions']
    foldingRange: NotRequired['ClientFoldingRangeOptions']

class SelectionRangeClientCapabilities(TypedDict):
    dynamicRegistration: NotRequired[bool]

class PublishDiagnosticsClientCapabilities(TypedDict):
    """The publish diagnostic client capabilities."""
    versionSupport: NotRequired[bool]
    relatedInformation: NotRequired[bool]
    tagSupport: NotRequired['ClientDiagnosticsTagOptions']
    codeDescriptionSupport: NotRequired[bool]
    dataSupport: NotRequired[bool]

class CallHierarchyClientCapabilities(TypedDict):
    """@since 3.16.0"""
    dynamicRegistration: NotRequired[bool]

class SemanticTokensClientCapabilities(TypedDict):
    """@since 3.16.0"""
    dynamicRegistration: NotRequired[bool]
    requests: ClientSemanticTokensRequestOptions
    tokenTypes: list[str]
    tokenModifiers: list[str]
    formats: list['TokenFormat']
    overlappingTokenSupport: NotRequired[bool]
    multilineTokenSupport: NotRequired[bool]
    serverCancelSupport: NotRequired[bool]
    augmentsSyntaxTokens: NotRequired[bool]

class LinkedEditingRangeClientCapabilities(TypedDict):
    """
    Client capabilities for the linked editing range request.

    @since 3.16.0
    """
    dynamicRegistration: NotRequired[bool]

class MonikerClientCapabilities(TypedDict):
    """
    Client capabilities specific to the moniker request.

    @since 3.16.0
    """
    dynamicRegistration: NotRequired[bool]

class TypeHierarchyClientCapabilities(TypedDict):
    """@since 3.17.0"""
    dynamicRegistration: NotRequired[bool]

class InlineValueClientCapabilities(TypedDict):
    """
    Client capabilities specific to inline values.

    @since 3.17.0
    """
    dynamicRegistration: NotRequired[bool]

class InlayHintClientCapabilities(TypedDict):
    """
    Inlay hint client capabilities.

    @since 3.17.0
    """
    dynamicRegistration: NotRequired[bool]
    resolveSupport: NotRequired['ClientInlayHintResolveOptions']

class DiagnosticClientCapabilities(TypedDict):
    """
    Client capabilities specific to diagnostic pull requests.

    @since 3.17.0
    """
    dynamicRegistration: NotRequired[bool]
    relatedDocumentSupport: NotRequired[bool]
    relatedInformation: NotRequired[bool]
    tagSupport: NotRequired['ClientDiagnosticsTagOptions']
    codeDescriptionSupport: NotRequired[bool]
    dataSupport: NotRequired[bool]

class InlineCompletionClientCapabilities(TypedDict):
    """
    Client capabilities specific to inline completions.

    @since 3.18.0
    @proposed
    """
    dynamicRegistration: NotRequired[bool]

class NotebookDocumentSyncClientCapabilities(TypedDict):
    """
    Notebook specific client capabilities.

    @since 3.17.0
    """
    dynamicRegistration: NotRequired[bool]
    executionSummarySupport: NotRequired[bool]

class ShowMessageRequestClientCapabilities(TypedDict):
    """Show message request client capabilities"""
    messageActionItem: NotRequired['ClientShowMessageActionItemOptions']

class ShowDocumentClientCapabilities(TypedDict):
    """
    Client capabilities for the showDocument request.

    @since 3.16.0
    """
    support: bool

class StaleRequestSupportOptions(TypedDict):
    """@since 3.18.0"""
    cancel: bool
    retryOnContentModified: list[str]

class RegularExpressionsClientCapabilities(TypedDict):
    """
    Client capabilities specific to regular expressions.

    @since 3.16.0
    """
    engine: RegularExpressionEngineKind
    version: NotRequired[str]

class MarkdownClientCapabilities(TypedDict):
    """
    Client capabilities specific to the used markdown parser.

    @since 3.16.0
    """
    parser: str
    version: NotRequired[str]
    allowedTags: NotRequired[list[str]]

class ChangeAnnotationsSupportOptions(TypedDict):
    """@since 3.18.0"""
    groupsOnLabel: NotRequired[bool]

class ClientSymbolKindOptions(TypedDict):
    """@since 3.18.0"""
    valueSet: NotRequired[list['SymbolKind']]

class ClientSymbolTagOptions(TypedDict):
    """@since 3.18.0"""
    valueSet: list['SymbolTag']

class ClientSymbolResolveOptions(TypedDict):
    """@since 3.18.0"""
    properties: list[str]

class ClientCompletionItemOptions(TypedDict):
    """@since 3.18.0"""
    snippetSupport: NotRequired[bool]
    commitCharactersSupport: NotRequired[bool]
    documentationFormat: NotRequired[list['MarkupKind']]
    deprecatedSupport: NotRequired[bool]
    preselectSupport: NotRequired[bool]
    tagSupport: NotRequired['CompletionItemTagOptions']
    insertReplaceSupport: NotRequired[bool]
    resolveSupport: NotRequired['ClientCompletionItemResolveOptions']
    insertTextModeSupport: NotRequired['ClientCompletionItemInsertTextModeOptions']
    labelDetailsSupport: NotRequired[bool]

class ClientCompletionItemOptionsKind(TypedDict):
    """@since 3.18.0"""
    valueSet: NotRequired[list['CompletionItemKind']]

class CompletionListCapabilities(TypedDict):
    """
    The client supports the following `CompletionList` specific
    capabilities.

    @since 3.17.0
    """
    itemDefaults: NotRequired[list[str]]
    applyKindSupport: NotRequired[bool]

class ClientSignatureInformationOptions(TypedDict):
    """@since 3.18.0"""
    documentationFormat: NotRequired[list['MarkupKind']]
    parameterInformation: NotRequired['ClientSignatureParameterInformationOptions']
    activeParameterSupport: NotRequired[bool]
    noActiveParameterSupport: NotRequired[bool]

class ClientCodeActionLiteralOptions(TypedDict):
    """@since 3.18.0"""
    codeActionKind: ClientCodeActionKindOptions

class ClientCodeActionResolveOptions(TypedDict):
    """@since 3.18.0"""
    properties: list[str]

class CodeActionTagOptions(TypedDict):
    """@since 3.18.0 - proposed"""
    valueSet: list['CodeActionTag']

class ClientCodeLensResolveOptions(TypedDict):
    """@since 3.18.0"""
    properties: list[str]

class ClientFoldingRangeKindOptions(TypedDict):
    """@since 3.18.0"""
    valueSet: NotRequired[list['FoldingRangeKind']]

class ClientFoldingRangeOptions(TypedDict):
    """@since 3.18.0"""
    collapsedText: NotRequired[bool]

class DiagnosticsCapabilities(TypedDict):
    """General diagnostics capabilities for pull and push model."""
    relatedInformation: NotRequired[bool]
    tagSupport: NotRequired['ClientDiagnosticsTagOptions']
    codeDescriptionSupport: NotRequired[bool]
    dataSupport: NotRequired[bool]

class ClientSemanticTokensRequestOptions(TypedDict):
    """@since 3.18.0"""
    range: NotRequired[bool | dict[str, LSPAny]]
    full: NotRequired[bool | ClientSemanticTokensRequestFullDelta]

class ClientInlayHintResolveOptions(TypedDict):
    """@since 3.18.0"""
    properties: list[str]

class ClientShowMessageActionItemOptions(TypedDict):
    """@since 3.18.0"""
    additionalPropertiesSupport: NotRequired[bool]

class CompletionItemTagOptions(TypedDict):
    """@since 3.18.0"""
    valueSet: list['CompletionItemTag']

class ClientCompletionItemResolveOptions(TypedDict):
    """@since 3.18.0"""
    properties: list[str]

class ClientCompletionItemInsertTextModeOptions(TypedDict):
    """@since 3.18.0"""
    valueSet: list['InsertTextMode']

class ClientSignatureParameterInformationOptions(TypedDict):
    """@since 3.18.0"""
    labelOffsetSupport: NotRequired[bool]

class ClientCodeActionKindOptions(TypedDict):
    """@since 3.18.0"""
    valueSet: list['CodeActionKind']

class ClientDiagnosticsTagOptions(TypedDict):
    """@since 3.18.0"""
    valueSet: list['DiagnosticTag']

class ClientSemanticTokensRequestFullDelta(TypedDict):
    """@since 3.18.0"""
    delta: NotRequired[bool]
