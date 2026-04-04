from __future__ import annotations

import textwrap
from collections.abc import Iterable

import mdpopups
import sublime
from more_itertools import first_true, unique_everseen

from ..template import load_resource_template
from ..types import CopilotPayloadPanelSolution, StLayout
from ..utils import (
    all_views,
    find_view_by_id,
    fix_completion_syntax_highlight,
    get_copilot_view_setting,
    get_view_language_id,
    remove_prefix,
    set_copilot_view_setting,
)


class ViewPanelCompletionManager:
    # ------------- #
    # view settings #
    # ------------- #

    @property
    def is_visible(self) -> bool:
        """Whether the panel completions is visible."""
        return get_copilot_view_setting(self.view, "is_visible_panel_completions", False)

    @is_visible.setter
    def is_visible(self, value: bool) -> None:
        set_copilot_view_setting(self.view, "is_visible_panel_completions", value)

    @property
    def is_waiting(self) -> bool:
        """Whether the panel completions synthesis has been done."""
        return get_copilot_view_setting(self.view, "is_waiting_panel_completions", False)

    @is_waiting.setter
    def is_waiting(self, value: bool) -> None:
        set_copilot_view_setting(self.view, "is_waiting_panel_completions", value)

    @property
    def group_id(self) -> int:
        """The ID of the group which is used to show panel completions."""
        return get_copilot_view_setting(self.view, "panel_group_id", -1)

    @group_id.setter
    def group_id(self, value: int) -> None:
        set_copilot_view_setting(self.view, "panel_group_id", value)

    @property
    def sheet_id(self) -> int:
        """The ID of the sheet which is used to show panel completions."""
        return get_copilot_view_setting(self.view, "panel_sheet_id", -1)

    @sheet_id.setter
    def sheet_id(self, value: int) -> None:
        set_copilot_view_setting(self.view, "panel_sheet_id", value)

    @property
    def original_layout(self) -> StLayout | None:
        """The original window layout prior to panel presentation."""
        return get_copilot_view_setting(self.view, "original_layout", None)

    @original_layout.setter
    def original_layout(self, value: StLayout | None) -> None:
        set_copilot_view_setting(self.view, "original_layout", value)

    @property
    def completion_target_count(self) -> int:
        """How many completions are synthesized in panel completions."""
        return get_copilot_view_setting(self.view, "panel_completion_target_count", 0)

    @completion_target_count.setter
    def completion_target_count(self, value: int) -> None:
        set_copilot_view_setting(self.view, "panel_completion_target_count", value)

    @property
    def completions(self) -> list[CopilotPayloadPanelSolution]:
        """All `completions` in the view. Note that this is a copy."""
        return get_copilot_view_setting(self.view, "panel_completions", [])

    @completions.setter
    def completions(self, value: list[CopilotPayloadPanelSolution]) -> None:
        set_copilot_view_setting(self.view, "panel_completions", value)

    @property
    def panel_id(self) -> str:
        """The panel ID sent to Copilot `getPanelCompletions` request."""
        return f"copilot://{self.view.id()}"

    # -------------- #
    # normal methods #
    # -------------- #

    def __init__(self, view: sublime.View) -> None:
        self.view = view

    def reset(self) -> None:
        self.is_waiting = False
        self.is_visible = False
        self.original_layout = None

    def get_completion(self, index: int) -> CopilotPayloadPanelSolution | None:
        try:
            return self.completions[index]
        except IndexError:
            return None

    def append_completion(self, completion: CopilotPayloadPanelSolution) -> None:
        completions = self.completions
        completions.append(completion)
        self.completions = completions

    @staticmethod
    def find_view_by_panel_id(panel_id: str) -> sublime.View | None:
        view_id = int(remove_prefix(panel_id, "copilot://"))
        return find_view_by_id(view_id)

    @classmethod
    def from_sheet_id(cls, sheet_id: int) -> ViewPanelCompletionManager | None:
        return first_true(map(cls, all_views()), pred=lambda self: self.sheet_id == sheet_id)

    def open(self, *, completion_target_count: int | None = None) -> None:
        """Open the completion panel."""
        if completion_target_count is not None:
            self.completion_target_count = completion_target_count

        _PanelCompletion(self.view).open()

    def update(self) -> None:
        """Update the completion panel."""
        _PanelCompletion(self.view).update()

    def close(self) -> None:
        """Close the completion panel."""
        _PanelCompletion(self.view).close()


