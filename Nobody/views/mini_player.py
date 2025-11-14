"""Mini player controller."""

from PyQt5.QtCore import Qt, QTimer, QObject
from PyQt5.QtWidgets import (
    QApplication,
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSlider,
)

from ..utils.logging import logger


class MiniPlayerController(QObject):
    """Encapsulates mini player UI and behavior for VideoDownloader."""

    def __init__(self, host):
        super().__init__(host)
        self.host = host
        self.dialog = None
        self.title_label = None
        self.play_button = None
        self.toggle_button = None
        self.always_on_top_button = None
        self.restore_button = None
        self.volume_slider = None
        self.is_mini_mode = False
        self.always_on_top = True
        self.current_volume = 0.5
        self._normal_geometry = None
        self._original_title = ""
        self._scroll_pos = 0
        self._scroll_timer = QTimer(self)
        self._scroll_timer.timeout.connect(self._scroll_step)

    def bind_toggle_button(self, button):
        """Bind mini player toggle button."""
        self.toggle_button = button
        if self.toggle_button is not None:
            self.toggle_button.clicked.connect(self.switch_to_mini_mode)
            self.toggle_button.setToolTip("Switch to mini player")

    def create(self):
        """Create mini player dialog with controls."""
        if self.dialog is not None:
            return

        self.dialog = QDialog(self.host)
        self.dialog.setWindowTitle("Nobody 3 - Mini Player")
        self.dialog.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint | Qt.WindowCloseButtonHint)
        self.dialog.setFixedSize(300, 100)

        layout = QVBoxLayout(self.dialog)
        layout.setContentsMargins(1, 1, 1, 1)
        layout.setSpacing(2)

        self.title_label = QLabel()
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet(
            """
            QLabel {
                color: white;
                border: 1px solid #555;
                border-radius: 3px;
                background-color: #333;
                padding: 1px;
                font-size: 12px;
                font-weight: bold;
            }
            """
        )
        self.title_label.setWordWrap(False)

        control_layout = QHBoxLayout()
        control_layout.setSpacing(2)
        control_layout.setContentsMargins(0, 0, 0, 0)

        back_button = QPushButton("⏮️")
        back_button.setFixedSize(35, 35)
        back_button.clicked.connect(self.host.play_back)

        self.play_button = QPushButton("⏯️")
        self.play_button.setFixedSize(40, 35)
        self.play_button.clicked.connect(self.host.play)

        next_button = QPushButton("⏭️")
        next_button.setFixedSize(35, 35)
        next_button.clicked.connect(self.host.play_next)

        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(int(self.current_volume * 100))
        self.volume_slider.setFixedHeight(20)
        self.volume_slider.setToolTip("Volume")
        self.volume_slider.valueChanged.connect(self.on_volume_changed)

        self.always_on_top_button = QPushButton("📌")
        self.always_on_top_button.setFixedSize(35, 35)
        self.always_on_top_button.clicked.connect(self.toggle_always_on_top)
        self.always_on_top_button.setToolTip("최상위 고정")

        self.restore_button = QPushButton("🔼")
        self.restore_button.setFixedSize(35, 35)
        self.restore_button.clicked.connect(self.restore_from_mini)
        self.restore_button.setToolTip("원래 크기로 복원")

        control_layout.addWidget(back_button)
        control_layout.addWidget(self.play_button)
        control_layout.addWidget(next_button)
        control_layout.addWidget(self.volume_slider, 1)
        control_layout.addWidget(self.always_on_top_button)
        control_layout.addWidget(self.restore_button)

        layout.addWidget(self.title_label)
        layout.addLayout(control_layout)

        self.dialog.setStyleSheet(
            """
            QDialog {
                background-color: #2D2D2D;
                border: 1px solid #555555;
                border-radius: 8px;
            }
            QPushButton {
                background-color: #444444;
                color: #FFFFFF;
                border: 2px solid #666666;
                border-radius: 5px;
                padding: 3px;
                font-size: 14px;
                font-weight: bold;
                min-width: 35px;
                min-height: 35px;
            }
            QPushButton:hover { 
                background-color: #666666; 
                border: 2px solid #888888;
            }
            QPushButton:pressed { 
                background-color: #555555; 
                border: 2px solid #777777;
            }
            QSlider::groove:horizontal {
                border: 1px solid #555555;
                height: 6px;
                background: #333333;
                border-radius: 3px;
            }
            QSlider::handle:horizontal {
                background: #666666;
                border: 1px solid #555555;
                width: 12px;
                margin: -3px 0;
                border-radius: 6px;
            }
            QSlider::handle:horizontal:hover {
                background: #777777;
            }
            """
        )

        self.dialog.closeEvent = self._handle_close_event

    def switch_to_mini_mode(self):
        """Switch from main window to mini player."""
        if self.dialog is None:
            self.create()
        if self.dialog is None or self.is_mini_mode:
            return

        self.is_mini_mode = True
        self._normal_geometry = self.host.geometry()

        if self.toggle_button:
            self.toggle_button.setEnabled(False)
            self.toggle_button.setToolTip("Mini player active")

        self.host.hide()
        self.update_title_from_host()
        self._position_dialog()
        self.dialog.show()
        self.dialog.raise_()
        self.dialog.activateWindow()

    def restore_from_mini(self):
        """Restore main window from mini player."""
        if not self.is_mini_mode:
            return

        self.is_mini_mode = False

        if self.toggle_button:
            self.toggle_button.setEnabled(True)
            self.toggle_button.setToolTip("Switch to mini player")

        if self.dialog:
            self.dialog.hide()

        self.host.show()
        if self._normal_geometry is not None:
            self.host.setGeometry(self._normal_geometry)
        self.host.setWindowState(Qt.WindowNoState)
        self.host.raise_()
        self.host.activateWindow()

    def toggle_always_on_top(self):
        """Toggle always-on-top flag."""
        if not self.dialog:
            return

        self.always_on_top = not self.always_on_top
        current_pos = self.dialog.pos()

        if self.always_on_top:
            self.dialog.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint | Qt.WindowCloseButtonHint)
            if self.always_on_top_button:
                self.always_on_top_button.setText("📌")
                self.always_on_top_button.setToolTip("최상위 고정 해제")
        else:
            self.dialog.setWindowFlags(Qt.Window | Qt.WindowCloseButtonHint)
            if self.always_on_top_button:
                self.always_on_top_button.setText("📍")
                self.always_on_top_button.setToolTip("최상위 고정")

        self.dialog.move(current_pos)
        self.dialog.show()
        self.dialog.raise_()
        self.dialog.activateWindow()

    def update_title(self, title):
        """Update mini player title and scrolling text."""
        self._original_title = title or ""
        self._scroll_pos = 0
        self._update_title_immediate()

    def update_title_from_host(self):
        """Sync title from host title label."""
        if hasattr(self.host, "title_label") and self.host.title_label:
            self.update_title(self.host.title_label.text())

    def update_play_button_icon(self, state):
        """Sync mini play button icon."""
        if not self.play_button:
            return
        if state == "playing":
            self.play_button.setText("⏸️")
        elif state == "paused":
            self.play_button.setText("▶️")

    def on_volume_changed(self, value):
        """Handle volume slider change."""
        self.current_volume = max(0.0, min(1.0, value / 100.0))
        if not hasattr(self.host, "browser") or not self.host.browser:
            return
        js = f"""
        (function() {{
            var v = document.querySelector('video');
            if (v) {{
                v.volume = {self.current_volume};
                return true;
            }}
            return false;
        }})();
        """
        try:
            self.host.browser.page().runJavaScript(js)
        except Exception as exc:  # pragma: no cover - defensive
            logger.warning("mini_on_volume_changed js error: %s", exc)

    def dispose(self):
        """Cleanup mini player resources."""
        self._scroll_timer.stop()
        if self.dialog:
            self.dialog.hide()
            self.dialog.deleteLater()
            self.dialog = None

    # Internal helpers -------------------------------------------------

    def _update_title_immediate(self):
        if not self.title_label:
            return
        max_visible = 24
        self._scroll_pos = 0
        if len(self._original_title) > max_visible:
            self.title_label.setText(self._original_title[:max_visible])
            self._scroll_timer.start(300)
        else:
            self.title_label.setText(self._original_title)
            self._scroll_timer.stop()

    def _scroll_step(self):
        if not self.title_label:
            return
        title = self._original_title
        if not title:
            return
        max_visible = 24
        if len(title) <= max_visible:
            self._scroll_timer.stop()
            return

        pos = self._scroll_pos
        if pos >= len(title):
            pos = 0

        display_text = title[pos : pos + max_visible]
        if pos + max_visible > len(title):
            remaining = max_visible - (len(title) - pos)
            display_text = title[pos:] + "   " + title[:remaining]

        self.title_label.setText(display_text)
        self._scroll_pos = pos + 1

    def _position_dialog(self):
        if not self.dialog:
            return
        screen = QApplication.desktop().screenGeometry()
        self.dialog.move(screen.width() - 320, screen.height() - 200)

    def _handle_close_event(self, event):  # pragma: no cover - Qt override
        self._scroll_timer.stop()
        self.host.close()
        event.accept()

