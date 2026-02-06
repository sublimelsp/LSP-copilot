# TODO
# e.set("context/registerProviders", RGe),
# e.set("context/unregisterProviders", Uje),
# e.set("conversation/registerTools", BWe),
# e.set("copilot/codeReview", LWe),
# e.set("git/commitGenerate", yGe),
# e.set("editConversation/create", MWe),
# e.set("editConversation/turn", OWe),
# e.set("editConversation/turnDelete", UWe),
# e.set("editConversation/destroy", QWe),
# e.set("mcp/getTools", qWe),
# e.set("mcp/updateToolsStatus", WWe),

from __future__ import annotations

import json
import os
import uuid
from abc import ABC
from collections.abc import Callable
from functools import partial, wraps
from pathlib import Path
from typing import Any, Literal, Sequence, cast

import mdpopups
import sublime
import sublime_plugin
from LSP.plugin import Request, Session
from LSP.plugin.core.registry import LspTextCommand, LspWindowCommand
from LSP.plugin.core.url import filename_to_uri
from lsp_utils.helpers import rmtree_ex

from .client import CopilotPlugin
from .constants import (
    COPILOT_OUTPUT_PANEL_PREFIX,
    PACKAGE_NAME,
    REQ_CHECK_STATUS,
    REQ_CONVERSATION_AGENTS,
    REQ_CONVERSATION_CREATE,
    REQ_CONVERSATION_DESTROY,
    REQ_CONVERSATION_PRECONDITIONS,
    REQ_CONVERSATION_RATING,
    REQ_CONVERSATION_REGISTER_TOOLS,
    REQ_CONVERSATION_TEMPLATES,
    REQ_CONVERSATION_TURN,
    REQ_CONVERSATION_TURN_DELETE,
    REQ_COPILOT_CODE_REVIEW,
    REQ_COPILOT_MODELS,
    REQ_COPILOT_SET_MODEL_POLICY,
    REQ_EDIT_CONVERSATION_CREATE,
    REQ_EDIT_CONVERSATION_DESTROY,
    REQ_EDIT_CONVERSATION_TURN,
    REQ_EDIT_CONVERSATION_TURN_DELETE,
    REQ_FILE_CHECK_STATUS,
    REQ_GET_PANEL_COMPLETIONS,
    REQ_GET_PROMPT,
    REQ_GET_VERSION,
    REQ_GIT_COMMIT_GENERATE,
    REQ_INLINE_COMPLETION,
    REQ_INLINE_COMPLETION_PROMPT,
    REQ_NOTIFY_ACCEPTED,
    REQ_NOTIFY_REJECTED,
    REQ_SIGN_IN_CONFIRM,
    REQ_SIGN_IN_INITIATE,
    REQ_SIGN_IN_WITH_GITHUB_TOKEN,
    REQ_SIGN_OUT,
)
from .decorators import must_be_active_view
from .helpers import (
    GitHelper,
    GithubInfo,
    prepare_code_review_request_doc,
    prepare_completion_request_doc,
    prepare_conversation_edit_request,
    prepare_conversation_turn_request,
    preprocess_chat_message,
    preprocess_message_for_html,
)
from .log import log_info
from .types import (
    CopilotConversationDebugTemplates,
    CopilotModel,
    CopilotPayloadConversationCreate,
    CopilotPayloadConversationPreconditions,
    CopilotPayloadConversationTemplate,
    CopilotPayloadFileStatus,
    CopilotPayloadGetVersion,
    CopilotPayloadNotifyAccepted,
    CopilotPayloadNotifyRejected,
    CopilotPayloadPanelCompletionSolutionCount,
    CopilotPayloadSignInConfirm,
    CopilotPayloadSignInInitiate,
    CopilotPayloadSignOut,
    CopilotRequestConversationAgent,
    CopilotUserDefinedPromptTemplates,
    T_Callable,
)
from .ui import (
    ViewCompletionManager,
    ViewPanelCompletionManager,
    WindowConversationManager,
    WindowEditConversationManager,
)
from .utils import (
    find_index_by_key_value,
    find_view_by_id,
    find_window_by_id,
    get_session_setting,
    message_dialog,
    mutable_view,
    ok_cancel_dialog,
    status_message,
)

REQUIRE_NOTHING = 0
REQUIRE_SIGN_IN = 1 << 0
REQUIRE_NOT_SIGN_IN = 1 << 1
REQUIRE_AUTHORIZED = 1 << 2


def _provide_plugin_session(*, failed_return: Any = None) -> Callable[[T_Callable], T_Callable]:
    """
    The first argument is always `self` for a decorated method.
    We want to provide `plugin` and `session` right after it. If we failed to find a `session`,
    then it will be early failed and return `failed_return`.
    """

    def decorator(func: T_Callable) -> T_Callable:
        @wraps(func)
        def wrapped(self: Any, *arg, **kwargs) -> Any:
            if not isinstance(self, (LspTextCommand)):
                raise RuntimeError('"_provide_session" decorator is only for LspTextCommand.')

            plugin, session = CopilotPlugin.plugin_session(self.view)
            if not (plugin and session):
                return failed_return

            return func(self, plugin, session, *arg, **kwargs)

        return cast(T_Callable, wrapped)

    return decorator


class CopilotPrepareAndEditSettingsCommand(sublime_plugin.ApplicationCommand):
    def run(self, *, base_file: str, user_file: str, default: str = "") -> None:
        window = sublime.active_window()
        user_file_resolved: str = sublime.expand_variables(user_file, window.extract_variables())  # type: ignore
        Path(user_file_resolved).parent.mkdir(parents=True, exist_ok=True)
        sublime.run_command("edit_settings", {"base_file": base_file, "user_file": user_file, "default": default})


class BaseCopilotCommand(ABC):
    session_name = PACKAGE_NAME
    requirement = REQUIRE_SIGN_IN | REQUIRE_AUTHORIZED

    def _can_meet_requirement(self, session: Session) -> bool:
        if get_session_setting(session, "debug"):
            return True

        account_status = CopilotPlugin.get_account_status()
        return not (
            ((self.requirement & REQUIRE_SIGN_IN) and not account_status.has_signed_in)
            or ((self.requirement & REQUIRE_NOT_SIGN_IN) and account_status.has_signed_in)
            or ((self.requirement & REQUIRE_AUTHORIZED) and not account_status.is_authorized)
        )


class CopilotTextCommand(BaseCopilotCommand, LspTextCommand, ABC):
    def want_event(self) -> bool:
        return False

    def _record_telemetry(
        self,
        session: Session,
        request: str,
        payload: CopilotPayloadNotifyAccepted | CopilotPayloadNotifyRejected,
    ) -> None:
        if not get_session_setting(session, "telemetry"):
            return

        session.send_request(Request(request, payload), lambda _: None)

    @must_be_active_view(failed_return=False)
    @_provide_plugin_session(failed_return=False)
    def is_enabled(self, plugin: CopilotPlugin, session: Session) -> bool:  # type: ignore
        return self._can_meet_requirement(session)


class CopilotWindowCommand(BaseCopilotCommand, LspWindowCommand, ABC):
    def is_enabled(self) -> bool:
        if not (session := self.session()):
            return False
        return self._can_meet_requirement(session)


class CopilotGetVersionCommand(CopilotTextCommand):
    requirement = REQUIRE_NOTHING

    @_provide_plugin_session()
    def run(self, plugin: CopilotPlugin, session: Session, _: sublime.Edit) -> None:
        session.send_request(Request(REQ_GET_VERSION, {}), self._on_result_get_version)

    def _on_result_get_version(self, payload: CopilotPayloadGetVersion) -> None:
        message_dialog(f"Server version: {payload['version']}")


class CopilotAskCompletionsCommand(CopilotTextCommand):
    @_provide_plugin_session()
    def run(self, plugin: CopilotPlugin, session: Session, _: sublime.Edit) -> None:
        plugin.request_get_completions(self.view)


