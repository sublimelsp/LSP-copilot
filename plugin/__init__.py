from __future__ import annotations

from .client import CopilotPlugin
from .commands import CopilotAcceptCompletionCommand
from .commands import CopilotAcceptPanelCompletionCommand
from .commands import CopilotAcceptPanelCompletionShimCommand
from .commands import CopilotAskCompletionsCommand
from .commands import CopilotCheckFileStatusCommand
from .commands import CopilotCheckStatusCommand
from .commands import CopilotClosePanelCompletionCommand
from .commands import CopilotConversationAgentsCommand
from .commands import CopilotConversationChatCommand
from .commands import CopilotConversationChatShimCommand
from .commands import CopilotConversationCloseCommand
from .commands import CopilotConversationCopyCodeCommand
from .commands import CopilotConversationDebugCommand
from .commands import CopilotConversationDestroyCommand
from .commands import CopilotConversationDestroyShimCommand
from .commands import CopilotConversationInsertCodeCommand
from .commands import CopilotConversationInsertCodeShimCommand
from .commands import CopilotConversationRatingCommand
from .commands import CopilotConversationRatingShimCommand
from .commands import CopilotConversationTemplatesCommand
from .commands import CopilotConversationToggleReferencesBlockCommand
from .commands import CopilotConversationTurnDeleteCommand
from .commands import CopilotConversationTurnDeleteShimCommand
from .commands import CopilotGetPanelCompletionsCommand
from .commands import CopilotGetPromptCommand
from .commands import CopilotGetVersionCommand
from .commands import CopilotNextCompletionCommand
from .commands import CopilotPrepareAndEditSettingsCommand
from .commands import CopilotPreviousCompletionCommand
from .commands import CopilotRejectCompletionCommand
from .commands import CopilotSendAnyRequestCommand
from .commands import CopilotSignInCommand
from .commands import CopilotSignInWithGithubTokenCommand
from .commands import CopilotSignOutCommand
from .commands import CopilotToggleConversationChatCommand
from .constants import SERVER_VERSION
from .helpers import CopilotIgnore
from .listeners import copilot_ignore_observer
from .listeners import EventListener
from .listeners import ViewEventListener
from .utils import all_windows
from .version_manager import version_manager
from LSP.plugin import register_plugin
from LSP.plugin import unregister_plugin

__all__ = (
    # ST: core
    "plugin_loaded",
    "plugin_unloaded",
    # ST: commands
    "CopilotAcceptCompletionCommand",
    "CopilotAcceptPanelCompletionCommand",
    "CopilotAcceptPanelCompletionShimCommand",
    "CopilotAskCompletionsCommand",
    "CopilotCheckFileStatusCommand",
    "CopilotCheckStatusCommand",
    "CopilotClosePanelCompletionCommand",
    "CopilotConversationAgentsCommand",
    "CopilotConversationChatCommand",
    "CopilotConversationChatShimCommand",
    "CopilotConversationCloseCommand",
    "CopilotConversationCopyCodeCommand",
    "CopilotConversationDebugCommand",
    "CopilotConversationDestroyCommand",
    "CopilotConversationDestroyShimCommand",
    "CopilotConversationInsertCodeCommand",
    "CopilotConversationInsertCodeShimCommand",
    "CopilotConversationRatingCommand",
    "CopilotConversationRatingShimCommand",
    "CopilotConversationTemplatesCommand",
    "CopilotConversationToggleReferencesBlockCommand",
    "CopilotConversationTurnDeleteCommand",
    "CopilotConversationTurnDeleteShimCommand",
    "CopilotGetPanelCompletionsCommand",
    "CopilotGetPromptCommand",
    "CopilotGetVersionCommand",
    "CopilotNextCompletionCommand",
    "CopilotPreviousCompletionCommand",
    "CopilotRejectCompletionCommand",
    "CopilotSendAnyRequestCommand",
    "CopilotSignInCommand",
    "CopilotSignInWithGithubTokenCommand",
    "CopilotSignOutCommand",
    "CopilotToggleConversationChatCommand",
    # ST: helper commands
    "CopilotPrepareAndEditSettingsCommand",
    # ST: event listeners
    "EventListener",
    "ViewEventListener",
)


def plugin_loaded() -> None:
    """Executed when this plugin is loaded."""
    register_plugin(CopilotPlugin)
    copilot_ignore_observer.setup()
    for window in all_windows():
        CopilotIgnore(window).load_patterns()

    version_manager.client_cls = CopilotPlugin
    version_manager.server_version = SERVER_VERSION


def plugin_unloaded() -> None:
    """Executed when this plugin is unloaded."""
    CopilotPlugin.cleanup()
    CopilotIgnore.cleanup()
    copilot_ignore_observer.cleanup()
    unregister_plugin(CopilotPlugin)
