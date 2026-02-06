from __future__ import annotations

from typing import Callable, Any, TypeVar, Generic, Type
from abc import ABC, abstractmethod

import mdpopups
import sublime

from ..constants import COPILOT_WINDOW_CONVERSATION_SETTINGS_PREFIX, COPILOT_OUTPUT_PANEL_PREFIX
from ..helpers import GithubInfo, preprocess_message_for_html
from ..template import load_resource_template
from ..types import CopilotPayloadConversationEntry, CopilotPayloadConversationEntryTransformed, StLayout
from ..utils import find_view_by_id, find_window_by_id, get_copilot_setting, remove_prefix, set_copilot_setting

T = TypeVar('T', bound='BaseConversationEntry')


class ConversationSettingsManager:
    """Mixin for managing conversation settings with consistent property patterns."""

    def __init__(self, window: sublime.Window, settings_prefix: str):
        self.window = window
        self.settings_prefix = settings_prefix

    def _get_setting(self, key: str, default: Any = None) -> Any:
        """Get a setting value."""
        return get_copilot_setting(self.window, self.settings_prefix, key, default)

    def _set_setting(self, key: str, value: Any) -> None:
        """Set a setting value."""
        set_copilot_setting(self.window, self.settings_prefix, key, value)

    def _create_property(self, key: str, default: Any = None):
        """Create a property descriptor for a setting."""
        def getter(self) -> Any:
            return self._get_setting(key, default)

        def setter(self, value: Any) -> None:
            self._set_setting(key, value)

        return property(getter, setter)


class BaseConversationManager(ConversationSettingsManager, ABC):
    """Base class for conversation managers with shared functionality."""

    def __init__(self, window: sublime.Window, settings_prefix: str):
        super().__init__(window, settings_prefix)
        self._ui_entry = None

    # Shared properties using descriptors
    @property
    def conversation_id(self) -> str:
        return self._get_setting("conversation_id", "")

    @conversation_id.setter
    def conversation_id(self, value: str) -> None:
        self._set_setting("conversation_id", value)

    @property
    def group_id(self) -> int:
        return self._get_setting("group_id", -1)

    @group_id.setter
    def group_id(self, value: int) -> None:
        self._set_setting("group_id", value)

    @property
    def view_id(self) -> int:
        return self._get_setting("view_id", -1)

    @view_id.setter
    def view_id(self, value: int) -> None:
        self._set_setting("view_id", value)

    @property
    def original_layout(self) -> StLayout | None:
        return self._get_setting("original_layout", None)

    @original_layout.setter
    def original_layout(self, value: StLayout | None) -> None:
        self._set_setting("original_layout", value)

    @property
    def is_waiting(self) -> bool:
        return self._get_setting("is_waiting", False)

    @is_waiting.setter
    def is_waiting(self, value: bool) -> None:
        self._set_setting("is_waiting", value)

    @property
    def is_visible(self) -> bool:
        return self._get_setting("is_visible", False)

    @is_visible.setter
    def is_visible(self, value: bool) -> None:
        self._set_setting("is_visible", value)

    @property
    def conversation_entries(self) -> list[CopilotPayloadConversationEntry]:
        return self._get_setting("conversation_entries", [])

    @conversation_entries.setter
    def conversation_entries(self, value: list[CopilotPayloadConversationEntry]) -> None:
        self._set_setting("conversation_entries", value)

    # Shared methods
    def append_conversation_entry(self, entry: CopilotPayloadConversationEntry) -> None:
        """Add a new conversation entry."""
        entries = self.conversation_entries
        entries.append(entry)
        self.conversation_entries = entries

    def reset_base_settings(self) -> None:
        """Reset shared settings to defaults."""
        self.conversation_id = ""
        self.group_id = -1
        self.view_id = -1
        self.original_layout = None
        self.is_waiting = False
        self.is_visible = False
        self.conversation_entries = []

    @abstractmethod
    def reset(self) -> None:
        """Reset all settings to defaults. Subclasses must implement."""
        pass

    @abstractmethod
    def get_ui_entry(self) -> 'BaseConversationEntry':
        """Get the UI entry for this conversation type."""
        pass

    def open(self) -> None:
        """Open the conversation UI."""
        self.get_ui_entry().open()

    def update(self) -> None:
        """Update the conversation UI."""
        self.get_ui_entry().update()

    def close(self) -> None:
        """Close the conversation UI."""
        self.get_ui_entry().close()


