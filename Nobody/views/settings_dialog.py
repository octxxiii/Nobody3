"""About/settings dialog."""

import os
from PyQt5.QtWidgets import QDialog, QLabel, QVBoxLayout, QPushButton
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtCore import Qt, QUrl

from ..utils.cache import resolve_writable_cache_dir


class SettingsDialog(QDialog):
    """Dialog displaying app information and quick links."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Nobody 3 - About")
        self.cacheDirectory = resolve_writable_cache_dir("Nobody 3")
        self.predefinedURL = "https://soundcloud.com/octxxiii"
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop)

        info_html = (
            "<h1>Nobody 3 v2.0</h1>"
            "<p>Personal YouTube/SoundCloud downloader & player." "<br/>"
            f"Cache directory: <code>{self.cacheDirectory}</code></p>"
        )

        info_label = QLabel(info_html)
        info_label.setTextFormat(Qt.RichText)
        info_label.setWordWrap(True)

        open_cache_button = QPushButton("Open Cache Folder")
        open_cache_button.clicked.connect(self._open_cache_folder)

        open_soundcloud_button = QPushButton("Open SoundCloud")
        open_soundcloud_button.clicked.connect(self._open_soundcloud)

        layout.addWidget(info_label)
        layout.addWidget(open_cache_button)
        layout.addWidget(open_soundcloud_button)

    def _open_cache_folder(self):
        os.makedirs(self.cacheDirectory, exist_ok=True)
        QDesktopServices.openUrl(QUrl.fromLocalFile(self.cacheDirectory))

    def _open_soundcloud(self):
        QDesktopServices.openUrl(QUrl(self.predefinedURL))

