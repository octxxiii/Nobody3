"""FFmpeg 체크 및 다운로드 서비스"""

import os
import sys
from PyQt5.QtCore import QThread, pyqtSignal
from ..utils.ffmpeg import check_ffmpeg_exists, download_ffmpeg_quietly


class FFmpegChecker(QThread):
    """백그라운드에서 FFmpeg 존재 여부를 체크하고 필요시 자동 다운로드하는 스레드"""
    check_complete = pyqtSignal(bool, str)  # (success, message)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.base_path = None
        
    def run(self):
        """FFmpeg 체크 및 다운로드 실행"""
        try:
            # Get the directory where the executable is located
            if getattr(sys, 'frozen', False):
                # Running as a compiled executable
                self.base_path = os.path.dirname(sys.executable)
            else:
                # Running as a script
                # 프로젝트 루트 (Nobody3 디렉터리) 찾기
                # Nobody/services/ffmpeg_checker.py -> Nobody -> Nobody3
                current_file = os.path.abspath(__file__)
                nobody_dir = os.path.dirname(os.path.dirname(current_file))  # Nobody/
                self.base_path = os.path.dirname(nobody_dir)  # Nobody3/ (프로젝트 루트)
            
            # Check if ffmpeg already exists
            if check_ffmpeg_exists():
                self.check_complete.emit(True, "FFmpeg가 이미 설치되어 있습니다.")
                return
            
            # FFmpeg not found, try to download
            if sys.platform.startswith("linux"):
                # Linux는 자동 다운로드 지원 안 함
                self.check_complete.emit(False, "Linux에서는 FFmpeg를 수동으로 설치해주세요.")
                return
            
            # Download FFmpeg quietly
            success = download_ffmpeg_quietly(self.base_path)
            
            if success:
                # Verify the download
                if check_ffmpeg_exists():
                    self.check_complete.emit(True, "FFmpeg가 자동으로 다운로드되었습니다.")
                else:
                    self.check_complete.emit(False, "FFmpeg 다운로드 후 검증 실패")
            else:
                self.check_complete.emit(False, "FFmpeg 자동 다운로드 실패")
                
        except Exception as e:
            self.check_complete.emit(False, f"FFmpeg 체크 중 오류: {str(e)}")