class CopilotInlineCompletionPromptCommand(CopilotTextCommand):
    """Command to get inline completions with a custom prompt/message."""

    @_provide_plugin_session()
    def run(self, plugin: CopilotPlugin, session: Session, _: sublime.Edit, message: str = "") -> None:
        if not (window := self.view.window()):
            return
        # Prompt for message if not provided
        if not message.strip():
            window.show_input_panel(
                "Completion Prompt:",
                "",
                lambda msg: self._request_inline_completion_with_prompt(plugin, session, msg),
                None,
                None,
            )
        else:
            self._request_inline_completion_with_prompt(plugin, session, message)

    def _request_inline_completion_with_prompt(self, plugin: CopilotPlugin, session: Session, message: str) -> None:
        """Send the inline completion request with the custom prompt."""
        if not message.strip():
            status_message("Please provide a message for the completion prompt", icon="❌")
            return

        # Prepare document information
        if not (doc := prepare_completion_request_doc(self.view)):
            status_message("Failed to prepare document for completion request", icon="❌")
            return

        # Get cursor position
        if not (sel := self.view.sel()) or len(sel) != 1:
            status_message("Please place cursor at a single position", icon="❌")
            return

        cursor_point = sel[0].begin()
        row, col = self.view.rowcol(cursor_point)

        # Prepare the request payload based on the structure from constants
        payload = {
            "textDocument": {"uri": doc["uri"]},
            "position": {"line": row, "character": col},
            "formattingOptions": {"tabSize": doc.get("tabSize", 4), "insertSpaces": doc.get("insertSpaces", True)},
            "context": {"triggerKind": 2},
            "data": {"message": message},
        }

        # Send the request
        session.send_request(
            Request(REQ_INLINE_COMPLETION_PROMPT, payload),
            lambda response: self._on_result_inline_completion_prompt(response, message),
        )

        status_message(f"Requesting completion with prompt: {message[:50]}...", icon="⏳")

    def _on_result_inline_completion_prompt(self, response: Any, original_message: str) -> None:
        """Handle the response from the inline completion prompt request."""
        if not (window := self.view.window()):
            return

        if not response:
            status_message("No completion suggestions received", icon="❌")
            return

        # Handle the new response format with items
        if isinstance(response, dict) and "items" in response:
            items = response["items"]
            if not items:
                status_message("No completion items received", icon="❌")
                return

            # Show the completion selection dialog
            window.run_command(
                "copilot_select_inline_completion", {"items": items, "original_message": original_message}
            )
        else:
            # Fallback for other response formats
            status_message(f"Unexpected response format: {type(response)}", icon="❌")


class CopilotInlineCompletionCommand(CopilotTextCommand):
    """Command to get inline completions (automatic trigger)."""

    @_provide_plugin_session()
    def run(self, plugin: CopilotPlugin, session: Session, _: sublime.Edit, message: str = "") -> None:
        if not (window := self.view.window()):
            return

        # Prompt for message if not provided
        if not message.strip():
            window.show_input_panel(
                "Completion Message:", "", lambda msg: self._request_inline_completion(plugin, session, msg), None, None
            )
        else:
            self._request_inline_completion(plugin, session, message)

    def _request_inline_completion(self, plugin: CopilotPlugin, session: Session, message: str) -> None:
        """Send the inline completion request."""
        if not message.strip():
            status_message("Please provide a message for the completion", icon="❌")
            return

        # Prepare document information
        if not (doc := prepare_completion_request_doc(self.view)):
            status_message("Failed to prepare document for completion request", icon="❌")
            return

        # Get cursor position
        if not (sel := self.view.sel()) or len(sel) != 1:
            status_message("Please place cursor at a single position", icon="❌")
            return

        cursor_point = sel[0].begin()
        row, col = self.view.rowcol(cursor_point)

        # Prepare the request payload - same as prompt but with triggerKind: 1
        payload = {
            "textDocument": {"uri": doc["uri"]},
            "position": {"line": row, "character": col},
            "formattingOptions": {"tabSize": doc.get("tabSize", 4), "insertSpaces": doc.get("insertSpaces", True)},
            "context": {
                "triggerKind": 1  # Different from prompt command which uses 2
            },
            "data": {"message": message},
        }

        # Send the request
        session.send_request(
            Request(REQ_INLINE_COMPLETION, payload),
            lambda response: self._on_result_inline_completion(response, message),
        )

        status_message(f"Requesting inline completion: {message[:50]}...", icon="⏳")

    def _on_result_inline_completion(self, response: Any, original_message: str) -> None:
        """Handle the response from the inline completion request."""
        if not (window := self.view.window()):
            return

        if not response:
            status_message("No completion suggestions received", icon="❌")
            return

        # Handle the new response format with items
        if isinstance(response, dict) and "items" in response:
            items = response["items"]
            if not items:
                status_message("No completion items received", icon="❌")
                return

            # Store the completion items for the input handler
            self._completion_items = items
            self._original_message = original_message

            # Show the completion selection dialog
            window.run_command(
                "copilot_select_inline_completion", {"items": items, "original_message": original_message}
            )
        else:
            # Fallback for other response formats
            status_message(f"Unexpected response format: {type(response)}", icon="❌")


class CopilotSelectInlineCompletionCommand(CopilotTextCommand):
    """Command to select and insert an inline completion from a list."""

    def run(
        self,
        edit: sublime.Edit,
        selected: int,
        items: list[dict[str, Any]],
        original_message: str,
        selected_item: dict[str, Any] | None = None,
    ) -> None:
        if selected_item:
            # Insert the selected completion
            insert_text = selected_item.get("insertText", "")
            if insert_text:
                # Get the range where to insert
                if "range" in selected_item:
                    range_data = selected_item["range"]
                    start_line = range_data["start"]["line"]
                    start_char = range_data["start"]["character"]
                    end_line = range_data["end"]["line"]
                    end_char = range_data["end"]["character"]

                    # Convert to Sublime Text points
                    start_point = self.view.text_point(start_line, start_char)
                    end_point = self.view.text_point(end_line, end_char)

                    # Replace the range with the completion
                    self.view.replace(edit, sublime.Region(start_point, end_point), insert_text)
                else:
                    # Insert at current cursor position
                    if sel := self.view.sel():
                        self.view.insert(edit, sel[0].begin(), insert_text)

                status_message(f"Inserted completion for: {original_message[:30]}...", icon="✅")

                # Handle acceptance command if present
                if "command" in selected_item and selected_item["command"]:
                    cmd = selected_item["command"]
                    if cmd.get("command") == "github.copilot.didAcceptCompletionItem":
                        # Send acceptance notification to Copilot
                        args = cmd.get("arguments", [])
                        if args:
                            # This would typically be handled by the LSP client
                            # For now, we'll just log it
                            print(f"Copilot completion accepted: {args[0]}")
            else:
                status_message("Selected completion has no text", icon="❌")

    def input(self, args: dict[str, Any]) -> sublime_plugin.CommandInputHandler | None:
        items = args.get("items", [])
        original_message = args.get("original_message", "")

        if not items:
            return None

        return CopilotInlineCompletionInputHandler(items, original_message)


