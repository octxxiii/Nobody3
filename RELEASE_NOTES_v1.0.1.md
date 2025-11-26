# Nobody 3 v1.0.1 Release Notes

**Youtube/Music Converter & Player**

**Release: 2025-01-XX**

## 🐛 Bug Fixes

### Critical Fix: WebEngine Crash on Windows
- **Fixed**: Qt5WebEngineCore.dll memory access violation (0xc0000005)
- **Root Cause**: System date changes during execution corrupted WebEngine profile data
- **Solution**: 
  - Added automatic profile validation and cleanup on startup
  - Detects and removes corrupted files with abnormal timestamps (e.g., from 2015)
  - Prevents crashes after system date changes
  - Improved WebEngine initialization with proper parent widget assignment
  - Added delayed URL loading to ensure proper initialization

### WebEngine Initialization Improvements
- Fixed QWebEngineView creation without parent widget (Windows compatibility)
- Added delayed URL loading using QTimer for stable initialization
- Added Windows-specific environment variables for software rendering fallback
- Improved error handling and logging for WebEngine operations

## 🔧 Technical Changes

### New Features
- **Profile Validation**: Automatic detection and cleanup of corrupted WebEngine profiles
- **Timestamp Validation**: Validates file timestamps to detect corruption from date changes
- **Safe Recovery**: Automatic profile cleanup on validation failure

### Code Improvements
- Enhanced `cache.py` with `validate_and_clean_profile()` function
- Improved WebEngine initialization sequence in `layout_builder.py`
- Added Windows-specific environment variable configuration in `main.py`
- Better error handling and logging throughout

## 📋 Migration Notes

- **No action required**: The fix is automatic and transparent
- If you experience crashes, the application will automatically clean corrupted profiles on next startup
- All cached data (cookies, localStorage) may be cleared if corruption is detected

## 📅 Release Date

2025-01-XX

---

**Made with ❤️ by nobody**