class BaseConversationEntry(ABC):
    """Base class for conversation UI entries."""

    def __init__(self, window: sublime.Window, manager: BaseConversationManager):
        self.window = window
        self.manager = manager

    @property
    @abstractmethod
    def completion_content(self) -> str:
        """Generate HTML content for the conversation sheet."""
        pass

    @property
    @abstractmethod
    def sheet_name(self) -> str:
        """Name for the conversation sheet."""
        pass

    def open(self) -> None:
        """Open the conversation sheet."""
        self.manager.is_visible = True
        active_group = self.window.active_group()
        if active_group == self.window.num_groups() - 1:
            self._open_in_side_by_side(self.window)
        else:
            self._open_in_group(self.window, active_group + 1)

        self.window.focus_view(self.window.active_view())

    def update(self) -> None:
        """Update the conversation sheet content."""
        if not (sheet := self.window.transient_sheet_in_group(self.manager.group_id)):
            return

        mdpopups.update_html_sheet(
            sheet=sheet,
            contents=self.completion_content,
            md=True,
            wrapper_class="wrapper"
        )

    def close(self) -> None:
        """Close the conversation sheet."""
        if not (sheet := self.window.transient_sheet_in_group(self.manager.group_id)):
            return

        sheet.close()

        self.manager.is_visible = False
        self.manager.window.run_command("hide_panel")
        if self.manager.original_layout:
            self.window.set_layout(self.manager.original_layout)
            self.manager.original_layout = None

        if view := self.window.active_view():
            self.window.focus_view(view)

    def _open_in_group(self, window: sublime.Window, group_id: int) -> None:
        """Open the conversation sheet in a specific group."""
        self.manager.group_id = group_id

        window.focus_group(group_id)
        sheet = mdpopups.new_html_sheet(
            window=window,
            name=self.sheet_name,
            contents=self.completion_content,
            md=True,
            flags=sublime.TRANSIENT,
            wrapper_class="wrapper",
        )
        self.manager.view_id = sheet.id()

    def _open_in_side_by_side(self, window: sublime.Window) -> None:
        """Open the conversation sheet in side-by-side layout."""
        self.manager.original_layout = window.layout()
        window.set_layout({
            "cols": [0.0, 0.5, 1.0],
            "rows": [0.0, 1.0],
            "cells": [[0, 0, 1, 1], [1, 0, 2, 1]],
        })
        self._open_in_group(window, 1)


