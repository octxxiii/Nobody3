"""Download history management."""

import os
import json
from datetime import datetime
from typing import List, Dict, Optional

from ..utils.cache import resolve_writable_cache_dir
from ..utils.logging import logger


class DownloadHistory:
    """Manage download history records."""

    def __init__(self):
        self.history_file = self._get_history_file_path()
        self.entries: List[Dict] = []
        self.load_history()

    def _get_history_file_path(self) -> str:
        """Return the filesystem path for the history JSON file."""
        cache_dir = resolve_writable_cache_dir("Nobody 3")
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir, exist_ok=True)
        return os.path.join(cache_dir, "history.json")

    def load_history(self) -> None:
        """Load history from disk."""
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.entries = data.get("entries", [])
                logger.info(
                    f"Loaded {len(self.entries)} history entries from "
                    f"{self.history_file}"
                )
            else:
                self.entries = []
                logger.info("No history file found, starting with empty history")
        except Exception as e:
            logger.error(f"Failed to load history: {e}")
            self.entries = []

    def save_history(self) -> bool:
        """Save history to disk.
        
        Returns:
            True if saved successfully, False otherwise
        """
        try:
            data = {
                "version": "1.0",
                "last_updated": datetime.now().isoformat(),
                "entries": self.entries,
            }
            with open(self.history_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            logger.info(f"Saved {len(self.entries)} history entries")
            return True
        except Exception as e:
            logger.error(f"Failed to save history: {e}")
            return False

    def add_entry(
        self,
        title: str,
        url: str,
        format_id: str,
        download_path: str,
        file_size: Optional[int] = None,
    ) -> None:
        """Add a new download entry to history.
        
        Args:
            title: Video title
            url: Video URL
            format_id: Selected format ID
            download_path: Full path to downloaded file
            file_size: File size in bytes (optional)
        """
        entry = {
            "title": title,
            "url": url,
            "format_id": format_id,
            "download_path": download_path,
            "file_size": file_size,
            "timestamp": datetime.now().isoformat(),
        }
        self.entries.append(entry)
        # Keep only last 1000 entries to prevent file from growing too large
        if len(self.entries) > 1000:
            self.entries = self.entries[-1000:]
        self.save_history()

    def get_recent_entries(self, limit: int = 50) -> List[Dict]:
        """Get recent download entries.
        
        Args:
            limit: Maximum number of entries to return
            
        Returns:
            List of history entries, most recent first
        """
        return list(reversed(self.entries[-limit:]))

    def search_entries(self, query: str) -> List[Dict]:
        """Search history entries by title or URL.
        
        Args:
            query: Search query string
            
        Returns:
            List of matching history entries
        """
        query_lower = query.lower()
        results = []
        for entry in reversed(self.entries):  # Most recent first
            if (query_lower in entry.get("title", "").lower() or
                    query_lower in entry.get("url", "").lower()):
                results.append(entry)
        return results

    def clear_history(self) -> bool:
        """Clear all history entries.
        
        Returns:
            True if cleared successfully, False otherwise
        """
        try:
            self.entries = []
            return self.save_history()
        except Exception as e:
            logger.error(f"Failed to clear history: {e}")
            return False

    def delete_entry(self, index: int) -> bool:
        """Delete a specific history entry by index.
        
        Args:
            index: Index of entry to delete (0 = oldest, -1 = newest)
            
        Returns:
            True if deleted successfully, False otherwise
        """
        try:
            if 0 <= index < len(self.entries):
                del self.entries[index]
                return self.save_history()
            elif -len(self.entries) <= index < 0:
                del self.entries[index]
                return self.save_history()
            return False
        except Exception as e:
            logger.error(f"Failed to delete history entry: {e}")
            return False
