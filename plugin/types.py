from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Literal, Tuple, TypedDict, TypeVar

from LSP.plugin.core.protocol import Position as LspPosition
from LSP.plugin.core.protocol import Range as LspRange
from LSP.plugin.core.typing import StrEnum

T_Callable = TypeVar("T_Callable", bound=Callable[..., Any])


@dataclass
class AccountStatus:
    has_signed_in: bool
    """Whether the user has signed in."""
    is_authorized: bool
    """Whether user's account can use the Copilot service."""
    user: str = ""
    """User's GitHub ID."""


class EnhancedStrEnum(StrEnum):
    @classmethod
    def has_value(cls, value: str) -> bool:
        return value in iter(cls)  # type: ignore


# ---------------------------- #
# realted to Sublime Text APIs #
# ---------------------------- #

StPoint = int
StRegion = Tuple[StPoint, StPoint]


class StLayout(TypedDict, total=True):
    cols: list[float]
    rows: list[float]
    cells: list[list[int]]


class NetworkProxy(TypedDict, total=True):
    host: str
    port: int
    username: str
    password: str
    rejectUnauthorized: bool


# ------------------- #
# basic Copilot types #
# ------------------- #


class CopilotDocType(TypedDict, total=True):
    source: str
    tabSize: int
    indentSize: int
    insertSpaces: bool
    path: str
    uri: str
    relativePath: str
    languageId: str
    position: LspPosition
    version: int


# --------------- #
# Copilot payload #
# --------------- #


class CopilotPayloadFileStatus(TypedDict, total=True):
    status: Literal["not included", "included"]


class CopilotPayloadCompletion(TypedDict, total=True):
    text: str
    position: LspPosition
    uuid: str
    range: LspRange
    displayText: str
    point: StPoint
    region: StRegion


class CopilotPayloadCompletions(TypedDict, total=True):
    completions: list[CopilotPayloadCompletion]


class CopilotPayloadFeatureFlagsNotification(TypedDict, total=True):
    ssc: bool
    chat: bool
    rt: bool


class CopilotPayloadGetVersion(TypedDict, total=True):
    version: str
    """E.g., `"1.202.0"`."""
    buildType: str
    """E.g., `"prod"`."""
    runtimeVersion: str
    """E.g., `"node/20.14.0"`."""


class CopilotPayloadNotifyAccepted(TypedDict, total=True):
    uuid: str


class CopilotPayloadNotifyRejected(TypedDict, total=True):
    uuids: list[str]


class CopilotPayloadSignInInitiate(TypedDict, total=True):
    verificationUri: str
    status: str
    userCode: str
    expiresIn: int
    interval: int


class CopilotPayloadSignInWithGithubToken(TypedDict, total=True):
    user: str
    githubToken: str


class CopilotPayloadSignInConfirm(TypedDict, total=True):
    status: Literal[
        "AlreadySignedIn",
        "MaybeOk",
        "NotAuthorized",
        "NotSignedIn",
        "OK",
    ]
    user: str


class CopilotPayloadSignOut(TypedDict, total=True):
    status: Literal["NotSignedIn"]


class CopilotPayloadLogMessage(TypedDict, total=True):
    metadataStr: str
    extra: str
    level: int
    message: str


class CopilotPayloadStatusNotification(TypedDict, total=True):
    message: str
    status: Literal["InProgress", "Normal"]


class CopilotPayloadPanelSolution(TypedDict, total=True):
    displayText: str
    solutionId: str
    score: int
    panelId: str
    completionText: str
    range: LspRange
    region: StRegion


class CopilotPayloadPanelCompletionSolutionCount(TypedDict, total=True):
    solutionCountTarget: int


# --------------------- #
#  Copilot Chat Types   #
# --------------------- #


class CopilotConversationTemplates(EnhancedStrEnum):
    FIX = "/fix"
    TESTS = "/tests"
    DOC = "/doc"
    EXPLAIN = "/explain"
    SIMPLIFY = "/simplify"


class CopilotConversationDebugTemplates(EnhancedStrEnum):
    FAIL = "/debug.fail"
    FILTER = "/debug.filter"
    DUMP = "/debug.dump"
    TREE = "/debug.tree"
    ECHO = "/debug.echo"
    PROMPT = "/debug.prompt"
    SKILLS = "/debug.skills"
    VULNERABILITY = "/debug.vulnerability"
    MARKDOWN = "/debug.markdown"


class CopilotPayloadConversationEntry(TypedDict, total=True):
    kind: str
    conversationId: str
    turnId: str
    reply: str
    annotations: list[str]
    references: list[CopilotRequestConversationTurnReference | CopilotGitHubWebSearch]
    hideText: bool
    warnings: list[Any]  # @todo define a detailed type


class CopilotPayloadConversationEntryTransformed(TypedDict, total=True):
    """Our own transformation of `CopilotPayloadConversationEntry`."""

    kind: str
    turnId: str
    messages: list[str]
    codeBlocks: list[str]
    codeBlockIndices: list[int]
    references: list[CopilotRequestConversationTurnReference | CopilotGitHubWebSearch]
    warnings: list[Any]


class CopilotPayloadConversationTemplate(TypedDict, total=True):
    id: str
    description: str
    shortDescription: str
    scopes: list[str]


class CopilotRequestConversationTurn(TypedDict, total=True):
    conversationId: str
    message: str
    workDoneToken: str
    doc: CopilotDocType
    computeSuggestions: bool
    references: list[CopilotRequestConversationTurnReference | CopilotGitHubWebSearch]
    source: Literal["panel", "inline"]


class CopilotRequestConversationTurnReference(TypedDict, total=True):
    type: str
    status: str
    uri: str
    position: LspPosition
    range: LspRange
    visibleRange: LspRange
    selection: LspRange
    openedAt: str | None
    activeAt: str | None


class CopilotGitHubWebDataResult(TypedDict, total=True):
    title: str
    excerpt: str
    url: str


class CopilotGitHubWebData(TypedDict, total=True):
    query: str
    type: str
    results: list[CopilotGitHubWebDataResult] | None


class CopilotGitHubWebMetadata(TypedDict, total=False):
    display_name: str | None
    display_icon: str | None


class CopilotGitHubWebSearch(TypedDict, total=True):
    type: Literal["github.web-search"]
    id: str
    data: CopilotGitHubWebData
    metadata: CopilotGitHubWebMetadata | None


class CopilotRequestConversationAgent(TypedDict, total=True):
    slug: str
    name: str
    description: str


class CopilotPayloadConversationPreconditions(TypedDict, total=True):
    pass


class CopilotPayloadConversationCreate(TypedDict, total=True):
    conversationId: str
    """E.g., `"15d1791c-42f4-490c-9f79-0b79c4142d17"`."""
    turnId: str
    """E.g., `"a4a3785f-808f-41cc-8037-cd6707ffe584"`."""


class CopilotPayloadConversationContext(TypedDict, total=True):
    conversationId: str
    """E.g., `"e3b0d5e3-0c3b-4292-a5ea-15d6003e7c45"`."""
    turnId: str
    """E.g., `"09ac7601-6c28-4617-b3e4-13f5ff8502b7"`."""
    skillId: Literal[
        "current-editor",
        "project-labels",
        "recent-files",
        "references",
        "problems-in-active-document",
    ]  # not the complet list yet


class CopilotUserDefinedPromptTemplates(TypedDict, total=True):
    id: str
    description: str
    prompt: list[str]
    scopes: list[str]
