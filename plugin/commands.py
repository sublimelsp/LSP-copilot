from __future__ import annotations

import json
import os
import uuid
from abc import ABC
from collections.abc import Callable
from functools import partial, wraps
from pathlib import Path
from typing import Any, Literal, Sequence, cast

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
    REQ_CONVERSATION_TEMPLATES,
    REQ_CONVERSATION_TURN,
    REQ_CONVERSATION_TURN_DELETE,
    REQ_FILE_CHECK_STATUS,
    REQ_GET_PANEL_COMPLETIONS,
    REQ_GET_PROMPT,
    REQ_GET_VERSION,
    REQ_NOTIFY_ACCEPTED,
    REQ_NOTIFY_REJECTED,
    REQ_SIGN_IN_CONFIRM,
    REQ_SIGN_IN_INITIATE,
    REQ_SIGN_IN_WITH_GITHUB_TOKEN,
    REQ_SIGN_OUT,
)
from .decorators import must_be_active_view
from .helpers import (
    GithubInfo,
    prepare_completion_request_doc,
    prepare_conversation_turn_request,
    preprocess_chat_message,
    preprocess_message_for_html,
)
from .log import log_info
from .types import (
    CopilotConversationDebugTemplates,
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
from .ui import ViewCompletionManager, ViewPanelCompletionManager, WindowConversationManager
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
        req_params: dict[str, Any] = {
            "turns": [{"request": msg}],
            "capabilities": {
                "allSkills": True,
                "skills": [],
            },
            "workDoneToken": f"copilot_chat://{window.id()}",
            "computeSuggestions": True,
            "source": "panel",
        }
        session.send_request(
            Request(REQ_CONVERSATION_CREATE, req_params),
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

        req_params: dict[str, Any] = {
            "conversationId": conversation_id,
            "options": {},
        }
        session.send_request(
            Request(REQ_CONVERSATION_DESTROY, req_params),
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

        req_params: dict[str, Any] = {
            "conversationId": conversation_id,
            "turnId": retrieved_turn_id,
            "options": {},
        }
        session.send_request(
            Request(REQ_CONVERSATION_TURN_DELETE, req_params),
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
        session.send_request(Request(REQ_CONVERSATION_AGENTS, {"options": {}}), self._on_result_conversation_agents)

    def _on_result_conversation_agents(self, payload: list[CopilotRequestConversationAgent]) -> None:
        if not (window := self.view.window()):
            return
        window.show_quick_panel([[item["slug"], item["description"]] for item in payload], lambda _: None)


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