class _PanelCompletion:
    def __init__(self, view: sublime.View) -> None:
        self.view = view
        self.completion_manager = ViewPanelCompletionManager(view)

    @property
    def completion_content(self) -> str:
        completions = self._synthesize(self.completion_manager.completions)

        return load_resource_template("panel_completion.md.jinja").render(
            close_url=sublime.command_url("copilot_close_panel_completion", {"view_id": self.view.id()}),
            is_waiting=self.completion_manager.is_waiting,
            sections=[
                {
                    "accept_url": sublime.command_url(
                        "copilot_accept_panel_completion_shim",
                        {"view_id": self.view.id(), "completion_index": index},
                    ),
                    "code": fix_completion_syntax_highlight(
                        self.view,
                        completion["region"][1],
                        self._prepare_popup_code_display_text(completion["displayText"]),
                    ),
                    "lang": get_view_language_id(self.view, completion["region"][1]),
                }
                for index, completion in completions
            ],
            total_solutions=self.completion_manager.completion_target_count,
        )

    def open(self) -> None:
        window = self.view.window()
        if not window:
            return

        active_group = window.active_group()
        if active_group == window.num_groups() - 1:
            self._open_in_side_by_side(window)
        else:
            self._open_in_group(window, active_group + 1)

        window.focus_view(self.view)

    def update(self) -> None:
        window = self.view.window()
        if not window:
            return

        sheet = window.transient_sheet_in_group(self.completion_manager.group_id)
        if not isinstance(sheet, sublime.HtmlSheet):
            return

        mdpopups.update_html_sheet(sheet=sheet, contents=self.completion_content, md=True)

    def close(self) -> None:
        window = self.view.window()
        if not window:
            return

        sheet = window.transient_sheet_in_group(self.completion_manager.group_id)
        if not isinstance(sheet, sublime.HtmlSheet):
            return

        sheet.close()
        self.completion_manager.is_visible = False
        if self.completion_manager.original_layout:
            window.set_layout(self.completion_manager.original_layout)  # type: ignore
            self.completion_manager.original_layout = None

        window.focus_view(self.view)

    @staticmethod
    def _prepare_popup_code_display_text(display_text: str) -> str:
        # The returned completion is in the form of
        #   - the first won't be indented
        #   - the rest of lines will be indented basing on the indentation level of the current line
        # The rest of lines don't visually look good if the current line is deeply indented.
        # Hence we modify the rest of lines into always indented by one level if it's originally indented.
        first_line, sep, rest = display_text.partition("\n")

        if rest.startswith((" ", "\t")):
            return first_line + sep + textwrap.indent(textwrap.dedent(rest), "\t")

        return display_text

    @staticmethod
    def _synthesize(
        completions: Iterable[CopilotPayloadPanelSolution],
    ) -> list[tuple[int, CopilotPayloadPanelSolution]]:
        """Return sorted-by-`score` completions in the form of `[(completion_index, completion), ...]`."""
        return sorted(
            # note that we must keep completion's original index
            unique_everseen(enumerate(completions), key=lambda pair: pair[1]["completionText"]),
            key=lambda pair: pair[1]["score"],
            reverse=True,
        )

    def _open_in_group(self, window: sublime.Window, group_id: int) -> None:
        self.completion_manager.group_id = group_id

        window.focus_group(group_id)
        sheet = mdpopups.new_html_sheet(
            window=window,
            name="Panel Completions",
            contents=self.completion_content,
            md=True,
            flags=sublime.TRANSIENT,
        )
        self.completion_manager.sheet_id = sheet.id()

    def _open_in_side_by_side(self, window: sublime.Window) -> None:
        self.completion_manager.original_layout = window.layout()  # type: ignore
        window.set_layout({
            "cols": [0.0, 0.5, 1.0],
            "rows": [0.0, 1.0],
            "cells": [[0, 0, 1, 1], [1, 0, 2, 1]],
        })
        self._open_in_group(window, 1)
