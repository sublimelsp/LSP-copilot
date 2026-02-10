from __future__ import annotations

import sublime

assert __package__

PACKAGE_NAME = __package__.partition(".")[0]
PLATFORM_ARCH = f"{sublime.platform()}_{sublime.arch()}"

SERVER_VERSION = "1.427.0"
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
REQ_FILE_CHECK_STATUS = "checkFileStatus"
REQ_GET_COMPLETIONS = "getCompletions"
REQ_GET_COMPLETIONS_CYCLING = "getCompletionsCycling"
REQ_GET_PROMPT = "getPrompt"
REQ_GET_PANEL_COMPLETIONS = "getPanelCompletions"
REQ_GET_VERSION = "getVersion"
REQ_NOTIFY_ACCEPTED = "notifyAccepted"
REQ_NOTIFY_REJECTED = "notifyRejected"
REQ_NOTIFY_SHOWN = "notifyShown"
REQ_RECORD_TELEMETRY_CONSENT = "recordTelemetryConsent"
REQ_SET_EDITOR_INFO = "setEditorInfo"
REQ_SIGN_IN_CONFIRM = "signInConfirm"
REQ_SIGN_IN_INITIATE = "signInInitiate"
REQ_SIGN_IN_WITH_GITHUB_TOKEN = "signInWithGithubToken"
REQ_SIGN_OUT = "signOut"

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

# --------------------- #
# Copilot notifications #
# --------------------- #

NTFY_FEATURE_FLAGS_NOTIFICATION = "featureFlagsNotification"
NTFY_LOG_MESSAGE = "LogMessage"
NTFY_PANEL_SOLUTION = "PanelSolution"
NTFY_PANEL_SOLUTION_DONE = "PanelSolutionsDone"
NTFY_PROGRESS = "$/progress"
NTFY_STATUS_NOTIFICATION = "statusNotification"
