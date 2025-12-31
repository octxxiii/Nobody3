"""String sanitization utilities for filenames and URLs."""

import re
import sys
from typing import Optional


# Windows reserved names that cannot be used as filenames
_WINDOWS_RESERVED_NAMES = {
    "CON", "PRN", "AUX", "NUL",
    "COM1", "COM2", "COM3", "COM4", "COM5", "COM6", "COM7", "COM8", "COM9",
    "LPT1", "LPT2", "LPT3", "LPT4", "LPT5", "LPT6", "LPT7", "LPT8", "LPT9",
}

# Characters that are invalid in Windows filenames
_WINDOWS_INVALID_CHARS = r'[<>:"/\\|?*\x00-\x1f]'

# Characters that are invalid in Unix filenames (more restrictive)
_UNIX_INVALID_CHARS = r'[/\x00]'


def sanitize_filename(filename: str, max_length: int = 200) -> str:
    """Sanitize a filename to be safe for all platforms.
    
    Removes or replaces invalid characters, handles reserved names,
    and ensures the filename is within length limits.
    
    Args:
        filename: The original filename to sanitize
        max_length: Maximum length for the filename (default: 200)
        
    Returns:
        A sanitized filename safe for Windows, macOS, and Linux
    """
    if not filename:
        return "untitled"
    
    # Remove leading/trailing whitespace and dots
    filename = filename.strip().strip('.')
    
    if not filename:
        return "untitled"
    
    # Determine invalid characters based on platform
    if sys.platform.startswith("win"):
        invalid_chars = _WINDOWS_INVALID_CHARS
    else:
        # Use Windows rules for cross-platform compatibility
        invalid_chars = _WINDOWS_INVALID_CHARS
    
    # Replace invalid characters with underscore
    sanitized = re.sub(invalid_chars, "_", filename)
    
    # Remove multiple consecutive underscores
    sanitized = re.sub(r'_+', '_', sanitized)
    
    # Handle Windows reserved names
    if sys.platform.startswith("win"):
        name_without_ext = sanitized.rsplit('.', 1)[0].upper()
        if name_without_ext in _WINDOWS_RESERVED_NAMES:
            sanitized = f"_{sanitized}"
    
    # Truncate to max_length while preserving extension if possible
    if len(sanitized) > max_length:
        # Try to preserve extension
        if '.' in sanitized:
            name_part, ext = sanitized.rsplit('.', 1)
            max_name_length = max_length - len(ext) - 1
            if max_name_length > 0:
                sanitized = f"{name_part[:max_name_length]}.{ext}"
            else:
                sanitized = sanitized[:max_length]
        else:
            sanitized = sanitized[:max_length]
    
    # Remove trailing dots and spaces (Windows doesn't allow these)
    sanitized = sanitized.rstrip('. ')
    
    # Ensure we still have a valid filename
    if not sanitized or sanitized.isspace():
        return "untitled"
    
    return sanitized


def validate_url(url: str) -> tuple[bool, Optional[str]]:
    """Validate URL format.
    
    Performs basic URL format validation to catch obvious errors
    before attempting to fetch content.
    
    Args:
        url: The URL string to validate
        
    Returns:
        A tuple of (is_valid, error_message)
        - is_valid: True if URL appears valid, False otherwise
        - error_message: None if valid, error description if invalid
    """
    if not url:
        return False, "URL is empty"
    
    url = url.strip()
    if not url:
        return False, "URL is empty"
    
    # Basic protocol check
    url_lower = url.lower()
    valid_protocols = ("http://", "https://", "youtube.com", "youtu.be", 
                      "soundcloud.com", "www.")
    
    has_protocol = any(url_lower.startswith(proto) for proto in valid_protocols)
    
    # Allow URLs without protocol if they contain common domain patterns
    if not has_protocol:
        if any(domain in url_lower for domain in ("youtube.com", "youtu.be", 
                                                   "soundcloud.com")):
            # Auto-prepend https:// for common domains
            return True, None
    
    # Check for basic URL structure
    if "://" in url or any(domain in url_lower for domain in 
                          ("youtube.com", "youtu.be", "soundcloud.com")):
        return True, None
    
    return False, "URL format appears invalid. Please include http:// or https://"


def sanitize_url(url: str) -> str:
    """Sanitize and normalize a URL.
    
    Removes whitespace and ensures proper formatting.
    
    Args:
        url: The URL to sanitize
        
    Returns:
        A sanitized URL string
    """
    if not url:
        return ""
    
    url = url.strip()
    
    # Auto-prepend https:// for common domains without protocol
    url_lower = url.lower()
    if not url.startswith(("http://", "https://")):
        if any(domain in url_lower for domain in 
               ("youtube.com", "youtu.be", "soundcloud.com")):
            url = f"https://{url}"
    
    return url
