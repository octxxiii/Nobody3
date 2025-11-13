"""Background search thread for retrieving video metadata."""

import yt_dlp
from PyQt5.QtCore import QThread, pyqtSignal

from ..utils.logging import logger


class Searcher(QThread):
    """Fetch metadata and available formats via yt_dlp."""

    updated_list = pyqtSignal(str, str, str, list)
    search_progress = pyqtSignal(int, int)

    def __init__(self, url, parent=None):
        super().__init__(parent)
        self.url = url

    def run(self):
        options = {
            "quiet": True,
            "no_warnings": True,
            "skip_download": True,
            "ignoreerrors": True,
            "ignore_no_formats_error": True,
            "extract_flat": False,
            "format": "best[height<=480]/best[height<=720]/best",
            "socket_timeout": 10,
            "retries": 2,
            "fragment_retries": 2,
            "concurrent_fragment_downloads": 1,
        }
        with yt_dlp.YoutubeDL(options) as ydl:
            try:
                result = ydl.extract_info(self.url, download=False)
                if result is None:
                    logger.debug("yt_dlp result is None.")
                    self.updated_list.emit("Video/Playlist not found", "", self.url, [])
                    return

                videos = result.get("entries", [result])
                if not videos:
                    logger.debug("No videos/entries found in yt_dlp result.")
                    self.updated_list.emit(result.get("title", "Video/Playlist not found"), "", self.url, [])
                    return

                for index, video in enumerate(videos):
                    if video is None:
                        logger.debug("Video %s is None, skipping.", index + 1)
                        continue

                    raw_formats = video.get("formats", [])
                    processed = []

                    if not raw_formats:
                        logger.debug("Video %s has no raw formats from yt_dlp.", index + 1)

                    best_audio = None
                    best_audio_bitrate = 0

                    for fmt in raw_formats:
                        if not fmt:
                            continue

                        format_id = fmt.get("format_id")
                        ext = fmt.get("ext")
                        if not format_id or not ext or "storyboard" in format_id.lower():
                            continue

                        filesize = fmt.get("filesize") or fmt.get("filesize_approx") or 0
                        type_label = "Unknown"
                        quality_desc: list[str] = []

                        vcodec = fmt.get("vcodec", "none")
                        acodec = fmt.get("acodec", "none")

                        abr = fmt.get("abr") or 0
                        if acodec != "none" and abr > best_audio_bitrate:
                            best_audio = fmt
                            best_audio_bitrate = abr

                        if vcodec != "none" and acodec != "none":
                            type_label = "Video"
                            if fmt.get("width") and fmt.get("height"):
                                quality_desc.append(f"{fmt.get('width')}x{fmt.get('height')}")
                            if fmt.get("fps"):
                                quality_desc.append(f"{fmt.get('fps')}fps")
                            if fmt.get("vbr"):
                                quality_desc.append(f"V:{round(fmt.get('vbr'))}k")
                            elif fmt.get("abr"):
                                quality_desc.append(f"A:{round(fmt.get('abr'))}k")
                        elif vcodec != "none":
                            type_label = "Video-only"
                            if fmt.get("width") and fmt.get("height"):
                                quality_desc.append(f"{fmt.get('width')}x{fmt.get('height')}")
                            if fmt.get("fps"):
                                quality_desc.append(f"{fmt.get('fps')}fps")
                            if fmt.get("vbr"):
                                quality_desc.append(f"V:{round(fmt.get('vbr'))}k")
                        elif acodec != "none":
                            type_label = "Audio-only"
                            if fmt.get("abr"):
                                quality_desc.append(f"A:{round(fmt.get('abr'))}k")

                        quality_str = " / ".join(filter(None, quality_desc))
                        filesize_mb = f"{filesize // 1024 // 1024}MB" if filesize > 0 else "N/A"
                        display_text = (
                            f"[{type_label}] {ext.upper()} {format_id} "
                            f"({quality_str if quality_str else 'data'}) - {filesize_mb}"
                        )
                        processed.append((display_text, format_id, type_label, filesize))

                    if best_audio:
                        estimated_size = best_audio.get("filesize", 0)
                        if estimated_size > 0:
                            estimated_size_mb = f"{estimated_size // 1024 // 1024}MB"
                        else:
                            duration = video.get("duration", 0)
                            if duration and best_audio_bitrate:
                                estimated_size = int(duration * best_audio_bitrate * 1000 / 8)
                                estimated_size_mb = f"~{estimated_size // 1024 // 1024}MB"
                            else:
                                estimated_size_mb = "N/A"

                        mp3_quality = f"A:{round(min(320, best_audio_bitrate))}k"
                        mp3_display = (
                            f"[Audio-only] MP3 bestaudio (MP3 Conversion / {mp3_quality}) - {estimated_size_mb}"
                        )
                        processed.append((mp3_display, "bestaudio/best", "Audio-only", estimated_size))

                    if not processed and raw_formats:
                        logger.warning(
                            "Video %s ('%s') - all formats were filtered out.",
                            index + 1,
                            video.get("title", "N/A"),
                        )

                    processed.sort(key=lambda x: (x[2] != "Audio-only", x[2] != "Video", x[2] != "Video-only", -x[3]))

                    self.updated_list.emit(
                        video.get("title", "No title"),
                        video.get("thumbnail", ""),
                        video.get("webpage_url", ""),
                        processed,
                    )
            except Exception as exc:  # noqa: BLE001
                logger.error("Searcher thread error: %s", exc, exc_info=True)
                self.updated_list.emit(f"Error: {exc}", "", self.url, [])

