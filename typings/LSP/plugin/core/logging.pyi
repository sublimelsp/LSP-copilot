from .constants import ST_PACKAGES_PATH as ST_PACKAGES_PATH
from typing import Any

log_debug: bool

def set_debug_logging(logging_enabled: bool) -> None: ...
def debug(*args: Any) -> None:
    '''Print args to the console if the "debug" setting is True.'''
def trace() -> None: ...
def exception_log(message: str, ex: Exception) -> None: ...
def printf(*args: Any, prefix: str = 'LSP') -> None:
    """Print args to the console, prefixed by the plugin name."""
