"""Application settings persistence helpers."""

import os
import json
from ..utils.cache import resolve_writable_cache_dir
from ..utils.logging import logger


class AppSettings:
    """Manage user preferences for the application."""

    def __init__(self):
        self.default_format = "mp3"  # default download format
        self.show_video_formats = True  # include mixed video+audio formats
        self.show_audio_formats = True  # include audio formats
        self.show_audio_only = True  # include audio-only variants
        self.max_quality = 720  # highest allowed resolution (0 = unlimited)

    def get_settings_file_path(self):
        """Return the filesystem path for the JSON settings file."""
        cache_dir = resolve_writable_cache_dir("Nobody 3")
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir, exist_ok=True)
        return os.path.join(cache_dir, "settings.json")

    def save_settings(self):
        """Serialize current preferences to disk."""
        settings = {
            "default_format": self.default_format,
            "show_video_formats": self.show_video_formats,
            "show_audio_formats": self.show_audio_formats,
            "show_audio_only": self.show_audio_only,
            "max_quality": self.max_quality,
        }
        try:
            settings_file = self.get_settings_file_path()
            with open(settings_file, "w", encoding="utf-8") as f:
                json.dump(settings, f, ensure_ascii=False, indent=2)
            logger.info("Saved settings: %s", settings_file)
        except Exception as e:  # pragma: no cover - defensive logging
            logger.error("Failed to save settings: %s", e)

    def load_settings(self):
        """Load preferences from disk if available."""
        try:
            settings_file = self.get_settings_file_path()
            if os.path.exists(settings_file):
                with open(settings_file, "r", encoding="utf-8") as f:
                    settings = json.load(f)
                    self.default_format = settings.get("default_format", "mp3")
                    self.show_video_formats = settings.get("show_video_formats", True)
                    self.show_audio_formats = settings.get("show_audio_formats", True)
                    self.show_audio_only = settings.get("show_audio_only", True)
                    self.max_quality = settings.get("max_quality", 720)
                logger.info("Loaded settings: %s", settings_file)
            else:
                logger.info("No settings file found; using defaults (%s)", settings_file)
        except Exception as e:  # pragma: no cover - defensive logging
            logger.error("Failed to load settings: %s", e)