class CopilotInlineCompletionInputHandler(sublime_plugin.ListInputHandler):
    """Input handler for selecting inline completions."""

    def __init__(self, items: list[dict[str, Any]], original_message: str):
        self.items = items
        self.original_message = original_message

    def name(self) -> str:
        return "selected_item"

    def placeholder(self) -> str:
        return f"Select completion for: {self.original_message[:50]}..."

    def list_items(self) -> list[sublime.ListInputItem]:  # type: ignore
        list_items: list[sublime.ListInputItem] = []
        for i, item in enumerate(self.items):
            insert_text = item.get("insertText", "")

            # Create preview using mdpopups to convert markdown to HTML
            if insert_text:
                # Detect language for syntax highlighting
                # This is a simple heuristic - you might want to improve this
                language = self._detect_language(insert_text)
                markdown_text = f"```{language}\n{insert_text}\n```"

                # Convert markdown to HTML using mdpopups
                try:
                    html_details = mdpopups.md2html(None, markdown_text)
                except Exception:
                    # Fallback to plain text if markdown conversion fails
                    html_details = f"<pre>{insert_text}</pre>"

                # Create a short preview for the main text
                preview = insert_text.strip().split("\n")[0]
                if len(preview) > 60:
                    preview = preview[:57] + "..."

                # Add line count annotation
                line_count = len(insert_text.split("\n"))
                annotation = f"{line_count} line{'s' if line_count != 1 else ''}"

                list_items.append(
                    sublime.ListInputItem(
                        text=preview, value=item, details=html_details, annotation=annotation, kind=sublime.KIND_SNIPPET
                    )
                )
            else:
                list_items.append(
                    sublime.ListInputItem(
                        text=f"Completion {i + 1}",
                        value=item,
                        details="<em>No preview available</em>",
                        annotation="",
                        kind=sublime.KIND_SNIPPET,
                    )
                )

        return list_items

    def _detect_language(self, text: str) -> str:
        """Simple language detection based on content."""
        text_lower = text.lower().strip()

        # Python
        if any(keyword in text_lower for keyword in ["def ", "import ", "from ", "class ", "if __name__"]):
            return "python"

        # JavaScript/TypeScript
        if any(keyword in text_lower for keyword in ["function ", "const ", "let ", "var ", "=>", "console.log"]):
            return "javascript"

        # HTML
        if text_lower.startswith("<") and ">" in text_lower:
            return "html"

        # CSS
        if "{" in text and "}" in text and ":" in text:
            return "css"

        # JSON
        if text.strip().startswith("{") and text.strip().endswith("}"):
            return "json"

        # Default to text
        return "text"


class CopilotAcceptPanelCompletionShimCommand(CopilotWindowCommand):
    def run(self, view_id: int, completion_index: int) -> None:
        if not (view := find_view_by_id(view_id)):
            return
        # Focus the view so that the command runs
        self.window.focus_view(view)
        view.run_command("copilot_accept_panel_completion", {"completion_index": completion_index})


class CopilotAcceptPanelCompletionCommand(CopilotTextCommand):
    def run(self, edit: sublime.Edit, completion_index: int) -> None:
        vcm = ViewPanelCompletionManager(self.view)
        if not (completion := vcm.get_completion(completion_index)):
            return

        # it seems that `completionText` always assume your cursor is at the end of the line
        source_line_region = self.view.line(sublime.Region(*completion["region"]))
        self.view.insert(edit, source_line_region.end(), completion["completionText"])
        self.view.show(self.view.sel(), show_surrounds=False, animate=self.view.settings().get("animation_enabled"))

        vcm.close()


class CopilotClosePanelCompletionCommand(CopilotWindowCommand):
    def run(self, view_id: int | None = None) -> None:
        if view_id is None:
            view = self.window.active_view()
        else:
            view = find_view_by_id(view_id)

        if not view:
            return

        ViewPanelCompletionManager(view).close()


class CopilotConversationChatShimCommand(CopilotWindowCommand):
    def run(self, window_id: int, message: str = "") -> None:
        if not (window := find_window_by_id(window_id)):
            return

        wcm = WindowConversationManager(window)
        if not (view := find_view_by_id(wcm.last_active_view_id)):
            return

        # Focus the view so that the command runs
        self.window.focus_view(view)
        view.run_command("copilot_conversation_chat", {"message": message})


class CopilotToggleConversationChatCommand(CopilotWindowCommand):
    def run(self) -> None:
        if not (wcm := WindowConversationManager(self.window)):
            return

        if wcm.is_visible:
            wcm.close()
        elif view := self.window.active_view():
            view.run_command("copilot_conversation_chat")


class CopilotConversationChatCommand(CopilotTextCommand):
    @_provide_plugin_session()
    def run(self, plugin: CopilotPlugin, session: Session, _: sublime.Edit, message: str = "") -> None:
        if not (window := self.view.window()):
            return

        wcm = WindowConversationManager(window)
        if wcm.conversation_id:
            wcm.open()
            wcm.prompt(callback=lambda msg: self._on_prompt(plugin, session, msg), initial_text=message)
            return

        session.send_request(
            Request(
                REQ_CONVERSATION_PRECONDITIONS,
                {},
            ),
            lambda response: self._on_result_conversation_preconditions(plugin, session, response, message),
        )

    def _on_result_conversation_preconditions(
        self,
        plugin: CopilotPlugin,
        session: Session,
        payload: CopilotPayloadConversationPreconditions,
        initial_message: str,
    ) -> None:
        if not (window := self.view.window()):
            return

        wcm = WindowConversationManager(window)
        if not (view := find_view_by_id(wcm.last_active_view_id)):
            return

        user_prompts: list[CopilotUserDefinedPromptTemplates] = session.config.settings.get("prompts") or []
        is_template, msg = preprocess_chat_message(view, initial_message, user_prompts)
        if msg:
            wcm.append_conversation_entry({
                "kind": plugin.get_account_status().user or "user",
                "conversationId": wcm.conversation_id,
                "reply": msg.split()[0] if is_template else preprocess_message_for_html(msg),
                "turnId": str(uuid.uuid4()),
                "references": [],
                "annotations": [],
                "hideText": False,
                "warnings": [],
            })
        session.send_request(
            Request(
                REQ_CONVERSATION_CREATE,
                {
                    "turns": [{"request": msg}],
                    "capabilities": {
                        "allSkills": True,
                        "skills": [],
                    },
                    "workDoneToken": f"copilot_chat://{window.id()}",
                    "computeSuggestions": True,
                    "source": "panel",
                },
            ),
            lambda msg: self._on_result_conversation_create(plugin, session, msg),
        )
        wcm.is_waiting = True
        wcm.update()

    def _on_result_conversation_create(
        self,
        plugin: CopilotPlugin,
        session: Session,
        payload: CopilotPayloadConversationCreate,
    ) -> None:
        if not (window := self.view.window()):
            return

        wcm = WindowConversationManager(window)
        wcm.conversation_id = payload["conversationId"]
        wcm.open()
        wcm.prompt(callback=lambda msg: self._on_prompt(plugin, session, msg))

    def _on_prompt(self, plugin: CopilotPlugin, session: Session, msg: str):
        if not (window := self.view.window()):
            return

        wcm = WindowConversationManager(window)
        if wcm.is_waiting:
            wcm.prompt(callback=lambda x: self._on_prompt(plugin, session, x), initial_text=msg)
            return

        if not (view := find_view_by_id(wcm.last_active_view_id)):
            return
        user_prompts: list[CopilotUserDefinedPromptTemplates] = session.config.settings.get("prompts") or []
        is_template, msg = preprocess_chat_message(view, msg, user_prompts)
        views = [sv.view for sv in session.session_views_async() if sv.view.id() != view.id()]
        if not (request := prepare_conversation_turn_request(wcm.conversation_id, wcm.window.id(), msg, view, views)):
            return

        wcm.append_conversation_entry({
            "kind": plugin.get_account_status().user or "user",
            "conversationId": wcm.conversation_id,
            "reply": msg.split()[0] if is_template else preprocess_message_for_html(msg),
            "turnId": str(uuid.uuid4()),
            "references": request["references"],
            "annotations": [],
            "hideText": False,
            "warnings": [],
        })
        session.send_request(
            Request(REQ_CONVERSATION_TURN, request),
            lambda _: wcm.prompt(callback=lambda x: self._on_prompt(plugin, session, x)),
        )
        wcm.is_waiting = True
        wcm.update()


class CopilotConversationCloseCommand(CopilotWindowCommand):
    def run(self, window_id: int | None = None) -> None:
        if not window_id:
            return
        if not (window := find_window_by_id(window_id)):
            return

        WindowConversationManager(window).close()


