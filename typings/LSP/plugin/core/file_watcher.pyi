from ...protocol import FileChangeType, WatchKind
from _typeshed import Incomplete
from abc import ABCMeta, abstractmethod
from typing import Protocol

DEFAULT_WATCH_KIND: Incomplete
FileWatcherEventType: Incomplete
FilePath = str
FileWatcherEvent = tuple[FileWatcherEventType, FilePath]

def lsp_watch_kind_to_file_watcher_event_types(kind: WatchKind) -> list[FileWatcherEventType]: ...
def file_watcher_event_type_to_lsp_file_change_type(kind: FileWatcherEventType) -> FileChangeType: ...

class FileWatcherProtocol(Protocol):
    def on_file_event_async(self, events: list[FileWatcherEvent]) -> None:
        """
        Called on file watcher events.
        This API must be triggered on async thread.

        :param events: The list of events to notify about.
        """

class FileWatcher(metaclass=ABCMeta):
    """
    A public interface of a file watcher implementation.

    The interface implements the file watcher and notifies the `handler` (through the `on_file_event_async` method)
    on file event changes.
    """
    @classmethod
    @abstractmethod
    def create(cls, root_path: str, patterns: list[str], events: list[FileWatcherEventType], ignores: list[str], handler: FileWatcherProtocol) -> FileWatcher:
        """
        Creates a new instance of the file watcher.

        :param patterns: The list of glob pattern to enable watching for.
        :param events: The type of events that should be watched.
        :param ignores: The list of glob patterns that should excluded from file watching.

        :returns: A new instance of file watcher.
        """
    @abstractmethod
    def destroy(self) -> None:
        """
        Called before the file watcher is disabled.
        """

watcher_implementation: type[FileWatcher] | None

def register_file_watcher_implementation(file_watcher: type[FileWatcher]) -> None: ...
def get_file_watcher_implementation() -> type[FileWatcher] | None: ...
