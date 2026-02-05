import sublime
from .logging import debug as debug, exception_log as exception_log, printf as printf
from .types import ClientConfig as ClientConfig
from .url import parse_uri as parse_uri
from .workspace import disable_in_project as disable_in_project, enable_in_project as enable_in_project
from _typeshed import Incomplete
from abc import ABCMeta, abstractmethod
from collections import deque
from datetime import datetime
from typing import Generator
from weakref import WeakSet

RETRY_MAX_COUNT: int
RETRY_COUNT_TIMEDELTA: Incomplete

class WindowConfigChangeListener(metaclass=ABCMeta):
    @abstractmethod
    def on_configs_changed(self, configs: list[ClientConfig]) -> None: ...

class WindowConfigManager:
    _window: Incomplete
    _global_configs: Incomplete
    _disabled_for_session: set[str]
    _crashes: dict[str, deque[datetime]]
    all: dict[str, ClientConfig]
    _change_listeners: WeakSet[WindowConfigChangeListener]
    def __init__(self, window: sublime.Window, global_configs: dict[str, ClientConfig]) -> None: ...
    def add_change_listener(self, listener: WindowConfigChangeListener) -> None: ...
    def get_config(self, config_name: str) -> ClientConfig | None: ...
    def get_configs(self) -> list[ClientConfig]: ...
    def match_view(self, view: sublime.View, include_disabled: bool = False) -> Generator[ClientConfig, None, None]:
        '''
        Yields configurations where:

        - the configuration\'s "selector" matches with the view\'s base scope, and
        - the view\'s URI scheme is an element of the configuration\'s "schemes".
        '''
    def update(self, updated_config_name: str | None = None) -> None: ...
    def _reload_configs(self, updated_config_name: str | None = None, notify_listeners: bool = False) -> None: ...
    def enable_config(self, config_name: str) -> None: ...
    def disable_config(self, config_name: str, only_for_session: bool = False) -> None: ...
    def record_crash(self, config_name: str, exit_code: int, exception: Exception | None) -> bool:
        """
        Signal that a session has crashed.

        Returns True if the session should be restarted automatically.
        """
    def _reenable_disabled_for_session(self, config_name: str) -> bool: ...
