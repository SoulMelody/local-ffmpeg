"""
macOS-specific implementation for FFmpeg installation
"""

import os
import pathlib
import platform
import shutil
import subprocess
import zipfile
from typing import Optional, Dict

__all__ = ["MacOSHandler"]


class MacOSHandler:
    """Handler for macOS platform"""

    def get_download_url(self) -> str:
        """
        Get the appropriate FFmpeg download URLs for macOS

        Returns:
            Dictionary with URLs for each binary (ffmpeg, ffplay, ffprobe)

        Raises:
            RuntimeError: Unsupported macOS architecture
        """
        # Get system architecture
        arch = platform.machine()

        # Map architecture to appropriate URL format
        if arch == "x86_64":
            return "https://github.com/ColorsWind/FFmpeg-macOS/releases/download/n5.0.1-patch3/FFmpeg_shared-n5.0.1-OSX-x86_64.zip"
        elif arch == "arm64":
            return "https://github.com/ColorsWind/FFmpeg-macOS/releases/download/n5.0.1-patch3/FFmpeg-shared-n5.0.1-OSX-arm64.zip"
        else:
            raise RuntimeError(f"Unsupported macOS architecture: {arch}")

    def install(self, download_path: str, install_path: str) -> None:
        """
        Install FFmpeg on macOS using osxexperts.net builds

        Args:
            download_path: Path to the directory containing downloaded archives
            install_path: Directory where FFmpeg binaries will be installed
        """
        # Create installation directory if it doesn't exist
        os.makedirs(install_path, exist_ok=True)

        try:
            # Extract the binary from the zip file
            with zipfile.ZipFile(download_path, "r") as zip_ref:
                # List files in the archive
                for file_info in zip_ref.infolist():
                    if "bin/" in file_info.filename or "lib/" in file_info.filename:
                        zip_ref.extract(file_info, path=os.path.dirname(download_path))
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

            print(f"FFmpeg has been installed to {install_path}")

        except Exception as e:
            raise RuntimeError(f"Failed to install FFmpeg: {str(e)}")

    def uninstall(self, install_path: str) -> None:
        """
        Uninstall FFmpeg from macOS

        Args:
            install_path: Directory where FFmpeg binaries are installed
        """
        for dir in ("bin", "lib"):
            dir_path = os.path.join(install_path, dir)
            if os.path.exists(dir_path):
                shutil.rmtree(dir_path)

    def check_installed(self, path: Optional[str] = None) -> bool:
        # Check in specified path if provided
        if path and os.path.exists(path):
            missing = []
            for binary in ("ffmpeg", "ffprobe", "ffplay"):
                binary_path = os.path.join(path, binary)
                if not (os.path.exists(binary_path) and os.access(binary_path, os.X_OK)):
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

        # Global check if path is not provided
        for binary in ("ffmpeg", "ffprobe", "ffplay"):
            try:
                result = subprocess.run([binary, "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=5)
                if result.returncode != 0:
                    print(f"Global binary {binary} returned error code {result.returncode}.")
                    return False
            except (subprocess.SubprocessError, OSError) as e:
                print(f"Error while executing global binary {binary}: {e}")
                return False
        return True
