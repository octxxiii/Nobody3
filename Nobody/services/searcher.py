"""비디오 검색 서비스"""

import yt_dlp
from PyQt5.QtCore import QThread, pyqtSignal
from ..utils.logging import logger


class Searcher(QThread):
    """비디오 정보 검색 스레드"""
    updated_list = pyqtSignal(str, str, str, list)  # title, thumbnail_url, video_url, [(display_text, format_id, type_label, filesize)]
    search_progress = pyqtSignal(int, int)  # Signal with two arguments: current progress and total count

    def __init__(self, url, parent=None):
        super().__init__(parent)
        self.url = url

    def run(self):
        # extract_flat 옵션을 제거하거나 False로 설정하여 전체 포맷 정보를 가져옵니다.
        ydl_opts = {
            'quiet': True,
            'no_warnings': True, # WARNING 메시지 숨김으로 속도 향상
            'skip_download': True,
            'ignoreerrors': True, # 일부 오류 무시
            'ignore_no_formats_error': True, # 포맷 없는 오류 무시
            'extract_flat': False, # 전체 포맷 정보 가져오기
            'format': 'best[height<=480]/best[height<=720]/best', # 480p 우선, 없으면 720p, 최후에 best
            'socket_timeout': 10, # 타임아웃 설정
            'retries': 2, # 재시도 횟수 제한
            'fragment_retries': 2, # 프래그먼트 재시도 제한
            'concurrent_fragment_downloads': 1, # 동시 다운로드 제한
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                result = ydl.extract_info(self.url, download=False)
                if result is None:
                    logger.debug("yt_dlp result is None.")
                    self.updated_list.emit("Video/Playlist not found", "", self.url, [])
                    return
                    
                videos = result.get('entries', [result])
                if not videos:
                    logger.debug("No videos/entries found in yt_dlp result.")
                    self.updated_list.emit(result.get('title', 'Video/Playlist not found'), "", self.url, [])
                    return

                for video_index, video in enumerate(videos):
                    if video is None:
                        logger.debug(f"Video {video_index + 1} is None, skipping.")
                        continue
                        
                    raw_formats = video.get('formats', [])
                    processed_format_list = []

                    if not raw_formats:
                        logger.debug(f"Video {video_index + 1} ('{video.get('title', 'N/A')}') has no raw formats from yt_dlp.")

                    # 최고 품질 오디오 포맷 찾기 (MP3 변환용)
                    best_audio = None
                    best_audio_bitrate = 0
                    
                    for f_index, f in enumerate(raw_formats):
                        if f is None:
                            continue
                            
                        format_id = f.get('format_id')
                        ext = f.get('ext')

                        if not format_id or not ext or 'storyboard' in format_id.lower():
                            continue

                        # filesize가 없더라도 0으로 처리하여 포함. N/A 표시는 display_text에서.
                        filesize = f.get('filesize') or f.get('filesize_approx') or 0

                        type_label = 'Unknown'
                        quality_desc = []

                        vcodec = f.get('vcodec', 'none')
                        acodec = f.get('acodec', 'none')

                        # 최고 품질 오디오 포맷 추적
                        abr = f.get('abr') or 0
                        if acodec != 'none' and abr > best_audio_bitrate:
                            best_audio = f
                            best_audio_bitrate = abr

                        # 타입 결정 로직 개선
                        if vcodec != 'none' and acodec != 'none':
                            type_label = 'Video' # Muxed (Video+Audio)
                            if f.get('width') and f.get('height'): quality_desc.append(f"{f.get('width')}x{f.get('height')}")
                            if f.get('fps'): quality_desc.append(f"{f.get('fps')}fps")
                            # 비디오 비트레이트나 오디오 비트레이트 중 하나라도 표시
                            if f.get('vbr'): quality_desc.append(f"V:{round(f.get('vbr'))}k")
                            elif f.get('abr'): quality_desc.append(f"A:{round(f.get('abr'))}k")
                        elif vcodec != 'none':
                            type_label = 'Video-only'
                            if f.get('width') and f.get('height'): quality_desc.append(f"{f.get('width')}x{f.get('height')}")
                            if f.get('fps'): quality_desc.append(f"{f.get('fps')}fps")
                            if f.get('vbr'): quality_desc.append(f"V:{round(f.get('vbr'))}k")
                        elif acodec != 'none':
                            type_label = 'Audio-only'
                            if f.get('abr'): quality_desc.append(f"A:{round(f.get('abr'))}k")
                        # Unknown 타입은 필터링하지 않고, 정보가 부족하면 그대로 표시
                        
                        quality_str = ' / '.join(filter(None, quality_desc))
                        filesize_mb_str = f"{(filesize // 1024 // 1024)}MB" if filesize > 0 else "N/A"

                        display_text = f"[{type_label}] {ext.upper()} {format_id} ({quality_str if quality_str else 'data'}) - {filesize_mb_str}"
                        
                        processed_format_list.append((display_text, format_id, type_label, filesize))
                    
                    # MP3 변환 옵션 추가
                    if best_audio:
                        # 추정 파일 크기 계산
                        estimated_size = best_audio.get('filesize', 0)
                        if estimated_size > 0:
                            estimated_size_mb = f"{estimated_size // 1024 // 1024}MB"
                        else:
                            # 파일 크기를 모르는 경우 비트레이트로 추정
                            duration = video.get('duration', 0)
                            if duration and best_audio_bitrate:
                                estimated_size = int(duration * best_audio_bitrate * 1000 / 8)  # bytes
                                estimated_size_mb = f"~{estimated_size // 1024 // 1024}MB"
                            else:
                                estimated_size_mb = "N/A"
                        
                        # MP3 옵션 추가
                        mp3_quality = f"A:{round(min(320, best_audio_bitrate))}k"  # 최대 320kbps
                        mp3_display_text = f"[Audio-only] MP3 bestaudio (MP3 Conversion / {mp3_quality}) - {estimated_size_mb}"
                        processed_format_list.append((mp3_display_text, "bestaudio/best", "Audio-only", estimated_size))
                    
                    if not processed_format_list and raw_formats:
                        logger.warning(f"Video {video_index + 1} ('{video.get('title', 'N/A')}') - all formats were filtered out.")
                    
                    processed_format_list.sort(key=lambda x: (x[2] != 'Audio-only', x[2] != 'Video', x[2] != 'Video-only', -x[3]))

                    self.updated_list.emit(
                        video.get('title', 'No title'),
                        video.get('thumbnail', ''),
                        video.get('webpage_url', ''),
                        processed_format_list
                    )
            except Exception as e:
                logger.error(f"Searcher thread 오류: {str(e)}", exc_info=True)
                self.updated_list.emit(f"Error: {str(e)}", "", self.url, []) # 에러 발생 시 빈 리스트와 함께 에러 메시지 전달

    def estimate_total_count(self, result):
        if 'entries' in result:
            # If it's a playlist, estimate the total count based on the number of entries
            return len(result['entries'])
        else:
            # If it's a single video, return 1 as the total count
            return 1

