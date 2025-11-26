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


def validate_and_clean_profile(cache_directory: str, logger=None, force_clear=False) -> bool:
    """Validate WebEngine profile integrity and clean corrupted data.
    
    Detects and removes files with abnormal timestamps (e.g., from 2015)
    that can cause WebEngine crashes after system date changes.
    
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
        if corrupted_file_count > 5:
            if logger:
                logger.warning(
                    f"Detected {corrupted_file_count} corrupted files. "
                    "Clearing entire profile for safety."
                )
            return clear_webengine_profile(cache_directory, logger)
        
        # If any corruption detected, log it
        if cleaned:
            if logger:
                logger.info(
                    f"Corrupted WebEngine profile detected and cleaned ({corrupted_file_count} files). "
                    "This may have been caused by system date changes."
                )
    except Exception as e:
        if logger:
            logger.error(f"Error during profile validation: {e}")
        # If validation fails completely, clear the entire cache as a safety measure
        try:
            shutil.rmtree(cache_directory, ignore_errors=True)
            os.makedirs(cache_directory, exist_ok=True)
            if logger:
                logger.warning("Cleared entire WebEngine profile due to validation failure.")
            cleaned = True
        except Exception as cleanup_error:
            if logger:
                logger.error(f"Failed to clear corrupted profile: {cleanup_error}")
    
    return cleaned

