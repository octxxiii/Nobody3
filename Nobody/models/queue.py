"""Download queue management."""

from typing import List, Dict, Optional
from enum import Enum
from dataclasses import dataclass


class DownloadStatus(Enum):
    """Download status enumeration."""
    PENDING = "pending"
    QUEUED = "queued"
    DOWNLOADING = "downloading"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class QueueItem:
    """Represents a single item in the download queue."""
    title: str
    url: str
    format_id: str
    row_index: int
    status: DownloadStatus = DownloadStatus.PENDING
    priority: int = 0  # Higher = more priority
    progress: float = 0.0
    speed: str = "N/A"
    eta: str = "N/A"
    file_path: Optional[str] = None
    file_size: Optional[int] = None


class DownloadQueue:
    """Manages download queue with priority and status tracking."""

    def __init__(self):
        """Initialize empty queue."""
        self.items: List[QueueItem] = []
        self._next_id = 0

    def add_item(
        self,
        title: str,
        url: str,
        format_id: str,
        row_index: int,
        priority: int = 0
    ) -> QueueItem:
        """Add item to queue.
        
        Args:
            title: Video title
            url: Video URL
            format_id: Format identifier
            row_index: Table row index
            priority: Priority (higher = more priority)
            
        Returns:
            Created QueueItem
        """
        item = QueueItem(
            title=title,
            url=url,
            format_id=format_id,
            row_index=row_index,
            priority=priority,
            status=DownloadStatus.PENDING
        )
        self.items.append(item)
        self._sort_by_priority()
        return item

    def remove_item(self, row_index: int) -> bool:
        """Remove item from queue by row index.
        
        Args:
            row_index: Table row index
            
        Returns:
            True if item was removed, False otherwise
        """
        for i, item in enumerate(self.items):
            if item.row_index == row_index:
                self.items.pop(i)
                return True
        return False

    def get_item(self, row_index: int) -> Optional[QueueItem]:
        """Get queue item by row index.
        
        Args:
            row_index: Table row index
            
        Returns:
            QueueItem or None
        """
        for item in self.items:
            if item.row_index == row_index:
                return item
        return None

    def get_next_item(self) -> Optional[QueueItem]:
        """Get next item to download (highest priority, pending/queued).
        
        Returns:
            Next QueueItem or None
        """
        for item in self.items:
            if item.status in (DownloadStatus.PENDING, DownloadStatus.QUEUED):
                return item
        return None

    def update_item_status(
        self,
        row_index: int,
        status: DownloadStatus
    ) -> bool:
        """Update item status.
        
        Args:
            row_index: Table row index
            status: New status
            
        Returns:
            True if updated, False otherwise
        """
        item = self.get_item(row_index)
        if item:
            item.status = status
            return True
        return False

    def update_item_progress(
        self,
        row_index: int,
        progress: float,
        speed: str = "N/A",
        eta: str = "N/A"
    ) -> bool:
        """Update item progress.
        
        Args:
            row_index: Table row index
            progress: Progress percentage (0-100)
            speed: Download speed string
            eta: Estimated time remaining
            
        Returns:
            True if updated, False otherwise
        """
        item = self.get_item(row_index)
        if item:
            item.progress = progress
            item.speed = speed
            item.eta = eta
            return True
        return False

    def set_priority(self, row_index: int, priority: int) -> bool:
        """Set item priority.
        
        Args:
            row_index: Table row index
            priority: New priority value
            
        Returns:
            True if updated, False otherwise
        """
        item = self.get_item(row_index)
        if item:
            item.priority = priority
            self._sort_by_priority()
            return True
        return False

    def _sort_by_priority(self):
        """Sort items by priority (descending)."""
        self.items.sort(key=lambda x: x.priority, reverse=True)

    def get_pending_count(self) -> int:
        """Get count of pending/queued items.
        
        Returns:
            Count of pending items
        """
        return sum(
            1 for item in self.items
            if item.status in (DownloadStatus.PENDING, DownloadStatus.QUEUED)
        )

    def get_downloading_count(self) -> int:
        """Get count of currently downloading items.
        
        Returns:
            Count of downloading items
        """
        return sum(
            1 for item in self.items
            if item.status == DownloadStatus.DOWNLOADING
        )

    def clear_completed(self):
        """Remove all completed items from queue."""
        self.items = [
            item for item in self.items
            if item.status != DownloadStatus.COMPLETED
        ]
