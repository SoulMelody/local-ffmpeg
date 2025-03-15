"""
Local-FFmpeg - Automatically download and install FFmpeg binaries locally for your project
"""

import os
import sys
import subprocess
from typing import Tuple, Optional

# 상대 임포트 대신 절대 임포트 사용
from local_ffmpeg.__download import download_url
from local_ffmpeg.__platform import get_platform_handler

__version__ = "0.1.0"

# Export public API
__all__ = ["install", "uninstall", "is_installed"]


def install(path: str = "./ffmpeg/") -> Tuple[bool, str]:
    """
    Download and install FFmpeg binaries to the specified path.

    Args:
        path: Directory where FFmpeg binaries will be installed

    Returns:
        Tuple of (success, message) where success is a boolean indicating if the
        installation was successful, and message is a string with details
    """
    try:
        # Ensure the directory exists
        os.makedirs(path, exist_ok=True)

        # Get platform-specific handler
        platform_handler = get_platform_handler()

        # If already installed, return success
        if platform_handler.check_installed(path):
            return True, "FFmpeg is already installed"

        # Download FFmpeg
        download_path = download_url(platform_handler.get_download_url())

        if not download_path:
            return False, "Failed to download FFmpeg binaries"

        # Install FFmpeg
        platform_handler.install(download_path, path)

        # Verify installation
        if platform_handler.check_installed(path):
            return True, f"FFmpeg installed successfully to {path}"
        else:
            return False, f"Failed to verify FFmpeg installation in {path}"

    except Exception as e:
        return False, f"Error installing FFmpeg: {str(e)}"


def uninstall(path: str = "./ffmpeg/") -> bool:
    """
    Uninstall FFmpeg binaries from the specified path.

    Args:
        path: Directory where FFmpeg binaries are installed

    Returns:
        True if successful, False otherwise
    """
    try:
        platform_handler = get_platform_handler()
        platform_handler.uninstall(path)
        return True
    except Exception as e:
        print(f"Error uninstalling FFmpeg: {e}")
        return False


def is_installed(path: str = "./ffmpeg/") -> bool:
    """
    Check if FFmpeg is installed at the specified path or available in PATH.

    Args:
        path: Directory to check for FFmpeg binaries

    Returns:
        True if FFmpeg is installed and available, False otherwise
    """
    try:
        # Check if path is provided and FFmpeg exists at that path
        if path:
            platform_handler = get_platform_handler()
            return platform_handler.check_installed(path)

        # If no path provided or path doesn't exist, check if FFmpeg is in system PATH
        subprocess.run(["ffmpeg", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return True
    except (subprocess.SubprocessError, FileNotFoundError):
        return False


def main() -> None:
    """Command-line entry point (simplified - use __main__.py for full CLI)"""
    # 실행 시 __main__.py의 main 함수를 호출합니다
    from local_ffmpeg.__main__ import main as main_cli

    sys.exit(main_cli())
