from PyQt5.QtWidgets import QTableWidget, QComboBox

from Nobody.models.settings import AppSettings
from Nobody.views.video_table import VideoTableManager


class DummyHost:
    def __init__(self):
        self.app_settings = AppSettings()


def test_filter_formats_respects_settings(qt_app):
    host = DummyHost()
    table = QTableWidget()
    manager = VideoTableManager(host, table)

    formats = [
        ("[Video] MP4 1920x1080 60fps - 50MB", "video/mp4", "Video", 50),
        ("[Video-only] WEBM 1920x1080 30fps - 40MB", "video/webm", "Video-only", 40),
        ("[Audio-only] MP3 bestaudio - 10MB", "bestaudio/best", "Audio-only", 10),
    ]

    host.app_settings.show_video_formats = False
    filtered = manager._filter_formats(formats)
    assert all(item[2] != "Video" and item[2] != "Video-only" for item in filtered)

    host.app_settings.show_video_formats = True
    host.app_settings.max_quality = 480
    filtered = manager._filter_formats(formats)
    assert all("480" in item[0] or item[2] == "Audio-only" for item in filtered)


def test_select_default_format_prefers_app_setting(qt_app):
    host = DummyHost()
    table = QTableWidget()
    manager = VideoTableManager(host, table)

    combo = QComboBox()
    combo.addItem("--- Audio-only ---")
    combo.model().item(0).setEnabled(False)
    combo.addItem("[Audio-only] MP3 bestaudio - 10MB", userData="bestaudio/best")
    combo.addItem("[Audio-only] M4A bestaudio - 12MB", userData="bestaudio/m4a")

    host.app_settings.default_format = "mp3"
    manager._select_default_format(combo)

    assert combo.currentData() == "bestaudio/best"
