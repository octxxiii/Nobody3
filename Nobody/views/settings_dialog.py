"""설정 다이얼로그 (정보 창)"""

import os
import shutil
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton, QTextEdit
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtWebEngineWidgets import QWebEngineProfile
from PyQt5.QtCore import QUrl
from ..utils.cache import resolve_writable_cache_dir
from ..utils.logging import logger


class SettingsDialog(QDialog):
    """설정 다이얼로그 (정보 창)"""
    dialogClosed = pyqtSignal()

    def __init__(self, parent=None, nobody_cache=None):
        super(SettingsDialog, self).__init__(parent)
        self.setModal(True)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.Nobody = nobody_cache
        self.setWindowTitle('OctXXIII - 정보')
        self.layout = QVBoxLayout()
        # Initialize cache directory BEFORE building UI
        self.cacheDirectory = resolve_writable_cache_dir("OctXXIII")
        if not os.path.exists(self.cacheDirectory):
            try:
                os.makedirs(self.cacheDirectory, exist_ok=True)
            except Exception as e:
                logger.error(f"Failed to create cache directory {self.cacheDirectory}: {e}")
        self.setupUI()

        # Define the URL and the descriptive text with HTML for line breaks
        self.predefinedURL = "https://soundcloud.com/octxxiii"
        predefinedText = """
            <p style="text-align: center;">
            <h1>OctXXIII v2.0</h1>
            <div>Youtube/Music Converter & Player</div>
            <div>Release: 2025-01-03</div>
            </p>
            <br>
            <p>
            <h3>2025 업데이트</h3>
                <ul>
                    <li>미니 플레이어 모드 추가</li>
                    <li>최상위 고정 토글 기능</li>
                    <li>최대화 버튼 활성화</li>
                    <li>FFmpeg 포함 빌드 시스템</li>
                    <li>크로스 플랫폼 지원</li>
                </ul>

                <h3>사용방법</h3>
                <ol>
                    <li>브라우저에서 원하는 영상/플레이리스트 선택</li>
                    <li>CopyURL 클릭 또는 URL 입력 후 검색</li>
                    <li>테이블에서 포맷 선택 후 다운로드</li>
                </ol>

                <h3>이전 버전들 (2024)</h3>
                <ul>
                    <li>v1.0 (240408): 현재 브라우저 비디오/오디오 컨트롤 패널 추가</li>
                    <li>240405: 클립보드 복사, 새로고침, SoundCloud 지원</li>
                    <li>240401: 브라우저 숨기기, YouTube Music 지원</li>
                    <li>240328: 브라우저 통합, 테마 시스템</li>
                    <li>240327: 플레이리스트 지원, URL 관리</li>
                    <li>240326: 기본 다운로드 기능, 썸네일 지원</li>
                </ul>
            </p>
            <h2>
            Creator: nobody 😜 
            <br>
            Last Updated: 2025-09-04
            </h2>
        """

        self.textArea = QTextEdit()
        self.textArea.setHtml(predefinedText)
        self.textArea.setReadOnly(True)
        self.textArea.setContentsMargins(0, 0, 0, 0)

        self.actionButton = QPushButton('Visit Created by Link', self)
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
            logger.error(f"Failed to update cache size: {e}")

    def closeEvent(self, event):
        """Reimplement the close event to emit the dialogClosed signal"""
        try:
            self.dialogClosed.emit()
        except Exception as e:
            logger.error(f"dialogClosed emit failed: {e}")
        super().closeEvent(event)

    def setupUI(self):
        cache_path = self.cacheDirectory

    def performAction(self):
        QDesktopServices.openUrl(QUrl(self.predefinedURL))
        self.close()

    def updateCacheSize(self):
        cache_size_mb = self.getDirectorySize(self.cacheDirectory) / (1024 * 1024)
        self.clearCacheButton.setText(f"Clear Cache: {cache_size_mb:.2f}MB")

    def getDirectorySize(self, directory):
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(directory):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                try:
                    if os.path.exists(fp):
                        total_size += os.path.getsize(fp)
                except Exception as e:
                    logger.debug(f"Skip size for {fp}: {e}")
        return total_size

    def clearCache(self):
        # Clear the cache of the default web engine profile
        QWebEngineProfile.defaultProfile().clearHttpCache()

        # Optionally remove all files in the cache directory manually
        for filename in os.listdir(self.cacheDirectory):
            file_path = os.path.join(self.cacheDirectory, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                logger.warning(f'Failed to delete {file_path}. Reason: {e}')

        # Assuming self.browser is defined in this class or accessible via a class attribute
        if hasattr(self, 'browser'):
            self.browser.reload()

        self.updateCacheSize()