class WindowConversationManager(BaseConversationManager):
    """Manager for regular chat conversations."""

    def __init__(self, window: sublime.Window):
        super().__init__(window, COPILOT_WINDOW_CONVERSATION_SETTINGS_PREFIX)

    # Chat-specific properties
    @property
    def last_active_view_id(self) -> int:
        return self._get_setting("last_active_view_id", -1)

    @last_active_view_id.setter
    def last_active_view_id(self, value: int) -> None:
        self._set_setting("last_active_view_id", value)

    @property
    def suggested_title(self) -> str:
        return self._get_setting("suggested_title", "")

    @suggested_title.setter
    def suggested_title(self, value: str) -> None:
        self._set_setting("suggested_title", value)

    @property
    def follow_up(self) -> str:
        return self._get_setting("follow_up", "")

    @follow_up.setter
    def follow_up(self, value: str) -> None:
        # Fixes: https://github.com/TerminalFi/LSP-copilot/issues/182
        self._set_setting("follow_up", value.replace("`", "&#96;"))

    @property
    def code_block_index(self) -> dict[str, str]:
        return self._get_setting("code_block_index", {})

    @code_block_index.setter
    def code_block_index(self, value: dict[str, str]) -> None:
        self._set_setting("code_block_index", value)

    @property
    def reference_block_state(self) -> dict[str, bool]:
        return self._get_setting("reference_block_state", {})

    @reference_block_state.setter
    def reference_block_state(self, value: dict[str, bool]) -> None:
        self._set_setting("reference_block_state", value)

    @property
    def conversation(self) -> list[CopilotPayloadConversationEntry]:
        """Alias for conversation_entries for backward compatibility."""
        return self.conversation_entries

    @conversation.setter
    def conversation(self, value: list[CopilotPayloadConversationEntry]) -> None:
        self.conversation_entries = value

    def reset(self) -> None:
        """Reset all chat conversation settings."""
        self.reset_base_settings()
        self.last_active_view_id = -1
        self.suggested_title = ""
        self.follow_up = ""
        self.code_block_index = {}
        self.reference_block_state = {}

    def get_ui_entry(self) -> '_ConversationEntry':
        """Get the UI entry for chat conversations."""
        if not self._ui_entry:
            self._ui_entry = _ConversationEntry(self.window, self)
        return self._ui_entry

    # Chat-specific methods
    def append_reference_block_state(self, turn_id: str, state: bool) -> None:
        reference_block_state = self.reference_block_state
        reference_block_state[turn_id] = state
        self.reference_block_state = reference_block_state

    def insert_code_block_index(self, index: int, code_block: str) -> None:
        code_block_index = self.code_block_index
        code_block_index[str(index)] = code_block
        self.code_block_index = code_block_index

    def toggle_references_block(self, turn_id: str) -> None:
        reference_block_state = self.reference_block_state
        reference_block_state[turn_id] = not reference_block_state.get(turn_id, False)
        self.reference_block_state = reference_block_state

    @staticmethod
    def find_window_by_token_id(token_id: str) -> sublime.Window | None:
        return sublime.active_window()

    def prompt(self, callback: Callable[[str], None], initial_text: str = "") -> None:
        self.window.show_input_panel("Copilot:", initial_text, callback, None, None)


class WindowEditConversationManager(BaseConversationManager):
    """Manager for edit conversations."""

    EDIT_CONVERSATION_SETTINGS_PREFIX = "copilot.window.edit_conversation"

    def __init__(self, window: sublime.Window):
        super().__init__(window, self.EDIT_CONVERSATION_SETTINGS_PREFIX)

    # Edit-specific properties
    @property
    def source_view_id(self) -> int:
        return self._get_setting("source_view_id", -1)

    @source_view_id.setter
    def source_view_id(self, value: int) -> None:
        self._set_setting("source_view_id", value)

    @property
    def pending_edits(self) -> list[dict[str, Any]]:
        return self._get_setting("pending_edits", [])

    @pending_edits.setter
    def pending_edits(self, value: list[dict[str, Any]]) -> None:
        self._set_setting("pending_edits", value)

    def reset(self) -> None:
        """Reset all edit conversation settings."""
        self.reset_base_settings()
        self.source_view_id = -1
        self.pending_edits = []

    def get_ui_entry(self) -> '_EditConversationEntry':
        """Get the UI entry for edit conversations."""
        if not self._ui_entry:
            self._ui_entry = _EditConversationEntry(self.window, self)
        return self._ui_entry

    # Edit-specific methods
    def add_pending_edit(self, edit: dict[str, Any]) -> None:
        """Add a pending edit that can be applied to the source view."""
        edits = self.pending_edits
        edits.append(edit)
        self.pending_edits = edits

    def clear_pending_edits(self) -> None:
        """Clear all pending edits."""
        self.pending_edits = []

    def get_source_view(self) -> sublime.View | None:
        """Get the source view being edited, if it still exists."""
        return find_view_by_id(self.source_view_id)

    def destroy(self) -> None:
        """Destroy the edit conversation and clean up all resources."""
        self.get_ui_entry().close()
        self.reset()

    @staticmethod
    def find_by_conversation_id(conversation_id: str) -> 'WindowEditConversationManager | None':
        """Find an edit conversation manager by conversation ID across all windows."""
        for window in sublime.windows():
            wecm = WindowEditConversationManager(window)
            if wecm.conversation_id == conversation_id:
                return wecm
        return None


