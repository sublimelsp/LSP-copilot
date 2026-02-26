from __future__ import annotations

import html
import textwrap
from abc import ABC, abstractmethod
from typing import Sequence

import mdpopups
import sublime
from more_itertools import first_true

from ..template import load_resource_template
from ..types import CopilotPayloadCompletion
from ..utils import (
    clamp,
    fix_completion_syntax_highlight,
    get_copilot_view_setting,
    get_view_language_id,
    is_active_view,
    set_copilot_view_setting,
)

_view_to_phantom_set: dict[int, sublime.PhantomSet] = {}


class ViewCompletionManager:
    # ------------- #
    # view settings #
    # ------------- #

    @property
    def is_visible(self) -> bool:
        """Whether Copilot's completion popup is visible."""
        return get_copilot_view_setting(self.view, "is_visible", False)

    @is_visible.setter
    def is_visible(self, value: bool) -> None:
        set_copilot_view_setting(self.view, "is_visible", value)

    @property
    def is_waiting(self) -> bool:
        """Whether the view is waiting for Copilot's completion response."""
        return get_copilot_view_setting(self.view, "is_waiting_completion", False)

    @is_waiting.setter
    def is_waiting(self, value: bool) -> None:
        set_copilot_view_setting(self.view, "is_waiting_completion", value)

    @property
    def completions(self) -> list[CopilotPayloadCompletion]:
        """All `completions` in the view. Note that this is a copy."""
        return get_copilot_view_setting(self.view, "completions", [])

    @completions.setter
    def completions(self, value: list[CopilotPayloadCompletion]) -> None:
        set_copilot_view_setting(self.view, "completions", value)

    @property
    def completion_style(self) -> str:
        """The completion style."""
        return get_copilot_view_setting(self.view, "completion_style", "")

    @completion_style.setter
    def completion_style(self, value: str) -> None:
        set_copilot_view_setting(self.view, "completion_style", value)

    @property
    def completion_index(self) -> int:
        """The index of the current chosen completion."""
        return get_copilot_view_setting(self.view, "completion_index", 0)

    @completion_index.setter
    def completion_index(self, value: int) -> None:
        set_copilot_view_setting(
            self.view,
            "completion_index",
            self._tidy_completion_index(value),
        )

    # -------------- #
    # normal methods #
    # -------------- #

    def __init__(self, view: sublime.View) -> None:
        self.view = view

    def reset(self) -> None:
        self.is_visible = False
        self.is_waiting = False

    @property
    def current_completion(self) -> CopilotPayloadCompletion | None:
        """The current chosen `completion`."""
        return self.completions[self.completion_index] if self.completions else None

    @property
    def completion_style_type(self) -> type[_BaseCompletion]:
        if completion_cls := first_true(
            _BaseCompletion.__subclasses__(),
            pred=lambda t: t.name == self.completion_style,
        ):
            return completion_cls
        raise RuntimeError(f"Unknown completion style type: {self.completion_style}")

    @property
    def is_phantom(self) -> bool:
        return self.completion_style == _PhantomCompletion.name

    def show_previous_completion(self) -> None:
        """Show the previous completion."""
        self.show(completion_index=self.completion_index - 1)

    def show_next_completion(self) -> None:
        """Show the next completion."""
        self.show(completion_index=self.completion_index + 1)

    def handle_selection_change(self) -> None:
        if not (self.is_phantom and self.is_visible):
            return

        self.hide()

    def handle_text_change(self) -> bool:
        if not (self.is_phantom and self.is_visible):
            return False

        if self.current_completion and len(self.view.sel()) == 1 and self.view.sel()[0].empty():
            current_completion = self.current_completion
            point = self.view.sel()[0].begin()
            region = sublime.Region(current_completion["point"], point)
            text = self.view.substr(region)

            if current_completion["displayText"].startswith(text):
                current_completion["displayText"] = current_completion["displayText"][len(region) :]
                self.completion_style_type(
                    self.view, current_completion, self.completion_index, len(self.completions)
                ).show()

                return True
            else:
                self.hide()

                return False
        else:
            self.hide()

            return False

    def handle_close(self) -> None:
        if not self.is_phantom:
            return

        self.completion_style_type.close(self.view)

    def hide(self) -> None:
        """Hide Copilot's completion popup."""
        # prevent from hiding other plugin's popup
        if self.is_visible:
            self.completion_style_type.hide(self.view)

        self.is_visible = False

    def show(
        self,
        completions: list[CopilotPayloadCompletion] | None = None,
        completion_index: int | None = None,
        completion_style: str | None = None,
    ) -> None:
        if not is_active_view(self.view):
            return

        """Show Copilot's completion popup."""
        if completions is not None:
            self.completions = completions
        if completion_index is not None:
            self.completion_index = completion_index
        if completion_style is not None:
            self.completion_style = completion_style

        completion = self.current_completion
        if not completion:
            return

        # the text after completion is the same
        current_line = self.view.line(completion["point"])
        if completion["text"] == self.view.substr(current_line):
            return

        self.completion_style_type(self.view, completion, self.completion_index, len(self.completions)).show()

        self.is_visible = True

    def _tidy_completion_index(self, index: int) -> int:
        """Revise `completion_index` to a valid value, or `0` if `self.completions` is empty."""
        completions_cnt = len(self.completions)
        if not completions_cnt:
            return 0

        # clamp if it's out-of-bounds or treat it as cyclic?
        if self.view.settings().get("auto_complete_cycle"):
            return index % completions_cnt
        return clamp(index, 0, completions_cnt - 1)


