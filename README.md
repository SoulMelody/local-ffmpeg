# 🎬 Local-FFmpeg

[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org)
[![Platform: Windows | Linux | macOS](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)](https://github.com/BtbN/FFmpeg-Builds)
[![FFmpeg](https://img.shields.io/badge/ffmpeg-master--latest-orange.svg)](https://ffmpeg.org/)

## 🚀 Overview

local-ffmpeg is a Python utility that automatically downloads and installs FFmpeg, FFplay, and FFprobe binaries for your operating system. It handles platform-specific installations and configurations so you can easily use FFmpeg in your projects.

This library is installed as a local dependency of your project, not as a system-wide installation.

## ✨ Features

- 🔄 Automatic detection of your operating system and architecture
- 📥 Download FFmpeg binaries optimized for environment
- 🛠️ Installs FFmpeg, FFplay, and FFprobe locally
- ✅ Verifies successful installation
- 🧹 Cleans up unnecessary files after installation

## 📋 Requirements

- Python 3.6+
- Internet connection (for downloading FFmpeg)

## 🔧 Installation

```bash
# Using pip
pip install local-ffmpeg
```

```bash
# Or clone the repository
git clone https://github.com/atsuiyo/local-ffmpeg
cd local-ffmpeg
pip install -e .
```


## 💻 Usage

### 🐍 Python API

```python
from local_ffmpeg import is_installed, install

# Check if FFmpeg is already installed
if not is_installed(path="./custom/path"):
    # Install FFmpeg if not found
    success, message = install(path="./custom/path")
    if success:
        print(message)  # FFmpeg installed successfully
    else:
        print(f"Error: {message}")
else:
    print("FFmpeg is already installed")
```

### 🖥️ Command Line Interface

#### 🚀 Install FFmpeg (default path: ./ffmpeg)
```bash
python -m local_ffmpeg install
```
#### 📁 Install FFmpeg to a custom path
```bash
python -m local_ffmpeg install --path /custom/path
```
#### 🔍 Check if FFmpeg is installed (default path: ./ffmpeg)
```bash
python -m local_ffmpeg is_installed
```
#### 🔎 Check if FFmpeg is installed at a custom path
```bash
python -m local_ffmpeg is_installed --path /custom/path
```
#### ℹ️ Show help information
```bash
python -m local_ffmpeg --help
```

## 🔍 How It Works

The installer:
1. 🔍 Detects your operating system and architecture
2. 📥 Downloads the appropriate FFmpeg build:
   - Windows/Linux: BtbN's GitHub repository (version latest)
   - macOS (Intel & Apple Silicon): osxexperts.net builds (version 7.1)
3. 📦 Extracts the files to a temporary directory
4. 📋 Copies the executables to a local directory
5. 🔒 Makes the executables executable (chmod)
6. 🧹 Cleans up temporary files

## 📦 Supported Platforms

- **Windows**: 64-bit (win64)
- **Linux**:
  - x86_64/amd64
  - aarch64/arm64
- **macOS**:
  - x86_64 (Intel) - via osxexperts.net
  - arm64 (Apple Silicon M1/M2) - via osxexperts.net

## 🗺️ Roadmap
### 📋 TODO
 [ ] Add functionality to install a specified version
### ✅ Completed
 ✅ 🍏 Add macOS (OS X) support for direct installation without requiring Homebrew

## 📢 Important Notes

- On macOS:
  - Both Intel Macs (x86_64) and Apple Silicon Macs (arm64) use builds from osxexperts.net
  - macOS builds are based on FFmpeg version 7.1
  - **The ffmpeg, ffplay, and ffprobe files provided by osxexperts.net are for educational purposes only.**
  - If you encounter issues, you can still use `brew install ffmpeg` as an alternative
  - The installer uses GPL-licensed FFmpeg builds
  - The default installation path is a directory "ffmpeg" in the same location as the script

## 🔗 Links

- [FFmpeg Official Website](https://ffmpeg.org/)
- [BtbN FFmpeg Builds](https://github.com/BtbN/FFmpeg-Builds)
- [OSXExperts.net FFmpeg Builds for macOS](https://www.osxexperts.net/)