class _ConversationEntry(BaseConversationEntry):
    """UI entry for regular chat conversations."""

    def __init__(self, window: sublime.Window, manager: WindowConversationManager):
        super().__init__(window, manager)
        self.wcm = manager  # Type-specific reference for backward compatibility

    @property
    def sheet_name(self) -> str:
        return "Copilot Chat"

    @property
    def completion_content(self) -> str:
        conversations_entries = self._synthesize()
        return load_resource_template("chat_panel.md.jinja", keep_trailing_newline=True).render(
            window_id=self.wcm.window.id(),
            is_waiting=self.wcm.is_waiting,
            avatar_img_src=GithubInfo.get_avatar_img_src(),
            suggested_title=preprocess_message_for_html(self.wcm.suggested_title),
            follow_up=preprocess_message_for_html(self.wcm.follow_up),
            follow_up_url=sublime.command_url(
                "copilot_conversation_chat_shim",
                {"window_id": self.wcm.window.id(), "message": self.wcm.follow_up},
            ),
            close_url=sublime.command_url(
                "copilot_conversation_close",
                {"window_id": self.wcm.window.id()},
            ),
            delete_url=sublime.command_url(
                "copilot_conversation_destroy_shim",
                {"conversation_id": self.wcm.conversation_id},
            ),
            sections=[
                {
                    "kind": entry["kind"],
                    "message": "".join(entry["messages"]),
                    "code_block_indices": entry["codeBlockIndices"],
                    "toggle_references_url": sublime.command_url(
                        "copilot_conversation_toggle_references_block",
                        {
                            "conversation_id": self.wcm.conversation_id,
                            "window_id": self.wcm.window.id(),
                            "turn_id": entry["turnId"],
                        },
                    ),
                    "references": [] if entry["kind"] != "report" else entry["references"],
                    "references_expanded": self.wcm.reference_block_state.get(entry["turnId"], False),
                    "turn_delete_url": sublime.command_url(
                        "copilot_conversation_turn_delete_shim",
                        {
                            "conversation_id": self.wcm.conversation_id,
                            "window_id": self.wcm.window.id(),
                            "turn_id": entry["turnId"],
                        },
                    ),
                    "thumbs_up_url": sublime.command_url(
                        "copilot_conversation_rating_shim",
                        {"turn_id": entry["turnId"], "rating": 1},
                    ),
                    "thumbs_down_url": sublime.command_url(
                        "copilot_conversation_rating_shim",
                        {"turn_id": entry["turnId"], "rating": -1},
                    ),
                    "warnings": entry.get("warnings", []),
                }
                for entry in conversations_entries
            ],
        )

    def _synthesize(self) -> list[CopilotPayloadConversationEntryTransformed]:
        def inject_code_block_commands(reply: str, code_block_index: int) -> str:
            return f"CODE_BLOCK_COMMANDS_{code_block_index}\n\n{reply}"

        transformed_conversation: list[CopilotPayloadConversationEntryTransformed] = []
        current_entry: CopilotPayloadConversationEntryTransformed | None = None
        is_inside_code_block = False
        code_block_index = -1

        for idx, entry in enumerate(self.wcm.conversation):
            kind = entry["kind"]
            reply = entry["reply"]
            turn_id = entry["turnId"]

            if current_entry and current_entry["kind"] == kind:
                if reply.startswith("```"):
                    is_inside_code_block = not is_inside_code_block
                    if is_inside_code_block:
                        code_block_index += 1
                        current_entry["codeBlockIndices"].append(code_block_index)
                        reply = inject_code_block_commands(reply, code_block_index)
                    else:
                        self.wcm.insert_code_block_index(code_block_index, "".join(current_entry["codeBlocks"]))
                        current_entry["codeBlocks"] = []
                elif is_inside_code_block:
                    current_entry["codeBlocks"].append(reply)
                current_entry["messages"].append(reply)
                if warnings := entry.get("warnings"):
                    current_entry["warnings"].extend(warnings)
            else:
                if current_entry:
                    transformed_conversation.append(current_entry)
                current_entry = {
                    "kind": kind,
                    "turnId": turn_id,
                    "messages": [reply],
                    "codeBlockIndices": [],
                    "codeBlocks": [],
                    "references": [],
                    "warnings": entry.get("warnings", []),
                }
                if kind == "report":
                    current_entry["references"] = self.wcm.conversation[idx - 1].get("references", [])

                if reply.startswith("```") and kind == "report":
                    is_inside_code_block = True
                    code_block_index += 1
                    current_entry["codeBlockIndices"].append(code_block_index)
                    reply = inject_code_block_commands(reply, code_block_index)
                    current_entry["messages"] = [reply]

        if current_entry:
            # Fixes: https://github.com/TerminalFi/LSP-copilot/issues/187
            if is_inside_code_block:
                current_entry["messages"].append("```")
            transformed_conversation.append(current_entry)

        return transformed_conversation


