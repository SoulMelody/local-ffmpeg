"""
Command-line interface for local-ffmpeg
"""

import argparse
import sys
from typing import List

# 상대 임포트 대신 절대 임포트 사용
from local_ffmpeg import install, is_installed, uninstall, __version__


def main(args: List[str] = None) -> int:
    """
    Command-line entry point

    Args:
        args: Command line arguments (defaults to sys.argv[1:])

    Returns:
        Exit code (0 for success, non-zero for error)
    """
    parser = argparse.ArgumentParser(description="Install, check, or uninstall FFmpeg locally for your project")

    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # Install command
    install_parser = subparsers.add_parser("install", help="Install FFmpeg locally")
    install_parser.add_argument(
        "--path", default="./ffmpeg/", help="Path where FFmpeg will be installed (default: ./ffmpeg/)"
    )

    # Check command
    check_parser = subparsers.add_parser("check", help="Check if FFmpeg is installed")
    check_parser.add_argument("--path", default="./ffmpeg/", help="Path where FFmpeg is installed (default: ./ffmpeg/)")

    # Uninstall command
    uninstall_parser = subparsers.add_parser("uninstall", help="Uninstall FFmpeg")
    uninstall_parser.add_argument(
        "--path", default="./ffmpeg/", help="Path where FFmpeg is installed (default: ./ffmpeg/)"
    )

    # Version command
    subparsers.add_parser("version", help="Show version information")

    # Parse arguments
    args = parser.parse_args(args)

    # Handle commands
    if args.command == "install":
        success, message = install(args.path)
        print(message)
        return 0 if success else 1

    elif args.command == "is_installed":
        installed = is_installed(args.path)
        if installed:
            print(f"FFmpeg is installed at {args.path}")
        else:
            print(f"FFmpeg is not installed at {args.path}")
        return 0 if installed else 1

    elif args.command == "uninstall":
        success = uninstall(args.path)
        if success:
            print(f"FFmpeg uninstalled from {args.path}")
        else:
            print(f"Failed to uninstall FFmpeg from {args.path}")
        return 0 if success else 1

    elif args.command == "version":
        print(f"local-ffmpeg version {__version__}")
        return 0

    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())
