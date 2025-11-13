"""애플리케이션 설정 모델"""

import os
import json
from ..utils.cache import resolve_writable_cache_dir
from ..utils.logging import logger


class AppSettings:
    """애플리케이션 설정 관리 클래스"""
    def __init__(self):
        self.default_format = "mp3"  # 기본 포맷
        self.show_video_formats = True  # 비디오 포맷 표시
        self.show_audio_formats = True  # 오디오 포맷 표시
        self.show_audio_only = True  # 오디오 전용 포맷 표시
        self.max_quality = 720  # 최대 품질 (480, 720, 1080, 0=무제한)
        
    def get_settings_file_path(self):
        """설정 파일 경로 반환"""
        cache_dir = resolve_writable_cache_dir("OctXXIII")
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir, exist_ok=True)
        return os.path.join(cache_dir, 'settings.json')
    
    def save_settings(self):
        """설정을 파일에 저장"""
        settings = {
            'default_format': self.default_format,
            'show_video_formats': self.show_video_formats,
            'show_audio_formats': self.show_audio_formats,
            'show_audio_only': self.show_audio_only,
            'max_quality': self.max_quality
        }
        try:
            settings_file = self.get_settings_file_path()
            with open(settings_file, 'w', encoding='utf-8') as f:
                json.dump(settings, f, ensure_ascii=False, indent=2)
            logger.info(f"설정 저장 완료: {settings_file}")
        except Exception as e:
            logger.error(f"설정 저장 실패: {e}")
    
    def load_settings(self):
        """파일에서 설정 로드"""
        try:
            settings_file = self.get_settings_file_path()
            if os.path.exists(settings_file):
                with open(settings_file, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                    self.default_format = settings.get('default_format', 'mp3')
                    self.show_video_formats = settings.get('show_video_formats', True)
                    self.show_audio_formats = settings.get('show_audio_formats', True)
                    self.show_audio_only = settings.get('show_audio_only', True)
                    self.max_quality = settings.get('max_quality', 720)
                logger.info(f"설정 로드 완료: {settings_file}")
            else:
                logger.info(f"설정 파일이 없습니다. 기본값을 사용합니다: {settings_file}")
        except Exception as e:
            logger.error(f"설정 로드 실패: {e}")

