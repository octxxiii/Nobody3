import os
import shutil
import sys
import requests
from PyQt5.QtGui import QPixmap, QIcon, QDesktopServices
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings, QWebEngineProfile
from PyQt5.QtWidgets import (QApplication, QDialog, QPushButton, QVBoxLayout, QLineEdit, QLabel, QProgressBar,
                             QTableWidget, QTableWidgetItem, QHeaderView, QCheckBox, QFileDialog,
                             QTextEdit, QComboBox, QAbstractItemView, QHBoxLayout, QSplitter, QWidget, QMessageBox,
                             QSlider)
from PyQt5.QtCore import QThread, pyqtSignal, Qt, pyqtSlot, QObject, QTimer, QUrl, QSize
import yt_dlp
import resources_rc # resources_rc 임포트 복원

# Dark Theme 스타일 시트 문자열만 남깁니다.
DARK_THEME_STYLESHEET = """
        QDialog { background-color: #2D2D2D; }
        QPushButton { background-color: #333333; color: #FFFFFF; border: 2px solid #555555; border-radius: 5px; padding: 5px; }
        QPushButton:hover { background-color: #555555; }
        QPushButton:pressed { background-color: #444444; }
        QComboBox { background-color: #333333; color: #FFFFFF; border: 2px solid #555555; border-radius: 5px; padding: 3px; }
        QComboBox QAbstractItemView { background: #2D2D2D; selection-background-color: #3D3D3D; color: #FFFFFF; }
        QLineEdit, QTextEdit { background-color: #333333; color: #FFFFFF; border: 2px solid #555555; }
        QTableWidget { background-color: #2D2D2D; color: #FFFFFF; border: none; }
        QTableWidget::item { background-color: #333333; color: #FFFFFF; border: 1px solid #2D2D2D; }
        QLabel { color: #FFFFFF; }
        QHeaderView::section { background-color: #333333; color: #FFFFFF; padding: 4px; border: 1px solid #2D2D2D; }
        QProgressBar { border: 2px solid #333333; border-radius: 5px; background-color: #2D2D2D; text-align: center; }
        QProgressBar::chunk { background-color: #555555; }
"""


def resolve_writable_cache_dir(application_name: str = "OctXXIII") -> str:
    """Return a user-writable cache directory for the given application.

    - Windows: %LOCALAPPDATA%\\<AppName>\\Caches
    - macOS:   ~/Library/Caches/<AppName>
    - Linux:   $XDG_CACHE_HOME/<AppName> or ~/.cache/<AppName>
    """
    if sys.platform.startswith("win"):
        base = os.getenv("LOCALAPPDATA") or os.path.join(os.path.expanduser("~"), "AppData", "Local")
        return os.path.join(base, application_name, "Caches")
    elif sys.platform == "darwin":
        return os.path.join(os.path.expanduser("~/Library/Caches"), application_name)
    else:
        base = os.getenv("XDG_CACHE_HOME", os.path.expanduser("~/.cache"))
        return os.path.join(base, application_name)


class SettingsDialog(QDialog):
    dialogClosed = pyqtSignal()

    def __init__(self, parent=None, nobody_cache=None):
        super(SettingsDialog, self).__init__(parent)
        self.setModal(True)  # This makes the dialog modal
        self.setAttribute(Qt.WA_DeleteOnClose)  # Ensures it closes with the application
        self.Nobody = nobody_cache  # Receive the parameter here
        self.setWindowTitle('Creator')
        self.layout = QVBoxLayout()
        # Initialize cache directory BEFORE building UI, as setupUI references it
        self.cacheDirectory = resolve_writable_cache_dir("OctXXIII")
        if not os.path.exists(self.cacheDirectory):
            try:
                os.makedirs(self.cacheDirectory, exist_ok=True)
            except Exception as e:
                print(f"Failed to create cache directory {self.cacheDirectory}: {e}")
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
        self.textArea.setHtml(predefinedText)  # Use setHtml to apply HTML formatting
        self.textArea.setReadOnly(True)
        self.textArea.setContentsMargins(0, 0, 0, 0)

        self.actionButton = QPushButton('Visit Created by Link', self)
        self.actionButton.clicked.connect(self.performAction)

        self.clearCacheButton = QPushButton('', self)
        self.clearCacheButton.clicked.connect(self.clearCache)

        self.layout.addWidget(self.textArea)
        self.layout.addWidget(self.actionButton)
        self.layout.addWidget(self.clearCacheButton)  # Add the new button to the layout

        self.setLayout(self.layout)
        self.setFixedSize(400, 300)

        try:
            self.updateCacheSize()
        except Exception as e:
            print(f"Failed to update cache size: {e}")

    def closeEvent(self, event):
        """ Reimplement the close event to emit the dialogClosed signal """
        try:
            self.dialogClosed.emit()
        except Exception as e:
            print(f"dialogClosed emit failed: {e}")
        super().closeEvent(event)

    def setupUI(self):
        cache_path = self.cacheDirectory

    def performAction(self):
        # Implement the action to open the URL in a web browser
        QDesktopServices.openUrl(QUrl(self.predefinedURL))
        self.close()

    def updateCacheSize(self):
        cache_size_mb = self.getDirectorySize(self.cacheDirectory) / (1024 * 1024)  # Convert bytes to MB
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
                    print(f"Skip size for {fp}: {e}")
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
                print(f'Failed to delete {file_path}. Reason: {e}')

        # Assuming self.browser is defined in this class or accessible via a class attribute
        if hasattr(self, 'browser'):
            self.browser.reload()

        self.updateCacheSize()  # Update the displayed cache size


class CheckBoxHeader(QHeaderView):
    def __init__(self, parent=None):
        super().__init__(Qt.Horizontal, parent)
        self.setSectionResizeMode(QHeaderView.Fixed)
        self.setDefaultAlignment(Qt.AlignCenter)
        self.setCheckBox()

    def setCheckBox(self):
        self.cb = QCheckBox(self)
        self.cb.setChecked(False)
        self.sectionResized.connect(self.resizeCheckBox)
        self.cb.clicked.connect(self.selectAll)
        self.cb.setStyleSheet("QCheckBox { margin-left: 6px; margin-right: 6px; }")  # Adjust the margins for alignment

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.resizeCheckBox()

    def resizeCheckBox(self):
        rect = self.sectionViewportPosition(0)
        self.cb.setGeometry(rect, 0, self.sectionSize(0), self.height())
        self.parent().setColumnWidth(0, self.cb.sizeHint().width())  # Set column width to checkbox width

    def selectAll(self):
        check_state = self.cb.isChecked()
        for row in range(self.parent().rowCount()):
            item = self.parent().item(row, 0)  # Assuming checkboxes are in the first column
            if item and isinstance(item, QTableWidgetItem):
                item.setCheckState(Qt.Checked if check_state else Qt.Unchecked)

    def updateState(self):
        all_checked = self.parent().rowCount() > 0
        for row in range(self.parent().rowCount()):
            item = self.parent().item(row, 0)
            if item is None or item.checkState() != Qt.Checked:
                all_checked = False
                break

        self.cb.setChecked(all_checked)


class VideoHandler(QObject):
    @pyqtSlot(float)
    def handleVideoDuration(self, duration):
        print("Video duration:", duration)


