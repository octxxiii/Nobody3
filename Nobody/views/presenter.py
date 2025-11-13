"""Presenter layer for VideoDownloader."""

from PyQt5.QtCore import QObject

from ..services.searcher import Searcher
from ..services.downloader import Downloader
from ..utils.logging import logger


class VideoPresenter(QObject):
    """Coordinates search and download flows between view and services."""

    def __init__(self, view, table_manager):
        super().__init__(view)
        self.view = view
        self.table_manager = table_manager
        self.search_thread = None
        self.downloader_thread = None

    # Search ------------------------------------------------------------

    def start_search(self, url: str):
        url = (url or "").strip()
        if not url:
            self.view.set_status("Please enter a URL to search.")
            return
        if self.view.is_duplicate_url(url):
            self.view.set_status("This video is already in the list.")
            return

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

    def _handle_search_update(self, title, thumbnail_url, video_url, formats):
        self.table_manager.update_video_list(title, thumbnail_url, video_url, formats)

    def _handle_search_finished(self):
        self.view.progress_bar.setRange(0, 100)
        self.view.progress_bar.setValue(100)
        self.view.set_status("Search completed.")
        self.search_thread = None

    # Download ----------------------------------------------------------

    def start_download(self, videos):
        if not videos:
            self.view.set_status("Select at least one video to download.")
            return

        directory = self.view.select_download_directory()
        if not directory:
            self.view.set_status("Select a valid download directory.")
            return

        self.downloader_thread = Downloader(videos, directory)
        self.downloader_thread.download_failed.connect(self.view.download_failed)
        self.downloader_thread.updated_status.connect(self.view.set_status)
        self.downloader_thread.updated_progress.connect(self.view.update_progress_bar)
        self.downloader_thread.start()

        logger.info("Download process started (%d items)", len(videos))
