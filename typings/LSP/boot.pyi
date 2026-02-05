import sublime
import sublime_plugin
from .plugin.code_actions import LspCodeActionsCommand as LspCodeActionsCommand, LspRefactorCommand as LspRefactorCommand, LspSourceActionCommand as LspSourceActionCommand
from .plugin.code_lens import LspCodeLensCommand as LspCodeLensCommand, LspToggleCodeLensesCommand as LspToggleCodeLensesCommand
from .plugin.color import LspColorPresentationCommand as LspColorPresentationCommand
from .plugin.completion import LspCommitCompletionWithOppositeInsertMode as LspCommitCompletionWithOppositeInsertMode, LspResolveDocsCommand as LspResolveDocsCommand, LspSelectCompletionCommand as LspSelectCompletionCommand
from .plugin.configuration import LspDisableLanguageServerGloballyCommand as LspDisableLanguageServerGloballyCommand, LspDisableLanguageServerInProjectCommand as LspDisableLanguageServerInProjectCommand, LspEnableLanguageServerGloballyCommand as LspEnableLanguageServerGloballyCommand, LspEnableLanguageServerInProjectCommand as LspEnableLanguageServerInProjectCommand
from .plugin.core.registry import LspCheckApplicableCommand as LspCheckApplicableCommand, LspNextDiagnosticCommand as LspNextDiagnosticCommand, LspOpenLocationCommand as LspOpenLocationCommand, LspPrevDiagnosticCommand as LspPrevDiagnosticCommand, LspRestartServerCommand as LspRestartServerCommand
from .plugin.core.signature_help import LspSignatureHelpNavigateCommand as LspSignatureHelpNavigateCommand, LspSignatureHelpShowCommand as LspSignatureHelpShowCommand
from .plugin.core.tree_view import LspCollapseTreeItemCommand as LspCollapseTreeItemCommand, LspExpandTreeItemCommand as LspExpandTreeItemCommand
from .plugin.core.views import LspRunTextCommandHelperCommand as LspRunTextCommandHelperCommand
from .plugin.document_link import LspOpenLinkCommand as LspOpenLinkCommand
from .plugin.documents import DocumentSyncListener as DocumentSyncListener, TextChangeListener as TextChangeListener
from .plugin.edit import LspApplyDocumentEditCommand as LspApplyDocumentEditCommand, LspApplyWorkspaceEditCommand as LspApplyWorkspaceEditCommand, LspConcludeWorkspaceEditPanelCommand as LspConcludeWorkspaceEditPanelCommand
from .plugin.execute_command import LspExecuteCommand as LspExecuteCommand
from .plugin.folding_range import LspFoldAllCommand as LspFoldAllCommand, LspFoldCommand as LspFoldCommand
from .plugin.formatting import LspFormatCommand as LspFormatCommand, LspFormatDocumentCommand as LspFormatDocumentCommand, LspFormatDocumentRangeCommand as LspFormatDocumentRangeCommand
from .plugin.goto import LspGotoDiagnosticCommand as LspGotoDiagnosticCommand, LspSymbolDeclarationCommand as LspSymbolDeclarationCommand, LspSymbolDefinitionCommand as LspSymbolDefinitionCommand, LspSymbolImplementationCommand as LspSymbolImplementationCommand, LspSymbolTypeDefinitionCommand as LspSymbolTypeDefinitionCommand
from .plugin.hierarchy import LspCallHierarchyCommand as LspCallHierarchyCommand, LspHierarchyToggleCommand as LspHierarchyToggleCommand, LspTypeHierarchyCommand as LspTypeHierarchyCommand
from .plugin.hover import LspCopyTextCommand as LspCopyTextCommand, LspHoverCommand as LspHoverCommand, LspToggleHoverPopupsCommand as LspToggleHoverPopupsCommand
from .plugin.inlay_hint import LspInlayHintClickCommand as LspInlayHintClickCommand, LspToggleInlayHintsCommand as LspToggleInlayHintsCommand
from .plugin.panels import LspClearLogPanelCommand as LspClearLogPanelCommand, LspClearPanelCommand as LspClearPanelCommand, LspShowDiagnosticsPanelCommand as LspShowDiagnosticsPanelCommand, LspToggleLogPanelLinesLimitCommand as LspToggleLogPanelLinesLimitCommand, LspToggleServerPanelCommand as LspToggleServerPanelCommand, LspUpdateLogPanelCommand as LspUpdateLogPanelCommand, LspUpdatePanelCommand as LspUpdatePanelCommand
from .plugin.references import LspSymbolReferencesCommand as LspSymbolReferencesCommand
from .plugin.rename import LspSymbolRenameCommand as LspSymbolRenameCommand
from .plugin.rename_file import LspRenamePathCommand as LspRenamePathCommand
from .plugin.save_command import LspSaveAllCommand as LspSaveAllCommand, LspSaveCommand as LspSaveCommand
from .plugin.selection_range import LspExpandSelectionCommand as LspExpandSelectionCommand
from .plugin.semantic_highlighting import LspShowScopeNameCommand as LspShowScopeNameCommand
from .plugin.symbols import LspDocumentSymbolsCommand as LspDocumentSymbolsCommand, LspSelectionAddCommand as LspSelectionAddCommand, LspSelectionClearCommand as LspSelectionClearCommand, LspSelectionSetCommand as LspSelectionSetCommand, LspWorkspaceSymbolsCommand as LspWorkspaceSymbolsCommand
from .plugin.tooling import LspCopyToClipboardFromBase64Command as LspCopyToClipboardFromBase64Command, LspDumpBufferCapabilities as LspDumpBufferCapabilities, LspDumpWindowConfigs as LspDumpWindowConfigs, LspOnDoubleClickCommand as LspOnDoubleClickCommand, LspParseVscodePackageJson as LspParseVscodePackageJson, LspTroubleshootServerCommand as LspTroubleshootServerCommand
from typing import Any

