"""비디오 다운로드 서비스"""

import os
import yt_dlp
from PyQt5.QtCore import QThread, pyqtSignal
from ..utils.ffmpeg import find_ffmpeg_executable
from ..utils.logging import logger


class Downloader(QThread):
    """비디오 다운로드 스레드"""
    updated_status = pyqtSignal(str)
    download_failed = pyqtSignal(str)
    updated_progress = pyqtSignal(float)  # Signal to update progress bar

    def __init__(self, videos, download_directory):
        super().__init__()
        self.videos = videos
        self.download_directory = download_directory

    def run(self):
        for title, url, format_id in self.videos:
            safe_title = title.replace("/", "_").replace("\\", "_")
            
            # MP3 변환이 필요한지 확인
            is_mp3_conversion = format_id == "bestaudio/best" or "MP3" in title
            
            # FFmpeg 경로 자동 탐지 (다운로드된 경로 우선 사용)
            ffmpeg_path = find_ffmpeg_executable()
            
            # 다운로드된 ffmpeg 경로 확인 및 로깅
            if ffmpeg_path != 'ffmpeg' and os.path.exists(ffmpeg_path):
                logger.info(f"FFmpeg 사용 중인 경로: {ffmpeg_path}")
            else:
                logger.warning(f"FFmpeg 시스템 PATH에서 찾는 중 (경로: {ffmpeg_path})")
            
            download_options = {
                'format': format_id,
                'outtmpl': os.path.join(self.download_directory, f"{safe_title}.%(ext)s"),
                'progress_hooks': [self.progress_hook],
                'nocheckcertificate': True,
                'prefer_insecure': True,
                'geo_bypass': True,
                'geo_verification_proxy': None,
                'socket_timeout': 30,
                'retries': 10,
                'fragment_retries': 10,
                'file_access_retries': 10,
                'extractor_retries': 10,
                'ignoreerrors': True,
                'no_color': True,
                'logtostderr': True,
                'verbose': True,
                'ffmpeg_location': ffmpeg_path,  # 다운로드된 절대 경로 또는 'ffmpeg' (시스템 PATH)
            }
            
            # MP3 변환 또는 일반 비디오 변환 설정
            if is_mp3_conversion:
                download_options['postprocessors'] = [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '320',  # 최대 320kbps
                }]
            else:
                download_options['postprocessors'] = [{
                    'key': 'FFmpegVideoConvertor',
                    'preferredformat': 'mp4',  # 오타 수정: preferedformat -> preferredformat
                }]
                download_options['merge_output_format'] = 'mp4'
                download_options['postprocessor_args'] = [
                    '-c:v', 'copy',
                    '-c:a', 'copy'
                ]

            with yt_dlp.YoutubeDL(download_options) as ydl:
                try:
                    self.updated_status.emit(f"다운로드 시작: {title}")
                    ydl.download([url])
                    self.updated_status.emit(f"다운로드 완료: {title}")
                except Exception as e:
                    error_msg = f"다운로드 실패 ({title}): {str(e)}"
                    logger.error(error_msg)
                    self.download_failed.emit(error_msg)

    def progress_hook(self, d):
        if d['status'] == 'downloading':
            # Trim the title to 14 characters and append "..." if it exceeds this limit
            title = os.path.splitext(os.path.basename(d['filename']))[0]
            if len(title) > 14:
                title = title[:14] + "..."
            # Extract the percentage and convert to a float
            percent_complete = float(d['_percent_str'].replace('%', ''))
            # Emit signal to update the progress bar (make sure this signal is connected to the actual progress bar update method)
            self.updated_progress.emit(percent_complete)
            # Emit status update with trimmed title and current download percentage
            self.updated_status.emit(f"Downloading {title}: {d['_percent_str']} {d['_eta_str']}")
        elif d['status'] == 'finished':
            # Repeat the trimming process for consistency in status updates
            title = os.path.splitext(os.path.basename(d['filename']))[0]
            if len(title) > 14:
                title = title[:14] + "..."
            self.updated_status.emit(f"Finished downloading {title}")
        elif d['status'] == 'error':
            # And again for error messages
            title = os.path.splitext(os.path.basename(d['filename']))[0]
            if len(title) > 14:
                title = title[:14] + "..."
            self.download_failed.emit(f"Error downloading {title}")

