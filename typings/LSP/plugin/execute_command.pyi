import sublime
from ..protocol import ExecuteCommandParams as ExecuteCommandParams
from .core.logging import debug as debug
from .core.protocol import Error as Error
from .core.registry import LspTextCommand as LspTextCommand
from .core.views import first_selection_region as first_selection_region, offset_to_point as offset_to_point, region_to_range as region_to_range, text_document_identifier as text_document_identifier, text_document_position_params as text_document_position_params, uri_from_view as uri_from_view, versioned_text_document_identifier as versioned_text_document_identifier
from typing import Any

class LspExecuteCommand(LspTextCommand):
    """
    Helper command for triggering workspace/executeCommand requests.
    """
    def run(self, edit: sublime.Edit, command_name: str | None = None, command_args: list[Any] | None = None, session_name: str | None = None, event: dict | None = None) -> None: ...
    def handle_success_async(self, result: Any, command_name: str) -> None:
        """
        Override this method to handle successful response to workspace/executeCommand.

        :param result: The result returned from the server.
        :param command_name: The name of the command that was executed.
        """
    def handle_error_async(self, error: Error, command_name: str) -> None:
        """
        Override this method to handle failed response to workspace/executeCommand.

        :param error: The Error object.
        :param command_name: The name of the command that was executed.
        """
    def _expand_variables(self, command_args: list[Any]) -> list[Any]: ...
