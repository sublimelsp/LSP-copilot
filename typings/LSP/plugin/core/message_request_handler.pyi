import sublime
from ...protocol import MessageType, ShowMessageRequestParams as ShowMessageRequestParams
from .protocol import Response as Response
from .sessions import Session as Session
from .views import show_lsp_popup as show_lsp_popup, text2html as text2html
from _typeshed import Incomplete
from typing import Any

ICONS: dict[MessageType, str]

class MessageRequestHandler:
    session: Incomplete
    request_id: Incomplete
    request_sent: bool
    view: Incomplete
    actions: Incomplete
    action_titles: Incomplete
    message: Incomplete
    message_type: Incomplete
    source: Incomplete
    def __init__(self, view: sublime.View, session: Session, request_id: Any, params: ShowMessageRequestParams, source: str) -> None: ...
    def show(self) -> None: ...
    def _send_user_choice(self, href: int = -1) -> None: ...