class VideoDownloader(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowFlags(self.windowFlags() | Qt.WindowMinimizeButtonHint | Qt.WindowMaximizeButtonHint | Qt.WindowCloseButtonHint) # 최소화, 최대화, 닫기 버튼 활성화
        self.settingsDialog = None
        self.Nobody = resolve_writable_cache_dir("Nobody")  # Define here
        
        # 미니 플레이어 관련 변수
        self.is_mini_mode = False
        self.normal_geometry = None
        self.mini_player = None
        self.mini_always_on_top = True  # 기본적으로 최상위 고정
        # Use a user-writable cache directory to avoid permission issues under Program Files
        self.cacheDirectory = resolve_writable_cache_dir("OctXXIII")
        if not os.path.exists(self.cacheDirectory):
            try:
                os.makedirs(self.cacheDirectory, exist_ok=True)
            except Exception as e:
                print(f"Failed to create cache directory {self.cacheDirectory}: {e}")

        # 지정된 경로에 폴더가 없으면 폴더 생성
        if not os.path.exists(self.cacheDirectory):
            os.makedirs(self.cacheDirectory)

        # 캐시 및 기타 설정 구성
        profile = QWebEngineProfile.defaultProfile()
        profile.setPersistentStoragePath(self.cacheDirectory)
        profile.setHttpCacheType(QWebEngineProfile.NoCache)
        profile.setPersistentCookiesPolicy(QWebEngineProfile.ForcePersistentCookies)

        settings = profile.settings()
        settings.setAttribute(QWebEngineSettings.LocalStorageEnabled, True)
        settings.setAttribute(QWebEngineSettings.JavascriptEnabled, True)
        settings.setAttribute(QWebEngineSettings.PluginsEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebGLEnabled, True)

        self.setWindowTitle("OctXXIII")
        self.player = QMediaPlayer(self)
        self.video_info_list = []

        self.videoDuration = 0
        self.currentTime = 0
        self.originalTitle = ""  # Initialize the title attribute
        self.isPlaying = False  # Initialize the attribute to False

        self.initUI()

        self.scrollTimer = QTimer(self)
        self.scrollTimer.timeout.connect(self.scrollTitle)
        self.scrollTimer.start(300)  # Scroll title every 300 ms

        self.predefinedURL = "https://soundcloud.com/octxxiii"

    def createMiniPlayer(self):
        """미니 플레이어 창 생성"""
        self.mini_player = QDialog(self)
        self.mini_player.setWindowTitle("OctXXIII - Mini Player")
        self.mini_player.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint | Qt.WindowCloseButtonHint)
        self.mini_player.setFixedSize(300, 120)
        
        # 미니 플레이어 레이아웃
        mini_layout = QVBoxLayout(self.mini_player)
        mini_layout.setContentsMargins(10, 10, 10, 10)
        mini_layout.setSpacing(5)
        
        # 제목 레이블 (미니 버전)
        self.mini_title_label = QLabel()
        self.mini_title_label.setAlignment(Qt.AlignCenter)
        self.mini_title_label.setStyleSheet("""
            QLabel {
                color: white;
                border: 1px solid #555;
                border-radius: 3px;
                background-color: #333;
                padding: 2px;
                font-size: 10px;
            }
        """)
        self.mini_title_label.setWordWrap(False)
        
        # 플레이어 컨트롤 (미니 버전)
        mini_player_layout = QHBoxLayout()
        mini_player_layout.setSpacing(5)
        
        self.mini_back_button = QPushButton("⏮️")
        self.mini_back_button.setFixedSize(30, 30)
        self.mini_back_button.clicked.connect(self.play_back)
        
        self.mini_play_button = QPushButton("⏯️")
        self.mini_play_button.setFixedSize(35, 30)
        self.mini_play_button.clicked.connect(self.play)
        
        self.mini_next_button = QPushButton("⏭️")
        self.mini_next_button.setFixedSize(30, 30)
        self.mini_next_button.clicked.connect(self.play_next)
        
        # 볼륨 슬라이더 (미니 전용)
        self.mini_volume_slider = QSlider(Qt.Horizontal)
        self.mini_volume_slider.setRange(0, 100)
        self.mini_volume_slider.setValue(50)
        self.mini_volume_slider.setFixedWidth(90)
        self.mini_volume_slider.setToolTip("볼륨")
        self.mini_volume_slider.valueChanged.connect(self.mini_on_volume_changed)
        
        # 최상위 고정 토글 버튼
        self.always_on_top_button = QPushButton("📌")
        self.always_on_top_button.setFixedSize(30, 30)
        self.always_on_top_button.clicked.connect(self.toggleAlwaysOnTop)
        self.always_on_top_button.setToolTip("최상위 고정 토글")
        
        # 복원 버튼
        self.restore_button = QPushButton("🔼")
        self.restore_button.setFixedSize(30, 30)
        self.restore_button.clicked.connect(self.restoreFromMini)
        self.restore_button.setToolTip("원래 크기로 복원")
        
        mini_player_layout.addWidget(self.mini_back_button)
        mini_player_layout.addWidget(self.mini_play_button)
        mini_player_layout.addWidget(self.mini_next_button)
        mini_player_layout.addStretch()
        mini_player_layout.addWidget(self.mini_volume_slider)
        mini_player_layout.addWidget(self.always_on_top_button)
        mini_player_layout.addWidget(self.restore_button)
        
        mini_layout.addWidget(self.mini_title_label)
        mini_layout.addLayout(mini_player_layout)
        
        # 미니 플레이어 스타일 적용
        self.mini_player.setStyleSheet("""
            QDialog { 
                background-color: #2D2D2D; 
                border: 2px solid #555555;
                border-radius: 10px;
            }
            QPushButton { 
                background-color: #333333; 
                color: #FFFFFF; 
                border: 1px solid #555555; 
                border-radius: 5px; 
                padding: 2px; 
            }
            QPushButton:hover { background-color: #555555; }
            QPushButton:pressed { background-color: #444444; }
        """)
        
        # 미니 플레이어 닫기 이벤트 처리
        self.mini_player.closeEvent = self.miniPlayerCloseEvent
        
        # 마키 초기화
        self.mini_scroll_timer = QTimer(self)
        self.mini_scroll_timer.timeout.connect(self._mini_scroll_step)
        self.mini_original_title = ""
        self.mini_scroll_pos = 0

    def _update_mini_title_immediate(self):
        """미니 플레이어 제목 즉시 반영 및 스크롤 필요시 타이머 시작"""
        title = getattr(self, 'mini_original_title', '') or ''
        max_visible = 24
        
        # 스크롤 위치 초기화
        self.mini_scroll_pos = 0
        
        if len(title) > max_visible:
            # 긴 제목의 경우 처음 부분을 보여주고 스크롤 시작
            self.mini_title_label.setText(title[:max_visible])
            if hasattr(self, 'mini_scroll_timer'):
                self.mini_scroll_timer.start(300)
        else:
            # 짧은 제목의 경우 그대로 표시하고 스크롤 중지
            self.mini_title_label.setText(title)
            if hasattr(self, 'mini_scroll_timer'):
                self.mini_scroll_timer.stop()

    def _mini_scroll_step(self):
        """미니 플레이어 제목 스크롤 한 스텝"""
        title = getattr(self, 'mini_original_title', '') or ''
        if not title:
            return
        max_visible = 24
        if len(title) <= max_visible:
            if hasattr(self, 'mini_scroll_timer'):
                self.mini_scroll_timer.stop()
            return
        
        pos = getattr(self, 'mini_scroll_pos', 0)
        # 제목 끝까지 도달하면 처음으로 돌아가기
        if pos >= len(title):
            pos = 0
        
        # 현재 위치부터 max_visible만큼 표시
        display_text = title[pos:pos + max_visible]
        
        # 제목이 화면보다 길면 스크롤 효과를 위해 공백 추가
        if len(title) > max_visible:
            # 제목 끝에 도달하면 처음 부분을 보여주기 위해 순환
            if pos + max_visible > len(title):
                remaining = max_visible - (len(title) - pos)
                display_text = title[pos:] + "   " + title[:remaining]
        
        self.mini_title_label.setText(display_text)
        self.mini_scroll_pos = pos + 1

    def mini_on_volume_changed(self, value):
        # 0-100 → 0.0-1.0 변환하여 웹 비디오 볼륨 적용
        vol = max(0.0, min(1.0, value / 100.0))
        js = f"""
        (function() {{
            var v = document.querySelector('video');
            if (v) {{ v.volume = {vol}; return true; }}
            return false;
        }})();
        """
        try:
            if hasattr(self, 'browser') and self.browser:
                self.browser.page().runJavaScript(js)
        except Exception as e:
            print(f"mini_on_volume_changed js error: {e}")

    def miniPlayerCloseEvent(self, event):
        """미니 플레이어 닫기 시 메인 창도 닫기"""
        self.close()
        event.accept()

    def changeEvent(self, event):
        """창 상태 변경 이벤트 처리"""
        if event.type() == event.WindowStateChange:
            if self.isMinimized() and not self.is_mini_mode:
                self.switchToMiniMode()
        super().changeEvent(event)

    def switchToMiniMode(self):
        """미니 플레이어 모드로 전환"""
        if self.is_mini_mode:
            return
            
        self.is_mini_mode = True
        self.normal_geometry = self.geometry()
        
        # 메인 창 숨기기
        self.hide()
        
        # 미니 플레이어 표시
        if self.mini_player:
            # 현재 제목을 미니 플레이어에 동기화
            if hasattr(self, 'title_label') and self.title_label.text():
                title_text = self.title_label.text()
                if len(title_text) > 30:
                    title_text = title_text[:27] + "..."
                self.mini_title_label.setText(title_text)
            
            # 미니 플레이어를 화면 우하단에 위치
            screen = QApplication.desktop().screenGeometry()
            self.mini_player.move(screen.width() - 320, screen.height() - 200)
            self.mini_player.show()
            self.mini_player.raise_()
            self.mini_player.activateWindow()

    def restoreFromMini(self):
        """미니 플레이어에서 원래 크기로 복원"""
        if not self.is_mini_mode:
            return
            
        self.is_mini_mode = False
        
        # 미니 플레이어 숨기기
        if self.mini_player:
            self.mini_player.hide()
        
        # 메인 창 복원
        self.show()
        if self.normal_geometry:
            self.setGeometry(self.normal_geometry)
        self.setWindowState(Qt.WindowNoState)
        self.raise_()
        self.activateWindow()

    def toggleAlwaysOnTop(self):
        """미니 플레이어 최상위 고정 토글"""
        if not self.mini_player:
            return
            
        self.mini_always_on_top = not self.mini_always_on_top
        
        # 현재 위치 저장
        current_pos = self.mini_player.pos()
        
        # 윈도우 플래그 업데이트
        if self.mini_always_on_top:
            self.mini_player.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint | Qt.WindowCloseButtonHint)
            self.always_on_top_button.setText("📌")
            self.always_on_top_button.setToolTip("최상위 고정 해제")
        else:
            self.mini_player.setWindowFlags(Qt.Window | Qt.WindowCloseButtonHint)
            self.always_on_top_button.setText("📍")
            self.always_on_top_button.setToolTip("최상위 고정")
        
        # 위치 복원 및 다시 표시
        self.mini_player.move(current_pos)
        self.mini_player.show()
        self.mini_player.raise_()
        self.mini_player.activateWindow()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.on_search()
        elif event.key() == Qt.Key_Escape:
            self.lower()
        else:
            super().keyPressEvent(event)  # Handle other key events normally

    def get_video_info(url):
        ydl_opts = {
            'quiet': True,
            'no_warnings': False, # WARNING 메시지를 보기 위해 False로 설정
            'skip_download': True,
            'ignoreerrors': True, # 일부 오류 무시
            'ignore_no_formats_error': True, # 포맷 없는 오류 무시
            # 'allow_unplayable_formats': True, # 디버깅용
            # 'verbose': True, # 더 자세한 로그
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best', # mp4 선호
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(url, download=False)
            if 'entries' in result:
                # Can handle a playlist or a list of videos, takes the first video
                video = result['entries'][0]
            else:
                # Just a single video
                video = result

            return {
                'duration': video.get('duration'),
                'title': video.get('title'),
                'url': video.get('webpage_url'),
            }

    def initUI(self):
        # Left Layout: Web Browser View and Navigation Buttons
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("https://www.youtube.com"))
        self.homePageUrl = QUrl("https://www.youtube.com")
        self.musicPageUrl = QUrl("https://music.youtube.com")
        self.SCPageUrl = QUrl("https://soundcloud.com/")

        self.toggleDownButton = QPushButton("💥", self)
        self.toggleDownButton.clicked.connect(self.toggleBrowser)
        self.toggleDownButton.setFixedSize(30, 30)

        # Navigation Buttons
        self.backButton = QPushButton('👈')
        self.backButton.clicked.connect(self.browser.back)
        self.refreshButton = QPushButton('🔄')
        self.refreshButton.setFixedSize(30, 30)
        self.refreshButton.clicked.connect(self.browser.reload)
        self.homeButton = QPushButton()
        self.homeButton.setFixedSize(30, 30)
        self.homeButton.setIcon(QIcon(':/homeIcon')) # 아이콘 설정 복원
        self.homeButton.clicked.connect(lambda: self.browser.setUrl(self.homePageUrl))
        self.musicButton = QPushButton()
        self.musicButton.setFixedSize(30, 30)
        self.musicButton.setIcon(QIcon(':/musicIcon')) # 아이콘 설정 복원
        self.musicButton.clicked.connect(lambda: self.browser.setUrl(self.musicPageUrl))
        self.SCButton = QPushButton()
        self.SCButton.setFixedSize(30, 30)
        self.SCButton.setIcon(QIcon(':/soundCloudIcon')) # 아이콘 설정 복원
        self.SCButton.clicked.connect(lambda: self.browser.setUrl(self.SCPageUrl))
        self.forwardButton = QPushButton('👉')
        self.forwardButton.clicked.connect(self.browser.forward)

        # Navigation Layout
        self.navLayout = QHBoxLayout()
        self.navLayout.addWidget(self.backButton)
        self.navLayout.addWidget(self.forwardButton)
        self.navLayout.addWidget(self.refreshButton)
        self.navLayout.addWidget(self.homeButton)  # Adding the home button between back and forward
        self.navLayout.addWidget(self.musicButton)
        self.navLayout.addWidget(self.SCButton)
        self.navLayout.addWidget(self.toggleDownButton)

        # Left Widget for Browser and Navigation
        self.browWidget = QWidget()
        self.leftLayout = QVBoxLayout(self.browWidget)
        self.leftLayout.addLayout(self.navLayout)
        self.leftLayout.addWidget(self.browser)

        # Right Layout: Existing UI Elements
        self.setupRightLayout()

        fixedWidth = 450
        self.downLayoutWidget.setFixedWidth(fixedWidth)

        # Splitter for dividing the layout into left and right sections
        self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.addWidget(self.browWidget)  # Adding left widget to the splitter
        self.splitter.addWidget(self.downLayoutWidget)

        # Prevent the right widget from resizing by fixing its maximum size
        self.downLayoutWidget.setMaximumSize(QSize(fixedWidth, 16777215))

        # Main Layout
        mainLayout = QVBoxLayout(self)
        mainLayout.setContentsMargins(0, 0, 0, 0)
        mainLayout.addWidget(self.splitter)
        self.setLayout(mainLayout)

        # Adjust initial split sizes
        self.splitter.setSizes([500, 300])
        self.browser.setMinimumSize(500, 300)
        self.browser.setZoomFactor(0.8)

        self.browser.loadFinished.connect(self.updateButtonStates)
        
        # 미니 플레이어 생성
        self.createMiniPlayer()

    def setupRightLayout(self):
        # Create a widget for the right side layout
        self.downLayoutWidget = QWidget()
        self.downLayoutWidget.setContentsMargins(0, 0, 0, 0)
        self.downLayoutWidget.setFixedSize(450, 560)
        self.rightLayout = QVBoxLayout(self.downLayoutWidget)

        # Initialize all widgets for the right side layout
        # self.theme_selector = QComboBox() # 테마 선택 콤보박스 삭제
        # self.theme_selector.setFixedSize(356, 30) # 테마 선택 콤보박스 삭제
        self.browHideButton = QPushButton('🦕')
        self.browHideButton.setFixedSize(30, 30)
        self.browHideButton.clicked.connect(self.toggleBrowWidgetVisibility)
        self.createrButton = QPushButton('💬')
        self.createrButton.setFixedSize(30, 30)
        self.createrButton.clicked.connect(self.openSettingsDialog)
        self.copyUrlButton = QPushButton('📋')
        self.copyUrlButton.setFixedSize(30, 30)
        self.search_url = QLineEdit()
        self.search_url.setStyleSheet("""
            QLineEdit {
                border: 2px solid #555555;  /* Adjust border color as needed */
                border-radius: 5px;  /* Adjust for more or less rounding */
                padding: 0px;
                background-color: #2D2D2D;  /* Adjust background color as needed */
                color: #ffffff;  /* Adjust text color as needed */
            }
        """)
        self.search_url.setFixedSize(356, 30)
        self.search_url.setClearButtonEnabled(True)
        self.search_button = QPushButton('🔍')
        self.search_button.setFixedSize(30, 30)
        self.download_list = QPushButton('📍')
        self.download_list.setFixedSize(100, 30)
        self.later_list = QPushButton('📌')
        self.later_list.setFixedSize(100, 30)
        self.video_table = QTableWidget()
        self.download_button = QPushButton('📥')
        self.delete_button = QPushButton('❌')
        self.status_label = QLabel('Ready')
        self.progress_bar = QProgressBar()

        self.back_button = QPushButton("⏮️", self)
        self.back_button.clicked.connect(self.play_back)
        self.play_button = QPushButton("⏯️", self)
        self.play_button.clicked.connect(self.play)
        self.next_button = QPushButton("⏭️", self)
        self.next_button.clicked.connect(self.play_next)  # Connect the button to the play_next method
        self.title_label = QLabel()
        self.title_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)  # Align text to the left and vertically center
        self.title_label.setStyleSheet("""
                QLabel {
                    color: white;
                    border: 2px solid #555;
                    border-radius: 5px;
                    background-color: #333;
                    padding: 4px 4px 4px 4px;
                }
            """)
        self.title_label.setWordWrap(False)

        # self.theme_selector.addItems(themes.keys()) # 테마 선택 콤보박스 관련 코드 삭제
        # self.theme_selector.currentIndexChanged.connect(self.applySelectedTheme) # 테마 선택 콤보박스 관련 코드 삭제
        self.search_button.clicked.connect(self.on_search)
        self.copyUrlButton.clicked.connect(self.copyUrlToClipboard)
        self.download_button.clicked.connect(self.on_download)
        self.delete_button.clicked.connect(self.on_delete_selected)

        self.setupVideoTable()

        self.animation_timer = QTimer(self)
        self.animation_timer.timeout.connect(self.toggle_loading_animation)
        self.direction = 1

        # settingsLayout은 이제 비게 되므로, 관련 위젯 추가 코드를 제거합니다.
        settingsLayout = QHBoxLayout()
        settingsLayout.setContentsMargins(0, 0, 0, 0)  # Set the margins to 0
        settingsLayout.setSpacing(5)  # Set the spacing between widgets
        # settingsLayout.addWidget(self.browHideButton) # titleLayout으로 이동
        # settingsLayout.addWidget(self.createrButton) # titleLayout으로 이동
        # settingsLayout.addStretch(1) # 위젯이 없으므로 스트레치도 제거

        titleLayout = QHBoxLayout()
        titleLayout.setContentsMargins(0, 0, 0, 0)
        titleLayout.setSpacing(5) # 버튼과 레이블 사이 간격 설정
        titleLayout.addWidget(self.browHideButton) # titleLayout 좌측에 추가
        titleLayout.addWidget(self.title_label) # title_label을 중앙으로 이동
        titleLayout.addWidget(self.createrButton) # createrButton을 titleLayout 우측에 추가

        playerLayout = QHBoxLayout()
        playerLayout.setContentsMargins(0, 0, 0, 0)
        playerLayout.setSpacing(5)
        playerLayout.addWidget(self.back_button)
        playerLayout.addWidget(self.play_button)
        playerLayout.addWidget(self.next_button)

        # self.positionSlider = QSlider(Qt.Horizontal, self)
        # self.positionSlider.setRange(0, 100)
        # self.durationLabel = QLabel("00:00 / 00:00", self)
        # self.setupMediaControls()
        #
        # positionLayout = QHBoxLayout()
        # positionLayout.setContentsMargins(0, 0, 0, 0)
        # positionLayout.setSpacing(5)
        # positionLayout.addWidget(self.positionSlider)
        # positionLayout.addWidget(self.durationLabel)

        # Group related widgets
        searchLayout = QHBoxLayout()
        searchLayout.setContentsMargins(0, 0, 0, 0)  # Set the margins to 0
        searchLayout.setSpacing(5)  # Set the spacing between widgets
        searchLayout.addWidget(self.copyUrlButton)
        searchLayout.addWidget(self.search_url)
        searchLayout.addWidget(self.search_button)
        # searchLayout.addStretch(1)  # This will push everything to the left

        listLayout = QHBoxLayout()

        statusLayout = QHBoxLayout()
        statusLayout.addWidget(self.progress_bar)
        statusLayout.addWidget(self.status_label)

        actionLayout = QHBoxLayout()
        actionLayout.addWidget(self.download_button)
        actionLayout.addWidget(self.delete_button)

        # Add grouped layouts to the main right layout
        # self.rightLayout.addLayout(settingsLayout) # settingsLayout이 비었으므로 제거
        self.rightLayout.addLayout(titleLayout)
        self.rightLayout.addLayout(playerLayout)
        # self.rightLayout.addLayout(positionLayout)
        self.rightLayout.addLayout(searchLayout)
        self.rightLayout.addWidget(self.video_table)
        self.rightLayout.addLayout(statusLayout)
        self.rightLayout.addLayout(actionLayout)
        # self.rightLayout.addLayout(settingsLayout)

        self.browser.titleChanged.connect(self.updateTitle)
        self.resetTimer = QTimer(self)  # Timer for delaying the reset of media controls
        self.resetTimer.setSingleShot(True)  # Ensure the timer only triggers once per timeout
        self.resetTimer.timeout.connect(self.performResetMediaControls)  # Connect timeout signal to the reset method
        self.browser.urlChanged.connect(self.checkAndTriggerReset)

        self.setStyleSheet(DARK_THEME_STYLESHEET) # 다크 테마 직접 적용

    def checkAndTriggerReset(self, url):
        """Check the URL and trigger the reset with a delay if it is the YouTube homepage."""
        if url.toString() == "https://www.youtube.com/":
            self.resetTimer.start(1000)  # Start the timer with a delay of 1000 milliseconds (1 second)

    def performResetMediaControls(self):
        """Reset the media controls."""
        # self.positionSlider.setValue(0)
        # self.durationLabel.setText("00:00 / 00:00")
        self.play_button.setIcon(QIcon(":/play_icon"))  # Reset to play icon
        self.play_button.setText("▶️")

    # def setupMediaControls(self):
    #     # Timer to update the position slider and duration label
    #     self.updateTimer = QTimer(self)
    #     self.updateTimer.timeout.connect(self.updateMediaStatus)
    #     self.updateTimer.start(1000)  # Update every second
    #
    #     # Connect the slider's valueChanged signal to the seekVideo method
    #     self.positionSlider.valueChanged.connect(self.seekVideo)
    #     self.positionSlider.sliderReleased.connect(
    #         self.onSliderRelease)  # Ensure seeking only occurs after user interaction

    def updateMediaStatus(self):
        """Check the media status and update controls."""
        jsCode = """
        (function() {
            var video = document.querySelector('video');
            if (video) {
                return {
                    playing: !video.paused && !video.ended && video.readyState > 2,
                    currentTime: video.currentTime,
                    duration: video.duration
                };
            }
            return null;
        })();
        """
        self.browser.page().runJavaScript(jsCode, self.onMediaStatusReceived)

    @pyqtSlot(object)
    def onMediaStatusReceived(self, result):
        if result:
            # Update the slider and duration label
            current_time = result.get('currentTime', 0)
            duration = result.get('duration', 0)
            if duration > 0:
                self.positionSlider.setValue(int((current_time / duration) * 100))
                self.update_duration_label(current_time, duration)

            # Manage scrolling based on playback state
            if result.get('playing', False):
                if not self.isPlaying:
                    self.isPlaying = True
                    self.startScrolling()  # Start scrolling if the video is playing
            else:
                if self.isPlaying:
                    self.isPlaying = False
                    self.stopScrolling()  # Stop scrolling if the video is not playing
        else:
            # print("No valid video found or video not ready.")
            self.stopScrolling()  # Ensure scrolling is stopped if video isn't ready

    def startScrolling(self):
        """Start the scroll timer."""
        if not self.scrollTimer.isActive():
            self.scrollTimer.start(300)

    def stopScrolling(self):
        """Stop the scroll timer."""
        if self.scrollTimer.isActive():
            self.scrollTimer.stop()

    def updateUISliderAndLabel(self, current_time, duration):
        if duration > 0:
            self.positionSlider.setValue(int((current_time / duration) * 100))
            self.update_duration_label(current_time, duration)
        else:
            print("No valid video or duration available.")

    def seekVideo(self):
        value = self.positionSlider.value()
        # Convert slider value to media time
        jsCode = f"""
        (function() {{
            var video = document.querySelector('video');
            if (video) {{
                var seekTime = video.duration * ({value} / 100);
                video.currentTime = seekTime;
            }}
        }})();
        """
        self.browser.page().runJavaScript(jsCode)

    # def onSliderRelease(self):
    #     # Calls seekVideo only when the user releases the slider
    #     self.seekVideo()
    #
    # def update_duration_label(self, current_time, duration):
    #     self.durationLabel.setText(f"{self.format_time(current_time)} / {self.format_time(duration)}")

    # def format_time(self, seconds):
    #     hours = int(seconds // 3600)
    #     minutes = int((seconds % 3600) // 60)
    #     seconds = int(seconds % 60)
    #     if hours > 0:
    #         return f"{hours:02}:{minutes:02}:{seconds:02}"
    #     else:
    #         return f"{minutes:02}:{seconds:02}"

    def scrollTitle(self):
        """Scrolls the video title if it is longer than the display area."""
        if not self.originalTitle:  # Check if the title is not set
            return  # Skip scrolling if there's no title

        displayLength = 50  # Adjust based on your display needs
        titleLength = len(self.originalTitle)

        # Update the title display based on current scroll position
        if titleLength > displayLength:
            # Logic to scroll the title smoothly
            scrolledTitle = self.originalTitle[self.scrollPosition:] + '   ' + self.originalTitle
            self.title_label.setText(scrolledTitle[:displayLength])
            self.scrollPosition = (self.scrollPosition + 1) % titleLength
        else:
            self.title_label.setText(self.originalTitle)
            self.scrollTimer.stop()  # Stop the timer if no scrolling is needed

    def updateTitle(self, newTitle):
        """Updates the title displayed on the UI."""
        self.originalTitle = newTitle
        self.scrollPosition = 0  # Reset scroll position with new title
        if len(newTitle) > 50:  # Assuming 20 is the max visible chars
            if not self.scrollTimer.isActive():
                self.scrollTimer.start(300)
        else:
            self.scrollTimer.stop()
        self.title_label.setText(newTitle)  # Set title immediately without scrolling
        
        # 미니 플레이어 제목도 업데이트 (마키 적용)
        if hasattr(self, 'mini_player') and self.mini_player and hasattr(self, 'mini_title_label'):
            self.mini_original_title = newTitle
            self.mini_scroll_pos = 0
            self._update_mini_title_immediate()

        # 재생 상태 확인 및 버튼 업데이트
        self.checkPlaybackState()

    def checkPlaybackState(self):
        jsCode = """
        (function() {
            var video = document.querySelector('video');
            if (video) {
                return video.paused ? 'paused' : 'playing';
            }
            return 'unknown';
        })();
        """
        self.browser.page().runJavaScript(jsCode, self.updatePlayButtonIcon)

    def startScrolling(self):
        # Only start the timer if the title needs scrolling
        if len(self.originalTitle) * 50 > self.title_label.width():
            self.scrollTimer.start(300)  # Adjust scrolling speed as needed

    def checkNeedForScrolling(self):
        # Determine if the title's length exceeds the label's display capacity
        if len(self.originalTitle) * 50 > self.title_label.width():
            self.scrollTimer.start(300)  # Restart scrolling with a delay
        else:
            self.title_label.setText(self.originalTitle)

    def updateButtonStates(self):
        current_url = self.browser.url().toString()
        is_youtube_music = "music.youtube.com" in current_url

        # Assuming you have a QWidget named self.playWidget that contains your media controls
        if is_youtube_music:
            self.play_button.hide()  # Hide the play widget if on YouTube Music
            self.next_button.hide()  # Hide the play widget if on YouTube Music
            self.back_button.hide()  # Hide the play widget if on YouTube Music


        else:
            self.play_button.show()  # Hide the play widget if on YouTube Music
            self.next_button.show()  # Hide the play widget if on YouTube Music
            self.back_button.show()  # Hide the play widget if on YouTube Music

        # Update the state of the buttons based on the content
        self.play_button.setEnabled(not is_youtube_music)
        self.next_button.setEnabled(not is_youtube_music)
        self.back_button.setEnabled(not is_youtube_music)

        if is_youtube_music:
            self.title_label.setText("YouTube Music에서는 컨트롤이 작동하지 않습니다.")
        else:
            self.title_label.setText("")

    def play_back(self):
        # Check if the current site is YouTube and adjust behavior
        current_url = self.browser.url().toString()
        youtube_homepage = "https://www.youtube.com/"

        # Check if the current URL is exactly the YouTube homepage
        if current_url.startswith(youtube_homepage) and len(current_url.strip('/')) == len(youtube_homepage.strip('/')):
            # Do not navigate back if on the YouTube homepage
            return
        elif "youtube.com" in current_url:
            self.browser.back()  # Navigate back in browser history if not on the homepage
        else:
            # JavaScript code to simulate clicking the "Previous" button for SoundCloud
            jsCode = """
            (function() {
                const host = window.location.host;
                if (host.includes('soundcloud.com')) {
                    document.querySelector('.playControls__prev')?.click();
                }
            })();
            """
            self.browser.page().runJavaScript(jsCode)

    def play(self):
        # JavaScript code to play/pause and return the current state
        jsCode = """
        (function() {
            const host = window.location.host;
            if (host.includes('youtube.com')) {
                var video = document.querySelector('video');
                if (video) {
                    if (video.paused) {
                        video.play();
                        return 'playing';
                    } else {
                        video.pause();
                        return 'paused';
                    }
                }
            } else if (host.includes('soundcloud.com')) {
                var playButton = document.querySelector('.playControls__play');
                if (playButton) {
                    if (playButton.classList.contains('playing')) {
                        playButton.click();
                        return 'paused';
                    } else {
                        playButton.click();
                        return 'playing';
                    }
                }
            }
            return 'unknown';
        })();
        """
        # Execute the JavaScript code and update the play button icon based on the returned state
        self.browser.page().runJavaScript(jsCode, self.updatePlayButtonIcon)

    @pyqtSlot(str)
    def updatePlayButtonIcon(self, state):
        if state == 'playing':
            self.play_button.setText("⏸️")  # Update to pause icon
            # 미니 플레이어 버튼도 동기화
            if hasattr(self, 'mini_play_button'):
                self.mini_play_button.setText("⏸️")
        elif state == 'paused':
            self.play_button.setText("▶️")  # Update to play icon
            # 미니 플레이어 버튼도 동기화
            if hasattr(self, 'mini_play_button'):
                self.mini_play_button.setText("▶️")
        else:
            # Optionally handle 'unknown' state or other states if necessary
            pass

    def play_next(self):
        # JavaScript 코드로 다음 영상으로 이동하고 재생 여부 확인
        jsCode = """
        (function() {
            const host = window.location.host;
            if (host.includes('youtube.com')) {
                document.querySelector('.ytp-next-button')?.click();
                var video = document.querySelector('video');
                if (video) {
                    // Delay to ensure the video state is updated after the next button is clicked
                    setTimeout(function() {
                        if (!video.paused) {
                            video.play();
                            return 'playing';
                        } else {
                            return 'paused';
                        }
                    }, 100); // Adjust delay as needed to match loading times
                }
            } else if (host.includes('soundcloud.com')) {
                document.querySelector('.skipControl__next')?.click();
                // Assuming SoundCloud plays automatically, return 'playing'
                return 'playing';
            }
            return 'unknown';
        })();
        """
        # JavaScript 실행 후 반환된 재생 상태에 따라 버튼 아이콘 업데이트
        self.browser.page().runJavaScript(jsCode, self.updatePlayButtonIcon)

    def setupVideoTable(self):
        self.video_table.setColumnCount(4)  # Adjust the count as necessary
        self.video_table.setHorizontalHeaderLabels(['', 'Thumbnail', 'Title', 'Format'])
        self.header = CheckBoxHeader()
        self.video_table.setHorizontalHeader(self.header)
        self.header.cb.clicked.connect(self.header.selectAll)
        header = self.video_table.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        self.video_table.horizontalHeader().setVisible(True)
        self.video_table.verticalHeader().setVisible(False)
        self.video_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.video_table.setShowGrid(False)  # This line is corrected
        self.video_table.setColumnWidth(0, 100)
        self.video_table.setColumnWidth(1, 150)
        self.video_table.setColumnWidth(2, 300)
        self.video_table.setColumnWidth(3, 180)

        self.video_table.itemChanged.connect(self.handle_item_changed) # itemChanged 시그널 연결

    def handle_item_changed(self, item):
        """테이블 아이템 변경 시 호출되어 헤더 체크박스 상태 업데이트"""
        if item.column() == 0: # 첫 번째 열 (체크박스 열)의 아이템이 변경된 경우
            self.header.updateState()

    def copyUrlToClipboard(self):
        currentUrl = self.browser.url().toString()
        print(f"Current URL: {currentUrl}")  # Debug print
        clipboard = QApplication.clipboard()
        clipboard.setText(currentUrl)
        self.search_url.setText(currentUrl)
        self.search_url.clear()
        self.search_url.setText(currentUrl)
        self.on_search()

    def navigateToLink(self):
        # Handle the predefined URL here. This could involve opening the URL in a web browser,
        # or performing another action based on the URL.
        print(f"Navigate to: {self.predefinedURL}")
        # Example: Open the URL in a web browser
        QDesktopServices.openUrl(QUrl(self.predefinedURL))

    def openSettingsDialog(self):
        if not self.settingsDialog:
            try:
                self.settingsDialog = SettingsDialog(self)
                self.settingsDialog.dialogClosed.connect(self.refreshBrowser)
                self.settingsDialog.finished.connect(self.onSettingsDialogClosed)
                self.settingsDialog.show()
            except Exception as e:
                # 예외로 앱이 종료되지 않도록 방어
                self.settingsDialog = None
                QMessageBox.critical(self, "Error", f"정보 창을 여는 중 오류가 발생했습니다:\n{e}")
        else:
            self.settingsDialog.raise_()  # Brings the dialog to the front if already open

    def onSettingsDialogClosed(self):
        self.settingsDialog.deleteLater()
        self.settingsDialog = None  # Clear the reference after the dialog is closed

    def refreshBrowser(self):
        """ Method to refresh the browser when the settings dialog is closed """
        if hasattr(self, 'browser') and self.browser is not None:
            self.browser.reload()
        else:
            print("Browser attribute is not set or is None")

    def toggleBrowser(self):
        if self.downLayoutWidget.isVisible():
            self.downLayoutWidget.hide()
            self.toggleDownButton.setText("😜")
            self.adjustMainLayoutSize()
        else:
            self.downLayoutWidget.show()
            self.toggleDownButton.setText("💥")
            self.resetMainLayoutSize()

    def toggleBrowWidgetVisibility(self):
        if self.browWidget.isVisible():
            self.browWidget.hide()
            self.browHideButton.setText('💥')  # Example icon when visible
            self.adjustMainLayoutSize()

        else:
            self.browWidget.show()
            self.browHideButton.setText('🦕')  # Example icon when hidden
            self.resetMainLayoutSize()

    def adjustMainLayoutSize(self):
        if not self.browWidget.isVisible():
            # 윈도우가 축소되지 않도록 최소 크기 설정
            self.setMinimumSize(450, 560)

            # 오른쪽 위젯을 맞추기 위해 메인 윈도우 크기 조정
            # 참고: 원하는 다른 동작이 있다면 조정할 수 있습니다.
            self.resize(450, 560)

            # downLayoutWidget에 선호하는 최소 크기가 있는지 확인합니다.
            self.downLayoutWidget.setMinimumSize(450, 560)

            # browWidget의 최소 크기를 조정하여 완전한 축소가 가능하도록 합니다.
            self.browWidget.setMinimumSize(0, 0)
        else:
            # browWidget이 다시 표시되면 윈도우가 확장되도록 합니다.
            # 전체 윈도우에 합리적인 최소 크기를 설정합니다.
            self.setMinimumSize(980, 560)

            # 두 위젯을 수용하기 위해 메인 윈도우 크기 조정
            # 필요에 따라 숨기기 전의 이전 크기를 저장하고 복원할 수 있습니다.
            self.resize(980, 560)

            # 두 위젯의 최소 크기를 복원합니다.
            self.browWidget.setMinimumSize(500, 560)  # 컨텐츠에 맞게 필요에 따라 조정합니다.
            self.downLayoutWidget.setMinimumSize(450, 560)

    def resetMainLayoutSize(self):
        # When making the browser visible again, adjust the layout to accommodate both widgets.
        self.setMinimumSize(1100, 560) # 최소 크기를 테마 선택기 제외한 크기로 조정 가능
        self.browWidget.setMinimumSize(500, 560)
        self.downLayoutWidget.setMinimumSize(450, 560) # 오른쪽 레이아웃 최소 너비 고정

        # Adjust splitter sizes to distribute space according to your preference.
        self.splitter.setSizes([500, 450]) # 스플리터 크기 조정

    def center_on_screen(self):
        # Get the main screen's geometry
        screen_geometry = QApplication.desktop().screenGeometry()

        # Calculate the center point
        center_point = screen_geometry.center()

        # Set the center point of the dialog
        self.move(center_point - self.rect().center())

    def search_duplicate_urls(self, url):
        return any(url == video_info[1] for video_info in self.video_info_list)

    def toggle_loading_animation(self):
        current_value = self.progress_bar.value()
        max_value = self.progress_bar.maximum()
        min_value = self.progress_bar.minimum()

        if current_value >= max_value or current_value <= min_value:
            self.direction *= -1
            self.animation_timer.stop()  # Stop the animation when loading is complete
        else:
            new_value = current_value + self.direction * 5
            self.progress_bar.setValue(new_value)

    def add_video_info(self, title, url):
        # Check if the URL is already in the list
        if not any(url == existing_url for _, existing_url in self.video_info_list):
            self.video_info_list.append((title, url))
            # Update the UI accordingly, e.g., adding a row to the table

    def is_duplicate_url(self, url):
        return any(url == existing_url for _, existing_url in self.video_info_list)

    def delete_selected_videos(self):
        # This assumes you have a method to determine which videos are selected for deletion
        selected_indexes = self.get_selected_video_indexes()
        self.video_info_list = [info for idx, info in enumerate(self.video_info_list) if idx not in selected_indexes]
        # Refresh the UI to reflect the changes

    @pyqtSlot()
    def on_search(self):
        url = self.search_url.text().strip()

        if self.is_duplicate_url(url):
            self.status_label.setText("이 비디오는 이미 목록에 추가되었습니다.")
            return

        self.search_button.setEnabled(False)
        self.animation_timer.start(50)
        self.set_status('로딩 중...')
        self.progress_bar.setRange(0, 0)  # Set to indeterminate mode

        self.search_thread = Searcher(url)
        self.search_thread.updated_list.connect(self.update_video_list)
        self.search_thread.finished.connect(self.search_finished)
        self.search_thread.finished.connect(self.enable_search_button)
        self.search_thread.finished.connect(self.check_results)  # Connect to a new slot to check for results
        self.search_thread.start()

    def check_results(self):
        # Assuming self.video_info_list is updated with search results
        if not self.video_info_list:
            self.status_label.setText("검색 결과가 없습니다.")

    def enable_search_button(self):
        self.search_button.setEnabled(True)
        self.progress_bar.setRange(0, 100)  # Reset the progress bar range

    def set_status(self, message):
        self.status_label.setText(message)

    @pyqtSlot(str, str, str, list)
    def update_video_list(self, title, thumbnail_url, video_url, formats_info_list):
        row_position = self.video_table.rowCount()
        self.video_table.insertRow(row_position)
        self.video_info_list.append((title, video_url))

        # Checkbox
        chkBoxItem = QTableWidgetItem()
        chkBoxItem.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
        chkBoxItem.setCheckState(Qt.Unchecked)
        self.video_table.setItem(row_position, 0, chkBoxItem)

        title_item = QTableWidgetItem(title)
        title_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable)  # Allow editing
        self.video_table.setItem(row_position, 2, title_item)

        if thumbnail_url:
            response = requests.get(thumbnail_url)
            pixmap = QPixmap()
            if pixmap.loadFromData(response.content):
                pixmap_resized = pixmap.scaled(30, 30, Qt.KeepAspectRatio)
                thumbnail_item = QTableWidgetItem()
                thumbnail_item.setData(Qt.DecorationRole, pixmap_resized)
                self.video_table.setItem(row_position, 1, thumbnail_item)

        # Format combo box with categorized and ordered formats
        format_combo = QComboBox()

        # 카테고리별로 포맷 추가
        current_category = None
        if not formats_info_list: # 포맷 정보가 없으면
            format_combo.addItem("No available formats", None) # userData도 None
        else:
            for display_text, format_id, type_label, filesize in formats_info_list:
                # 카테고리 헤더 추가 (type_label 변경 시)
                if type_label != current_category:
                    if format_combo.count() > 0 and current_category is not None: # 첫 카테고리가 아니고, 이전 카테고리가 있었다면 구분선 고려 가능
                        pass # 구분선 대신 카테고리명으로 구분
                    format_combo.addItem(f"--- {type_label} --- ") # 카테고리 명칭 표시
                    format_combo.model().item(format_combo.count() - 1).setEnabled(False) # 카테고리명은 선택 불가
                    current_category = type_label
                
                format_combo.addItem(display_text, userData=format_id) # userData에 format_id 저장

        # Set the default format if available
        # 첫 번째 실제 선택 가능한 아이템을 기본값으로 설정
        default_index = -1
        for i in range(format_combo.count()):
            if format_combo.model().item(i).isEnabled():
                default_index = i
                break
        if default_index != -1:
            format_combo.setCurrentIndex(default_index)

        self.video_table.setCellWidget(row_position, 3, format_combo)

    def search_finished(self):
        self.set_status('검색 완료.')
        self.progress_bar.setRange(0, 100)  # Reset the progress bar range
        self.progress_bar.setValue(100)  # Set completion value

    def download_finished(self):
        self.status_label.setText('다운로드 완료.')

    def set_status(self, message):
        self.status_label.setText(message)

    @pyqtSlot(float)
    def update_progress_bar(self, progress):
        self.progress_bar.setValue(int(progress))

    def status_update(self, message):
        self.status_label.setText(message)

    def progress_update(self, progress):
        self.progress_bar.setValue(progress)

    def get_selected_videos(self):
        return {index.row() for index in self.video_table.selectedIndexes() if index.column() == 0}

    @pyqtSlot()
    def on_download(self):
        selected_videos = []
        invalid_selection = False

        for row in range(self.video_table.rowCount()):
            checkbox = self.video_table.item(row, 0)
            # 체크된 항목만 다운로드
            if not (checkbox and checkbox.checkState() == Qt.Checked):
                continue

            # 변수들을 먼저 초기화
            title_item = self.video_table.item(row, 2)
            format_combo_box = self.video_table.cellWidget(row, 3)
            selected_format_id = None
            
            # 제목과 URL 가져오기
            modified_title = title_item.text() if title_item else "Untitled"
            video_url = self.video_info_list[row][1]
            
            # 포맷 ID 확인
            if format_combo_box:
                selected_format_id = format_combo_box.currentData()
                if selected_format_id is None:
                    current_text = format_combo_box.currentText()
                    if "--- " in current_text or current_text == "No available formats":
                        invalid_selection = True
                        break
                    else:
                        invalid_selection = True
                        break

            if selected_format_id is None:
                invalid_selection = True
                break

            selected_videos.append((modified_title, video_url, selected_format_id))

        if invalid_selection:
            self.status_label.setText("각 비디오에 대해 유효한 포맷을 선택해 주세요.")
            return

        if selected_videos:
            self.start_download(selected_videos)
        else:
            self.status_label.setText("다운로드할 비디오를 최소 하나 이상 선택해 주세요.")

    def start_download(self, selected_videos):
        # This method should initiate the download process for the selected videos.
        # Ensure you have the Downloader class properly defined to accept the videos and download directory.

        download_directory = self.select_download_directory()
        if not download_directory:
            self.status_label.setText("유효한 다운로드 디렉토리를 선택해 주세요.")
            return

        # Initialize and start the Downloader thread
        self.downloader_thread = Downloader(selected_videos, download_directory)
        self.downloader_thread.download_failed.connect(self.download_failed)
        self.downloader_thread.updated_status.connect(self.set_status)
        self.downloader_thread.updated_progress.connect(self.update_progress_bar)
        self.downloader_thread.start()

    def download_failed(self, message):
        self.set_status(f"다운로드 실패: {message}")

    def select_download_directory(self):
        dir_path = QFileDialog.getExistingDirectory(self, "다운로드 디렉토리 선택", os.path.expanduser("~"))
        return dir_path if dir_path else None

    @pyqtSlot()
    def on_delete_selected(self):
        # 테이블에서 선택된 행들을 역순으로 순회하며 삭제
        # 역순으로 하는 이유는 행 삭제 시 인덱스가 변경되는 것을 방지하기 위함
        rows_to_delete = []
        for row in range(self.video_table.rowCount()):
            checkbox_item = self.video_table.item(row, 0) # 체크박스는 첫 번째 열에 있다고 가정
            if checkbox_item and checkbox_item.checkState() == Qt.Checked:
                rows_to_delete.append(row)

        if not rows_to_delete:
            self.status_label.setText("삭제할 비디오를 선택해 주세요.")
            return

        for row in sorted(rows_to_delete, reverse=True):
            # video_info_list에서도 해당 정보 삭제 (인덱스 주의)
            if row < len(self.video_info_list):
                self.video_info_list.pop(row)
            # 테이블에서 행 삭제
            self.video_table.removeRow(row)
        
        self.header.updateState() # 헤더 체크박스 상태 업데이트
        self.status_label.setText(f"{len(rows_to_delete)}개 비디오 삭제 완료.")


