"""Layout builder utilities for VideoDownloader."""

from PyQt5.QtCore import Qt, QSize, QUrl, QTimer
from PyQt5.QtWidgets import (
    QHBoxLayout,
    QVBoxLayout,
    QWidget,
    QPushButton,
    QLineEdit,
    QTableWidget,
    QLabel,
    QProgressBar,
    QSplitter,
)
from PyQt5.QtGui import QIcon
from PyQt5.QtWebEngineWidgets import QWebEngineView

from ..config.constants import DARK_THEME_STYLESHEET
from .video_table import VideoTableManager
from .browser_tab import BrowserTabWidget


class LayoutBuilder:
    """Constructs UI layouts for VideoDownloader."""

    def __init__(self, host):
        self.host = host
        self.table_manager: VideoTableManager | None = None

    def build_left_panel(self):
        host = self.host
        
        # Create parent widget first
        host.browWidget = QWidget()
        host.leftLayout = QVBoxLayout(host.browWidget)
        host.leftLayout.setContentsMargins(0, 0, 0, 0)
        host.leftLayout.setSpacing(0)
        
        # Set URL URLs before creating browser
        host.homePageUrl = QUrl("https://www.youtube.com")
        host.musicPageUrl = QUrl("https://music.youtube.com")
        host.SCPageUrl = QUrl("https://soundcloud.com/")
        
        # Create simple browser (original structure)
        from ..utils.logging import logger
        try:
            host.browser = QWebEngineView(host.browWidget)
            host.browser.setUrl(host.homePageUrl)
            logger.info("QWebEngineView created successfully.")
        except Exception as browser_error:
            logger.error(f"Failed to create QWebEngineView: {browser_error}")
            from PyQt5.QtWidgets import QLabel
            host.browser = QLabel(
                "WebEngine initialization failed. "
                "Please restart the application.",
                host.browWidget
            )
            host.browser.setStyleSheet("color: red; padding: 20px;")

        host.toggleDownButton = QPushButton("💥", host)
        host.toggleDownButton.clicked.connect(host.toggleBrowser)
        host.toggleDownButton.setFixedSize(30, 30)

        # Navigation buttons are now in browser_toolbar, but keep these for compatibility
        host.backButton = QPushButton("👈")
        host.backButton.clicked.connect(host._on_browser_back)

        host.forwardButton = QPushButton("👉")
        host.forwardButton.clicked.connect(host._on_browser_forward)

        host.refreshButton = QPushButton("🔄")
        host.refreshButton.setFixedSize(30, 30)
        host.refreshButton.clicked.connect(host._on_browser_refresh)

        host.homeButton = QPushButton()
        host.homeButton.setFixedSize(30, 30)
        host.homeButton.setIcon(QIcon(":/homeIcon"))
        host.homeButton.clicked.connect(host._on_browser_home)

        host.musicButton = QPushButton()
        host.musicButton.setFixedSize(30, 30)
        host.musicButton.setIcon(QIcon(":/musicIcon"))
        host.musicButton.clicked.connect(lambda: host.browser.setUrl(host.musicPageUrl))

        host.SCButton = QPushButton()
        host.SCButton.setFixedSize(30, 30)
        host.SCButton.setIcon(QIcon(":/soundCloudIcon"))
        host.SCButton.clicked.connect(lambda: host.browser.setUrl(host.SCPageUrl))

        host.miniPlayerButton = QPushButton("🎧")
        host.miniPlayerButton.setFixedSize(30, 30)
        host.miniPlayerButton.setToolTip("미니 플레이어 모드 (Ctrl+M) / Mini Player Mode (Ctrl+M)")
        host.miniPlayerButton.setAccessibleName("Mini player toggle button")
        host.miniPlayerButton.setAccessibleDescription("Toggle mini player mode for compact playback control")
        host.mini_player_controller.bind_toggle_button(host.miniPlayerButton)

        host.navLayout = QHBoxLayout()
        host.navLayout.addWidget(host.backButton)
        host.navLayout.addWidget(host.forwardButton)
        host.navLayout.addWidget(host.refreshButton)
        host.navLayout.addWidget(host.homeButton)
        host.navLayout.addWidget(host.musicButton)
        host.navLayout.addWidget(host.SCButton)
        host.navLayout.addWidget(host.miniPlayerButton)
        host.navLayout.addWidget(host.toggleDownButton)

        host.leftLayout.addLayout(host.navLayout)
        host.leftLayout.addWidget(host.browser, 1)
        return host.browWidget

    def build_right_panel(self):
        host = self.host
        host.downLayoutWidget = QWidget()
        host.downLayoutWidget.setContentsMargins(0, 0, 0, 0)
        host.downLayoutWidget.setFixedSize(450, 560)
        host.rightLayout = QVBoxLayout(host.downLayoutWidget)

        host.browHideButton = QPushButton("🦕")
        host.browHideButton.setFixedSize(30, 30)
        host.browHideButton.clicked.connect(host.toggleBrowWidgetVisibility)

        host.createrButton = QPushButton("💬")
        host.createrButton.setFixedSize(30, 30)
        host.createrButton.clicked.connect(host.openSettingsDialog)
        host.createrButton.setToolTip("설정/정보 (F1) / Settings/About (F1)")
        host.createrButton.setAccessibleName("Settings and about dialog button")
        host.createrButton.setAccessibleDescription("Open settings and about dialog with cache management options")

        host.formatSettingsButton = QPushButton("⚙️")
        host.formatSettingsButton.setFixedSize(30, 30)
        host.formatSettingsButton.clicked.connect(host.openFormatSettingsDialog)
        host.formatSettingsButton.setToolTip("포맷 설정 (Ctrl+,) / Format Settings (Ctrl+,)")
        host.formatSettingsButton.setAccessibleName("Format settings button")
        host.formatSettingsButton.setAccessibleDescription("Configure video and audio format display options")

        host.copyUrlButton = QPushButton("📋")
        host.copyUrlButton.setFixedSize(30, 30)

        host.search_url = QLineEdit()
        host.search_url.setPlaceholderText("Enter URL and press Enter or click Search...")
        host.search_url.setAccessibleName("URL input field")
        host.search_url.setAccessibleDescription("Enter YouTube, YouTube Music, or SoundCloud URL to search for videos")
        host.search_url.setStyleSheet(
            """
            QLineEdit {
                border: 2px solid #555555;
                border-radius: 5px;
                padding: 0px;
                background-color: #2D2D2D;
                color: #ffffff;
            }
            """
        )
        host.search_url.setFixedSize(356, 30)
        host.search_url.setClearButtonEnabled(True)

        host.search_button = QPushButton("🔍")
        host.search_button.setFixedSize(30, 30)
        host.search_button.clicked.connect(host.on_search)
        host.search_button.setToolTip("검색 (Enter) / Search (Enter)")
        host.search_button.setAccessibleName("Search button")
        host.search_button.setAccessibleDescription("Search for videos using the URL in the input field")
        host.copyUrlButton.clicked.connect(host.copyUrlToClipboard)

        host.download_list = QPushButton("📍 History")
        host.download_list.setFixedSize(100, 30)
        host.download_list.setToolTip("다운로드 히스토리 / Download History")
        host.download_list.clicked.connect(host.openHistoryDialog)
        host.later_list = QPushButton("📌")
        host.later_list.setFixedSize(100, 30)

        host.video_table = QTableWidget()
        self.table_manager = VideoTableManager(host, host.video_table)
        self.table_manager.initialize()

        host.download_button = QPushButton("📥")
        host.download_button.clicked.connect(host.on_download)
        host.download_button.setToolTip("다운로드 (Ctrl+D) / Download (Ctrl+D)")
        host.download_button.setAccessibleName("Download button")
        host.download_button.setAccessibleDescription("Download selected videos to the chosen directory")

        host.delete_button = QPushButton("❌")
        host.delete_button.clicked.connect(host.on_delete_selected)

        host.status_label = QLabel("Ready")
        host.progress_bar = QProgressBar()

        host.back_button = QPushButton("⏮️", host)
        host.back_button.clicked.connect(host.play_back)

        host.play_button = QPushButton("⏯️", host)
        host.play_button.clicked.connect(host.play)

        host.next_button = QPushButton("⏭️", host)
        host.next_button.clicked.connect(host.play_next)

        host.title_label = QLabel()
        host.title_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        host.title_label.setStyleSheet(
            """
            QLabel {
                color: white;
                border: 2px solid #555;
                border-radius: 5px;
                background-color: #333;
                padding: 4px;
            }
            """
        )
        host.title_label.setWordWrap(False)

        host.animation_timer = QTimer(host)
        host.animation_timer.timeout.connect(host.toggle_loading_animation)
        host.direction = 1

        titleLayout = QHBoxLayout()
        titleLayout.setContentsMargins(0, 0, 0, 0)
        titleLayout.setSpacing(5)
        titleLayout.addWidget(host.browHideButton)
        titleLayout.addWidget(host.title_label)
        titleLayout.addWidget(host.formatSettingsButton)
        titleLayout.addWidget(host.createrButton)

        playerLayout = QHBoxLayout()
        playerLayout.setContentsMargins(0, 0, 0, 0)
        playerLayout.setSpacing(5)
        playerLayout.addWidget(host.back_button)
        playerLayout.addWidget(host.play_button)
        playerLayout.addWidget(host.next_button)

        searchLayout = QHBoxLayout()
        searchLayout.setContentsMargins(0, 0, 0, 0)
        searchLayout.setSpacing(5)
        searchLayout.addWidget(host.copyUrlButton)
        searchLayout.addWidget(host.search_url)
        searchLayout.addWidget(host.search_button)

        statusLayout = QHBoxLayout()
        statusLayout.addWidget(host.progress_bar)
        statusLayout.addWidget(host.status_label)

        buttonLayout = QHBoxLayout()
        buttonLayout.setSpacing(10)
        buttonLayout.addWidget(host.download_button)
        buttonLayout.addWidget(host.delete_button)

        # 레이아웃 순서: titleLayout -> playerLayout -> searchLayout -> video_table -> statusLayout -> actionLayout
        host.rightLayout.addLayout(titleLayout)
        host.rightLayout.addLayout(playerLayout)
        host.rightLayout.addLayout(searchLayout)
        host.rightLayout.addWidget(host.video_table)
        host.rightLayout.addLayout(statusLayout)
        host.rightLayout.addLayout(buttonLayout)

        return host.downLayoutWidget

    def build_splitter(self, left_widget, right_widget):
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)
        return splitter