class CopilotConversationRatingShimCommand(CopilotWindowCommand):
    def run(self, turn_id: str, rating: int) -> None:
        wcm = WindowConversationManager(self.window)
        if not (view := find_view_by_id(wcm.last_active_view_id)):
            return
        # Focus the view so that the command runs
        self.window.focus_view(view)
        view.run_command("copilot_conversation_rating", {"turn_id": turn_id, "rating": rating})


class CopilotConversationRatingCommand(CopilotTextCommand):
    @_provide_plugin_session()
    def run(self, plugin: CopilotPlugin, session: Session, _: sublime.Edit, turn_id: str, rating: int) -> None:
        session.send_request(
            Request(
                REQ_CONVERSATION_RATING,
                {
                    "turnId": turn_id,
                    "rating": rating,
                },
            ),
            self._on_result_conversation_rating,
        )

    def _on_result_conversation_rating(self, payload: Literal["OK"]) -> None:
        # Returns OK
        pass

    def is_enabled(self, event: dict[Any, Any] | None = None, point: int | None = None) -> bool:  # type: ignore
        return True


class CopilotConversationDestroyShimCommand(CopilotWindowCommand):
    def run(self, conversation_id: str) -> None:
        wcm = WindowConversationManager(self.window)
        if not (view := find_view_by_id(wcm.last_active_view_id)):
            status_message("Failed to find last active view.")
            return
        # Focus the view so that the command runs
        self.window.focus_view(view)
        view.run_command("copilot_conversation_destroy", {"conversation_id": conversation_id})


class CopilotConversationDestroyCommand(CopilotTextCommand):
    @_provide_plugin_session()
    def run(self, plugin: CopilotPlugin, session: Session, _: sublime.Edit, conversation_id: str) -> None:
        if not (
            (window := self.view.window())
            and (wcm := WindowConversationManager(window))
            and wcm.conversation_id == conversation_id
        ):
            status_message("Failed to find window or conversation.")
            return

        session.send_request(
            Request(
                REQ_CONVERSATION_DESTROY,
                {
                    "conversationId": conversation_id,
                    "options": {},
                },
            ),
            self._on_result_conversation_destroy,
        )

    def _on_result_conversation_destroy(self, payload: str) -> None:
        if not (window := self.view.window()):
            status_message("Failed to find window")
            return
        if payload != "OK":
            status_message("Failed to destroy conversation.")
            return

        status_message("Destroyed conversation.")
        wcm = WindowConversationManager(window)
        wcm.close()
        wcm.reset()

    def is_enabled(self, event: dict[Any, Any] | None = None, point: int | None = None) -> bool:  # type: ignore
        if not (window := self.view.window()):
            return False
        return bool(WindowConversationManager(window).conversation_id)


class CopilotConversationToggleReferencesBlockCommand(CopilotWindowCommand):
    def run(self, window_id: int, conversation_id: str, turn_id: str) -> None:
        wcm = WindowConversationManager(self.window)
        if conversation_id != wcm.conversation_id:
            return

        wcm.toggle_references_block(turn_id)
        wcm.update()


class CopilotConversationTurnDeleteShimCommand(CopilotWindowCommand):
    def run(self, window_id: int, conversation_id: str, turn_id: str) -> None:
        wcm = WindowConversationManager(self.window)
        if not (view := find_view_by_id(wcm.last_active_view_id)):
            return
        # Focus the view so that the command runs
        self.window.focus_view(view)
        view.run_command(
            "copilot_conversation_turn_delete",
            {"window_id": window_id, "conversation_id": conversation_id, "turn_id": turn_id},
        )


class CopilotConversationTurnDeleteCommand(CopilotTextCommand):
    @_provide_plugin_session()
    def run(
        self,
        plugin: CopilotPlugin,
        session: Session,
        _: sublime.Edit,
        window_id: int,
        conversation_id: str,
        turn_id: str,
    ) -> None:
        if not (window := find_window_by_id(window_id)):
            return

        wcm = WindowConversationManager(window)
        if wcm.conversation_id != conversation_id:
            return

        # Fixes: https://github.com/TerminalFi/LSP-copilot/issues/181
        index = find_index_by_key_value(wcm.conversation, "turnId", turn_id) + 1
        if index >= len(wcm.conversation):
            return
        retrieved_turn_id = wcm.conversation[index]["turnId"]

        session.send_request(
            Request(
                REQ_CONVERSATION_TURN_DELETE,
                {
                    "conversationId": conversation_id,
                    "turnId": retrieved_turn_id,
                    "options": {},
                },
            ),
            lambda x: self._on_result_conversation_turn_delete(window_id, conversation_id, turn_id, x),
        )

    def _on_result_conversation_turn_delete(
        self,
        window_id: int,
        conversation_id: str,
        turn_id: str,
        payload: str,
    ) -> None:
        if payload != "OK":
            status_message("Failed to delete turn.")
            return

        if not (window := find_window_by_id(window_id)):
            return

        wcm = WindowConversationManager(window)
        if wcm.conversation_id != conversation_id:
            return

        index = find_index_by_key_value(wcm.conversation, "turnId", turn_id)
        conversation = wcm.conversation
        del conversation[index:]
        wcm.follow_up = ""
        wcm.conversation = conversation
        wcm.update()

    def is_enabled(self, event: dict[Any, Any] | None = None, point: int | None = None) -> bool:  # type: ignore
        return True


class CopilotConversationCopyCodeCommand(CopilotWindowCommand):
    def run(self, window_id: int, code_block_index: int) -> None:
        if not (window := find_window_by_id(window_id)):
            return

        wcm = WindowConversationManager(window)
        if not (code := wcm.code_block_index.get(str(code_block_index), None)):
            return

        sublime.set_clipboard(code)


class CopilotConversationInsertCodeShimCommand(CopilotWindowCommand):
    def run(self, window_id: int, code_block_index: int) -> None:
        if not (window := find_window_by_id(window_id)):
            status_message(f"Failed to find window based on ID. ({window_id})")
            return

        wcm = WindowConversationManager(window)
        if not (view := find_view_by_id(wcm.last_active_view_id)):
            status_message("Window has no active view")
            return

        if not (code := wcm.code_block_index.get(str(code_block_index), None)):
            status_message(f"Failed to find code based on index. {code_block_index}")
            return

        # Focus the view so that the command runs
        self.window.focus_view(view)
        view.run_command("copilot_conversation_insert_code", {"characters": code})


class CopilotConversationInsertCodeCommand(sublime_plugin.TextCommand):
    def run(self, edit: sublime.Edit, characters: str) -> None:
        if len(self.view.sel()) > 1:
            return

        begin = self.view.sel()[0].begin()
        self.view.erase(edit, self.view.sel()[0])
        self.view.insert(edit, begin, characters)


class CopilotConversationAgentsCommand(CopilotTextCommand):
    @_provide_plugin_session()
    def run(self, plugin: CopilotPlugin, session: Session, _: sublime.Edit) -> None:
        session.send_request(Request(REQ_CONVERSATION_AGENTS, {}), self._on_result_conversation_agents)

    def _on_result_conversation_agents(self, payload: list[CopilotRequestConversationAgent]) -> None:
        if not payload:
            status_message("No conversation agents available", icon="❌")
            return

        window = self.view.window() or sublime.active_window()
        window.show_quick_panel(
            [
                sublime.QuickPanelItem(
                    trigger=agent["slug"],
                    details=agent["name"],
                    annotation=agent["description"],
                )
                for agent in payload
            ],
            lambda index: self._on_agent_selected(index, payload),
        )

    def _on_agent_selected(self, index: int, agents: list[CopilotRequestConversationAgent]) -> None:
        if index == -1:
            return

        # For now, just show detailed info about the selected agent
        agent = agents[index]
        message_dialog(f"Agent: {agent['name']}\nSlug: {agent['slug']}\nDescription: {agent['description']}")


