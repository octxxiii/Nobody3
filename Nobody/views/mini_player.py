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
        self.time_label = None
        self.position_slider = None
        self.is_mini_mode = False
        self.always_on_top = True
        self.current_volume = 1.0  # Default to 100%
        self._normal_geometry = None
        self._original_title = ""
        self._scroll_pos = 0
        self._scroll_timer = QTimer(self)
        self._scroll_timer.timeout.connect(self._scroll_step)
        self._time_update_timer = QTimer(self)
        self._time_update_timer.timeout.connect(self._update_time)

    def bind_toggle_button(self, button):
        """Bind mini player toggle button."""
        self.toggle_button = button
        if self.toggle_button is not None:
            self.toggle_button.clicked.connect(self.switch_to_mini_mode)
            self.toggle_button.setToolTip("미니 플레이어 모드 / Mini Player Mode")

    def create(self):
        """Create mini player dialog with controls."""
        if self.dialog is not None:
            return

        self.dialog = QDialog(self.host)
        self.dialog.setWindowTitle("Nobody 3 - Mini Player")
        self.dialog.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint | Qt.WindowCloseButtonHint)
        # Slightly wider to accommodate vertical volume slider
        self.dialog.setFixedSize(320, 100)

        # Main layout: horizontal split between content and volume
        main_layout = QHBoxLayout(self.dialog)
        main_layout.setContentsMargins(1, 1, 1, 1)
        main_layout.setSpacing(2)

        # Left side: content area
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(2)

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
        back_button.setFixedSize(28, 28)
        back_button.clicked.connect(self.host.play_back)

        self.play_button = QPushButton("⏯️")
        self.play_button.setFixedSize(32, 28)
        self.play_button.clicked.connect(self.host.play)

        next_button = QPushButton("⏭️")
        next_button.setFixedSize(28, 28)
        next_button.clicked.connect(self.host.play_next)

        # Time label replaces volume slider position
        self.time_label = QLabel("00:00 / 00:00")
        self.time_label.setAlignment(Qt.AlignCenter)
        self.time_label.setStyleSheet(
            """
            QLabel {
                color: #CCCCCC;
                background-color: #2D2D2D;
                border: 1px solid #555;
                border-radius: 3px;
                padding: 2px;
                font-size: 11px;
                font-family: monospace;
            }
            """
        )
        self.time_label.setFixedHeight(20)

        self.always_on_top_button = QPushButton("📌")
        self.always_on_top_button.setFixedSize(28, 28)
        self.always_on_top_button.clicked.connect(self.toggle_always_on_top)
        self.always_on_top_button.setToolTip("최상위 고정")

        self.restore_button = QPushButton("🔼")
        self.restore_button.setFixedSize(28, 28)
        self.restore_button.clicked.connect(self.restore_from_mini)
        self.restore_button.setToolTip("원래 크기로 복원")

        control_layout.addWidget(back_button)
        control_layout.addWidget(self.play_button)
        control_layout.addWidget(next_button)
        control_layout.addWidget(self.time_label, 1)
        control_layout.addWidget(self.always_on_top_button)
        control_layout.addWidget(self.restore_button)

        # Position slider (progress bar) for seeking
        self.position_slider = QSlider(Qt.Horizontal)
        self.position_slider.setRange(0, 100)
        self.position_slider.setValue(0)
        self.position_slider.setFixedHeight(20)
        self.position_slider.setToolTip("재생 위치 조절 / Seek position")
        self.position_slider.sliderReleased.connect(self._seek_video)
        # Prevent seeking while dragging to avoid conflicts
        self._is_seeking = False

        content_layout.addWidget(self.title_label)
        content_layout.addWidget(self.position_slider)
        content_layout.addLayout(control_layout)

        # Right side: vertical volume slider
        self.volume_slider = QSlider(Qt.Vertical)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(int(self.current_volume * 100))
        self.volume_slider.setFixedWidth(20)
        self._update_volume_tooltip(int(self.current_volume * 100))
        self.volume_slider.valueChanged.connect(self.on_volume_changed)

        main_layout.addLayout(content_layout, 1)
        main_layout.addWidget(self.volume_slider)

        self.dialog.setStyleSheet(
            """
            QDialog {
                background-color: #2D2D2D;
                border: 1px solid #555555;
                border-radius: 8px;
            }
            QPushButton {
                background-color: #333333;
                color: #FFFFFF;
                border: 1px solid #555555;
                border-radius: 4px;
                padding: 1px;
                font-size: 12px;
            }
            QPushButton:hover { background-color: #555555; }
            QPushButton:pressed { background-color: #444444; }
            QSlider::groove:vertical {
                border: 1px solid #555555;
                width: 6px;
                background: #333333;
                border-radius: 3px;
            }
            QSlider::handle:vertical {
                background: #666666;
                border: 1px solid #555555;
                height: 12px;
                margin: 0 -3px;
                border-radius: 6px;
            }
            QSlider::handle:vertical:hover {
                background: #777777;
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
        # Override keyPressEvent to handle ESC key
        self.dialog.keyPressEvent = self._handle_key_press

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
            self.toggle_button.setToolTip("미니 플레이어 활성화됨 / Mini Player Active")

        self.host.hide()
        self.update_title_from_host()
        self._position_dialog()
        self.dialog.show()
        self.dialog.raise_()
        self.dialog.activateWindow()
        # Start time update timer
        self._time_update_timer.start(500)  # Update every 500ms

    def restore_from_mini(self):
        """Restore main window from mini player."""
        if not self.is_mini_mode:
            return

        self.is_mini_mode = False

        if self.toggle_button:
            self.toggle_button.setEnabled(True)
            self.toggle_button.setToolTip("미니 플레이어 모드 / Mini Player Mode")

        if self.dialog:
            self.dialog.hide()

        # Stop time update timer
        self._time_update_timer.stop()

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
        self._update_volume_tooltip(value)
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

    def _update_volume_tooltip(self, value: int) -> None:
        """Update volume slider tooltip with current value.
        
        Args:
            value: Volume value (0-100)
        """
        if self.volume_slider:
            self.volume_slider.setToolTip(f"Volume: {value}%")

    def dispose(self):
        """Cleanup mini player resources."""
        self._scroll_timer.stop()
        self._time_update_timer.stop()
        if self.dialog:
            self.dialog.hide()
            self.dialog.deleteLater()
            self.dialog = None

    def update_time(self, current_time: float, duration: float) -> None:
        """Update time label and position slider with current playback time.
        
        Args:
            current_time: Current playback time in seconds
            duration: Total duration in seconds
        """
        if not self.time_label:
            return
        time_str = f"{self._format_time(current_time)} / {self._format_time(duration)}"
        self.time_label.setText(time_str)
        
        # Update position slider (only if not currently being dragged by user)
        if self.position_slider and not self._is_seeking and duration > 0:
            position = int((current_time / duration) * 100)
            self.position_slider.setValue(position)

    def _format_time(self, seconds: float) -> str:
        """Format seconds into MM:SS or HH:MM:SS format.
        
        Args:
            seconds: Time in seconds
            
        Returns:
            Formatted time string
        """
        if not seconds or seconds < 0:
            return "00:00"
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{secs:02d}"
        return f"{minutes:02d}:{secs:02d}"

    def _update_time(self) -> None:
        """Update time label by querying video element."""
        if not hasattr(self.host, "browser") or not self.host.browser:
            return
        js = """
        (function() {
            var video = document.querySelector('video');
            if (video) {
                return {
                    currentTime: video.currentTime || 0,
                    duration: video.duration || 0
                };
            }
            return null;
        })();
        """
        try:
            def on_result(result):
                if result and self.time_label:
                    current = result.get('currentTime', 0)
                    duration = result.get('duration', 0)
                    self.update_time(current, duration)
            self.host.browser.page().runJavaScript(js, on_result)
        except Exception as exc:
            logger.debug("mini _update_time js error: %s", exc)

    def _seek_video(self) -> None:
        """Seek video to position indicated by slider."""
        if not self.position_slider:
            return
        if not hasattr(self.host, "browser") or not self.host.browser:
            return
        
        self._is_seeking = True
        value = self.position_slider.value()
        
        js = f"""
        (function() {{
            var video = document.querySelector('video');
            if (video && video.duration) {{
                var seekTime = video.duration * ({value} / 100);
                video.currentTime = seekTime;
                return true;
            }}
            return false;
        }})();
        """
        try:
            self.host.browser.page().runJavaScript(js)
        except Exception as exc:
            logger.debug("mini _seek_video js error: %s", exc)
        finally:
            # Reset seeking flag after a short delay
            from PyQt5.QtCore import QTimer
            QTimer.singleShot(100, lambda: setattr(self, '_is_seeking', False))

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
        # Adjust position for new width (320px)
        self.dialog.move(screen.width() - 340, screen.height() - 200)

    def _handle_close_event(self, event):  # pragma: no cover - Qt override
        """Handle close event - restore to main window instead of closing."""
        self._scroll_timer.stop()
        self.restore_from_mini()
        event.ignore()  # Don't actually close, just restore
    
    def _handle_key_press(self, event):  # pragma: no cover - Qt override
        """Handle key press events in mini player dialog."""
        from PyQt5.QtCore import Qt
        if event.key() == Qt.Key_Escape:
            # ESC key: restore to main window
            self.restore_from_mini()
            event.accept()
        else:
            # Let default handling occur
            QDialog.keyPressEvent(self.dialog, event)

