from __future__ import annotations

import sublime

assert __package__

PACKAGE_NAME = __package__.partition(".")[0]
PLATFORM_ARCH = f"{sublime.platform()}_{sublime.arch()}"

SERVER_VERSION = "1.425.0"
"""The server tag. You can find them on https://github.com/github/copilot-language-server-release/releases"""

# ---------------- #
# Setting prefixes #
# ---------------- #

COPILOT_OUTPUT_PANEL_PREFIX = "copilot"
COPILOT_VIEW_SETTINGS_PREFIX = "copilot.completion"
COPILOT_WINDOW_SETTINGS_PREFIX = "copilot"
COPILOT_WINDOW_CONVERSATION_SETTINGS_PREFIX = "copilot.conversation"

# ---------------- #
# Copilot requests #
# ---------------- #

REQ_CHECK_STATUS = "checkStatus"
REQ_CHECK_QUOTA = "checkQuota"
REQ_COPILOT_MODELS = "copilot/models"
REQ_COPILOT_SET_MODEL_POLICY = "copilot/setModelPolicy"
REQ_COPILOT_CODE_REVIEW = "copilot/codeReview"
REQ_FILE_CHECK_STATUS = "checkFileStatus"
REQ_GET_COMPLETIONS = "getCompletions"
REQ_GET_COMPLETIONS_CYCLING = "getCompletionsCycling"
REQ_GET_PANEL_COMPLETIONS = "getPanelCompletions"
REQ_GET_PROMPT = "getPrompt"
REQ_GET_VERSION = "getVersion"
REQ_INLINE_COMPLETION_PROMPT = "textDocument/inlineCompletionPrompt"
REQ_INLINE_COMPLETION = "textDocument/inlineCompletion"
REQ_GIT_COMMIT_GENERATE = "git/commitGenerate"
REQ_NOTIFY_ACCEPTED = "notifyAccepted"
REQ_NOTIFY_REJECTED = "notifyRejected"
REQ_NOTIFY_SHOWN = "notifyShown"
REQ_RECORD_TELEMETRY_CONSENT = "recordTelemetryConsent"
REQ_SET_EDITOR_INFO = "setEditorInfo"
REQ_SIGN_IN_CONFIRM = "signInConfirm"
REQ_SIGN_IN_INITIATE = "signInInitiate"
REQ_SIGN_IN_WITH_GITHUB_TOKEN = "signInWithGithubToken"
REQ_SIGN_OUT = "signOut"
REQ_TEXT_DOCUMENT_DID_FOCUS = "textDocument/didFocus"
# {
#     "textDocument": {
#         "uri": "file:///path/to/file"
#     }
# }

# textDocument/inlineCompletionPrompt
# {
#         textDocument: {
#             uri: string;
#     },
#         position: {
#         line: I.Integer({ minimum: 0 }),
#         character: I.Integer({ minimum: 0 }),
#     },
#         formattingOptions: I.Optional(
#             I.Object({
#                 tabSize: I.Optional(I.Union([I.Integer({ minimum: 1 }), I.String()])),
#                 insertSpaces: I.Optional(I.Union([I.Boolean(), I.String()])),
#             }),
#         ),
#         context: {
#                 triggerKind: "Invoked" or "Automatic",
#                 selectedCompletionInfo: I.Optional(
#                     I.Object({
#                         text: I.String(),
#                         range: { start: {line: character}, end: wl },
#                         tooltipSignature: I.Optional(I.String()),
#                     }),
#                 ),
#             },
#         data: {
# "message": "string",
# },
#     }
# textDocument/inlineCompletion

# --------------------- #
# Copilot chat requests #
# --------------------- #

REQ_CONVERSATION_AGENTS = "conversation/agents"
REQ_CONVERSATION_CONTEXT = "conversation/context"
REQ_CONVERSATION_COPY_CODE = "conversation/copyCode"
REQ_CONVERSATION_CREATE = "conversation/create"
REQ_CONVERSATION_DESTROY = "conversation/destroy"
REQ_CONVERSATION_INSERT_CODE = "conversation/insertCode"
REQ_CONVERSATION_PERSISTANCE = "conversation/persistance"
REQ_CONVERSATION_PRECONDITIONS = "conversation/preconditions"
REQ_CONVERSATION_RATING = "conversation/rating"
REQ_CONVERSATION_TEMPLATES = "conversation/templates"
REQ_CONVERSATION_TURN = "conversation/turn"
REQ_CONVERSATION_TURN_DELETE = "conversation/turnDelete"
REQ_CONVERSATION_REGISTER_TOOLS = "conversation/registerTools"

# ---------------------------- #
# Copilot edit chat requests #
# ---------------------------- #

REQ_EDIT_CONVERSATION_CREATE = "editConversation/create"
REQ_EDIT_CONVERSATION_TURN = "editConversation/turn"
REQ_EDIT_CONVERSATION_TURN_DELETE = "editConversation/turnDelete"
REQ_EDIT_CONVERSATION_DESTROY = "editConversation/destroy"

# -------------------------- #
# Copilot context requests #
# -------------------------- #

REQ_CONTEXT_REGISTER_PROVIDERS = "context/registerProviders"
REQ_CONTEXT_UNREGISTER_PROVIDERS = "context/unregisterProviders"

# --------------------- #
# Copilot notifications #
# --------------------- #

NTFY_FEATURE_FLAGS_NOTIFICATION = "featureFlagsNotification"
NTFY_LOG_MESSAGE = "LogMessage"
NTFY_PANEL_SOLUTION = "PanelSolution"
NTFY_PANEL_SOLUTION_DONE = "PanelSolutionsDone"
NTFY_PROGRESS = "$/progress"
NTFY_STATUS_NOTIFICATION = "statusNotification"

# Edit conversation file generation statuses
EDIT_STATUS_BEGIN = "edit-conversation-begin"
EDIT_STATUS_END = "edit-conversation-end"
EDIT_STATUS_PLAN_GENERATED = "edit-plan-generated"
EDIT_STATUS_OVERALL_DESCRIPTION = "overall-description-generated"
EDIT_STATUS_CODE_GENERATED = "updated-code-generated"
EDIT_STATUS_NO_CODE_BLOCKS = "no-code-blocks-found"
# "updated-code-generating"
