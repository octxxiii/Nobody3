"""Cache directory utility functions."""

import os
import sys
import shutil
import time
from datetime import datetime


def resolve_writable_cache_dir(application_name: str = "Nobody 3") -> str:
    r"""Return a user-writable cache directory for the given application.

    - Windows: %LOCALAPPDATA%\<AppName>\Caches
    - macOS:   ~/Library/Caches/<AppName>
    - Linux:   $XDG_CACHE_HOME/<AppName> or ~/.cache/<AppName>
    """
    if sys.platform.startswith("win"):
        base = os.getenv("LOCALAPPDATA") or os.path.join(os.path.expanduser("~"), "AppData", "Local")
        return os.path.join(base, application_name, "Caches")
    if sys.platform == "darwin":
        return os.path.join(os.path.expanduser("~/Library/Caches"), application_name)
    base = os.getenv("XDG_CACHE_HOME", os.path.expanduser("~/.cache"))
    return os.path.join(base, application_name)


def clear_webengine_profile(cache_directory: str, logger=None) -> bool:
    """Completely clear WebEngine profile directory.
    
    This is a more aggressive approach that removes all profile data
    to ensure a clean start when corruption is detected.
    
    Args:
        cache_directory: Path to the WebEngine profile cache directory
        logger: Optional logger instance for error reporting
        
    Returns:
        True if profile was cleared, False otherwise
    """
    if not os.path.exists(cache_directory):
        return False
    
    try:
        if logger:
            logger.warning(f"Clearing entire WebEngine profile: {cache_directory}")
        shutil.rmtree(cache_directory, ignore_errors=True)
        os.makedirs(cache_directory, exist_ok=True)
        if logger:
            logger.info("WebEngine profile cleared successfully.")
        return True
    except Exception as e:
        if logger:
            logger.error(f"Failed to clear WebEngine profile: {e}")
        return False


def clean_service_worker_cache(cache_directory: str, logger=None) -> bool:
    """Clean Service Worker cache to prevent database IO errors.
    
    Service Worker 스토리지 데이터베이스가 손상되었을 때 발생하는
    "Failed to delete the database: Database IO error" 에러를 방지하기 위해
    Service Worker 캐시를 정리합니다.
    
    Args:
        cache_directory: Path to the WebEngine profile cache directory
        logger: Optional logger instance for error reporting
        
    Returns:
        True if Service Worker cache was cleaned, False otherwise
    """
    service_worker_paths = [
        os.path.join(cache_directory, "Service Worker"),
        os.path.join(cache_directory, "ServiceWorkers"),
    ]
    
    cleaned = False
    for sw_path in service_worker_paths:
        if os.path.exists(sw_path):
            try:
                if logger:
                    logger.info(f"Cleaning Service Worker cache: {sw_path}")
                shutil.rmtree(sw_path, ignore_errors=True)
                cleaned = True
            except Exception as e:
                if logger:
                    logger.warning(f"Failed to clean Service Worker cache {sw_path}: {e}")
    
    return cleaned