class CopilotRegisterConversationToolsCommand(CopilotTextCommand):
    """Command to register custom tools for Copilot Chat conversations."""

    @_provide_plugin_session()
    def run(self, plugin: CopilotPlugin, session: Session, _: sublime.Edit) -> None:
        # Define tools to register
        tools = [
            {
                "id": "sublime-file-search",
                "name": "Search Files in Sublime",
                "description": "Search for files in the current project or workspace",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "The search query"},
                        "maxResults": {"type": "integer", "description": "Maximum number of results to return"},
                    },
                    "required": ["query"],
                },
            },
            {
                "id": "sublime-text-search",
                "name": "Search Text in Sublime",
                "description": "Search for text content across files in the project",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "The text to search for"},
                        "filePattern": {"type": "string", "description": "Optional file pattern to limit search"},
                    },
                    "required": ["query"],
                },
            },
        ]

        # Send request to register tools
        session.send_request(Request(REQ_CONVERSATION_REGISTER_TOOLS, {"tools": tools}), self._on_result_register_tools)

        status_message("Registering conversation tools...", icon="⏳")

    def _on_result_register_tools(self, payload: Any) -> None:
        if isinstance(payload, dict) and payload.get("status") == "OK":
            status_message("Successfully registered conversation tools", icon="✅")
        else:
            status_message("Failed to register conversation tools", icon="❌")


class CopilotModelsCommand(CopilotTextCommand):
    @_provide_plugin_session()
    def run(self, plugin: CopilotPlugin, session: Session, _: sublime.Edit) -> None:
        session.send_request(Request(REQ_COPILOT_MODELS, {}), self._on_result_copilot_models)

    def _on_result_copilot_models(self, payload: list[CopilotModel]) -> None:
        window = self.view.window() or sublime.active_window()
        window.show_quick_panel(
            [
                sublime.QuickPanelItem(
                    trigger=item["modelFamily"],
                    details=item["modelName"],
                    annotation=", ".join(item["scopes"]),
                )
                for item in payload
            ],
            lambda index: self._set_model_policy(index, payload),
        )

    def _set_model_policy(self, index: int, models: list[CopilotModel]) -> None:
        if index == -1:
            return
        model_name = models[index]["modelFamily"]
        self.view.run_command("copilot_set_model_policy", {"model": model_name, "status": "enabled"})


class CopilotCodeReviewCommand(CopilotTextCommand):
    """Command to perform code review using GitHub Copilot."""

    @_provide_plugin_session()
    def run(self, plugin: CopilotPlugin, session: Session, _: sublime.Edit) -> None:
        if not (window := self.view.window()):
            return

        # Get the file URI for the current view
        file_uri = filename_to_uri(self.view.file_name() or "")
        if not file_uri:
            status_message("Cannot perform code review on an unsaved file", icon="❌")
            return
        doc = prepare_code_review_request_doc(self.view)

        # Send request to perform code review
        session.send_request(
            Request(
                REQ_COPILOT_CODE_REVIEW,
                {
                    "uri": file_uri,
                    "document": doc,
                    "selection": doc["selection"],
                    "source": "command_palette",
                },
            ),
            lambda response: self._on_result_code_review(response, window),
        )

        status_message("Analyzing code...", icon="⏳")

    def _on_result_code_review(self, payload: dict, window: sublime.Window) -> None:
        """Handle the code review response from Copilot."""
        if not payload:
            status_message("Code review failed or returned no results", icon="❌")
            return

        # Create an output panel to show the review results
        panel_name = f"{COPILOT_OUTPUT_PANEL_PREFIX}_code_review"
        panel = window.create_output_panel(panel_name)
        panel.set_read_only(False)
        panel.run_command("append", {"characters": "# GitHub Copilot Code Review\n\n"})

        # Process review comments if available
        if comments := payload.get("comments", []):
            for i, comment in enumerate(comments, 1):
                # Extract comment details
                message = comment.get("message", "No message provided")
                kind = comment.get("kind", "unknown")
                severity = comment.get("severity", "unknown")

                # Format the comment header
                panel.run_command("append", {"characters": f"## Comment {i} ({kind.title()} - {severity.title()})\n\n"})
                panel.run_command("append", {"characters": f"{message}\n\n"})

                # Add line range information if available
                if file_range := comment.get("range"):
                    line_start = file_range.get("start", {}).get("line", 0) + 1
                    line_end = file_range.get("end", {}).get("line", 0) + 1
                    char_start = file_range.get("start", {}).get("character", 0)
                    char_end = file_range.get("end", {}).get("character", 0)

                    if line_start == line_end:
                        panel.run_command(
                            "append",
                            {"characters": f"**Location:** Line {line_start}, characters {char_start}-{char_end}\n\n"},
                        )
                    else:
                        panel.run_command("append", {"characters": f"**Location:** Lines {line_start}-{line_end}\n\n"})

                # Add file information if different from current file
                if uri := comment.get("uri"):
                    import urllib.parse

                    file_path = urllib.parse.unquote(uri.replace("file://", ""))
                    file_name = file_path.split("/")[-1] if "/" in file_path else file_path
                    panel.run_command("append", {"characters": f"**File:** {file_name}\n\n"})

                panel.run_command("append", {"characters": "---\n\n"})
        else:
            panel.run_command("append", {"characters": "No issues found in your code. Great job! ✅\n\n"})

        panel.set_read_only(True)
        window.run_command("show_panel", {"panel": f"output.{panel_name}"})
        status_message("Code review completed", icon="✅")


class CopilotGitCommitGenerateCommand(CopilotTextCommand):
    """Command to generate Git commit messages using GitHub Copilot."""

    @_provide_plugin_session()
    def run(self, plugin: CopilotPlugin, session: Session, _: sublime.Edit) -> None:
        if not (window := self.view.window()):
            return

        # Gather all Git data using GitHelper
        git_data = GitHelper.gather_git_commit_data(self.view)
        if not git_data:
            status_message("Not in a Git repository or no workspace folder found", icon="❌")
            return
        status_message("Generating commit message...", icon="⏳")

        # Send request to generate commit message
        session.send_request(
            Request(REQ_GIT_COMMIT_GENERATE, git_data),
            lambda response: self._on_result_git_commit_generate(response, window),
        )

    def _on_result_git_commit_generate(self, payload: dict, window: sublime.Window) -> None:
        """Handle the git commit message generation response from Copilot."""
        if not payload or not (commit_message := payload.get("commitMessage")):
            status_message("Failed to generate commit message", icon="❌")
            return

        # Create a new view for the commit message
        view = window.new_file()
        view.set_name("Git Commit Message")
        view.set_scratch(True)

        # Insert the generated commit message
        with mutable_view(view) as v:
            v.run_command("append", {"characters": commit_message})

        # Set commit message syntax
        view.assign_syntax("Packages/Git/Git Commit.sublime-syntax")

        status_message("Commit message generated", icon="✅")


class CopilotSetModelPolicyCommand(CopilotTextCommand):
    @_provide_plugin_session()
    def run(self, plugin: CopilotPlugin, session: Session, _: sublime.Edit, model: str, status: str) -> None:
        session.send_request(
            Request(REQ_COPILOT_SET_MODEL_POLICY, {"model": model, "status": status}),
            lambda _: None,
        )


class CopilotGetPromptCommand(CopilotTextCommand):
    @_provide_plugin_session()
    def run(self, plugin: CopilotPlugin, session: Session, _: sublime.Edit) -> None:
        doc = prepare_completion_request_doc(self.view)
        session.send_request(Request(REQ_GET_PROMPT, {"doc": doc}), self._on_result_get_prompt)

    def _on_result_get_prompt(self, payload) -> None:
        if not (window := self.view.window()):
            return
        view = window.create_output_panel(f"{COPILOT_OUTPUT_PANEL_PREFIX}.prompt_view", unlisted=True)
        view.assign_syntax("scope:source.json")

        with mutable_view(view) as view:
            view.run_command("append", {"characters": json.dumps(payload, indent=4)})
        window.run_command("show_panel", {"panel": f"output.{COPILOT_OUTPUT_PANEL_PREFIX}.prompt_view"})


