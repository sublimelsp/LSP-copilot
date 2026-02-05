import sublime
from ..protocol import DocumentUri as DocumentUri, Location as Location, LocationLink as LocationLink, Position as Position
from .core.constants import ST_PACKAGES_PATH as ST_PACKAGES_PATH, SublimeKind as SublimeKind
from .core.logging import debug as debug
from .core.sessions import Session as Session
from .core.views import get_uri_and_position_from_location as get_uri_and_position_from_location, location_to_human_readable as location_to_human_readable, to_encoded_filename as to_encoded_filename
from _typeshed import Incomplete

def open_location_async(session: Session, location: Location | LocationLink, side_by_side: bool, force_group: bool, group: int = -1) -> None: ...
def open_basic_file(session: Session, uri: str, position: Position, flags: sublime.NewFileFlags = ..., group: int | None = None) -> sublime.View | None: ...

class LocationPicker:
    _view: Incomplete
    _view_states: Incomplete
    _window: Incomplete
    _weaksession: Incomplete
    _side_by_side: Incomplete
    _force_group: Incomplete
    _group: Incomplete
    _items: Incomplete
    _highlighted_view: sublime.View | None
    def __init__(self, view: sublime.View, session: Session, locations: list[Location] | list[LocationLink], side_by_side: bool, force_group: bool = True, group: int = -1, placeholder: str = '', kind: SublimeKind = ..., selected_index: int = -1) -> None: ...
    def _unpack(self, index: int) -> tuple[Session | None, Location | LocationLink, DocumentUri, Position]: ...
    def _select_entry(self, index: int) -> None: ...
    def _highlight_entry(self, index: int) -> None: ...
