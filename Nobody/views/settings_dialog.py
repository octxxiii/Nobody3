"""About/settings dialog."""

import os
import shutil
from PyQt5.QtWidgets import QDialog, QLabel, QVBoxLayout, QPushButton, QTextEdit
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtCore import Qt, QUrl, pyqtSignal
from PyQt5.QtWebEngineWidgets import QWebEngineProfile

from ..utils.cache import resolve_writable_cache_dir


class SettingsDialog(QDialog):
    """Dialog displaying app information and quick links."""
    dialogClosed = pyqtSignal()

    def __init__(self, parent=None, nobody_cache=None):
        super().__init__(parent)
        self.setModal(True)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.Nobody = nobody_cache
        self.setWindowTitle("OctXXIII - 정보")
        self.layout = QVBoxLayout()
        self.cacheDirectory = resolve_writable_cache_dir("OctXXIII")
        if not os.path.exists(self.cacheDirectory):
            try:
                os.makedirs(self.cacheDirectory, exist_ok=True)
            except Exception as e:
                print(f"Failed to create cache directory {self.cacheDirectory}: {e}")
        self.predefinedURL = "https://soundcloud.com/octxxiii"
        self.setupUI()

    def setupUI(self):
        cache_path = self.cacheDirectory
        info_text = f"OctXXIII v2.0\n\n캐시 디렉토리:\n{cache_path}\n\nSoundCloud 링크:\n{self.predefinedURL}"

        self.textArea = QTextEdit(self)
        self.textArea.setReadOnly(True)
        self.textArea.setText(info_text)

        self.actionButton = QPushButton('SoundCloud 열기', self)
        self.actionButton.clicked.connect(self.performAction)

        self.clearCacheButton = QPushButton('', self)
        self.clearCacheButton.clicked.connect(self.clearCache)

        self.layout.addWidget(self.textArea)
        self.layout.addWidget(self.actionButton)
        self.layout.addWidget(self.clearCacheButton)

        self.setLayout(self.layout)
        self.setFixedSize(400, 300)

        try:
            self.updateCacheSize()
        except Exception as e:
            print(f"Failed to update cache size: {e}")

    def closeEvent(self, event):
        """Reimplement the close event to emit the dialogClosed signal"""
        try:
            self.dialogClosed.emit()
        except Exception as e:
            print(f"dialogClosed emit failed: {e}")
        super().closeEvent(event)

    def performAction(self):
        """Open the URL in a web browser"""
        QDesktopServices.openUrl(QUrl(self.predefinedURL))
        self.close()

    def updateCacheSize(self):
        """Update the cache size display"""
        cache_size_mb = self.getDirectorySize(self.cacheDirectory) / (1024 * 1024)
        self.clearCacheButton.setText(f"Clear Cache: {cache_size_mb:.2f}MB")

    def getDirectorySize(self, directory):
        """Calculate directory size"""
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(directory):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                try:
                    if os.path.exists(fp):
                        total_size += os.path.getsize(fp)
                except Exception as e:
                    print(f"Skip size for {fp}: {e}")
        return total_size

    def clearCache(self):
        """Clear the cache"""
        QWebEngineProfile.defaultProfile().clearHttpCache()

        for filename in os.listdir(self.cacheDirectory):
            file_path = os.path.join(self.cacheDirectory, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f'Failed to delete {file_path}. Reason: {e}')

        self.updateCacheSize()

