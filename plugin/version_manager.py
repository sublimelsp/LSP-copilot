from __future__ import annotations

import io
from pathlib import Path

from LSP.plugin import AbstractPlugin

from .constants import PACKAGE_NAME, PLATFORM_ARCH
from .log import log_info
from .utils import decompress_buffer, rmtree_ex, simple_urlopen


class VersionManager:
    # https://github.com/github/copilot-language-server-release
    DOWNLOAD_URL_TEMPLATE = (
        "https://github.com/github/copilot-language-server-release/releases/download/{version}/{tarball_name}"
    )

    TARBALL_NAMES = {
        "linux_arm64": "copilot-language-server-linux-arm64-{version}.zip",
        "linux_x64": "copilot-language-server-linux-x64-{version}.zip",
        "osx_arm64": "copilot-language-server-darwin-arm64-{version}.zip",
        "osx_x64": "copilot-language-server-darwin-x64-{version}.zip",
        "windows_x64": "copilot-language-server-win32-x64-{version}.zip",
    }
    """`platform_arch`-specific tarball names for the server."""
    THIS_TARBALL_NAME = TARBALL_NAMES[PLATFORM_ARCH]
    """The tarball name for the current platform architecture."""

    TARBALL_BIN_PATHS = {
        "linux_arm64": "copilot-language-server",
        "linux_x64": "copilot-language-server",
        "osx_arm64": "copilot-language-server",
        "osx_x64": "copilot-language-server",
        "windows_x64": "copilot-language-server.exe",
    }
    """`platform_arch`-specific relative path of the server executable in the tarball."""
    THIS_TARBALL_BIN_PATH = TARBALL_BIN_PATHS[PLATFORM_ARCH]
    """The relative path of the server executable in the tarball for the current platform architecture."""

    def __init__(self) -> None:
        self.client_cls: type[AbstractPlugin] | None = None
        self.server_version = ""

    @property
    def server_download_url(self) -> str:
        """The URL for downloading the server tarball."""
        return self.DOWNLOAD_URL_TEMPLATE.format(
            tarball_name=self.THIS_TARBALL_NAME.format(version=self.server_version),
            version=self.server_version,
        )

    @property
    def plugin_storage_dir(self) -> Path:
        """The storage directory for this plugin."""
        assert self.client_cls, "VersionManager.client_cls must be set to a subclass of Abstract"
        return Path(self.client_cls.storage_path()) / PACKAGE_NAME

    @property
    def versioned_server_dir(self) -> Path:
        """The directory specific to the current server version."""
        return self.plugin_storage_dir / f"v{self.server_version}"

    @property
    def server_path(self) -> Path:
        """The path of the language server binary."""
        return self.versioned_server_dir / self.THIS_TARBALL_BIN_PATH

    @property
    def is_installed(self) -> bool:
        """Checks if the server executable is already installed."""
        return self.server_path.is_file()

    def install_server(self) -> None:
        """Installs the server executable."""
        rmtree_ex(self.plugin_storage_dir, ignore_errors=True)  # delete old versions

        log_info(f"Downloading server tarball: {self.server_download_url}")
        data = simple_urlopen(self.server_download_url)

        decompress_buffer(
            io.BytesIO(data),
            filename=self.THIS_TARBALL_NAME,
            dst_dir=self.versioned_server_dir,
        )
        # make the server binary executable (required on Mac/Linux)
        self.server_path.chmod(0o755)


version_manager = VersionManager()
