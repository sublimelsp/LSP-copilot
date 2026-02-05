from __future__ import annotations

import json
from functools import cached_property

import jmespath
import sublime

from .constants import PACKAGE_NAME, PLATFORM_ARCH


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
        lock_file_content = sublime.load_resource(f"Packages/{PACKAGE_NAME}/language-server/package-lock.json")
        data = json.loads(lock_file_content)
        return jmespath.search('packages."node_modules/@github/copilot-language-server".version', data) or ""

    @cached_property
    def server_download_url(self) -> str:
        """The URL for downloading the server tarball."""
        return self.DOWNLOAD_URL_TEMPLATE.format(
            tarball_name=self.THIS_TARBALL_NAME,
            version=self.server_version,
        ).format(version=self.server_version)


version_manager = VersionManager()