class CopilotConversationTemplatesCommand(CopilotTextCommand):
    @_provide_plugin_session()
    def run(self, plugin: CopilotPlugin, session: Session, _: sublime.Edit) -> None:
        user_prompts: list[CopilotUserDefinedPromptTemplates] = session.config.settings.get("prompts") or []
        session.send_request(
            Request(REQ_CONVERSATION_TEMPLATES, {"options": {}}),
            lambda payload: self._on_result_conversation_templates(user_prompts, payload),
        )

    def _on_result_conversation_templates(
        self,
        user_prompts: list[CopilotUserDefinedPromptTemplates],
        payload: list[CopilotPayloadConversationTemplate],
    ) -> None:
        if not (window := self.view.window()):
            return

        templates = payload + user_prompts
        prompts = [
            [
                item["id"],
                item["description"],
                ", ".join(item["scopes"]) if item.get("scopes") else "chat-panel",
            ]
            for item in templates
        ]
        window.show_quick_panel(
            prompts,
            lambda index: self._on_selected(index, templates),
        )

    def _on_selected(
        self,
        index: int,
        items: list[CopilotPayloadConversationTemplate | CopilotUserDefinedPromptTemplates],
    ) -> None:
        if index == -1:
            return
        self.view.run_command("copilot_conversation_chat", {"message": f"/{items[index]['id']}"})


class CopilotAcceptCompletionCommand(CopilotTextCommand):
    @_provide_plugin_session()
    def run(self, plugin: CopilotPlugin, session: Session, edit: sublime.Edit) -> None:
        if not (vcm := ViewCompletionManager(self.view)).is_visible:
            return

        vcm.hide()
        if not (completion := vcm.current_completion):
            return

        # Remove the current line and then insert full text.
        # We don't have to care whether it's an inline completion or not.
        source_line_region = self.view.line(completion["point"])
        self.view.erase(edit, source_line_region)
        self.view.insert(edit, source_line_region.begin(), completion["text"])
        self.view.show(self.view.sel(), show_surrounds=False, animate=self.view.settings().get("animation_enabled"))

        self._record_telemetry(session, REQ_NOTIFY_ACCEPTED, {"uuid": completion["uuid"]})

        other_uuids = [completion["uuid"] for completion in vcm.completions]
        other_uuids.remove(completion["uuid"])
        if other_uuids:
            self._record_telemetry(session, REQ_NOTIFY_REJECTED, {"uuids": other_uuids})


class CopilotRejectCompletionCommand(CopilotTextCommand):
    @_provide_plugin_session()
    def run(self, plugin: CopilotPlugin, session: Session, _: sublime.Edit) -> None:
        vcm = ViewCompletionManager(self.view)
        vcm.hide()

        self._record_telemetry(
            session,
            REQ_NOTIFY_REJECTED,
            {"uuids": [completion["uuid"] for completion in vcm.completions]},
        )


class CopilotGetPanelCompletionsCommand(CopilotTextCommand):
    @_provide_plugin_session()
    def run(self, plugin: CopilotPlugin, session: Session, _: sublime.Edit) -> None:
        if not (doc := prepare_completion_request_doc(self.view)):
            return

        vcm = ViewPanelCompletionManager(self.view)
        vcm.is_waiting = True
        vcm.is_visible = True
        vcm.completions = []

        params = {"doc": doc, "panelId": vcm.panel_id}
        session.send_request(Request(REQ_GET_PANEL_COMPLETIONS, params), self._on_result_get_panel_completions)

    def _on_result_get_panel_completions(self, payload: CopilotPayloadPanelCompletionSolutionCount) -> None:
        count = payload["solutionCountTarget"]
        status_message(f"retrieving panel completions: {count}")

        ViewPanelCompletionManager(self.view).open(completion_target_count=count)


class CopilotPreviousCompletionCommand(CopilotTextCommand):
    def run(self, _: sublime.Edit) -> None:
        ViewCompletionManager(self.view).show_previous_completion()


class CopilotNextCompletionCommand(CopilotTextCommand):
    def run(self, _: sublime.Edit) -> None:
        ViewCompletionManager(self.view).show_next_completion()


class CopilotCheckStatusCommand(CopilotTextCommand):
    requirement = REQUIRE_NOTHING

    @_provide_plugin_session()
    def run(self, plugin: CopilotPlugin, session: Session, _: sublime.Edit) -> None:
        local_checks = get_session_setting(session, "local_checks")
        session.send_request(Request(REQ_CHECK_STATUS, {"localChecksOnly": local_checks}), self._on_result_check_status)

    def _on_result_check_status(self, payload: CopilotPayloadSignInConfirm | CopilotPayloadSignOut) -> None:
        if not ((user := payload.get("user")) and isinstance(user, str)):
            user = ""

        CopilotPlugin.set_account_status(user=user)
        GithubInfo.update_avatar(user)

        if payload["status"] == "OK":
            CopilotPlugin.set_account_status(signed_in=True, authorized=True)
            message_dialog(f'Signed in and authorized with user "{user}".')
        elif payload["status"] == "MaybeOk":
            CopilotPlugin.set_account_status(signed_in=True, authorized=True)
            message_dialog(f'(localChecksOnly) Signed in and authorized with user "{user}".')
        elif payload["status"] == "NotAuthorized":
            CopilotPlugin.set_account_status(signed_in=True, authorized=False)
            message_dialog("Your GitHub account doesn't subscribe to Copilot.", error=True)
        else:
            CopilotPlugin.set_account_status(signed_in=False, authorized=False)
            message_dialog("You haven't signed in yet.")


class CopilotCheckFileStatusCommand(CopilotTextCommand):
    @_provide_plugin_session()
    def run(self, plugin: CopilotPlugin, session: Session, _: sublime.Edit) -> None:
        file_path = self.view.file_name() or ""
        uri = file_path and filename_to_uri(file_path)
        session.send_request(Request(REQ_FILE_CHECK_STATUS, {"uri": uri}), self._on_result_check_file_status)

    def _on_result_check_file_status(self, payload: CopilotPayloadFileStatus) -> None:
        status_message(f"File is {payload['status']} in session")


class CopilotSignInCommand(CopilotTextCommand):
    requirement = REQUIRE_NOT_SIGN_IN

    @_provide_plugin_session()
    def run(self, plugin: CopilotPlugin, session: Session, _: sublime.Edit) -> None:
        session.send_request(
            Request(REQ_SIGN_IN_INITIATE, {}),
            partial(self._on_result_sign_in_initiate, session),
        )

    def _on_result_sign_in_initiate(
        self,
        session: Session,
        payload: CopilotPayloadSignInConfirm | CopilotPayloadSignInInitiate,
    ) -> None:
        if payload["status"] == "AlreadySignedIn":
            return
        CopilotPlugin.set_account_status(signed_in=False, authorized=False, quiet=True)

        user_code = str(payload.get("userCode", ""))
        verification_uri = str(payload.get("verificationUri", ""))
        if not (user_code and verification_uri):
            return
        sublime.set_clipboard(user_code)
        sublime.run_command("open_url", {"url": verification_uri})
        log_info(f"Sign-in URL: {verification_uri} (User code = {user_code})")
        if not ok_cancel_dialog(
            "The device activation code has been copied."
            + " Please paste it in the popup GitHub page. Press OK when completed."
            + " If you don't see a popup GitHub page, please check Sublime Text's console,"
            + " open the given URL and paste the user code manually.",
        ):
            return
        session.send_request(
            Request(REQ_SIGN_IN_CONFIRM, {"userCode": user_code}),
            self._on_result_sign_in_confirm,
        )

    def _on_result_sign_in_confirm(self, payload: CopilotPayloadSignInConfirm) -> None:
        self.view.run_command("copilot_check_status")


