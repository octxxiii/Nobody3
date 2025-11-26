# Nobody 3 v1.0.1 Release Notes

**Youtube/Music Converter & Player**

**Release: 2025-11-26**

## 🐛 Bug Fixes

### Critical Fix: WebEngine Crash on Windows
- **Fixed**: Qt5WebEngineCore.dll memory access violation (0xc0000005)
- **Root Cause**: System date changes and Windows Store Python sandbox corrupted WebEngine profile data
- **Solution**: 
  - **Forced profile reset** on every startup (no residual cache survives)
  - Automatic detection/removal of corrupted files with abnormal timestamps (e.g., from 2015)
  - Robust fallback that deletes the entire profile if any corruption is detected
  - Improved WebEngine initialization with proper parent widget assignment
  - Longer delayed URL loading to ensure WebEngine is fully initialized before navigation

### WebEngine Initialization Improvements
- Defensive creation of `QWebEngineView` with placeholder fallback (prevents hard crash)
- Delayed URL loading increased to 500 ms for stability on slower systems
- Added Windows-specific Chromium flags (`--disable-gpu --disable-software-rasterizer`)
- Added sandbox/logging disable toggles to reduce WebEngine overhead
- Improved error handling and logging for WebEngine operations

## 🔧 Technical Changes

### New Features
- **Profile Validation**: Automatic detection and cleanup of corrupted WebEngine profiles
- **Forced Reset Mode**: Ability to fully clear the profile when validation is inconclusive
- **Safe Recovery**: Placeholder widget shown when WebEngine cannot initialize

### Code Improvements
- Enhanced `cache.py` with `clear_webengine_profile()` + stricter validation heuristics
- Reworked WebEngine initialization sequence in `layout_builder.py`
- Added Windows-specific environment variable configuration in `main.py`
- Broader exception handling across initialization path

## 📋 Migration Notes

- **No action required**: The fix is automatic and transparent
- If you experience crashes, the application will automatically clean corrupted profiles on next startup
- All cached data (cookies, localStorage) may be cleared if corruption is detected

## 📅 Release Date

2025-11-26

---

**Made with ❤️ by nobody**

