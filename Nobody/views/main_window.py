"""메인 윈도우 (VideoDownloader)"""

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

# Nobody 모듈 임포트
from ..config.constants import DARK_THEME_STYLESHEET
from ..utils.cache import resolve_writable_cache_dir
from ..utils.logging import logger
from ..models.settings import AppSettings
from ..services.ffmpeg_checker import FFmpegChecker
from .mini_player import MiniPlayerController
from .layout_builder import LayoutBuilder
from .format_settings_dialog import FormatSettingsDialog
from .settings_dialog import SettingsDialog
from .presenter import VideoPresenter

# resources_rc는 선택적으로 임포트 (없어도 동작)
try:
    import resources_rc
except ImportError:
    pass  # resources_rc가 없어도 동작하도록


# 중복된 클래스들은 이미 다른 모듈로 분리되었으므로 제거됨
# - AppSettings: models.settings에서 임포트
# - FormatSettingsDialog: views.format_settings_dialog에서 임포트
# - SettingsDialog: views.settings_dialog에서 임포트
# - MiniPlayerController: views.mini_player에서 임포트
# - VideoTableManager: views.video_table에서 임포트
# - VideoPresenter: views.presenter에서 임포트


class VideoDownloader(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowFlags(self.windowFlags() | Qt.WindowMinimizeButtonHint | Qt.WindowMaximizeButtonHint | Qt.WindowCloseButtonHint) # 최소화, 최대화, 닫기 버튼 활성화
        self.settingsDialog = None
        self.formatSettingsDialog = None  # 포맷 설정 다이얼로그 참조
        self.Nobody = resolve_writable_cache_dir("Nobody")  # Define here
        
        # 앱 설정 초기화 및 로드
        self.app_settings = AppSettings()
        self.app_settings.load_settings()
        
        # 미니 플레이어 컨트롤러
        self.mini_player_controller = MiniPlayerController(self)
        # Use a user-writable cache directory to avoid permission issues under Program Files
        self.cacheDirectory = resolve_writable_cache_dir("OctXXIII")
        if not os.path.exists(self.cacheDirectory):
            try:
                os.makedirs(self.cacheDirectory, exist_ok=True)
            except Exception as e:
                logger.error(f"Failed to create cache directory {self.cacheDirectory}: {e}")

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

        self.setWindowTitle("OctXXIII - YouTube/Music Converter & Player")
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
        
        # FFmpeg 자동 체크 및 다운로드 시작 (백그라운드에서 조용히)
        self.ffmpeg_checker = FFmpegChecker(self)
        self.ffmpeg_checker.check_complete.connect(self.on_ffmpeg_check_complete)
        self.ffmpeg_checker.start()

    def changeEvent(self, event):
        """창 상태 변경 이벤트 처리"""
        # 최소화와 미니플레이어 기능 분리 - 최소화는 일반 최소화만 수행
        super().changeEvent(event)
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            # 엔터 키는 검색만 수행 (클립보드 복사는 📋 버튼으로만)
            if hasattr(self, 'search_url'):
                focused_widget = QApplication.focusWidget()
                # search_url에 포커스가 있고 텍스트가 있을 때만 검색
                if focused_widget == self.search_url and self.search_url.text().strip():
                    self.on_search()
                # 포커스가 없거나 비어있으면 아무 동작도 하지 않음
            else:
                self.on_search()
        elif event.key() == Qt.Key_Escape:
            self.lower()
        else:
            super().keyPressEvent(event)  # Handle other key events normally
    
    def closeEvent(self, event):
        """애플리케이션 종료 시 설정 저장"""
        try:
            self.app_settings.save_settings()
        except Exception as e:
            logger.error(f"설정 저장 중 오류: {e}")
        
        # 미니 플레이어 리소스 정리
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
        
        # 미니 플레이어 제목도 업데이트 (마키 적용)
        self.mini_player_controller.update_title(newTitle)

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
        elif state == 'paused':
            self.play_button.setText("▶️")  # Update to play icon
        else:
            # Optionally handle 'unknown' state or other states if necessary
            pass
        self.mini_player_controller.update_play_button_icon(state)

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

    def copyUrlToClipboard(self):
        """브라우저의 현재 URL을 클립보드에 복사하고 검색 필드에 설정한 후 검색"""
        currentUrl = self.browser.url().toString()
        logger.debug(f"Current URL: {currentUrl}")
        
        # 클립보드에 복사
        clipboard = QApplication.clipboard()
        clipboard.setText(currentUrl)
        
        # 검색 필드에 URL 설정
        if hasattr(self, 'search_url'):
            self.search_url.setText(currentUrl)
            # 검색 실행 (중복 체크는 on_search에서 수행)
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
                # 예외로 앱이 종료되지 않도록 방어
                self.settingsDialog = None
                QMessageBox.critical(self, "Error", f"정보 창을 여는 중 오류가 발생했습니다:\n{e}")
        else:
            self.settingsDialog.raise_()  # Brings the dialog to the front if already open

    def onSettingsDialogClosed(self):
        self.settingsDialog.deleteLater()
        self.settingsDialog = None  # Clear the reference after the dialog is closed
    
    def openFormatSettingsDialog(self):
        """포맷 설정 다이얼로그 열기"""
        if not self.formatSettingsDialog:
            try:
                self.formatSettingsDialog = FormatSettingsDialog(self, self.app_settings)
                self.formatSettingsDialog.settingsChanged.connect(self.onFormatSettingsChanged)
                self.formatSettingsDialog.finished.connect(self.onFormatSettingsDialogClosed)
                self.formatSettingsDialog.show()
            except Exception as e:
                # 예외로 앱이 종료되지 않도록 방어
                self.formatSettingsDialog = None
                QMessageBox.critical(self, "Error", f"포맷 설정 창을 여는 중 오류가 발생했습니다:\n{e}")
        else:
            self.formatSettingsDialog.raise_()  # Brings the dialog to the front if already open

    def onFormatSettingsDialogClosed(self):
        """포맷 설정 다이얼로그 닫힘 처리"""
        if self.formatSettingsDialog:
            self.formatSettingsDialog.deleteLater()
            self.formatSettingsDialog = None

    def onFormatSettingsChanged(self):
        """포맷 설정 변경 시 호출"""
        self.table_manager.apply_filters()
        self.status_label.setText("포맷 설정이 적용되었습니다.")

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
        """중복 URL 검색 (is_duplicate_url과 동일한 기능 - 호환성을 위해 유지)"""
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
        """선택된 비디오 삭제 (on_delete_selected와 동일한 기능 - 호환성을 위해 유지)"""
        # on_delete_selected 메서드를 사용하도록 리다이렉트
        self.on_delete_selected()

    @pyqtSlot()
    def on_search(self):
        self.presenter.start_search(self.search_url.text())

    def check_results(self):
        # Assuming self.video_info_list is updated with search results
        if not self.video_info_list:
            self.status_label.setText("검색 결과가 없습니다.")

    def enable_search_button(self):
        self.search_button.setEnabled(True)
        self.progress_bar.setRange(0, 100)  # Reset the progress bar range

    def set_status(self, message):
        self.status_label.setText(message)

    def on_ffmpeg_check_complete(self, success: bool, message: str):
        """FFmpeg 체크 완료 시 호출되는 콜백 (조용히 로깅만 수행)"""
        if success:
            # 성공 시 조용히 로그만 남김 (사용자 방해 없음)
            logger.info(f"FFmpeg: {message}")
        else:
            # 실패 시에도 조용히 로그만 남김 (사용자 방해 없음)
            logger.warning(f"FFmpeg: {message}")
            # 필요시 나중에 사용자가 다운로드를 시도할 때 알림을 표시할 수 있음
    
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
            self.status_label.setText("각 비디오에 대해 유효한 포맷을 선택해 주세요.")
            return

        self.presenter.start_download(selected_videos)

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


# MainThreadSignalEmitter, FFmpegChecker, Searcher, Downloader는 이미 다른 모듈로 분리됨
# - services/searcher.py에 Searcher 클래스