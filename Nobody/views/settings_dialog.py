"""About/settings dialog."""

import os
import shutil
from PyQt5.QtWidgets import QDialog, QLabel, QVBoxLayout, QPushButton, QTextEdit, QHBoxLayout
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtCore import Qt, QUrl, pyqtSignal
from PyQt5.QtWebEngineWidgets import QWebEngineProfile

from ..utils.cache import resolve_writable_cache_dir
from ..config.constants import DARK_THEME_STYLESHEET


class SettingsDialog(QDialog):
    """Dialog displaying app information and quick links."""
    dialogClosed = pyqtSignal()

    def __init__(self, parent=None, nobody_cache=None):
        super().__init__(parent)
        self.setModal(True)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.Nobody = nobody_cache
        self.current_language = "ko"  # Default to Korean
        self.layout = QVBoxLayout()
        self.cacheDirectory = resolve_writable_cache_dir("OctXXIII")
        if not os.path.exists(self.cacheDirectory):
            try:
                os.makedirs(self.cacheDirectory, exist_ok=True)
            except Exception as e:
                print(f"Failed to create cache directory {self.cacheDirectory}: {e}")
        self.predefinedURL = "https://soundcloud.com/octxxiii"
        self.setupUI()

    def get_text_ko(self):
        """Korean text content"""
        return """
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
            <br>
            <h3>FFmpeg 배포</h3>
            <p>
            이 애플리케이션은 LGPL/GPL 라이선스 하에 배포되는 FFmpeg를 포함합니다.
            <br>
            FFmpeg는 미디어 파일을 디코딩, 인코딩, 트랜스코딩, 멀티플렉싱, 디멀티플렉싱, 스트리밍, 필터링 및 재생할 수 있는 멀티미디어 프레임워크입니다.
            <br>
            자세한 정보는 다음을 방문하세요: <a href="https://ffmpeg.org/">https://ffmpeg.org/</a>
            </p>
            <br>
            <h3>저작권 안내</h3>
            <p>
            <strong>중요:</strong> 이 도구는 개인 사용 전용입니다.
            <br>
            다운로드한 콘텐츠는 원작자의 저작권이 있습니다.
            <br>
            무단 배포 또는 상업적 사용은 불법입니다.
            <br>
            저작권법을 준수하고 이 도구를 책임감 있게 사용하세요.
            </p>
            <br>
            <h3>감사의 말</h3>
            <p>
            - <strong>yt-dlp</strong>: 미디어 추출 엔진
            <br>
            - <strong>FFmpeg</strong>: 미디어 처리 (LGPL/GPL)
            <br>
            - <strong>PyQt5</strong>: GUI 프레임워크
            <br>
            - <strong>Python Community</strong>: 훌륭한 도구와 라이브러리 제공
            </p>
        """

    def get_text_en(self):
        """English text content"""
        return """
            <p style="text-align: center;">
            <h1>OctXXIII v2.0</h1>
            <div>Youtube/Music Converter & Player</div>
            <div>Release: 2025-01-03</div>
            </p>
            <br>
            <p>
            <h3>2025 Updates</h3>
                <ul>
                    <li>Mini player mode added</li>
                    <li>Always-on-top toggle feature</li>
                    <li>Maximize button enabled</li>
                    <li>FFmpeg included build system</li>
                    <li>Cross-platform support</li>
                </ul>

                <h3>How to Use</h3>
                <ol>
                    <li>Select desired video/playlist in browser</li>
                    <li>Click CopyURL or enter URL and search</li>
                    <li>Select format from table and download</li>
                </ol>

                <h3>Previous Versions (2024)</h3>
                <ul>
                    <li>v1.0 (240408): Current browser video/audio control panel added</li>
                    <li>240405: Clipboard copy, refresh, SoundCloud support</li>
                    <li>240401: Browser hide, YouTube Music support</li>
                    <li>240328: Browser integration, theme system</li>
                    <li>240327: Playlist support, URL management</li>
                    <li>240326: Basic download feature, thumbnail support</li>
                </ul>
            </p>
            <h2>
            Creator: nobody 😜 
            <br>
            Last Updated: 2025-09-04
            </h2>
            <br>
            <h3>FFmpeg Distribution</h3>
            <p>
            This application includes FFmpeg, which is licensed under the LGPL/GPL.
            <br>
            FFmpeg is a multimedia framework that can decode, encode, transcode, mux, demux, stream, filter and play media files.
            <br>
            For more information, visit: <a href="https://ffmpeg.org/">https://ffmpeg.org/</a>
            </p>
            <br>
            <h3>Copyright Notice</h3>
            <p>
            <strong>Important:</strong> This tool is for personal use only.
            <br>
            Downloaded content is copyrighted by the original creators.
            <br>
            Unauthorized distribution or commercial use is illegal.
            <br>
            Please respect copyright laws and use this tool responsibly.
            </p>
            <br>
            <h3>Acknowledgments</h3>
            <p>
            - <strong>yt-dlp</strong>: Media extraction engine
            <br>
            - <strong>FFmpeg</strong>: Media processing (LGPL/GPL)
            <br>
            - <strong>PyQt5</strong>: GUI framework
            <br>
            - <strong>Python Community</strong>: For amazing tools and libraries
            </p>
        """

    def setupUI(self):
        cache_path = self.cacheDirectory

        # Language toggle button
        self.languageButton = QPushButton("한국어 / English", self)
        self.languageButton.clicked.connect(self.toggle_language)

        # Text area
        self.textArea = QTextEdit()
        self.textArea.setReadOnly(True)
        self.textArea.setContentsMargins(0, 0, 0, 0)
        self.update_text()

        # Buttons
        self.actionButton = QPushButton('Visit Created by Link', self)
        self.actionButton.clicked.connect(self.performAction)

        self.supportButton = QPushButton('☕ Buy Me a Coffee', self)
        self.supportButton.clicked.connect(self.openSupportLink)

        self.clearCacheButton = QPushButton('', self)
        self.clearCacheButton.clicked.connect(self.clearCache)

        # Layout
        header_layout = QHBoxLayout()
        header_layout.addWidget(self.languageButton)
        header_layout.addStretch()

        self.layout.addLayout(header_layout)
        self.layout.addWidget(self.textArea)
        self.layout.addWidget(self.actionButton)
        self.layout.addWidget(self.supportButton)
        self.layout.addWidget(self.clearCacheButton)

        self.setLayout(self.layout)
        self.setFixedSize(500, 600)
        self.setStyleSheet(DARK_THEME_STYLESHEET)

        try:
            self.updateCacheSize()
        except Exception as e:
            print(f"Failed to update cache size: {e}")

    def toggle_language(self):
        """Toggle between Korean and English"""
        if self.current_language == "ko":
            self.current_language = "en"
            self.setWindowTitle("OctXXIII - About")
            self.languageButton.setText("한국어 / English")
        else:
            self.current_language = "ko"
            self.setWindowTitle("OctXXIII - 정보")
            self.languageButton.setText("한국어 / English")
        self.update_text()
        self.update_buttons()

    def update_text(self):
        """Update text area content based on current language"""
        if self.current_language == "ko":
            self.textArea.setHtml(self.get_text_ko())
        else:
            self.textArea.setHtml(self.get_text_en())

    def update_buttons(self):
        """Update button texts based on current language"""
        if self.current_language == "ko":
            self.actionButton.setText("SoundCloud 링크 열기")
            self.supportButton.setText("☕ 커피 사주기")
            # Clear cache button text is updated in updateCacheSize
        else:
            self.actionButton.setText("Visit Created by Link")
            self.supportButton.setText("☕ Buy Me a Coffee")
            # Clear cache button text is updated in updateCacheSize

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

    def openSupportLink(self):
        """Open Buy Me a Coffee support link"""
        support_url = "https://www.buymeacoffee.com/octxxiii"
        QDesktopServices.openUrl(QUrl(support_url))

    def updateCacheSize(self):
        """Update the cache size display"""
        cache_size_mb = self.getDirectorySize(self.cacheDirectory) / (1024 * 1024)
        if self.current_language == "ko":
            self.clearCacheButton.setText(f"캐시 삭제: {cache_size_mb:.2f}MB")
        else:
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