__all__ = ['DocumentSyncListener', 'Listener', 'LspApplyDocumentEditCommand', 'LspApplyWorkspaceEditCommand', 'LspCallHierarchyCommand', 'LspCheckApplicableCommand', 'LspClearLogPanelCommand', 'LspClearPanelCommand', 'LspCodeActionsCommand', 'LspCodeLensCommand', 'LspCollapseTreeItemCommand', 'LspColorPresentationCommand', 'LspCommitCompletionWithOppositeInsertMode', 'LspConcludeWorkspaceEditPanelCommand', 'LspCopyTextCommand', 'LspCopyToClipboardFromBase64Command', 'LspDisableLanguageServerGloballyCommand', 'LspDisableLanguageServerInProjectCommand', 'LspDocumentSymbolsCommand', 'LspDumpBufferCapabilities', 'LspDumpWindowConfigs', 'LspEnableLanguageServerGloballyCommand', 'LspEnableLanguageServerInProjectCommand', 'LspExecuteCommand', 'LspExpandSelectionCommand', 'LspExpandTreeItemCommand', 'LspFoldAllCommand', 'LspFoldCommand', 'LspFormatCommand', 'LspFormatDocumentCommand', 'LspFormatDocumentRangeCommand', 'LspGotoDiagnosticCommand', 'LspHierarchyToggleCommand', 'LspHoverCommand', 'LspInlayHintClickCommand', 'LspNextDiagnosticCommand', 'LspOnDoubleClickCommand', 'LspOpenLinkCommand', 'LspOpenLocationCommand', 'LspParseVscodePackageJson', 'LspPrevDiagnosticCommand', 'LspRefactorCommand', 'LspRenamePathCommand', 'LspResolveDocsCommand', 'LspRestartServerCommand', 'LspRunTextCommandHelperCommand', 'LspSaveAllCommand', 'LspSaveCommand', 'LspSelectCompletionCommand', 'LspSelectionAddCommand', 'LspSelectionClearCommand', 'LspSelectionSetCommand', 'LspShowDiagnosticsPanelCommand', 'LspShowScopeNameCommand', 'LspSignatureHelpNavigateCommand', 'LspSignatureHelpShowCommand', 'LspSourceActionCommand', 'LspSymbolDeclarationCommand', 'LspSymbolDefinitionCommand', 'LspSymbolImplementationCommand', 'LspSymbolReferencesCommand', 'LspSymbolRenameCommand', 'LspSymbolTypeDefinitionCommand', 'LspToggleCodeLensesCommand', 'LspToggleHoverPopupsCommand', 'LspToggleInlayHintsCommand', 'LspToggleLogPanelLinesLimitCommand', 'LspToggleServerPanelCommand', 'LspTroubleshootServerCommand', 'LspTypeHierarchyCommand', 'LspUpdateLogPanelCommand', 'LspUpdatePanelCommand', 'LspWorkspaceSymbolsCommand', 'TextChangeListener', 'plugin_loaded', 'plugin_unloaded']

def plugin_loaded() -> None: ...
def plugin_unloaded() -> None: ...

class Listener(sublime_plugin.EventListener):
    def on_exit(self) -> None: ...
    def on_load_project_async(self, window: sublime.Window) -> None: ...
    def on_post_save_project_async(self, window: sublime.Window) -> None: ...
    def on_new_window_async(self, window: sublime.Window) -> None: ...
    def on_pre_close_window(self, window: sublime.Window) -> None: ...
    def on_pre_move(self, view: sublime.View) -> None: ...
    def on_load(self, view: sublime.View) -> None: ...
    def on_pre_close(self, view: sublime.View) -> None: ...
    def on_window_command(self, window: sublime.Window, command_name: str, args: dict[str, Any]) -> tuple[str, dict[str, Any]] | None: ...
    def on_post_window_command(self, window: sublime.Window, command_name: str, args: dict[str, Any] | None) -> None: ...
