"""Main window for the Nobody 3 application."""

import os
import sys
from PyQt5.QtGui import QIcon, QDesktopServices
from PyQt5.QtMultimedia import QMediaPlayer
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings, QWebEngineProfile
from PyQt5.QtWidgets import (
    QApplication,
    QDialog,
    QPushButton,
    QVBoxLayout,
    QLineEdit,
    QLabel,
    QProgressBar,
    QTableWidget,
    QFileDialog,
    QHBoxLayout,
    QSplitter,
    QWidget,
    QMessageBox,
    QSlider,
)
from PyQt5.QtCore import pyqtSignal, Qt, pyqtSlot, QTimer, QUrl, QSize

# import optional resource module when available
try:
    import resources_rc
except ImportError:
    pass

from ..config.constants import DARK_THEME_STYLESHEET
from ..models.settings import AppSettings
from ..services.ffmpeg_checker import FFmpegChecker
from ..utils.cache import resolve_writable_cache_dir
from ..utils.logging import logger
from .layout_builder import LayoutBuilder
from .mini_player import MiniPlayerController
from .presenter import VideoPresenter
from .settings_dialog import SettingsDialog
from .format_settings_dialog import FormatSettingsDialog
from .history_dialog import HistoryDialog

class VideoDownloader(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowFlags(
            self.windowFlags()
            | Qt.WindowMinimizeButtonHint
            | Qt.WindowMaximizeButtonHint
            | Qt.WindowCloseButtonHint
        )
        self.settingsDialog = None
        self.formatSettingsDialog = None
        self.historyDialog = None
        self.Nobody = resolve_writable_cache_dir("Nobody")  # Define here
        
        # Load persisted application settings
        self.app_settings = AppSettings()
        self.app_settings.load_settings()

        # Initialize mini player controller
        self.mini_player_controller = MiniPlayerController(self)
        # Initialize download queue and notification manager
        from ..models.queue import DownloadQueue
        from ..utils.notifications import NotificationManager
        self.download_queue = DownloadQueue()
        self.notification_manager = NotificationManager(self)
        # Use a user-writable cache directory to avoid permission issues under Program Files
        self.cacheDirectory = resolve_writable_cache_dir("Nobody 3")
        if not os.path.exists(self.cacheDirectory):
            try:
                os.makedirs(self.cacheDirectory, exist_ok=True)
            except Exception as e:
                logger.error(f"Failed to create cache directory {self.cacheDirectory}: {e}")

        # Validate WebEngine profile on startup (conservative approach)
        # This only removes files with clearly corrupted timestamps while
        # preserving cookies, sessions, and login data
        # Profile validation is now very conservative to prevent login loss
        from ..utils.cache import validate_and_clean_profile
        try:
            logger.info("Checking WebEngine profile integrity (preserving login data)...")
            cleaned = validate_and_clean_profile(self.cacheDirectory, logger, force_clear=False)
            if cleaned:
                logger.info("WebEngine profile checked - some corrupted files removed, login data preserved.")
            else:
                logger.info("WebEngine profile is valid, no cleaning needed.")
        except Exception as e:
            logger.error(f"Failed to validate WebEngine profile: {e}")
            # Do NOT clear profile on validation failure - preserve login state
            # Only log the error and continue
            logger.warning("Profile validation error occurred, but preserving profile to maintain login state.")

        # Configure persistent browser profile paths
        # Do this AFTER profile cleanup to ensure clean state
        try:
            profile = QWebEngineProfile.defaultProfile()
            profile.setPersistentStoragePath(self.cacheDirectory)
            profile.setHttpCacheType(QWebEngineProfile.NoCache)
            profile.setPersistentCookiesPolicy(QWebEngineProfile.ForcePersistentCookies)

            settings = profile.settings()
            settings.setAttribute(QWebEngineSettings.LocalStorageEnabled, True)
            settings.setAttribute(QWebEngineSettings.JavascriptEnabled, True)
            settings.setAttribute(QWebEngineSettings.PluginsEnabled, True)
            settings.setAttribute(QWebEngineSettings.WebGLEnabled, True)
        except Exception as profile_error:
            logger.error(f"Failed to configure WebEngine profile: {profile_error}")
            # Try to validate/clean and retry, but preserve login data
            try:
                from ..utils.cache import validate_and_clean_profile
                # Try selective cleaning (preserves cookies/sessions)
                if validate_and_clean_profile(self.cacheDirectory, logger, force_clear=False):
                    logger.info("Profile cleaned (login data preserved), retrying configuration...")
                
                # Retry profile configuration
                profile = QWebEngineProfile.defaultProfile()
                profile.setPersistentStoragePath(self.cacheDirectory)
                profile.setHttpCacheType(QWebEngineProfile.NoCache)
                profile.setPersistentCookiesPolicy(QWebEngineProfile.ForcePersistentCookies)
                settings = profile.settings()
                settings.setAttribute(QWebEngineSettings.LocalStorageEnabled, True)
                settings.setAttribute(QWebEngineSettings.JavascriptEnabled, True)
                settings.setAttribute(QWebEngineSettings.PluginsEnabled, True)
                settings.setAttribute(QWebEngineSettings.WebGLEnabled, True)
                logger.info("WebEngine profile reconfigured (login data preserved).")
            except Exception as retry_error:
                logger.error(f"Failed to reconfigure WebEngine profile: {retry_error}")
                logger.warning("Continuing with default profile settings to preserve login state.")

        self.setWindowTitle("Nobody 3")
        self.player = QMediaPlayer(self)
        self.video_info_list = []

        self.videoDuration = 0
        self.currentTime = 0
        self.originalTitle = ""  # Initialize the title attribute
        self.isPlaying = False  # Initialize the attribute to False

        self.initUI()
        self.presenter = VideoPresenter(self, self.table_manager)

        self.scrollTimer = QTimer(self)
        self.scrollTimer.timeout.connect(self.scrollTitle)
        self.scrollTimer.start(300)  # Scroll title every 300 ms

        self.predefinedURL = "https://soundcloud.com/octxxiii"
        
        # Kick off background FFmpeg availability check
        self.ffmpeg_checker = FFmpegChecker(self)
        self.ffmpeg_checker.check_complete.connect(self.on_ffmpeg_check_complete)
        self.ffmpeg_checker.start()

    def changeEvent(self, event):
        """Handle generic window state changes."""
        super().changeEvent(event)
    def keyPressEvent(self, event):
        """Handle keyboard shortcuts and accessibility.
        
        Keyboard shortcuts:
        - Enter/Return: Search (when URL input is focused)
        - Escape: Lower window
        - Ctrl+S: Take screenshot
        - Ctrl+F: Focus search URL input
        - Ctrl+D: Start download
        - Ctrl+M: Toggle mini player
        - Ctrl+,: Open format settings
        - F1: Open settings/about dialog
        """
        modifiers = event.modifiers()
        key = event.key()
        
        # Enter/Return: Search
        if key in (Qt.Key_Enter, Qt.Key_Return):
            if hasattr(self, "search_url"):
                focused_widget = QApplication.focusWidget()
                if focused_widget == self.search_url and self.search_url.text().strip():
                    self.on_search()
            else:
                self.on_search()
        # Escape: Restore from mini player or lower window
        elif key == Qt.Key_Escape:
            # If in mini player mode, restore to main window
            if (hasattr(self, "mini_player_controller") and
                    self.mini_player_controller and
                    self.mini_player_controller.is_mini_mode):
                self.mini_player_controller.restore_from_mini()
                event.accept()
            else:
                # Otherwise, just lower the window
                self.lower()
        # Ctrl+S: Screenshot
        elif modifiers == Qt.ControlModifier and key == Qt.Key_S:
            self.take_screenshot()
        # Ctrl+F: Focus search URL
        elif modifiers == Qt.ControlModifier and key == Qt.Key_F:
            if hasattr(self, "search_url"):
                self.search_url.setFocus()
                self.search_url.selectAll()
            event.accept()
        # Ctrl+D: Download
        elif modifiers == Qt.ControlModifier and key == Qt.Key_D:
            if hasattr(self, "download_button") and self.download_button.isEnabled():
                self.on_download()
            event.accept()
        # Ctrl+M: Toggle mini player
        elif modifiers == Qt.ControlModifier and key == Qt.Key_M:
            if hasattr(self, "miniPlayerButton"):
                self.miniPlayerButton.click()
            event.accept()
        # Ctrl+,: Format settings
        elif modifiers == Qt.ControlModifier and key == Qt.Key_Comma:
            if hasattr(self, "formatSettingsButton"):
                self.formatSettingsButton.click()
            event.accept()
        # F1: Settings/About
        elif key == Qt.Key_F1:
            if hasattr(self, "createrButton"):
                self.createrButton.click()
            event.accept()
        # Ctrl+R: Browser refresh
        elif modifiers == Qt.ControlModifier and key == Qt.Key_R:
            if hasattr(self, "browser") and self.browser:
                self.browser.reload()
            event.accept()
        # Ctrl+W: Close window (or current tab in future)
        elif modifiers == Qt.ControlModifier and key == Qt.Key_W:
            # For now, just close the window
            self.close()
            event.accept()
        # Space: Play/Pause
        elif key == Qt.Key_Space and modifiers == Qt.NoModifier:
            if hasattr(self, "play_button"):
                self.play()
            event.accept()
        # Left Arrow: Seek backward 5 seconds
        elif key == Qt.Key_Left and modifiers == Qt.NoModifier:
            self._seek_video(-5)
            event.accept()
        # Right Arrow: Seek forward 5 seconds
        elif key == Qt.Key_Right and modifiers == Qt.NoModifier:
            self._seek_video(5)
            event.accept()
        # Up Arrow: Volume up
        elif key == Qt.Key_Up and modifiers == Qt.NoModifier:
            self._adjust_volume(5)
            event.accept()
        # Down Arrow: Volume down
        elif key == Qt.Key_Down and modifiers == Qt.NoModifier:
            self._adjust_volume(-5)
            event.accept()
        # F12 or Ctrl+Shift+I: Open developer tools
        elif (key == Qt.Key_F12 or
              (modifiers == (Qt.ControlModifier | Qt.ShiftModifier) and
               key == Qt.Key_I)):
            self._open_developer_tools()
            event.accept()
        # Delete: Delete selected items
        elif key == Qt.Key_Delete and modifiers == Qt.NoModifier:
            if hasattr(self, "video_table"):
                self.on_delete_selected()
            event.accept()
        # Ctrl+A: Select all
        elif modifiers == Qt.ControlModifier and key == Qt.Key_A:
            if hasattr(self, "video_table"):
                for row in range(self.video_table.rowCount()):
                    item = self.video_table.item(row, 0)
                    if item:
                        item.setCheckState(Qt.Checked)
            event.accept()
        else:
            super().keyPressEvent(event)
    
    def take_screenshot(self, filename=None):
        """Take a screenshot of the current window."""
        try:
            from PyQt5.QtGui import QPixmap, QScreen
            screen = QApplication.primaryScreen()
            pixmap = screen.grabWindow(self.winId())
            
            if filename is None:
                from pathlib import Path
                import datetime
                screenshots_dir = Path(__file__).parent.parent.parent / "docs" / "screenshots"
                screenshots_dir.mkdir(parents=True, exist_ok=True)
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = screenshots_dir / f"screenshot_{timestamp}.png"
            else:
                from pathlib import Path
                screenshots_dir = Path(__file__).parent.parent.parent / "docs" / "screenshots"
                screenshots_dir.mkdir(parents=True, exist_ok=True)
                filename = screenshots_dir / filename
            
            pixmap.save(str(filename), "PNG")
            logger.info(f"Screenshot saved: {filename}")
            return str(filename)
        except Exception as e:
            logger.error(f"Failed to take screenshot: {e}")
            return None
    
    def closeEvent(self, event):
        """Handle application shutdown and persist state."""
        try:
            self.app_settings.save_settings()
        except Exception as exc:
            logger.error(f"Failed to save settings: {exc}")

        # Clean up background threads with improved timeout handling
        try:
            # Clean up FFmpeg checker thread
            if hasattr(self, 'ffmpeg_checker') and self.ffmpeg_checker:
                self._cleanup_thread(
                    self.ffmpeg_checker,
                    "FFmpeg checker",
                    timeout_ms=2000  # 2 seconds for FFmpeg operations
                )
            
            # Clean up search and download threads via presenter
            if hasattr(self, 'presenter') and self.presenter:
                if hasattr(self.presenter, 'search_thread') and self.presenter.search_thread:
                    self._cleanup_thread(
                        self.presenter.search_thread,
                        "Search thread",
                        timeout_ms=3000  # 3 seconds for search operations
                    )
                if hasattr(self.presenter, 'downloader_thread') and self.presenter.downloader_thread:
                    self._cleanup_thread(
                        self.presenter.downloader_thread,
                        "Downloader thread",
                        timeout_ms=5000  # 5 seconds for download operations
                    )
        except Exception as exc:
            logger.warning(f"Error cleaning up background threads: {exc}")

        # Clean up mini player
        try:
            self.mini_player_controller.dispose()
        except Exception as exc:
            logger.warning(f"Error disposing mini player: {exc}")

        # Clean up dialogs
        try:
            if self.settingsDialog:
                self.settingsDialog.deleteLater()
            if self.formatSettingsDialog:
                self.formatSettingsDialog.deleteLater()
        except Exception as exc:
            logger.warning(f"Error cleaning up dialogs: {exc}")

        # Stop all timers
        try:
            if hasattr(self, 'scrollTimer') and self.scrollTimer:
                self.scrollTimer.stop()
            if hasattr(self, 'resetTimer') and self.resetTimer:
                self.resetTimer.stop()
            if hasattr(self, 'animation_timer') and self.animation_timer:
                self.animation_timer.stop()
        except Exception as exc:
            logger.warning(f"Error stopping timers: {exc}")

        # Clean up WebEngine browser
        try:
            if hasattr(self, 'browser') and self.browser:
                # Disconnect all signals
                try:
                    self.browser.titleChanged.disconnect()
                    self.browser.urlChanged.disconnect()
                    self.browser.loadFinished.disconnect()
                except (TypeError, RuntimeError):
                    # Signals may already be disconnected
                    pass
                # Clear browser history and cache
                try:
                    if hasattr(self.browser, 'page'):
                        self.browser.page().deleteLater()
                except Exception:
                    pass
        except Exception as exc:
            logger.warning(f"Error cleaning up browser: {exc}")

        try:
            logger.info("Application shutting down")
        except (AttributeError, RuntimeError):
            # Logger may not be available or already destroyed
            pass

        super().closeEvent(event)

    def _cleanup_thread(self, thread, thread_name, timeout_ms=2000):
        """Safely cleanup a QThread with timeout and fallback termination.

        Args:
            thread: QThread instance to cleanup
            thread_name: Name for logging purposes
            timeout_ms: Maximum wait time in milliseconds
        """
        if not thread:
            return

        try:
            if thread.isRunning():
                logger.debug(f"Stopping {thread_name}...")
                thread.quit()

                # Wait for graceful shutdown
                if not thread.wait(timeout_ms):
                    logger.warning(
                        f"{thread_name} did not stop within {timeout_ms}ms, "
                        "terminating forcefully"
                    )
                    thread.terminate()
                    # Wait additional 500ms after terminate
                    thread.wait(500)
                else:
                    logger.debug(f"{thread_name} stopped gracefully")

            thread.deleteLater()
        except Exception as exc:
            logger.warning(f"Error cleaning up {thread_name}: {exc}")

    def initUI(self):
        builder = LayoutBuilder(self)
        self.browWidget = builder.build_left_panel()
        self.downLayoutWidget = builder.build_right_panel()
        self.table_manager = builder.table_manager

        fixedWidth = 450
        self.downLayoutWidget.setFixedWidth(fixedWidth)
        self.downLayoutWidget.setMaximumSize(QSize(fixedWidth, 16777215))

        self.splitter = builder.build_splitter(self.browWidget, self.downLayoutWidget)

        mainLayout = QVBoxLayout(self)
        mainLayout.setContentsMargins(0, 0, 0, 0)
        mainLayout.addWidget(self.splitter)
        self.setLayout(mainLayout)

        self.splitter.setSizes([500, 300])
        self.browser.setMinimumSize(500, 300)
        self.browser.setZoomFactor(0.8)

        self.browser.titleChanged.connect(self.updateTitle)
        self.resetTimer = QTimer(self)
        self.resetTimer.setSingleShot(True)
        self.resetTimer.timeout.connect(self.performResetMediaControls)
        self.browser.urlChanged.connect(self.checkAndTriggerReset)
        self.browser.urlChanged.connect(self._on_browser_url_changed)
        self.browser.loadFinished.connect(self.updateButtonStates)
        self.browser.loadFinished.connect(self._on_browser_load_finished)

        self.mini_player_controller.create()

        # Apply dark theme stylesheet
        self.setStyleSheet(DARK_THEME_STYLESHEET)

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
            logger.debug("No valid video or duration available.")

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

    def _seek_video(self, seconds: int) -> None:
        """Seek video by specified seconds.
        
        Args:
            seconds: Number of seconds to seek (positive = forward, negative = backward)
        """
        if not hasattr(self, "browser") or not self.browser:
            return
        js = f"""
        (function() {{
            var video = document.querySelector('video');
            if (video) {{
                var newTime = video.currentTime + {seconds};
                video.currentTime = Math.max(0, Math.min(newTime, video.duration));
                return true;
            }}
            return false;
        }})();
        """
        try:
            self.browser.page().runJavaScript(js)
        except Exception as exc:
            logger.debug(f"Seek video error: {exc}")

    def _adjust_volume(self, delta: int) -> None:
        """Adjust video volume.
        
        Args:
            delta: Volume change in percentage (-100 to 100)
        """
        if not hasattr(self, "browser") or not self.browser:
            return
        js = f"""
        (function() {{
            var video = document.querySelector('video');
            if (video) {{
                var currentVolume = video.volume || 1.0;
                var newVolume = Math.max(0, Math.min(1.0, currentVolume + ({delta} / 100)));
                video.volume = newVolume;
                return newVolume;
            }}
            return null;
        }})();
        """
        try:
            self.browser.page().runJavaScript(js)
            # Also update mini player volume if active
            if (hasattr(self, "mini_player_controller") and
                    self.mini_player_controller and
                    self.mini_player_controller.is_mini_mode and
                    self.mini_player_controller.volume_slider):
                # Get current volume from video and update slider
                def update_slider(volume):
                    if volume is not None and self.mini_player_controller.volume_slider:
                        slider_value = int(volume * 100)
                        self.mini_player_controller.volume_slider.setValue(slider_value)
                get_volume_js = """
                (function() {
                    var video = document.querySelector('video');
                    return video ? video.volume : null;
                })();
                """
                self.browser.page().runJavaScript(get_volume_js, update_slider)
        except Exception as exc:
            logger.debug(f"Adjust volume error: {exc}")

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
        
        # Mirror the title into the mini player as well
        self.mini_player_controller.update_title(newTitle)

        # Ensure mini player playback controls reflect the current state
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
            self.title_label.setText("YouTube Music hides inline controls")
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
        # Run JavaScript to detect player state and update button icon
        self.browser.page().runJavaScript(jsCode, self.updatePlayButtonIcon)

    @pyqtSlot(str)
    def updatePlayButtonIcon(self, state):
        if state == 'playing':
            self.play_button.setText("⏸️")  # Update to pause icon
        elif state == 'paused':
            self.play_button.setText("▶️")  # Update to play icon
        else:
            # Optionally handle 'unknown' state or other states if necessary
            pass
        self.mini_player_controller.update_play_button_icon(state)

    def play_next(self):
        # JavaScript helper to advance playback on supported sites
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
        # Update play/pause button state once the script finishes
        self.browser.page().runJavaScript(jsCode, self.updatePlayButtonIcon)

    def copyUrlToClipboard(self):
        """Copy the current browser URL to the clipboard and search field."""
        currentUrl = self.browser.url().toString()
        logger.debug(f"Current URL: {currentUrl}")
        
        # Clipboard copy helper
        clipboard = QApplication.clipboard()
        clipboard.setText(currentUrl)
        
        # Sync search box and optionally trigger search
        if hasattr(self, "search_url"):
            self.search_url.setText(currentUrl)
            self.on_search()

    def navigateToLink(self):
        # Handle the predefined URL here. This could involve opening the URL in a web browser,
        # or performing another action based on the URL.
        logger.debug(f"Navigate to: {self.predefinedURL}")
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
                self.settingsDialog = None
                QMessageBox.critical(self, "Error", f"Failed to open settings dialog:\n{e}")
        else:
            self.settingsDialog.raise_()

    def onSettingsDialogClosed(self):
        self.settingsDialog.deleteLater()
        self.settingsDialog = None
    
    def openHistoryDialog(self):
        """Open download history dialog."""
        if not hasattr(self, 'historyDialog') or self.historyDialog is None:
            self.historyDialog = HistoryDialog(self)
            self.historyDialog.redownload_requested.connect(
                self._on_history_redownload
            )
        self.historyDialog.show()
        self.historyDialog.raise_()
        self.historyDialog.activateWindow()

    def _on_history_redownload(self, url: str, title: str, format_id: str):
        """Handle redownload request from history dialog.
        
        Args:
            url: Video URL
            title: Video title
            format_id: Format ID
        """
        # Add to search URL and trigger search
        if hasattr(self, "search_url"):
            self.search_url.setText(url)
            # Trigger search
            self.presenter.start_search(url)

    def openFormatSettingsDialog(self):
        """Display the format settings dialog, creating it on first use."""
        if not self.formatSettingsDialog:
            try:
                self.formatSettingsDialog = FormatSettingsDialog(self, self.app_settings)
                self.formatSettingsDialog.settingsChanged.connect(self.onFormatSettingsChanged)
                self.formatSettingsDialog.finished.connect(self.onFormatSettingsDialogClosed)
                self.formatSettingsDialog.show()
            except Exception as e:
                self.formatSettingsDialog = None
                QMessageBox.critical(self, "Error", f"Failed to open format settings dialog:\n{e}")
        else:
            self.formatSettingsDialog.raise_()

    def onFormatSettingsDialogClosed(self):
        """Dispose of the cached format settings dialog."""
        if self.formatSettingsDialog:
            self.formatSettingsDialog.deleteLater()
            self.formatSettingsDialog = None

    def onFormatSettingsChanged(self):
        """Apply updated format filters to the table."""
        self.table_manager.apply_filters()
        self.status_label.setText("Format filters updated.")

    def refreshBrowser(self):
        """ Method to refresh the browser when the settings dialog is closed """
        if hasattr(self, 'browser') and self.browser is not None:
            self.browser.reload()
        else:
            logger.warning("Browser attribute is not set or is None")

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
            self.browHideButton.setText("💥")
            self.adjustMainLayoutSize()
        else:
            self.browWidget.show()
            self.browHideButton.setText("🦕")
            self.resetMainLayoutSize()

    def adjustMainLayoutSize(self):
        if not self.browWidget.isVisible():
            self.setMinimumSize(450, 560)
            self.resize(450, 560)
            self.downLayoutWidget.setMinimumSize(450, 560)
            self.browWidget.setMinimumSize(0, 0)
        else:
            self.setMinimumSize(980, 560)
            self.resize(980, 560)
            self.browWidget.setMinimumSize(500, 560)
            self.downLayoutWidget.setMinimumSize(450, 560)

    def resetMainLayoutSize(self):
        """Restore default split sizes when both panels are visible."""
        self.setMinimumSize(1100, 560)
        self.browWidget.setMinimumSize(500, 560)
        self.downLayoutWidget.setMinimumSize(450, 560)
        self.splitter.setSizes([500, 450])

    def center_on_screen(self):
        # Get the main screen's geometry
        screen_geometry = QApplication.desktop().screenGeometry()

        # Calculate the center point
        center_point = screen_geometry.center()

        # Set the center point of the dialog
        self.move(center_point - self.rect().center())

    def search_duplicate_urls(self, url):
        """Maintain backwards compatibility with legacy duplicate check."""
        return self.is_duplicate_url(url)

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
        """Remove all videos currently checked in the table."""
        self.on_delete_selected()

    @pyqtSlot()
    def on_search(self):
        self.presenter.start_search(self.search_url.text())

    def check_results(self):
        # Assuming self.video_info_list is updated with search results
        if not self.video_info_list:
            self.status_label.setText("No results found.")

    def enable_search_button(self):
        self.search_button.setEnabled(True)
        self.progress_bar.setRange(0, 100)  # Reset the progress bar range

    def set_status(self, message):
        self.status_label.setText(message)

    def on_ffmpeg_check_complete(self, success: bool, message: str):
        """Log FFmpeg availability checks and surface warnings."""
        if success:
            logger.info("FFmpeg: %s", message)
            self.ffmpeg_status = "✓"
        else:
            logger.warning("FFmpeg: %s", message)
            self.ffmpeg_status = "✗"
        self._update_status_bar()

    def search_finished(self):
        self.set_status("Search complete.")
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(100)

    def download_finished(self):
        self.status_label.setText("Download complete.")

    def set_status(self, message):
        """Set status message and update status bar with queue info.
        
        Args:
            message: Status message
        """
        self.status_label.setText(message)
        self._update_status_bar()

    @pyqtSlot(float)
    def update_progress_bar(self, progress):
        self.progress_bar.setValue(int(progress))

    @pyqtSlot(int, float, str, str)
    def update_item_progress(self, row: int, percent: float, speed: str, eta: str):
        """Update download progress for a specific table row.
        
        Args:
            row: Row index in the table
            percent: Download percentage (0-100)
            speed: Download speed string
            eta: Estimated time remaining
        """
        if hasattr(self, 'table_manager') and self.table_manager:
            self.table_manager.update_download_progress(row, percent, speed, eta)

    @pyqtSlot(int)
    def mark_item_complete(self, row: int):
        """Mark a download as complete in the table.
        
        Args:
            row: Row index in the table
        """
        if hasattr(self, 'table_manager') and self.table_manager:
            self.table_manager.mark_download_complete(row)

    @pyqtSlot(int, str)
    def mark_item_started(self, row: int, title: str):
        """Mark a download as started in the table.
        
        Args:
            row: Row index in the table
            title: Video title
        """
        if hasattr(self, 'table_manager') and self.table_manager:
            self.table_manager.mark_download_started(row, title)

    @pyqtSlot(str, str, str, str, object)
    def add_to_history(
        self, title: str, url: str, format_id: str, path: str, size: object
    ):
        """Add a completed download to history.
        
        Args:
            title: Video title
            url: Video URL
            format_id: Format ID used
            path: Download file path
            size: File size in bytes (optional)
        """
        try:
            from ..models.history import DownloadHistory
            history = DownloadHistory()
            history.add_entry(title, url, format_id, path, size)
            # Show notification
            if hasattr(self, 'notification_manager'):
                # Get settings for auto-open folder (default False)
                open_folder = getattr(self.app_settings, 'auto_open_folder', False)
                self.notification_manager.notify_download_complete(
                    title, path, open_folder
                )
        except Exception as exc:
            logger.warning(f"Failed to add to history: {exc}")

    def _on_address_bar_entered(self, url_or_query: str):
        """Handle address bar URL entry.
        
        Args:
            url_or_query: URL or search query
        """
        if not hasattr(self, "browser") or not self.browser:
            return

        # If it's a search query (doesn't start with http), treat as search
        if not url_or_query.startswith(("http://", "https://")):
            # Could implement search here, for now just try as URL
            url_or_query = f"https://www.google.com/search?q={url_or_query}"

        try:
            qurl = QUrl(url_or_query)
            if qurl.isValid():
                self.browser.setUrl(qurl)
            else:
                logger.warning(f"Invalid URL: {url_or_query}")
        except Exception as exc:
            logger.error(f"Failed to navigate to URL: {exc}")

    def _on_browser_url_changed(self, url: QUrl):
        """Handle browser URL change to update address bar.
        
        Args:
            url: New browser URL
        """
        if hasattr(self, "browser_toolbar") and self.browser_toolbar:
            url_str = url.toString()
            if url_str != self.browser_toolbar.get_url():
                self.browser_toolbar.set_url(url_str)

    def _on_browser_load_finished(self, success: bool):
        """Handle browser load finished to update navigation buttons.
        
        Args:
            success: Whether load was successful
        """
        if (hasattr(self, "browser") and self.browser and
                hasattr(self, "browser_toolbar") and self.browser_toolbar):
            can_go_back = self.browser.history().canGoBack()
            can_go_forward = self.browser.history().canGoForward()
            self.browser_toolbar.update_navigation_state(
                can_go_back, can_go_forward
            )

    def _on_browser_back(self):
        """Handle back button click."""
        if hasattr(self, "browser") and self.browser:
            self.browser.back()

    def _on_browser_forward(self):
        """Handle forward button click."""
        if hasattr(self, "browser") and self.browser:
            self.browser.forward()

    def _on_browser_refresh(self):
        """Handle refresh button click."""
        if hasattr(self, "browser") and self.browser:
            self.browser.reload()

    def _on_browser_home(self):
        """Handle home button click."""
        if hasattr(self, "browser") and self.browser:
            self.browser.setUrl(self.homePageUrl)

    def status_update(self, message):
        self.status_label.setText(message)

    def progress_update(self, progress):
        self.progress_bar.setValue(progress)

    def get_selected_videos(self):
        return {index.row() for index in self.video_table.selectedIndexes() if index.column() == 0}

    @pyqtSlot()
    def on_download(self):
        selected_videos = []
        selected_rows = []
        invalid_selection = False

        for row in range(self.video_table.rowCount()):
            checkbox = self.video_table.item(row, 0)
            if not (checkbox and checkbox.checkState() == Qt.Checked):
                continue

            title_item = self.video_table.item(row, 2)
            format_combo_box = self.video_table.cellWidget(row, 3)
            selected_format_id = None
            
            modified_title = title_item.text() if title_item else "Untitled"
            if row < len(self.video_info_list) and self.video_info_list[row] is not None:
                video_url = self.video_info_list[row][1]
            else:
                logger.error(f"Invalid video_info_list entry at row {row}")
                continue
            
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
            selected_rows.append(row)

        if invalid_selection:
            self.status_label.setText("Select a valid format before downloading.")
            return

        self.presenter.start_download(selected_videos, selected_rows)

    def download_failed(self, message):
        self.set_status(f"Download failed: {message}")

    def select_download_directory(self):
        dir_path = QFileDialog.getExistingDirectory(self, "Choose download folder", os.path.expanduser("~"))
        return dir_path if dir_path else None

    @pyqtSlot()
    def on_delete_selected(self):
        rows_to_delete = []
        for row in range(self.video_table.rowCount()):
            checkbox_item = self.video_table.item(row, 0)
            if checkbox_item and checkbox_item.checkState() == Qt.Checked:
                rows_to_delete.append(row)

        if not rows_to_delete:
            self.status_label.setText("No videos selected.")
            return

        for row in sorted(rows_to_delete, reverse=True):
            if row < len(self.video_info_list):
                self.video_info_list.pop(row)
            self.video_table.removeRow(row)

        if hasattr(self, "header"):
            self.header.updateState()
        self.status_label.setText(f"Removed {len(rows_to_delete)} item(s).")

    def _on_new_tab(self):
        """Handle new tab button click."""
        if hasattr(self, 'browser_tabs'):
            self.browser_tabs.add_tab(self.homePageUrl, "New Tab")

    def _on_tab_changed(self, index: int):
        """Handle tab change.
        
        Args:
            index: New tab index
        """
        if hasattr(self, 'browser_tabs'):
            current_tab = self.browser_tabs.get_current_tab()
            if current_tab:
                # Update browser reference
                self.browser = current_tab.browser
                # Update address bar
                if hasattr(self, 'browser_toolbar'):
                    self.browser_toolbar.set_url(
                        current_tab.get_url().toString()
                    )
                # Update navigation buttons
                self._on_browser_load_finished(True)
                # Update zoom display
                if hasattr(self, 'browser_toolbar') and hasattr(self.browser, 'zoomFactor'):
                    self.browser_toolbar.update_zoom(self.browser.zoomFactor())

    def _on_zoom_in(self):
        """Handle zoom in request."""
        if hasattr(self, 'browser') and hasattr(self.browser, 'zoomFactor'):
            current_zoom = self.browser.zoomFactor()
            new_zoom = min(5.0, current_zoom + 0.1)
            self.browser.setZoomFactor(new_zoom)
            if hasattr(self, 'browser_toolbar'):
                self.browser_toolbar.update_zoom(new_zoom)

    def _on_zoom_out(self):
        """Handle zoom out request."""
        if hasattr(self, 'browser') and hasattr(self.browser, 'zoomFactor'):
            current_zoom = self.browser.zoomFactor()
            new_zoom = max(0.25, current_zoom - 0.1)
            self.browser.setZoomFactor(new_zoom)
            if hasattr(self, 'browser_toolbar'):
                self.browser_toolbar.update_zoom(new_zoom)

    def _on_zoom_reset(self):
        """Handle zoom reset request."""
        if hasattr(self, 'browser') and hasattr(self.browser, 'setZoomFactor'):
            self.browser.setZoomFactor(1.0)
            if hasattr(self, 'browser_toolbar'):
                self.browser_toolbar.update_zoom(1.0)

    def _update_status_bar(self):
        """Update status bar with comprehensive status information."""
        if not hasattr(self, 'status_label'):
            return
        
        # Get queue counts
        pending = 0
        downloading = 0
        if hasattr(self, 'download_queue'):
            pending = self.download_queue.get_pending_count()
            downloading = self.download_queue.get_downloading_count()
        
        # Build status parts
        parts = []
        if downloading > 0:
            parts.append(f"Downloading: {downloading}")
        if pending > 0:
            parts.append(f"Queued: {pending}")
        if hasattr(self, 'ffmpeg_status'):
            parts.append(f"FFmpeg: {self.ffmpeg_status}")
        if hasattr(self, 'network_status'):
            parts.append(f"Network: {self.network_status}")
        
        # Update status if we have parts
        if parts:
            current_text = self.status_label.text()
            # Only update if not a transient message
            if not any(x in current_text.lower() for x in ['downloading', 'complete', 'failed']):
                self.status_label.setText(f"{current_text} | {' | '.join(parts)}")

    def _open_developer_tools(self):
        """Open browser developer tools in a separate window."""
        if not hasattr(self, 'browser') or not self.browser:
            return
        
        try:
            from PyQt5.QtWebEngineWidgets import QWebEngineView
            from PyQt5.QtWidgets import QDialog, QVBoxLayout
            
            # Create dev tools dialog
            if not hasattr(self, '_dev_tools_dialog') or self._dev_tools_dialog is None:
                self._dev_tools_dialog = QDialog(self)
                self._dev_tools_dialog.setWindowTitle("Developer Tools")
                self._dev_tools_dialog.setMinimumSize(800, 600)
                
                layout = QVBoxLayout(self._dev_tools_dialog)
                layout.setContentsMargins(0, 0, 0, 0)
                
                # Create dev tools view
                self._dev_tools_view = QWebEngineView(self._dev_tools_dialog)
                layout.addWidget(self._dev_tools_view)
                
                # Connect browser page to dev tools
                if hasattr(self.browser, 'page'):
                    page = self.browser.page()
                    if hasattr(page, 'setDevToolsPage'):
                        dev_tools_page = self._dev_tools_view.page()
                        page.setDevToolsPage(dev_tools_page)
                
                self._dev_tools_dialog.finished.connect(
                    lambda: setattr(self, '_dev_tools_dialog', None)
                )
            
            self._dev_tools_dialog.show()
            self._dev_tools_dialog.raise_()
            self._dev_tools_dialog.activateWindow()
        except Exception as e:
            logger.error(f"Failed to open developer tools: {e}")
            QMessageBox.warning(
                self,
                "Developer Tools",
                f"Failed to open developer tools:\n{e}"
            )