class MainThreadSignalEmitter(QObject):
    # Signal to emit warning messages
    warning_message = pyqtSignal(str)

    def __init__(self):
        super().__init__()

    def emit_warning(self, message):
        # Emit warning message signal
        self.warning_message.emit(message)


main_thread_signal_emitter = MainThreadSignalEmitter()


class Searcher(QThread):
    updated_list = pyqtSignal(str, str, str, list)  # title, thumbnail_url, video_url, [(display_text, format_id, type_label, filesize)]
    search_progress = pyqtSignal(int, int)  # Signal with two arguments: current progress and total count

    def __init__(self, url, parent=None):
        super().__init__(parent)
        self.url = url

    def run(self):
        # extract_flat 옵션을 제거하거나 False로 설정하여 전체 포맷 정보를 가져옵니다.
        ydl_opts = {
            'quiet': True,
            'no_warnings': False, # WARNING 메시지를 보기 위해 False로 설정
            'skip_download': True,
            'ignoreerrors': True, # 일부 오류 무시
            'ignore_no_formats_error': True, # 포맷 없는 오류 무시
            # 'allow_unplayable_formats': True, # 디버깅용
            # 'verbose': True, # 더 자세한 로그
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best', # mp4 선호
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                result = ydl.extract_info(self.url, download=False)
                videos = result.get('entries', [result])
                if not videos:
                    print("[Debug Searcher] No videos/entries found in yt_dlp result.")
                    self.updated_list.emit(result.get('title', 'Video/Playlist not found'), "", self.url, [])
                    return

                for video_index, video in enumerate(videos):
                    raw_formats = video.get('formats', [])
                    processed_format_list = []

                    if not raw_formats:
                        print(f"[Debug Searcher] Video {video_index + 1} ('{video.get('title', 'N/A')}') has no raw formats from yt_dlp.")

                    # 최고 품질 오디오 포맷 찾기 (MP3 변환용)
                    best_audio = None
                    best_audio_bitrate = 0
                    
                    for f_index, f in enumerate(raw_formats):
                        format_id = f.get('format_id')
                        ext = f.get('ext')

                        if not format_id or not ext or 'storyboard' in format_id.lower():
                            continue

                        # filesize가 없더라도 0으로 처리하여 포함. N/A 표시는 display_text에서.
                        filesize = f.get('filesize') or f.get('filesize_approx') or 0

                        type_label = 'Unknown'
                        quality_desc = []

                        vcodec = f.get('vcodec', 'none')
                        acodec = f.get('acodec', 'none')

                        # 최고 품질 오디오 포맷 추적
                        if acodec != 'none' and f.get('abr', 0) > best_audio_bitrate:
                            best_audio = f
                            best_audio_bitrate = f.get('abr', 0)

                        # 타입 결정 로직 개선
                        if vcodec != 'none' and acodec != 'none':
                            type_label = 'Video' # Muxed (Video+Audio)
                            if f.get('width') and f.get('height'): quality_desc.append(f"{f.get('width')}x{f.get('height')}")
                            if f.get('fps'): quality_desc.append(f"{f.get('fps')}fps")
                            # 비디오 비트레이트나 오디오 비트레이트 중 하나라도 표시
                            if f.get('vbr'): quality_desc.append(f"V:{round(f.get('vbr'))}k")
                            elif f.get('abr'): quality_desc.append(f"A:{round(f.get('abr'))}k")
                        elif vcodec != 'none':
                            type_label = 'Video-only'
                            if f.get('width') and f.get('height'): quality_desc.append(f"{f.get('width')}x{f.get('height')}")
                            if f.get('fps'): quality_desc.append(f"{f.get('fps')}fps")
                            if f.get('vbr'): quality_desc.append(f"V:{round(f.get('vbr'))}k")
                        elif acodec != 'none':
                            type_label = 'Audio-only'
                            if f.get('abr'): quality_desc.append(f"A:{round(f.get('abr'))}k")
                        # Unknown 타입은 필터링하지 않고, 정보가 부족하면 그대로 표시
                        
                        quality_str = ' / '.join(filter(None, quality_desc))
                        filesize_mb_str = f"{(filesize // 1024 // 1024)}MB" if filesize > 0 else "N/A"

                        display_text = f"[{type_label}] {ext.upper()} {format_id} ({quality_str if quality_str else 'data'}) - {filesize_mb_str}"
                        
                        processed_format_list.append((display_text, format_id, type_label, filesize))
                    
                    # MP3 변환 옵션 추가
                    if best_audio:
                        # 추정 파일 크기 계산
                        estimated_size = best_audio.get('filesize', 0)
                        if estimated_size > 0:
                            estimated_size_mb = f"{estimated_size // 1024 // 1024}MB"
                        else:
                            # 파일 크기를 모르는 경우 비트레이트로 추정
                            duration = video.get('duration', 0)
                            if duration and best_audio_bitrate:
                                estimated_size = int(duration * best_audio_bitrate * 1000 / 8)  # bytes
                                estimated_size_mb = f"~{estimated_size // 1024 // 1024}MB"
                            else:
                                estimated_size_mb = "N/A"
                        
                        # MP3 옵션 추가
                        mp3_quality = f"A:{round(min(320, best_audio_bitrate))}k"  # 최대 320kbps
                        mp3_display_text = f"[Audio-only] MP3 bestaudio (MP3 Conversion / {mp3_quality}) - {estimated_size_mb}"
                        processed_format_list.append((mp3_display_text, "bestaudio/best", "Audio-only", estimated_size))
                    
                    if not processed_format_list and raw_formats:
                        print(f"[Debug Searcher] Video {video_index + 1} ('{video.get('title', 'N/A')}') - all formats were filtered out. This shouldn't happen with relaxed filters.")
                    
                    processed_format_list.sort(key=lambda x: (x[2] != 'Audio-only', x[2] != 'Video', x[2] != 'Video-only', -x[3]))

                    self.updated_list.emit(
                        video.get('title', 'No title'),
                        video.get('thumbnail', ''),
                        video.get('webpage_url', ''),
                        processed_format_list
                    )
            except Exception as e:
                print(f"[Error Searcher] An unexpected error occurred in Searcher thread: {str(e)}")
                import traceback
                traceback.print_exc()
                self.updated_list.emit(f"Error: {str(e)}", "", self.url, []) # 에러 발생 시 빈 리스트와 함께 에러 메시지 전달

    def estimate_total_count(self, result):
        if 'entries' in result:
            # If it's a playlist, estimate the total count based on the number of entries
            return len(result['entries'])
        else:
            # If it's a single video, return 1 as the total count
            return 1


class Downloader(QThread):
    updated_status = pyqtSignal(str)
    download_failed = pyqtSignal(str)
    updated_progress = pyqtSignal(float)  # Signal to update progress bar

    def __init__(self, videos, download_directory):
        super().__init__()
        self.videos = videos
        self.download_directory = download_directory

    def run(self):
        for title, url, format_id in self.videos:
            safe_title = title.replace("/", "_").replace("\\", "_")
            
            # MP3 변환이 필요한지 확인
            is_mp3_conversion = format_id == "bestaudio/best" or "MP3" in title
            
            download_options = {
                'format': format_id,
                'outtmpl': os.path.join(self.download_directory, f"{safe_title}.%(ext)s"),
                'progress_hooks': [self.progress_hook],
                'nocheckcertificate': True,
                'prefer_insecure': True,
                'geo_bypass': True,
                'geo_verification_proxy': None,
                'socket_timeout': 30,
                'retries': 10,
                'fragment_retries': 10,
                'file_access_retries': 10,
                'extractor_retries': 10,
                'ignoreerrors': True,
                'no_color': True,
                'logtostderr': True,
                'verbose': True,
                'ffmpeg_location': 'ffmpeg',
            }
            
            # MP3 변환 또는 일반 비디오 변환 설정
            if is_mp3_conversion:
                download_options['postprocessors'] = [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '320',  # 최대 320kbps
                }]
            else:
                download_options['postprocessors'] = [{
                    'key': 'FFmpegVideoConvertor',
                    'preferedformat': 'mp4',
                }]
                download_options['merge_output_format'] = 'mp4'
                download_options['postprocessor_args'] = [
                    '-c:v', 'copy',
                    '-c:a', 'copy'
                ]

            with yt_dlp.YoutubeDL(download_options) as ydl:
                try:
                    self.updated_status.emit(f"다운로드 시작: {title}")
                    ydl.download([url])
                    self.updated_status.emit(f"다운로드 완료: {title}")
                except Exception as e:
                    error_msg = f"다운로드 실패 ({title}): {str(e)}"
                    print(error_msg)  # 콘솔에 에러 출력
                    self.download_failed.emit(error_msg)

    def progress_hook(self, d):
        if d['status'] == 'downloading':
            # Trim the title to 14 characters and append "..." if it exceeds this limit
            title = os.path.splitext(os.path.basename(d['filename']))[0]
            if len(title) > 14:
                title = title[:14] + "..."
            # Extract the percentage and convert to a float
            percent_complete = float(d['_percent_str'].replace('%', ''))
            # Emit signal to update the progress bar (make sure this signal is connected to the actual progress bar update method)
            self.updated_progress.emit(percent_complete)
            # Emit status update with trimmed title and current download percentage
            self.updated_status.emit(f"Downloading {title}: {d['_percent_str']} {d['_eta_str']}")
        elif d['status'] == 'finished':
            # Repeat the trimming process for consistency in status updates
            title = os.path.splitext(os.path.basename(d['filename']))[0]
            if len(title) > 14:
                title = title[:14] + "..."
            self.updated_status.emit(f"Finished downloading {title}")
        elif d['status'] == 'error':
            # And again for error messages
            title = os.path.splitext(os.path.basename(d['filename']))[0]
            if len(title) > 14:
                title = title[:14] + "..."
            self.download_failed.emit(f"Error downloading {title}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("fusion")  # Fusion 스타일을 설정합니다.
    app.setWindowIcon(QIcon('st2.icns')) # 아이콘 설정 복원 (macOS 특정)

    # Enable hardware acceleration
    QWebEngineSettings.globalSettings().setAttribute(QWebEngineSettings.WebGLEnabled, True)
    QWebEngineSettings.globalSettings().setAttribute(QWebEngineSettings.Accelerated2dCanvasEnabled,
                                                     True)  # Corrected attribute name

    mainWindow = VideoDownloader()
    mainWindow.show()
    view = QWebEngineView()
    sys.exit(app.exec_())

# pyinstaller --windowed --icon=st2.icns --additional-hooks-dir=hooks Nobody3.py