"""Bookmark management for browser."""

import os
import json
from typing import List, Dict, Optional
from datetime import datetime
from ..utils.cache import resolve_writable_cache_dir
from ..utils.logging import logger


class Bookmark:
    """Represents a single bookmark."""

    def __init__(self, title: str, url: str, folder: str = ""):
        """Initialize bookmark.
        
        Args:
            title: Bookmark title
            url: Bookmark URL
            folder: Folder name (for organization)
        """
        self.title = title
        self.url = url
        self.folder = folder
        self.date_added = datetime.now().isoformat()

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            "title": self.title,
            "url": self.url,
            "folder": self.folder,
            "date_added": self.date_added,
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Bookmark':
        """Create from dictionary."""
        bookmark = cls(data.get("title", ""), data.get("url", ""), data.get("folder", ""))
        bookmark.date_added = data.get("date_added", datetime.now().isoformat())
        return bookmark


class BookmarkManager:
    """Manages browser bookmarks."""

    def __init__(self):
        """Initialize bookmark manager."""
        self.bookmarks: List[Bookmark] = []
        self._load_bookmarks()

    def _get_bookmarks_file(self) -> str:
        """Get bookmarks file path."""
        cache_dir = resolve_writable_cache_dir("Nobody 3")
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir, exist_ok=True)
        return os.path.join(cache_dir, "bookmarks.json")

    def _load_bookmarks(self):
        """Load bookmarks from file."""
        try:
            bookmarks_file = self._get_bookmarks_file()
            if os.path.exists(bookmarks_file):
                with open(bookmarks_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.bookmarks = [
                        Bookmark.from_dict(item) for item in data.get("bookmarks", [])
                    ]
        except Exception as e:
            logger.warning(f"Failed to load bookmarks: {e}")
            self.bookmarks = []

    def _save_bookmarks(self):
        """Save bookmarks to file."""
        try:
            bookmarks_file = self._get_bookmarks_file()
            data = {
                "bookmarks": [bm.to_dict() for bm in self.bookmarks]
            }
            with open(bookmarks_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"Failed to save bookmarks: {e}")

    def add_bookmark(self, title: str, url: str, folder: str = "") -> bool:
        """Add a bookmark.
        
        Args:
            title: Bookmark title
            url: Bookmark URL
            folder: Folder name (optional)
            
        Returns:
            True if added, False if already exists
        """
        # Check if already exists
        if any(bm.url == url for bm in self.bookmarks):
            return False
        
        bookmark = Bookmark(title, url, folder)
        self.bookmarks.append(bookmark)
        self._save_bookmarks()
        return True

    def remove_bookmark(self, url: str) -> bool:
        """Remove a bookmark by URL.
        
        Args:
            url: Bookmark URL
            
        Returns:
            True if removed, False if not found
        """
        for i, bm in enumerate(self.bookmarks):
            if bm.url == url:
                self.bookmarks.pop(i)
                self._save_bookmarks()
                return True
        return False

    def get_bookmarks(self, folder: Optional[str] = None) -> List[Bookmark]:
        """Get bookmarks, optionally filtered by folder.
        
        Args:
            folder: Folder name to filter by (None for all)
            
        Returns:
            List of bookmarks
        """
        if folder is None:
            return self.bookmarks.copy()
        return [bm for bm in self.bookmarks if bm.folder == folder]

    def get_folders(self) -> List[str]:
        """Get list of bookmark folders.
        
        Returns:
            List of folder names
        """
        folders = set(bm.folder for bm in self.bookmarks if bm.folder)
        return sorted(folders)
