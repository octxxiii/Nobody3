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
        self.Nobody = resolve_writable_cache_dir("Nobody")  # Define here
        
        # Load persisted application settings
        self.app_settings = AppSettings()
        self.app_settings.load_settings()

        # Initialize mini player controller
        self.mini_player_controller = MiniPlayerController(self)
        # Use a user-writable cache directory to avoid permission issues under Program Files
        self.cacheDirectory = resolve_writable_cache_dir("Nobody 3")
        if not os.path.exists(self.cacheDirectory):
            try:
                os.makedirs(self.cacheDirectory, exist_ok=True)
            except Exception as e:
                logger.error(f"Failed to create cache directory {self.cacheDirectory}: {e}")

        # Validate and clean corrupted WebEngine profile (e.g., from system date changes)
        from ..utils.cache import validate_and_clean_profile
        profile_cleaned = validate_and_clean_profile(self.cacheDirectory, logger)
        if profile_cleaned:
            logger.info("WebEngine profile validated and cleaned. "
                       "This may resolve crashes caused by system date changes.")

        # Configure persistent browser profile paths
        profile = QWebEngineProfile.defaultProfile()
        profile.setPersistentStoragePath(self.cacheDirectory)
        profile.setHttpCacheType(QWebEngineProfile.NoCache)
        profile.setPersistentCookiesPolicy(QWebEngineProfile.ForcePersistentCookies)

        settings = profile.settings()
        settings.setAttribute(QWebEngineSettings.LocalStorageEnabled, True)
        settings.setAttribute(QWebEngineSettings.JavascriptEnabled, True)
        settings.setAttribute(QWebEngineSettings.PluginsEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebGLEnabled, True)

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
        if event.key() in (Qt.Key_Enter, Qt.Key_Return):
            if hasattr(self, "search_url"):
                focused_widget = QApplication.focusWidget()
                if focused_widget == self.search_url and self.search_url.text().strip():
                    self.on_search()
            else:
                self.on_search()
        elif event.key() == Qt.Key_Escape:
            self.lower()
        elif event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_S:
            # Ctrl+S to take screenshot
            self.take_screenshot()
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

        self.mini_player_controller.dispose()
        super().closeEvent(event)

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
        self.browser.loadFinished.connect(self.updateButtonStates)

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
        else:
            logger.warning("FFmpeg: %s", message)

    def search_finished(self):
        self.set_status("Search complete.")
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(100)

    def download_finished(self):
        self.status_label.setText("Download complete.")

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

        if invalid_selection:
            self.status_label.setText("Select a valid format before downloading.")
            return

        self.presenter.start_download(selected_videos)

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

