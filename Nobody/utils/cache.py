"""Cache directory utility functions."""

import os
import sys


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

