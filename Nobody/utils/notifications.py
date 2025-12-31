"""Notification utilities for download completion and system alerts."""

import os
import platform
from typing import Optional
from PyQt5.QtWidgets import QSystemTrayIcon, QApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QDesktopServices

from ..utils.logging import logger


class NotificationManager:
    """Manages system notifications for downloads."""

    def __init__(self, parent=None):
        """Initialize notification manager.
        
        Args:
            parent: Parent widget
        """
        self.parent = parent
        self.tray_icon: Optional[QSystemTrayIcon] = None
        self._init_tray_icon()

    def _init_tray_icon(self):
        """Initialize system tray icon."""
        if not QSystemTrayIcon.isSystemTrayAvailable():
            logger.warning("System tray not available")
            return

        try:
            self.tray_icon = QSystemTrayIcon(parent=self.parent)
            # Try to set an icon if available
            try:
                import resources_rc
                self.tray_icon.setIcon(QIcon(":/appIcon"))
            except ImportError:
                pass
            self.tray_icon.show()
        except Exception as e:
            logger.warning("Failed to initialize tray icon: %s", e)

    def show_notification(
        self,
        title: str,
        message: str,
        duration: int = 5000
    ):
        """Show system notification.
        
        Args:
            title: Notification title
            message: Notification message
            duration: Duration in milliseconds
        """
        if self.tray_icon:
            try:
                self.tray_icon.showMessage(
                    title,
                    message,
                    QSystemTrayIcon.Information,
                    duration
                )
            except Exception as e:
                logger.warning("Failed to show notification: %s", e)
        else:
            # Fallback: log to console
            logger.info("%s: %s", title, message)

    def notify_download_complete(
        self,
        title: str,
        file_path: Optional[str] = None,
        open_folder: bool = False
    ):
        """Notify user of download completion.
        
        Args:
            title: Video title
            message: Notification message
            file_path: Path to downloaded file
            open_folder: Whether to open folder automatically
        """
        message = f"Download complete: {title}"
        self.show_notification("Download Complete", message)
        
        # Play notification sound if available
        self._play_notification_sound()
        
        # Open folder if requested
        if open_folder and file_path:
            folder_path = os.path.dirname(file_path)
            if os.path.exists(folder_path):
                QDesktopServices.openUrl(QUrl.fromLocalFile(folder_path))

    def notify_download_failed(self, title: str, error: str):
        """Notify user of download failure.
        
        Args:
            title: Video title
            error: Error message
        """
        message = f"Download failed: {title}\n{error}"
        self.show_notification("Download Failed", message)

    def _play_notification_sound(self):
        """Play notification sound (platform-specific)."""
        try:
            system = platform.system()
            if system == "Windows":
                # Windows beep
                import winsound
                winsound.MessageBeep(winsound.MB_ICONASTERISK)
            elif system == "Darwin":
                # macOS notification sound
                os.system("afplay /System/Library/Sounds/Glass.aiff")
            elif system == "Linux":
                # Linux beep (if available)
                try:
                    os.system("paplay /usr/share/sounds/freedesktop/stereo/complete.oga")
                except:
                    pass
        except Exception as e:
            logger.debug("Could not play notification sound: %s", e)
