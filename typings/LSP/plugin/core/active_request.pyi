from .progress import ProgressReporter as ProgressReporter, ViewProgressReporter as ViewProgressReporter, WindowProgressReporter as WindowProgressReporter
from .protocol import Request as Request
from .sessions import SessionViewProtocol as SessionViewProtocol
from _typeshed import Incomplete
from typing import Any

class ActiveRequest:
    """
    Holds state per request.
    """
    weaksv: Incomplete
    request_id: Incomplete
    request: Incomplete
    canceled: bool
    progress: ProgressReporter | None
    def __init__(self, sv: SessionViewProtocol, request_id: int, request: Request[Any, Any]) -> None: ...
    def on_request_canceled_async(self) -> None: ...
    def _start_progress_reporter_async(self, title: str, message: str | None = None, percentage: float | None = None) -> ProgressReporter | None: ...
    def update_progress_async(self, params: dict[str, Any]) -> None: ...
