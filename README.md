# Nobody 3

<div align="center">

![Nobody 3](https://img.shields.io/badge/version-1.0.2-blue.svg)
![Python](https://img.shields.io/badge/python-3.12-blue.svg)
![PyQt5](https://img.shields.io/badge/PyQt5-5.15.10-green.svg)
![License](https://img.shields.io/badge/license-Open%20Source-lightgrey.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)

**A cross-platform personal media manager and player**

[English](README.md) | [한국어](README.ko.md)

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Development](#-development) • [Contributing](#-contributing)

</div>

---

## 📖 Overview

Nobody 3 is a desktop application that combines browsing, downloading, and playing media content from YouTube, YouTube Music, and SoundCloud in a single, elegant interface. Built with PyQt5 for native performance across Windows, macOS, and Linux.

### Why Nobody 3?

- **Unified Experience**: Browse, search, download, and play—all in one app
- **Privacy-Focused**: Keep your media local, no cloud required
- **Lightweight**: ~50MB bundle size (vs 100MB+ for Electron apps)
- **Native Performance**: Built with PyQt5, not a web wrapper
- **Open Source**: Full source code available, contributions welcome

---

## ✨ Features

### Core Features
- 🎬 **Integrated Browser**: Built-in browser for YouTube, YouTube Music, and SoundCloud
- 📋 **Format Selection**: Choose from multiple video/audio formats with quality indicators
- 🎵 **Local Playback**: Built-in media player with mini player mode
- 🎨 **Dark Theme**: Eye-friendly interface for extended use
- ⚡ **FFmpeg Integration**: Automatic download and bundling (Windows)
- 🔒 **Security**: URL validation, filename sanitization, SSL verification

### 2025 Updates
- ✨ Mini player mode with always-on-top option
- 🔧 Enhanced format selection UI
- 📦 FFmpeg included builds (Windows)
- 🌐 Improved cross-platform compatibility
- 🔐 Security improvements (input validation, path sanitization)

---

## 📸 Screenshots

### Main Interface
![Main Interface](resource/img/Main%20Interface.png)

*Main window with integrated browser and video table*

### Format Selection
![Format Selection](resource/img/Format%20Selection.png)

*Format selection table with quality indicators*

### Mini Player
![Mini Player](resource/img/Mini%20Player.png)

*Compact mini player with always-on-top option*

### Settings Dialog
![Settings Dialog](resource/img/Settings%20Dialog.png)

*Settings dialog with collapsible sections*

---

## 🛠️ Installation

### Option 1: Pre-built Executables (Recommended)

Download the latest release for your platform:

- **Windows**: [Download `Nobody3-Windows.zip`](https://github.com/octxxiii/Nobody3/releases)
- **macOS**: [Download `Nobody3-macOS.zip`](https://github.com/octxxiii/Nobody3/releases)
- **Linux**: [Download `Nobody3-Linux.tar.gz`](https://github.com/octxxiii/Nobody3/releases)

**Windows**: Extract and run `Nobody3.exe`  
**macOS**: Extract and open `Nobody3.app`  
**Linux**: Extract and run `./Nobody3`

### Option 2: Build from Source

#### Prerequisites
- Python 3.12 or higher
- pip

#### Steps
```bash
# Clone the repository
git clone https://github.com/octxxiii/Nobody3.git
cd Nobody3

# Install dependencies
pip install -r requirements.txt

# Run the application
python -m Nobody.main
```

#### Building Executables
```bash
# Windows
pyinstaller --clean --noconfirm Nobody3.spec

# macOS/Linux
chmod +x build_macos.sh  # or build_linux.sh
./build_macos.sh
```

---

## 📖 Usage

### Basic Workflow

1. **Launch the app**: Run the executable or `python -m Nobody.main`
2. **Browse content**: Use the integrated browser to find videos/music
3. **Copy URL**: Click the "CopyURL" button or paste a URL manually
4. **Select format**: Choose your preferred format from the table
5. **Download**: Click the download button to save to your selected directory

### Mini Player

- Click the minimize button to switch to mini player mode
- Toggle always-on-top with the pin button
- Control playback without switching windows

### Format Settings

Access format filters via the settings menu:
- Show/hide video formats
- Show/hide audio formats
- Set maximum quality/resolution

---

## 🏗️ Architecture

```
Nobody/
├── main.py                 # Application entry point
├── config/                 # Configuration
│   └── constants.py       # Theme and constants
├── models/                 # Domain models
│   └── settings.py        # App settings
├── services/               # Background workers
│   ├── searcher.py        # Metadata fetcher
│   ├── downloader.py      # Download worker
│   └── ffmpeg_checker.py  # FFmpeg download
├── utils/                  # Utilities
│   ├── cache.py           # Cache directory helpers
│   ├── logging.py         # Logging setup
│   ├── ffmpeg.py          # FFmpeg discovery
│   └── security.py        # Security utilities
└── views/                  # UI components
    ├── main_window.py     # Main window
    ├── mini_player.py     # Mini player controller
    ├── video_table.py     # Table manager
    ├── presenter.py       # Business logic
    └── layout_builder.py  # UI layout
```

### Design Patterns

- **MVP (Model-View-Presenter)**: Separation of concerns
- **Service Layer**: Background tasks in QThread
- **Utility Layer**: Reusable helper functions

---

## 🔧 Development

### Setup Development Environment

```bash
# Clone and install
git clone https://github.com/octxxiii/Nobody3.git
cd Nobody3
pip install -r requirements.txt

# Run tests
pytest

# Run with logging
python -m Nobody.main
```

### Project Structure

```
.
├── Nobody/            # Application source package
├── docs/              # Documentation
├── scripts/           # Build and deployment scripts
├── tests/             # Unit tests (pytest)
├── legacy/            # Legacy code (reference)
└── releases/          # Release packages
```

### Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=Nobody

# Run specific test file
pytest tests/test_video_table.py
```

### Logging

Logs are written to:
- **Windows**: `%LOCALAPPDATA%\Nobody 3\Caches\nobody3.log`
- **macOS**: `~/Library/Caches/Nobody 3/nobody3.log`
- **Linux**: `~/.cache/Nobody 3/nobody3.log`

---

## 🔒 Security

### Implemented Security Features

- ✅ **SSL/TLS Verification**: Certificate checking enabled
- ✅ **URL Validation**: SSRF protection, protocol whitelist
- ✅ **Filename Sanitization**: Path traversal prevention
- ✅ **Input Validation**: User input sanitization

See [SECURITY_AUDIT.md](SECURITY_AUDIT.md) for details.

---

## 📦 Dependencies

- **PyQt5** (5.15.10): GUI framework
- **PyQtWebEngine** (≥5.15.7): Embedded browser
- **yt-dlp** (≥2023.12.30): Media extraction
- **requests** (≥2.31.0): HTTP client
- **FFmpeg**: Media processing (auto-downloaded on Windows)

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### How to Contribute

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Code Style

- Follow PEP 8 for Python code
- Use type hints where applicable
- Add docstrings for public functions/classes
- Write tests for new features

---

## 📝 License

This project is open source. Please use responsibly and respect copyright laws.

**Important**: This tool is for personal use only. Downloaded content is copyrighted by the original creators. Unauthorized distribution or commercial use is illegal.

---

## 🙏 Acknowledgments

- **yt-dlp**: Media extraction engine
- **FFmpeg**: Media processing
- **PyQt5**: GUI framework
- **Python Community**: For amazing tools and libraries

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/octxxiii/Nobody3/issues)
- **Discussions**: [GitHub Discussions](https://github.com/octxxiii/Nobody3/discussions)

---

<div align="center">

**Made with ❤️ by nobody**

⭐ Star this repo if you find it useful!

</div>