class _EditConversationEntry(BaseConversationEntry):
    """UI entry for edit conversations."""

    def __init__(self, window: sublime.Window, manager: WindowEditConversationManager):
        super().__init__(window, manager)
        self.wecm = manager  # Type-specific reference

    @property
    def sheet_name(self) -> str:
        return "Copilot Edit"

    @property
    def completion_content(self) -> str:
        """Generate the HTML content for the edit conversation sheet."""
        # Get source file name if available
        source_file = ""
        if source_view := self.wecm.get_source_view():
            if file_name := source_view.file_name():
                import os
                source_file = os.path.basename(file_name)

        # Process conversation entries into sections
        sections = []
        for entry in self.wecm.conversation_entries:
            sections.append({
                "kind": entry.get("kind", "unknown"),
                "message": entry.get("reply", ""),
                "turnId": entry.get("turnId", ""),
                "annotations": entry.get("annotations", []),
                "thumbs_up_url": sublime.command_url(
                    "copilot_conversation_rating_shim",
                    {"turn_id": entry.get("turnId", ""), "rating": 1}
                ),
                "thumbs_down_url": sublime.command_url(
                    "copilot_conversation_rating_shim",
                    {"turn_id": entry.get("turnId", ""), "rating": -1}
                ),
                "turn_delete_url": sublime.command_url(
                    "copilot_edit_conversation_turn_delete",
                    {
                        "conversation_id": self.wecm.conversation_id,
                        "turn_id": entry.get("turnId", "")
                    }
                ),
            })

        return load_resource_template("edit_conversation.md.jinja", keep_trailing_newline=True).render(
            window_id=self.window.id(),
            is_waiting=self.wecm.is_waiting,
            avatar_img_src=GithubInfo.get_avatar_img_src(),
            source_file=source_file,
            sections=sections,
            pending_edits=self.wecm.pending_edits,
            close_url=sublime.command_url(
                "copilot_edit_conversa~tion_close",
                {"conversation_id": self.wecm.conversation_id}
            ),
            destroy_url=sublime.command_url(
                "copilot_edit_conversation_destroy_shim",
                {"conversation_id": self.wecm.conversation_id}
            ),
            apply_edits_url=sublime.command_url(
                "copilot_apply_edit_conversation_edits",
                {}
            ),
        )

    def prompt_for_message(self, callback: Callable[[str], None], initial_text: str = "") -> None:
        """Show input panel for new message in edit conversation."""
        self.window.show_input_panel("Edit Conversation:", initial_text, callback, None, None)

    def add_user_message(self, message: str) -> None:
        """Add a user message to the edit conversation."""
        import uuid

        self.wecm.append_conversation_entry({
            "kind": "user",
            "conversationId": self.wecm.conversation_id,
            "reply": preprocess_message_for_html(message),
            "turnId": str(uuid.uuid4()),
            "references": [],
            "annotations": [],
            "hideText": False,
            "warnings": [],
        })
        self.update()

    def add_assistant_message(self, message: str, turn_id: str | None = None) -> None:
        """Add an assistant message to the edit conversation."""
        import uuid

        self.wecm.append_conversation_entry({
            "kind": "assistant",
            "conversationId": self.wecm.conversation_id,
            "reply": preprocess_message_for_html(message),
            "turnId": turn_id or str(uuid.uuid4()),
            "references": [],
            "annotations": [],
            "hideText": False,
            "warnings": [],
        })
        self.update()

    def show_waiting_state(self, waiting: bool = True) -> None:
        """Show or hide waiting state in the sheet."""
        self.wecm.is_waiting = waiting
        self.update()

    def add_pending_edit(self, edit: dict[str, Any]) -> None:
        """Add a pending edit and update the sheet."""
        self.wecm.add_pending_edit(edit)
        self.update()

    def clear_pending_edits(self) -> None:
        """Clear pending edits and update the sheet."""
        self.wecm.clear_pending_edits()
        self.update()
