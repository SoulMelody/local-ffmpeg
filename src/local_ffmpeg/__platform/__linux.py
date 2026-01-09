"""
Linux-specific implementation for FFmpeg installation
"""

import os
import pathlib
import platform
import shutil
import subprocess
import tarfile
from typing import List, Optional

__all__ = ["LinuxHandler"]


class LinuxHandler:
    """Handler for Linux platform"""

    def get_download_url(self) -> str:
        """
        Get the appropriate FFmpeg download URL for the current Linux architecture

        Returns:
            URL to download FFmpeg from

        Raises:
            RuntimeError: If architecture is unsupported
        """
        arch = platform.machine().lower()
        base_url = "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest"

        if arch in ("x86_64", "amd64"):
            return f"{base_url}/ffmpeg-master-latest-linux64-gpl-shared.tar.xz"
        elif arch in ("aarch64", "arm64"):
            return f"{base_url}/ffmpeg-master-latest-linuxarm64-gpl-shared.tar.xz"
        else:
            raise RuntimeError(f"Unsupported Linux architecture: {arch}")

    def install(self, download_path: str, install_path: str) -> None:
        """
        Install FFmpeg from downloaded archive to the specified path

        Args:
            download_path: Path to the downloaded archive
            install_path: Directory where FFmpeg binaries will be installed

        Raises:
            RuntimeError: If installation fails
        """
        # Create temporary directory for extraction
        try:
            print(f"Extracting FFmpeg archive...")

            # Extract .tar.xz file
            with tarfile.open(download_path, "r:xz") as tar:
                # Extract only bin directory (usually in a subdirectory)
                members = []
                for member in tar.getmembers():
                    if "bin/" in member.name or "lib/" in member.name:
                        members.append(member)

                if not members:
                    raise RuntimeError("No FFmpeg binaries found in archive")

                tar.extractall(path=os.path.dirname(download_path), members=members)

            # Find and move the binaries to the install path
            extracted_dir = os.path.dirname(download_path)
            for root, _, files in os.walk(extracted_dir):
                subdir = pathlib.Path(root).relative_to(extracted_dir).name
                if subdir == "bin":
                    os.makedirs(os.path.join(install_path, subdir), exist_ok=True)
                    for file in files:
                        src = os.path.join(root, file)
                        dst = os.path.join(install_path, subdir, file)
                        shutil.move(src, dst)
                        os.chmod(dst, 0o755)  # Make executable
                elif subdir == "lib":
                    os.makedirs(os.path.join(install_path, subdir), exist_ok=True)
                    for file in files:
                        src = os.path.join(root, file)
                        dst = os.path.join(install_path, subdir, file)
                        shutil.move(src, dst)

            # Clean up temporary files
            if os.path.exists(download_path):
                os.remove(download_path)

            print(f"FFmpeg installed successfully to {install_path}")

        except Exception as e:
            raise RuntimeError(f"Failed to install FFmpeg: {e}")

    def uninstall(self, install_path: str) -> None:
        """
        Uninstall FFmpeg from the specified path

        Args:
            install_path: Directory where FFmpeg binaries are installed
        """
        for dir in ("bin", "lib"):
            dir_path = os.path.join(install_path, dir)
            if os.path.exists(dir_path):
                shutil.rmtree(dir_path)

    def check_installed(self, path: Optional[str] = None) -> bool:
        """
        Check if FFmpeg is installed at the specified path

        Args:
            path: Directory to check for FFmpeg binaries

        Returns:
            True if FFmpeg is installed, False otherwise
        """
        if not path:
            print("FFmpeg installation path is not specified.")
            return False

        missing = []
        for binary in ("ffmpeg", "ffprobe", "ffplay"):
            binary_path = os.path.join(path, binary)
            if not os.path.exists(binary_path):
                missing.append(binary)
        if missing:
            print("Missing binaries:", ", ".join(missing))
            return False

        for binary in ("ffmpeg", "ffprobe", "ffplay"):
            binary_path = os.path.join(path, binary)
            try:
                result = subprocess.run(
                    [binary_path, "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=5
                )
                if result.returncode != 0:
                    print(f"Binary {binary} exists but returned error code {result.returncode}.")
                    return False
            except (subprocess.SubprocessError, OSError) as e:
                print(f"Error while executing {binary}: {e}")
                return False

        return True
