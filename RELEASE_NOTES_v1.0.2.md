# Nobody 3 v1.0.2 Release Notes

**Youtube/Music Converter & Player**

**Release: 2025-11-27**

## 🎯 Major Fix: Login State Preservation

### Critical Fix: Cache Management
- **Fixed**: Login state being lost on every program restart
- **Root Cause**: Aggressive cache clearing was deleting cookies and session data
- **Solution**: 
  - **Selective cache cleaning**: Only removes corrupted files, preserves login data
  - **Protected data**: Cookies, LocalStorage, SessionStorage, IndexedDB are now protected
  - **Conservative validation**: Profile validation is now very conservative to prevent login loss
  - **Smart cleanup**: Only removes files with clearly corrupted timestamps (e.g., from 2015)

### Protected Data
The following critical data is now preserved across restarts:
- **Cookies** (`Cookies`, `Cookies-journal`) - Login sessions
- **Local Storage** - Website preferences and data
- **Session Storage** - Temporary session data
- **IndexedDB** - Database storage
- **Service Worker** - Service worker cache

## 🔧 Technical Changes

### Cache Management Improvements
- **Protected Patterns**: Added protection list for critical WebEngine profile files
- **Conservative Validation**: Profile validation no longer clears entire profile on errors
- **Error Handling**: Improved error handling to preserve login state even on validation failures
- **Selective Cleaning**: Only removes files with abnormal timestamps, not entire directories

### Code Improvements
- Enhanced `validate_and_clean_profile()` in `cache.py` with protected file patterns
- Updated `main_window.py` to use conservative profile validation
- Improved error messages and logging for cache operations
- Better handling of profile configuration failures

## 📋 Migration Notes

- **No action required**: The fix is automatic and transparent
- **Login state preserved**: You should now stay logged in across program restarts
- **Cache optimization**: Only corrupted cache files are removed, valid cache is preserved for better performance
- **If issues persist**: Manual cache clearing is still available in Settings dialog

## 🐛 Bug Fixes

### v1.0.1 Issues Resolved
- Fixed login state being lost on every restart
- Fixed cookies being deleted unnecessarily
- Fixed session data being cleared on startup

## 📅 Release Date

2025-11-27

---

**Made with ❤️ by nobody**

