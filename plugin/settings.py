from __future__ import annotations

from functools import lru_cache
from typing import Any

import jmespath
import sublime

from .constants import PACKAGE_NAME


@lru_cache
def _compile_jmespath_expression(expression: str) -> jmespath.parser.ParsedResult:
    return jmespath.compile(expression)


def get_plugin_settings() -> sublime.Settings:
    return sublime.load_settings(f"{PACKAGE_NAME}.sublime-settings")


def get_plugin_setting(key: str, default: Any = None) -> Any:
    return get_plugin_settings().get(key, default)


def get_plugin_setting_dotted(dotted: str, default: Any = None) -> Any:
    return _compile_jmespath_expression(dotted).search(get_plugin_settings()) or default
