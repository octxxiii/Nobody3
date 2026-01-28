# Nobody 3 — A Small Tool That Returns Choice to You

A lightweight personal media tool — built to give freedom back to the user.

English | 한국어

---

## 🧠 Philosophy

Every product is a means to an end.  
Nobody 3 is not a final destination — it is a tool that takes someone somewhere.

### 1. Problem
We no longer own our music or video.  
Streaming is convenient, but our taste has been consumed by algorithms.

### 2. Emotion
Our freedom to choose is shrinking.  
Subscriptions rise, and what we want fades away.

### 3. Solution (Nobody 3)
Nobody 3 disrupts the flow.  
It lets you listen, watch, save, and create — **on your own terms.**

### 4. Future
No one knows where this tool will take you.  
That’s why it’s called **Nobody.**

---

## 🚀 What Nobody 3 Enables
- Choose ownership over subscription
- Build your personal media space
- Disconnect from algorithmic noise
- Create without permission
- Keep your world local & private

Nobody 3 is not just a downloader.  
It is a way to reclaim your time — and **a starting point for creativity.**

---

## ✨ Features
- Integrated browser for YouTube / YouTube Music / SoundCloud
- Built-in mini player with always-on-top mode
- Selectable formats & resolutions (via yt-dlp)
- Local playback & personal library structure
- FFmpeg integrated (Windows: auto-download)
- Lightweight PyQt5 native performance (~50MB)
- Privacy-first (no analytics, no cloud, no tracking)

---

## 📸 Screenshots

### Main Interface
![Main Interface](resource/img/Main%20Interface.png)

### Format Selection
![Format Selection](resource/img/Format%20Selection.png)

### Mini Player
![Mini Player](resource/img/Mini%20Player.png)

### Settings Dialog
![Settings Dialog](resource/img/Settings%20Dialog.png)

---

## 📦 Installation

Releases:  
https://github.com/octxxiii/Nobody3/releases

```bash
git clone https://github.com/octxxiii/Nobody3.git
cd Nobody3
pip install -r requirements.txt
python -m Nobody.main

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
