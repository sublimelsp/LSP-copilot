from ...protocol import DocumentUri as DocumentUri
from .sessions import Session as Session
from .views import parse_uri as parse_uri
from pathlib import Path
from typing import Iterable

def simple_path(session: Session | None, uri: DocumentUri) -> str: ...
def project_path(project_folders: Iterable[Path], file_path: Path) -> Path | None:
    """
    The project path of `/path/to/project/file` in the project `/path/to/project` is `file`.
    """
def simple_project_path(project_folders: Iterable[Path], file_path: Path) -> Path | None:
    """
    The simple project path of `/path/to/project/file` in the project `/path/to/project` is `project/file`.
    """
def resolve_simple_project_path(project_folders: Iterable[Path], file_path: Path) -> Path | None:
    """
    The inverse of `simple_project_path()`.
    """
def project_base_dir(project_folders: Iterable[Path], file_path: Path) -> Path | None:
    """
    The project base dir of `/path/to/project/file` in the project `/path/to/project` is `/path/to`.
    """
def split_project_path(project_folders: Iterable[Path], file_path: Path) -> tuple[Path, Path] | None: ...