class CopilotSignInWithGithubTokenCommand(CopilotTextCommand):
    requirement = REQUIRE_NOT_SIGN_IN

    @_provide_plugin_session()
    def run(self, plugin: CopilotPlugin, session: Session, _: sublime.Edit) -> None:
        session.send_request(
            Request(REQ_SIGN_IN_INITIATE, {}),
            partial(self._on_result_sign_in_initiate, session),
        )

    def _on_result_sign_in_initiate(
        self,
        session: Session,
        payload: CopilotPayloadSignInConfirm | CopilotPayloadSignInInitiate,
    ) -> None:
        if payload["status"] == "AlreadySignedIn":
            return
        CopilotPlugin.set_account_status(signed_in=False, authorized=False, quiet=True)

        if not (window := self.view.window()):
            return

        window.show_input_panel(
            "Github Username",
            "",
            on_done=lambda username: self._on_select_github_username(session, username),
            on_change=None,
            on_cancel=None,
        )

    def _on_select_github_username(self, session: Session, username: str) -> None:
        if not (window := self.view.window()):
            return

        window.show_input_panel(
            "Github Token",
            "ghu_",
            on_done=lambda token: session.send_request(
                Request(REQ_SIGN_IN_WITH_GITHUB_TOKEN, {"githubToken": token, "user": username}),
                self._on_result_sign_in_confirm,
            ),
            on_change=None,
            on_cancel=None,
        )

    def _on_result_sign_in_confirm(self, payload: CopilotPayloadSignInConfirm) -> None:
        self.view.run_command("copilot_check_status")


class CopilotSignOutCommand(CopilotTextCommand):
    requirement = REQUIRE_SIGN_IN

    @_provide_plugin_session()
    def run(self, plugin: CopilotPlugin, session: Session, _: sublime.Edit) -> None:
        session.send_request(Request(REQ_SIGN_OUT, {}), self._on_result_sign_out)

    def _on_result_sign_out(self, payload: CopilotPayloadSignOut) -> None:
        if sublime.platform() == "windows":
            session_dir = Path(os.environ.get("LOCALAPPDATA", "")) / "github-copilot"
        else:
            session_dir = Path.home() / ".config/github-copilot"

        if not session_dir.is_dir():
            message_dialog(f"Failed to find the session directory: {session_dir}", error=True)
            return

        rmtree_ex(str(session_dir), ignore_errors=True)
        if not session_dir.is_dir():
            CopilotPlugin.set_account_status(signed_in=False, authorized=False, user=None)
            message_dialog("Sign out OK. Bye!")

        GithubInfo.clear_avatar()


class CopilotConversationDebugCommand(CopilotTextCommand):
    @_provide_plugin_session()
    def run(self, plugin: CopilotPlugin, session: Session, _: sublime.Edit) -> None:
        if not (window := self.view.window()):
            return

        templates = tuple(CopilotConversationDebugTemplates)
        window.show_quick_panel(
            [[template.name, template.value] for template in templates],
            lambda index: self._on_selected(index, templates),
        )

    def _on_selected(self, index: int, templates: Sequence[CopilotConversationDebugTemplates]) -> None:
        if index == -1:
            return
        self.view.run_command("copilot_conversation_chat", {"message": f"{templates[index].value}"})


class CopilotSendAnyRequestCommand(CopilotTextCommand):
    @_provide_plugin_session()
    def run(self, plugin: CopilotPlugin, session: Session, _: sublime.Edit, request_type: str, payload: str) -> None:
        try:
            decode_payload = sublime.decode_value(payload)
        except ValueError as e:
            message_dialog(f"Failed to parse payload: {e}", error=True)
            decode_payload = {}
        session.send_request(Request(request_type, decode_payload), self._on_results_any_request)

    def _on_results_any_request(self, payload: Any) -> None:
        print(payload)

    def input(self, args: dict[str, Any]) -> sublime_plugin.CommandInputHandler | None:
        return CopilotSendAnyRequestCommandTextInputHandler()


class CopilotSendAnyRequestCommandTextInputHandler(sublime_plugin.TextInputHandler):
    def placeholder(self) -> str:
        return "Enter type of request. Example: conversation/turn"

    def name(self) -> str:
        return "request_type"

    def next_input(self, args: dict[str, Any]) -> sublime_plugin.CommandInputHandler | None:
        return CopilotSendAnyRequestPayloadInputHandler(args)


class CopilotSendAnyRequestPayloadInputHandler(sublime_plugin.TextInputHandler):
    def __init__(self, args: dict[str, Any]) -> None:
        self.args = args

    def placeholder(self) -> str:
        return 'Enter payload JSON. Example: {"conversationId": "12345"}'

    def name(self) -> str:
        return "payload"


# THIS IS NOT IMPLEMENTED
# {
#     partialResultToken: I.Union([I.String(), I.Number()]),
#     turns: I.Array({ request: I.String(), response: I.Optional(I.String()) }), { minItems: 1 }),
#     workingSet: I.Optional(I.Array({
#     t-ype: I.Literal("file"),
#     uri: I.String(),
#     visibleRange: I.Optional(Ea),
#     selection: I.Optional(Ea),
#     status: I.Optional(xNt),
#     range: I.Optional(Ea),
# })),
#     source: I.Optional(yLt),
#     workspaceFolder: I.Optional(I.String()),
#     userLanguage: I.Optional(I.String()),
#     model: I.Optional(I.String()),
# })