def validate_and_clean_profile(cache_directory: str, logger=None, force_clear=False) -> bool:
    """Validate WebEngine profile integrity and clean corrupted data.
    
    Detects and removes files with abnormal timestamps (e.g., from 2015)
    that can cause WebEngine crashes after system date changes.
    
    IMPORTANT: This function protects cookies, session data, and login information
    by excluding critical WebEngine profile files from deletion.
    
    Args:
        cache_directory: Path to the WebEngine profile cache directory
        logger: Optional logger instance for error reporting
        force_clear: If True, completely clear the profile instead of selective cleaning
        
    Returns:
        True if profile was cleaned, False otherwise
    """
    if not os.path.exists(cache_directory):
        return False
    
    # Force clear if requested (more aggressive approach)
    if force_clear:
        return clear_webengine_profile(cache_directory, logger)
    
    # Service Worker 캐시 정리 (손상된 DB 에러 방지)
    sw_cleaned = clean_service_worker_cache(cache_directory, logger)
    
    # Critical files/directories that must be preserved (cookies, sessions, login data)
    # These are essential for maintaining user login state
    protected_patterns = [
        'Cookies',  # Cookie database
        'Cookies-journal',  # Cookie journal
        'Local Storage',  # LocalStorage data
        'Session Storage',  # SessionStorage data
        'IndexedDB',  # IndexedDB data
        # Service Worker는 손상된 경우 정리 가능하도록 보호 목록에서 제외
        # (손상된 Service Worker DB가 에러를 유발할 수 있음)
        'WebStorage',  # Web storage data
        'GPUCache',  # GPU cache (can be regenerated but safe to keep)
    ]
    
    def is_protected(path):
        """Check if a file or directory path should be protected from deletion."""
        path_lower = path.lower()
        for pattern in protected_patterns:
            if pattern.lower() in path_lower:
                return True
        return False
    
    cleaned = False
    current_time = time.time()
    # Consider files older than 10 years or newer than 1 day in the future as corrupted
    min_valid_time = current_time - (10 * 365 * 24 * 60 * 60)  # 10 years ago
    max_valid_time = current_time + (24 * 60 * 60)  # 1 day in the future
    
    corrupted_file_count = 0
    
    try:
        for root, dirs, files in os.walk(cache_directory):
            # Check files
            for filename in files:
                file_path = os.path.join(root, filename)
                
                # Skip protected files (cookies, sessions, etc.)
                if is_protected(file_path):
                    if logger:
                        logger.debug(f"Protecting critical file: {file_path}")
                    continue
                
                try:
                    mtime = os.path.getmtime(file_path)
                    # Check if timestamp is abnormal (too old or future)
                    if mtime < min_valid_time or mtime > max_valid_time:
                        corrupted_file_count += 1
                        if logger:
                            logger.warning(
                                f"Detected corrupted file with abnormal timestamp: {file_path} "
                                f"(mtime: {datetime.fromtimestamp(mtime).isoformat()})"
                            )
                        try:
                            os.remove(file_path)
                            cleaned = True
                        except Exception as remove_error:
                            if logger:
                                logger.warning(f"Failed to remove corrupted file {file_path}: {remove_error}")
                except (OSError, ValueError) as e:
                    if logger:
                        logger.warning(f"Failed to check/remove file {file_path}: {e}")
            
            # Check directories
            for dirname in dirs[:]:  # Copy list to allow modification
                dir_path = os.path.join(root, dirname)
                
                # Skip protected directories (cookies, sessions, etc.)
                if is_protected(dir_path):
                    if logger:
                        logger.debug(f"Protecting critical directory: {dir_path}")
                    continue
                
                try:
                    mtime = os.path.getmtime(dir_path)
                    if mtime < min_valid_time or mtime > max_valid_time:
                        if logger:
                            logger.warning(
                                f"Detected corrupted directory with abnormal timestamp: {dir_path} "
                                f"(mtime: {datetime.fromtimestamp(mtime).isoformat()})"
                            )
                        shutil.rmtree(dir_path, ignore_errors=True)
                        cleaned = True
                        dirs.remove(dirname)  # Don't walk into removed directory
                except (OSError, ValueError) as e:
                    if logger:
                        logger.warning(f"Failed to check/remove directory {dir_path}: {e}")
        
        # If significant corruption detected (more than 5 files), clear entire profile
        # BUT: Only if no protected files were affected
        if corrupted_file_count > 5:
            if logger:
                logger.warning(
                    f"Detected {corrupted_file_count} corrupted files. "
                    "However, protected files (cookies/sessions) are preserved."
                )
            # Don't clear entire profile - just log the issue
            # Only clear if absolutely necessary and user explicitly requests it
            if logger:
                logger.info(
                    "Skipping full profile clear to preserve login state. "
                    "If crashes persist, manual cache clearing may be needed."
                )
        
        # If any corruption detected, log it
        if cleaned or sw_cleaned:
            if logger:
                if sw_cleaned:
                    logger.info("Service Worker cache cleaned to prevent database IO errors.")
                if cleaned:
                    logger.info(
                        f"Corrupted WebEngine profile detected and cleaned ({corrupted_file_count} files). "
                        "Cookies and session data were preserved. "
                        "This may have been caused by system date changes."
                    )
        
        return cleaned or sw_cleaned
    except Exception as e:
        if logger:
            logger.error(f"Error during profile validation: {e}")
        # If validation fails completely, DO NOT clear the entire cache
        # This would delete all cookies and sessions
        # Instead, just log the error and continue
        if logger:
            logger.warning(
                "Profile validation failed, but preserving profile to maintain login state. "
                f"Error: {e}"
            )
        # 예외 발생 시에도 Service Worker 캐시 정리는 시도
        try:
            sw_cleaned = clean_service_worker_cache(cache_directory, logger)
            return sw_cleaned
        except:
            return False
    
    return cleaned or sw_cleaned

