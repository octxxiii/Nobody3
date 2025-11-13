"""Background thread that ensures FFmpeg is available."""

import os
import sys
from PyQt5.QtCore import QThread, pyqtSignal

from ..utils.ffmpeg import check_ffmpeg_exists, download_ffmpeg_quietly


class FFmpegChecker(QThread):
    """Verify FFmpeg availability and download it if missing."""

    check_complete = pyqtSignal(bool, str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.base_path = None

    def run(self):
        try:
            if getattr(sys, "frozen", False):
                self.base_path = os.path.dirname(sys.executable)
            else:
                current_file = os.path.abspath(__file__)
                nobody_dir = os.path.dirname(os.path.dirname(current_file))
                self.base_path = os.path.dirname(nobody_dir)

            if check_ffmpeg_exists():
                self.check_complete.emit(True, "FFmpeg already available.")
                return

            if sys.platform.startswith("linux"):
                self.check_complete.emit(False, "Install FFmpeg manually on Linux.")
                return

            success = download_ffmpeg_quietly(self.base_path)

            if success and check_ffmpeg_exists():
                self.check_complete.emit(True, "FFmpeg downloaded successfully.")
            elif success:
                self.check_complete.emit(False, "FFmpeg download finished but binary not found.")
            else:
                self.check_complete.emit(False, "FFmpeg download failed.")
        except Exception as exc:  # noqa: BLE001
            self.check_complete.emit(False, f"FFmpeg check error: {exc}")