class CopilotEditConversationCreateCommand(CopilotTextCommand):
    """Command to create a new edit conversation with GitHub Copilot."""

    @_provide_plugin_session()
    def run(self, plugin: CopilotPlugin, session: Session, _: sublime.Edit, message: str = "") -> None:
        if not (window := self.view.window()):
            return

        file_uri = filename_to_uri(self.view.file_name() or "")
        if not file_uri:
            status_message("Cannot start edit conversation on an unsaved file", icon="❌")
            return

        wecm = WindowEditConversationManager(window)
        if wecm.conversation_id:
            ui_entry = wecm.get_ui_entry()
            ui_entry.open()
            ui_entry.prompt_for_message(
                callback=lambda msg: self._on_edit_prompt(plugin, session, msg), initial_text=message
            )
            return

        # If no message provided, prompt for it first
        if not message.strip():
            wecm = WindowEditConversationManager(window)
            wecm.source_view_id = self.view.id()
            ui_entry = wecm.get_ui_entry()
            ui_entry.open()
            ui_entry.prompt_for_message(
                callback=lambda msg: self._create_edit_conversation_with_message(plugin, session, msg), initial_text=""
            )
            return

        # Create conversation with the provided message
        self._create_edit_conversation_with_message(plugin, session, message)

    def _create_edit_conversation_with_message(self, plugin: CopilotPlugin, session: Session, message: str) -> None:
        """Create a new edit conversation with the specified message."""
        if not (window := self.view.window()):
            return

        if not message.strip():
            status_message("Please provide a message for the edit conversation", icon="❌")
            return

        file_uri = filename_to_uri(self.view.file_name() or "")
        if not file_uri:
            status_message("Cannot start edit conversation on an unsaved file", icon="❌")
            return

        # Prepare the document for the request
        doc = prepare_conversation_edit_request(self.view)
        if not doc:
            status_message("Failed to prepare document for edit conversation", icon="❌")
            return

        # Add user message to conversation before sending request
        wecm = WindowEditConversationManager(window)
        wecm.source_view_id = self.view.id()
        is_template, msg = preprocess_chat_message(self.view, message, [])
        # Add the user's message to the conversation
        wecm.append_conversation_entry({
            "kind": plugin.get_account_status().user or "user",
            "conversationId": "",  # Will be set when conversation is created
            "reply": preprocess_message_for_html(msg),
            "turnId": str(uuid.uuid4()),
            "references": [],
            "annotations": [],
            "hideText": False,
            "warnings": [],
        })

        # Update UI to show the user message
        ui_entry = wecm.get_ui_entry()
        ui_entry.update()

        # Send request to create a new edit conversation
        session.send_request(
            Request(
                REQ_EDIT_CONVERSATION_CREATE,
                {
                    "partialResultToken": f"copilot_pedit://{window.id()}",
                    "turns": [{"request": msg, "doc": doc}],
                    "workingSet": [
                        {"type": "file", "uri": file_uri, "selection": doc["selection"], "range": doc["range"]}
                    ],
                    "source": "panel",
                    "workspaceFolder": "",
                    "userLanguage": "en-US",  # Default to English
                    "model": None,  # Let the server choose the model
                },
            ),
            lambda response: self._on_result_edit_conversation_create(plugin, session, response),
        )

        status_message("Creating edit conversation...", icon="⏳")

    def _on_result_edit_conversation_create(self, plugin: CopilotPlugin, session: Session, response: list) -> None:
        if not (window := self.view.window()):
            return
        if len(response) != 0:
            status_message(f"{response} Failed to create edit conversation", icon="❌")
            return

        # The conversation ID will come from progress updates
        # Set up the manager and UI for continuous conversation
        wecm = WindowEditConversationManager(window)
        wecm.source_view_id = self.view.id()
        ui_entry = wecm.get_ui_entry()
        ui_entry.open()
        ui_entry.prompt_for_message(callback=lambda msg: self._on_edit_prompt(plugin, session, msg))

    def _on_edit_prompt(self, plugin: CopilotPlugin, session: Session, msg: str):
        if not (window := self.view.window()):
            return

        wecm = WindowEditConversationManager(window)
        ui_entry = wecm.get_ui_entry()
        if wecm.is_waiting:
            ui_entry.prompt_for_message(callback=lambda x: self._on_edit_prompt(plugin, session, x), initial_text=msg)
            return

        if not (source_view := find_view_by_id(wecm.source_view_id)):
            status_message("Source view no longer available", icon="❌")
            return

        is_template, msg = preprocess_chat_message(source_view, msg, [])
        # Get workspace folder if available
        if window.folders():
            window.folders()[0]

        # Prepare the document for the request
        doc = prepare_conversation_edit_request(source_view)
        if not doc:
            status_message("Failed to prepare document for edit conversation", icon="❌")
            return

        file_uri = filename_to_uri(source_view.file_name() or "")

        # Add user message to conversation
        wecm.append_conversation_entry({
            "kind": plugin.get_account_status().user or "user",
            "conversationId": wecm.conversation_id,
            "reply": preprocess_message_for_html(msg),
            "turnId": str(uuid.uuid4()),
            "references": [],
            "annotations": [],
            "hideText": False,
            "warnings": [],
        })

        # Update UI to show the user message
        ui_entry.update()

        # Send the turn request
        session.send_request(
            Request(
                REQ_EDIT_CONVERSATION_TURN,
                {
                    "partialResultToken": f"copilot_edit://{window.id()}_{wecm.conversation_id}",
                    "editConversationId": wecm.conversation_id,
                    "message": msg,
                    "workingSet": [
                        {"type": "file", "uri": file_uri, "selection": doc["selection"], "range": doc["range"]}
                    ],
                    "workspaceFolder": "",
                    "userLanguage": "en-US",
                    "model": None,
                },
            ),
            lambda _: ui_entry.prompt_for_message(callback=lambda x: self._on_edit_prompt(plugin, session, x)),
        )
        ui_entry.show_waiting_state(True)


class CopilotApplyEditConversationEditsCommand(CopilotTextCommand):
    """Command to apply edits from an edit conversation."""

    @_provide_plugin_session()
    def run(self, plugin: CopilotPlugin, session: Session, edit: sublime.Edit) -> None:
        if not (window := self.view.window()):
            return

        wecm = WindowEditConversationManager(window)
        # Get pending edits and source view from the edit conversation manager
        pending_edits = wecm.pending_edits
        source_view = wecm.get_source_view()

        if not pending_edits:
            status_message("No pending edits to apply", icon="❌")
            return

        if not source_view:
            status_message("Source view no longer available", icon="❌")
            return

        # Apply edits to the source view
        window.focus_view(source_view)
        with mutable_view(source_view) as view:
            for edit_item in pending_edits:
                if range_data := edit_item.get("range"):
                    # Convert LSP range to Sublime Text region
                    start_point = source_view.text_point(range_data["start"]["line"], range_data["start"]["character"])
                    end_point = source_view.text_point(range_data["end"]["line"], range_data["end"]["character"])
                    region = sublime.Region(start_point, end_point)

                    # Replace the text in the region
                    view.replace(edit, region, edit_item.get("newText", ""))

        # Clear pending edits
        wecm.clear_pending_edits()
        status_message("Applied edits to the document", icon="✅")


class CopilotEditConversationTurnDeleteCommand(CopilotTextCommand):
    """Command to delete a turn from an edit conversation."""

    @_provide_plugin_session()
    def run(self, plugin: CopilotPlugin, session: Session, _: sublime.Edit, conversation_id: str, turn_id: str) -> None:
        session.send_request(
            Request(REQ_EDIT_CONVERSATION_TURN_DELETE, {"conversationId": conversation_id, "turnId": turn_id}),
            lambda response: self._on_result_edit_conversation_turn_delete(conversation_id, turn_id, response),
        )

    def _on_result_edit_conversation_turn_delete(self, conversation_id: str, turn_id: str, payload: Any) -> None:
        status_message("Deleted turn from edit conversation", icon="✅")

        # Update the panel if it exists
        if not (window := self.view.window()):
            return

        panel_name = f"{COPILOT_OUTPUT_PANEL_PREFIX}_edit_{conversation_id[:8]}"
        for view in window.views():
            if view.settings().get("output.name") == panel_name:
                view.run_command("copilot_refresh_edit_conversation_panel", {"conversation_id": conversation_id})
                break


class CopilotEditConversationDestroyShimCommand(CopilotWindowCommand):
    def run(self, conversation_id: str) -> None:
        wecm = WindowEditConversationManager(self.window)
        if not (view := find_view_by_id(wecm.source_view_id)):
            status_message("Failed to find source view.")
            return
        # Focus the view so that the command runs
        self.window.focus_view(view)
        view.run_command("copilot_edit_conversation_destroy", {"conversation_id": conversation_id})


class CopilotEditConversationDestroyCommand(CopilotTextCommand):
    """Command to destroy an edit conversation."""

    @_provide_plugin_session()
    def run(self, plugin: CopilotPlugin, session: Session, _: sublime.Edit, conversation_id: str) -> None:
        if not (
            (window := self.view.window())
            and (wecm := WindowEditConversationManager(window))
            and wecm.conversation_id == conversation_id
        ):
            status_message("Failed to find window or edit conversation.")
            return

        session.send_request(
            Request(
                REQ_EDIT_CONVERSATION_DESTROY,
                {
                    "editConversationId": conversation_id,
                    "options": {},
                },
            ),
            self._on_result_edit_conversation_destroy,
        )

    def _on_result_edit_conversation_destroy(self, payload: str) -> None:
        if not (window := self.view.window()):
            status_message("Failed to find window")
            return
        if payload != "OK":
            status_message("Failed to destroy edit conversation.")
            return

        status_message("Destroyed edit conversation.")
        wecm = WindowEditConversationManager(window)
        wecm.close()
        wecm.reset()

    def is_enabled(self, event: dict[Any, Any] | None = None, point: int | None = None) -> bool:  # type: ignore
        if not (window := self.view.window()):
            return False
        return bool(WindowEditConversationManager(window).conversation_id)


class CopilotRefreshEditConversationPanelCommand(sublime_plugin.TextCommand):
    """Command to refresh the edit conversation panel."""

    def run(self, edit: sublime.Edit, conversation_id: str) -> None:
        # This is a utility command to update the panel after deleting a turn
        # In a real implementation, this would fetch the updated conversation
        # and redraw the panel contents
        self.view.set_read_only(False)
        self.view.run_command("append", {"characters": "\n[Turn deleted]\n\n"})
        self.view.set_read_only(True)
