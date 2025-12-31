"""Presenter layer for VideoDownloader."""

from typing import List, Tuple, Optional
from PyQt5.QtCore import QObject

from ..services.searcher import Searcher
from ..services.downloader import Downloader
from ..utils.logging import logger
from ..utils.sanitize import validate_url, sanitize_url


class VideoPresenter(QObject):
    """Coordinates search and download flows between view and services."""

    def __init__(self, view, table_manager):
        super().__init__(view)
        self.view = view
        self.table_manager = table_manager
        self.search_thread = None
        self.downloader_thread = None

    # Search ------------------------------------------------------------

    def start_search(self, url: str) -> None:
        """Start search operation with URL validation.
        
        Args:
            url: URL to search for videos
        """
        url = (url or "").strip()
        if not url:
            self.view.set_status("Please enter a URL to search.")
            return
        
        # Validate URL format
        is_valid, error_msg = validate_url(url)
        if not is_valid:
            self.view.set_status(f"Invalid URL: {error_msg}")
            logger.warning(f"Invalid URL rejected: {url} - {error_msg}")
            return
        
        # Sanitize and normalize URL
        url = sanitize_url(url)
        
        if self.view.is_duplicate_url(url):
            self.view.set_status("This video is already in the list.")
            return

        # Cancel previous search if still running
        if self.search_thread and self.search_thread.isRunning():
            logger.info("Cancelling previous search operation")
            self.search_thread.quit()
            self.search_thread.wait(500)  # Wait up to 500ms
            if self.search_thread.isRunning():
                self.search_thread.terminate()
                self.search_thread.wait(200)
            # Disconnect old signals
            try:
                self.search_thread.updated_list.disconnect()
                self.search_thread.finished.disconnect()
            except (TypeError, RuntimeError):
                pass
            self.search_thread.deleteLater()

        self.view.search_button.setEnabled(False)
        self.view.animation_timer.start(50)
        self.view.set_status("Searching...")
        self.view.progress_bar.setRange(0, 0)

        self.search_thread = Searcher(url)
        self.search_thread.updated_list.connect(self._handle_search_update)
        self.search_thread.finished.connect(self.view.search_finished)
        self.search_thread.finished.connect(self.view.enable_search_button)
        self.search_thread.finished.connect(self.view.check_results)
        self.search_thread.finished.connect(self._handle_search_finished)
        self.search_thread.start()

    def _handle_search_update(
        self, title, thumbnail_url, video_url, formats
    ):
        self.table_manager.update_video_list(
            title, thumbnail_url, video_url, formats
        )

    def _handle_search_finished(self):
        self.view.progress_bar.setRange(0, 100)
        self.view.progress_bar.setValue(100)
        self.view.set_status("Search completed.")

        # Disconnect signals before clearing reference
        if self.search_thread:
            try:
                self.search_thread.updated_list.disconnect()
                self.search_thread.finished.disconnect()
            except (TypeError, RuntimeError):
                # Signals may already be disconnected
                pass
            self.search_thread = None

    # Download ----------------------------------------------------------

    def start_download(self, videos: List[Tuple[str, str, str]], row_indices: List[int] = None) -> None:
        """Start download operation for selected videos.
        
        Args:
            videos: List of tuples (title, url, format_id)
            row_indices: Optional list of row indices corresponding to videos
        """
        if not videos:
            self.view.set_status("Select at least one video to download.")
            return

        # Check if download is already in progress
        if self.downloader_thread and self.downloader_thread.isRunning():
            logger.warning(
                "Download already in progress, skipping new request"
            )
            self.view.set_status("Download already in progress. Please wait.")
            return

        directory = self.view.select_download_directory()
        if not directory:
            self.view.set_status("Select a valid download directory.")
            return

        # Clean up previous download thread if exists
        if self.downloader_thread:
            try:
                if self.downloader_thread.isRunning():
                    self.downloader_thread.quit()
                    self.downloader_thread.wait(500)
                # Disconnect old signals
                try:
                    self.downloader_thread.download_failed.disconnect()
                    self.downloader_thread.updated_status.disconnect()
                    self.downloader_thread.updated_progress.disconnect()
                    self.downloader_thread.item_progress.disconnect()
                    self.downloader_thread.item_completed.disconnect()
                    self.downloader_thread.item_started.disconnect()
                except (TypeError, RuntimeError):
                    pass
                self.downloader_thread.deleteLater()
            except Exception as cleanup_exc:
                logger.warning(
                    f"Error cleaning up previous download thread: "
                    f"{cleanup_exc}"
                )

        # Create row mapping: (title, url) -> row index
        # If row_indices provided, use them; otherwise try to match by title/url
        row_mapping = {}
        if row_indices and len(row_indices) == len(videos):
            for idx, (title, url, _) in enumerate(videos):
                row_mapping[(title, url)] = row_indices[idx]
        else:
            # Fallback: try to find rows by matching title/url in video_info_list
            for idx, (title, url, _) in enumerate(videos):
                # Try to find matching row in table
                row_idx = idx  # Default to index if not found
                if hasattr(self.view, 'video_info_list'):
                    for row, (list_title, list_url) in enumerate(self.view.video_info_list):
                        if list_url == url:  # Match by URL (more reliable)
                            row_idx = row
                            break
                row_mapping[(title, url)] = row_idx

        self.downloader_thread = Downloader(videos, directory, row_mapping)
        self.downloader_thread.download_failed.connect(
            self.view.download_failed
        )
        self.downloader_thread.updated_status.connect(self.view.set_status)
        self.downloader_thread.updated_progress.connect(
            self.view.update_progress_bar
        )
        # Connect new individual progress signals
        self.downloader_thread.item_progress.connect(
            self.view.update_item_progress
        )
        self.downloader_thread.item_completed.connect(
            self.view.mark_item_complete
        )
        self.downloader_thread.item_started.connect(
            self.view.mark_item_started
        )
        # Connect history signal
        self.downloader_thread.history_added.connect(
            self.view.add_to_history
        )
        self.downloader_thread.start()

        logger.info("Download process started (%d items)", len(videos))