class _BaseCompletion(ABC):
    name = ""

    def __init__(
        self,
        view: sublime.View,
        completion: CopilotPayloadCompletion,
        index: int = 0,
        count: int = 1,
    ) -> None:
        self.view = view
        self.completion = completion
        self.index = index
        self.count = count

        self._settings = self.view.settings()

    @abstractmethod
    def show(self) -> None:
        pass

    @classmethod
    @abstractmethod
    def hide(cls, view: sublime.View) -> None:
        pass

    @classmethod
    def close(cls, view: sublime.View) -> None:
        pass


class _PopupCompletion(_BaseCompletion):
    name = "popup"

    @property
    def popup_content(self) -> str:
        return load_resource_template("completion@popup.md.jinja").render(
            code=self.popup_code,
            completion=self.completion,
            count=self.count,
            index=self.index,
            lang=get_view_language_id(self.view, self.completion["point"]),
        )

    @property
    def popup_code(self) -> str:
        return fix_completion_syntax_highlight(
            self.view,
            self.completion["point"],
            textwrap.dedent(self.completion["text"]),
        )

    def show(self) -> None:
        mdpopups.show_popup(
            view=self.view,
            content=self.popup_content,
            md=True,
            layout=sublime.LAYOUT_INLINE,
            flags=sublime.COOPERATE_WITH_AUTO_COMPLETE,
            max_width=640,
        )

    @classmethod
    def hide(cls, view: sublime.View) -> None:
        mdpopups.hide_popup(view)


class _PhantomCompletion(_BaseCompletion):
    name = "phantom"

    COPILOT_PHANTOM_COMPLETION = "copilot_phantom_completion"
    PHANTOM_TEMPLATE = """
    <body id="copilot-completion">
        <style>
            body {{
                color: #808080;
                font-style: italic;
            }}

            .copilot-completion-line {{
                line-height: 0;
                margin-top: {line_padding_top}px;
                margin-bottom: {line_padding_bottom}px;
            }}

            .copilot-completion-line.first {{
                margin-top: 0;
            }}
        </style>
        {body}
    </body>
    """
    PHANTOM_LINE_TEMPLATE = '<div class="copilot-completion-line {class_name}">{content}</div>'

    def __init__(
        self,
        view: sublime.View,
        completion: CopilotPayloadCompletion,
        index: int = 0,
        count: int = 1,
    ) -> None:
        super().__init__(view, completion, index, count)

        self._phantom_set = self._get_phantom_set(view)

    @classmethod
    def _get_phantom_set(cls, view: sublime.View) -> sublime.PhantomSet:
        view_id = view.id()

        # create phantom set if there is no existing one
        if not _view_to_phantom_set.get(view_id):
            _view_to_phantom_set[view_id] = sublime.PhantomSet(view, cls.COPILOT_PHANTOM_COMPLETION)

        return _view_to_phantom_set[view_id]

    def normalize_phantom_line(self, line: str) -> str:
        return html.escape(line).replace(" ", "&nbsp;").replace("\t", "&nbsp;" * self._settings.get("tab_size"))

    def _build_phantom(
        self,
        lines: str | Sequence[str],
        begin: int,
        end: int | None = None,
        *,
        inline: bool = True,
    ) -> sublime.Phantom:
        body = (
            self.normalize_phantom_line(lines)
            if isinstance(lines, str)
            else "".join(
                self.PHANTOM_LINE_TEMPLATE.format(
                    class_name=("rest" if index else "first"),
                    content=self.normalize_phantom_line(line),
                )
                for index, line in enumerate(lines)
            )
        )

        return sublime.Phantom(
            sublime.Region(begin, begin if end is None else end),
            self.PHANTOM_TEMPLATE.format(
                body=body,
                line_padding_top=int(self._settings.get("line_padding_top")) * 2,  # TODO: play with this more
                line_padding_bottom=int(self._settings.get("line_padding_bottom")) * 2,
            ),
            sublime.LAYOUT_INLINE if inline else sublime.LAYOUT_BLOCK,
        )

    def show(self) -> None:
        first_line, *rest_lines = self.completion["displayText"].splitlines()

        assert self._phantom_set
        self._phantom_set.update([
            self._build_phantom(first_line, self.completion["point"] + 1, self.completion["point"]),
            # an empty phantom is required to prevent the cursor from jumping, even if there is only one line
            self._build_phantom(rest_lines, self.completion["point"], inline=False),
        ])

    @classmethod
    def hide(cls, view: sublime.View) -> None:
        cls._get_phantom_set(view).update([])

    @classmethod
    def close(cls, view: sublime.View) -> None:
        _view_to_phantom_set.pop(view.id(), None)
