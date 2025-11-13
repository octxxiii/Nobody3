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


class LayoutBuilder:
    """Constructs UI layouts for VideoDownloader."""

    def __init__(self, host):
        self.host = host
        self.table_manager = None

    def build_left_panel(self):
        host = self.host
        host.browser = QWebEngineView()
        host.browser.setUrl(QUrl("https://www.youtube.com"))
        host.homePageUrl = QUrl("https://www.youtube.com")
        host.musicPageUrl = QUrl("https://music.youtube.com")
        host.SCPageUrl = QUrl("https://soundcloud.com/")

        host.toggleDownButton = QPushButton("💥", host)
        host.toggleDownButton.clicked.connect(host.toggleBrowser)
        host.toggleDownButton.setFixedSize(30, 30)

        host.backButton = QPushButton("👈")
        host.backButton.clicked.connect(host.browser.back)

        host.refreshButton = QPushButton("🔄")
        host.refreshButton.setFixedSize(30, 30)
        host.refreshButton.clicked.connect(host.browser.reload)

        host.homeButton = QPushButton()
        host.homeButton.setFixedSize(30, 30)
        host.homeButton.setIcon(QIcon(":/homeIcon"))
        host.homeButton.clicked.connect(lambda: host.browser.setUrl(host.homePageUrl))

        host.musicButton = QPushButton()
        host.musicButton.setFixedSize(30, 30)
        host.musicButton.setIcon(QIcon(":/musicIcon"))
        host.musicButton.clicked.connect(lambda: host.browser.setUrl(host.musicPageUrl))

        host.SCButton = QPushButton()
        host.SCButton.setFixedSize(30, 30)
        host.SCButton.setIcon(QIcon(":/soundCloudIcon"))
        host.SCButton.clicked.connect(lambda: host.browser.setUrl(host.SCPageUrl))

        host.forwardButton = QPushButton("👉")
        host.forwardButton.clicked.connect(host.browser.forward)

        host.miniPlayerButton = QPushButton("🎵")
        host.miniPlayerButton.setFixedSize(30, 30)
        host.miniPlayerButton.setToolTip("미니 플레이어 모드")
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

        host.browWidget = QWidget()
        host.leftLayout = QVBoxLayout(host.browWidget)
        host.leftLayout.addLayout(host.navLayout)
        host.leftLayout.addWidget(host.browser)
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

        host.formatSettingsButton = QPushButton("⚙️")
        host.formatSettingsButton.setFixedSize(30, 30)
        host.formatSettingsButton.clicked.connect(host.openFormatSettingsDialog)
        host.formatSettingsButton.setToolTip("포맷 설정")

        host.copyUrlButton = QPushButton("📋")
        host.copyUrlButton.setFixedSize(30, 30)

        host.search_url = QLineEdit()
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
        host.copyUrlButton.clicked.connect(host.copyUrlToClipboard)

        host.download_list = QPushButton("📍")
        host.download_list.setFixedSize(100, 30)
        host.later_list = QPushButton("📌")
        host.later_list.setFixedSize(100, 30)

        host.video_table = QTableWidget()
        self.table_manager = VideoTableManager(host, host.video_table)
        self.table_manager.initialize()

        host.download_button = QPushButton("📥")
        host.download_button.clicked.connect(host.on_download)

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
                padding: 4px 4px 4px 4px;
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

        actionLayout = QHBoxLayout()
        actionLayout.addWidget(host.download_button)
        actionLayout.addWidget(host.delete_button)

        host.rightLayout.addLayout(titleLayout)
        host.rightLayout.addLayout(playerLayout)
        host.rightLayout.addLayout(searchLayout)
        host.rightLayout.addWidget(host.video_table)
        host.rightLayout.addLayout(statusLayout)
        host.rightLayout.addLayout(actionLayout)

        host.setStyleSheet(DARK_THEME_STYLESHEET)
        return host.downLayoutWidget

    def build_splitter(self, left_widget, right_widget):
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)
        return splitter

