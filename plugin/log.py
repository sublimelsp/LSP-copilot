from __future__ import annotations

from typing import Any

import sublime

from .constants import PACKAGE_NAME


def log_debug(message: str) -> None:
    print(f"[{PACKAGE_NAME}][DEBUG] {message}")


def log_info(message: str) -> None:
    print(f"[{PACKAGE_NAME}][INFO] {message}")


def log_warning(message: str) -> None:
    print(f"[{PACKAGE_NAME}][WARNING] {message}")


def log_error(message: str) -> None:
    print(f"[{PACKAGE_NAME}][ERROR] {message}")


def pluginfy_msg(msg: str, *args: Any, **kwargs: Any) -> str:
    return msg.format(*args, _=PACKAGE_NAME, **kwargs)


def console_msg(msg: str, *args: Any, **kwargs: Any) -> None:
    print(pluginfy_msg(msg, *args, **kwargs))


def status_msg(msg: str, *args: Any, **kwargs: Any) -> None:
    sublime.status_message(pluginfy_msg(msg, *args, **kwargs))


def info_box(msg: str, *args: Any, **kwargs: Any) -> None:
    sublime.message_dialog(pluginfy_msg(msg, *args, **kwargs))


def error_box(msg: str, *args: Any, **kwargs: Any) -> None:
    sublime.error_message(pluginfy_msg(msg, *args, **kwargs))
