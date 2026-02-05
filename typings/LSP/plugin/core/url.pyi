import sublime
from ...protocol import DocumentUri as DocumentUri
from .constants import ST_INSTALLED_PACKAGES_PATH as ST_INSTALLED_PACKAGES_PATH, ST_PACKAGES_PATH as ST_PACKAGES_PATH
from typing import Any

def normalize_uri(uri: DocumentUri) -> DocumentUri: ...
def filename_to_uri(file_name: str) -> str:
    """
    Convert a file name obtained from view.file_name() into an URI
    """
def view_to_uri(view: sublime.View) -> str: ...
def uri_to_filename(uri: str) -> str:
    '''
    DEPRECATED: An URI associated to a view does not necessarily have a "file:" scheme.
    Use parse_uri instead.
    '''
def parse_uri(uri: str) -> tuple[str, str]:
    """
    Parses an URI into a tuple where the first element is the URI scheme. The
    second element is the local filesystem path if the URI is a file URI,
    otherwise the second element is the original URI.
    """
def unparse_uri(parsed_uri: tuple[str, str]) -> str:
    """
    Reverse of `parse_uri()`.
    """
def _to_resource_uri(path: str, prefix: str) -> str:
    """
    Terrible hacks from ST core leak into packages as well.

    See: https://github.com/sublimehq/sublime_text/issues/3742
    """
def _uppercase_driveletter(match: Any) -> str:
    """
    For compatibility with Sublime's VCS status in the status bar.
    """
