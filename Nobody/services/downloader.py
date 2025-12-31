"""Background downloader thread using yt_dlp."""

import os
import yt_dlp
from PyQt5.QtCore import QThread, pyqtSignal
from typing import List, Tuple

from ..utils.ffmpeg import find_ffmpeg_executable
from ..utils.logging import logger
from ..utils.sanitize import sanitize_filename


class Downloader(QThread):
    """Download videos and emit progress/status updates."""

    updated_status = pyqtSignal(str)
    download_failed = pyqtSignal(str)
    updated_progress = pyqtSignal(float)
    # New signals for individual item progress
    item_progress = pyqtSignal(int, float, str, str)  # row, percent, speed, eta
    item_completed = pyqtSignal(int)  # row
    item_started = pyqtSignal(int, str)  # row, title
    history_added = pyqtSignal(str, str, str, str, object)  # title, url, format, path, size

    def __init__(self, videos: List[Tuple[str, str, str]], download_directory: str, row_mapping: dict = None):
        """Initialize downloader thread.
        
        Args:
            videos: List of tuples (title, url, format_id)
            download_directory: Target directory for downloads
            row_mapping: Dictionary mapping (title, url) to row index
        """
        super().__init__()
        self.videos = videos
        self.download_directory = download_directory
        self.row_mapping = row_mapping or {}  # Maps (title, url) to row index
        self.current_row = -1
        self.current_title = ""

    def run(self):
        """Execute download process for all videos."""
        for idx, (title, url, format_id) in enumerate(self.videos):
            # Find row index for this video
            row_idx = self.row_mapping.get((title, url), idx)
            self.current_row = row_idx
            self.current_title = title
            
            # Emit started signal
            self.item_started.emit(row_idx, title)
            
            # Use improved filename sanitization
            safe_title = sanitize_filename(title)
            is_mp3_conversion = format_id == "bestaudio/best" or "MP3" in title

            ffmpeg_path = find_ffmpeg_executable()
            if ffmpeg_path != "ffmpeg" and os.path.exists(ffmpeg_path):
                logger.info("Using FFmpeg at: %s", ffmpeg_path)
            else:
                logger.warning("FFmpeg fallback to PATH (resolved value: %s)", ffmpeg_path)

            download_options = {
                "format": format_id,
                "outtmpl": os.path.join(self.download_directory, f"{safe_title}.%(ext)s"),
                "progress_hooks": [self.progress_hook],
                "nocheckcertificate": True,
                "prefer_insecure": True,
                "geo_bypass": True,
                "geo_verification_proxy": None,
                "socket_timeout": 30,
                "retries": 10,
                "fragment_retries": 10,
                "file_access_retries": 10,
                "extractor_retries": 10,
                "ignoreerrors": True,
                "no_color": True,
                "logtostderr": True,
                "verbose": True,
                "ffmpeg_location": ffmpeg_path,
            }

            if is_mp3_conversion:
                download_options["postprocessors"] = [
                    {
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "mp3",
                        "preferredquality": "320",
                    }
                ]
            else:
                download_options["postprocessors"] = [
                    {
                        "key": "FFmpegVideoConvertor",
                        "preferredformat": "mp4",
                    }
                ]
                download_options["merge_output_format"] = "mp4"
                download_options["postprocessor_args"] = ["-c:v", "copy", "-c:a", "copy"]

            with yt_dlp.YoutubeDL(download_options) as ydl:
                try:
                    self.updated_status.emit(f"Starting download: {title}")
                    ydl.download([url])
                    self.updated_status.emit(f"Download complete: {title}")
                    # Emit completion signal
                    self.item_completed.emit(row_idx)
                    
                    # Find downloaded file and add to history
                    downloaded_file = None
                    file_size = None
                    try:
                        # Try to find the downloaded file by checking common extensions
                        base_path = os.path.join(
                            self.download_directory, safe_title
                        )
                        for ext in ["mp3", "mp4", "webm", "m4a", "opus"]:
                            test_path = f"{base_path}.{ext}"
                            if os.path.exists(test_path):
                                downloaded_file = test_path
                                file_size = os.path.getsize(test_path)
                                break
                    except Exception as file_exc:
                        logger.debug(
                            f"Could not determine downloaded file path: "
                            f"{file_exc}"
                        )
                    
                    # Emit history signal
                    self.history_added.emit(
                        title, url, format_id,
                        downloaded_file or "",
                        file_size
                    )
                except (yt_dlp.utils.DownloadError, 
                        yt_dlp.utils.ExtractorError,
                        OSError,
                        IOError) as exc:
                    error_msg = f"Download failed ({title}): {exc}"
                    logger.error(error_msg, exc_info=True)
                    self.download_failed.emit(error_msg)
                except Exception as exc:  # noqa: BLE001
                    # Catch-all for unexpected errors
                    error_msg = f"Unexpected error downloading {title}: {exc}"
                    logger.error(error_msg, exc_info=True)
                    self.download_failed.emit(error_msg)

    def progress_hook(self, data: dict) -> None:
        """Handle download progress updates from yt-dlp.
        
        Args:
            data: Progress data dictionary from yt-dlp
        """
        status = data.get("status")
        if status == "downloading":
            title = os.path.splitext(os.path.basename(data.get("filename", "")))[0]
            if len(title) > 14:
                title = title[:14] + "..."
            percent_complete = float(data.get("_percent_str", "0%").replace("%", ""))
            
            # Extract speed and ETA
            speed_str = data.get("_speed_str", "N/A")
            eta_str = data.get("_eta_str", "N/A")
            
            # Emit overall progress (for backward compatibility)
            self.updated_progress.emit(percent_complete)
            
            # Emit individual item progress
            if self.current_row >= 0:
                self.item_progress.emit(self.current_row, percent_complete, speed_str, eta_str)
            
            self.updated_status.emit(
                f"Downloading {title}: {data.get('_percent_str', '')} {data.get('_eta_str', '')}"
            )
        elif status == "finished":
            title = os.path.splitext(os.path.basename(data.get("filename", "")))[0]
            if len(title) > 14:
                title = title[:14] + "..."
            self.updated_status.emit(f"Finished downloading {title}")
            # Emit completion for current row
            if self.current_row >= 0:
                self.item_completed.emit(self.current_row)
        elif status == "error":
            title = os.path.splitext(os.path.basename(data.get("filename", "")))[0]
            if len(title) > 14:
                title = title[:14] + "..."
            self.download_failed.emit(f"Error downloading {title}")

