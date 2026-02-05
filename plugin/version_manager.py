from __future__ import annotations

from functools import cached_property

from .constants import PLATFORM_ARCH, SERVER_VERSION


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

    @cached_property
    def server_version(self) -> str:
        """The server version without a "v" prefix."""
        return SERVER_VERSION.lstrip("v")

    @cached_property
    def server_download_url(self) -> str:
        """The URL for downloading the server tarball."""
        return self.DOWNLOAD_URL_TEMPLATE.format(
            tarball_name=self.THIS_TARBALL_NAME.format(version=self.server_version),
            version=self.server_version,
        )


version_manager = VersionManager()
