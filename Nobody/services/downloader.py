"""Background downloader thread using yt_dlp."""

import os
import yt_dlp
from PyQt5.QtCore import QThread, pyqtSignal

from ..utils.ffmpeg import find_ffmpeg_executable
from ..utils.logging import logger


class Downloader(QThread):
    """Download videos and emit progress/status updates."""

    updated_status = pyqtSignal(str)
    download_failed = pyqtSignal(str)
    updated_progress = pyqtSignal(float)

    def __init__(self, videos, download_directory):
        super().__init__()
        self.videos = videos
        self.download_directory = download_directory

    def run(self):
        for title, url, format_id in self.videos:
            safe_title = title.replace("/", "_").replace("\\", "_")
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
                download_options["merge_output_format"] = "mp4"

            with yt_dlp.YoutubeDL(download_options) as ydl:
                try:
                    self.updated_status.emit(f"Starting download: {title}")
                    ydl.download([url])
                    self.updated_status.emit(f"Download complete: {title}")
                except Exception as exc:  # noqa: BLE001
                    error_msg = f"Download failed ({title}): {exc}"
                    logger.error(error_msg)
                    self.download_failed.emit(error_msg)

    def progress_hook(self, data):
        status = data.get("status")
        if status == "downloading":
            title = os.path.splitext(os.path.basename(data.get("filename", "")))[0]
            if len(title) > 14:
                title = title[:14] + "..."
            percent_complete = float(data.get("_percent_str", "0%" ).replace("%", ""))
            self.updated_progress.emit(percent_complete)
            self.updated_status.emit(
                f"Downloading {title}: {data.get('_percent_str', '')} {data.get('_eta_str', '')}"
            )
        elif status == "finished":
            title = os.path.splitext(os.path.basename(data.get("filename", "")))[0]
            if len(title) > 14:
                title = title[:14] + "..."
            self.updated_status.emit(f"Finished downloading {title}")
        elif status == "error":
            title = os.path.splitext(os.path.basename(data.get("filename", "")))[0]
            if len(title) > 14:
                title = title[:14] + "..."
            self.download_failed.emit(f"Error downloading {title}")

