"""FFmpeg-related utilities."""

import os
import shutil
import sys
import urllib.request
import zipfile
import tempfile
from .logging import logger


def find_ffmpeg_executable() -> str:
    """Find FFmpeg executable path relative to the application."""
    if getattr(sys, "frozen", False):
        base_path = os.path.dirname(sys.executable)
    else:
        current_file = os.path.abspath(__file__)
        nobody_dir = os.path.dirname(os.path.dirname(current_file))
        base_path = os.path.dirname(nobody_dir)

    ffmpeg_name = "ffmpeg.exe" if sys.platform.startswith("win") else "ffmpeg"
    ffmpeg_path = os.path.join(base_path, ffmpeg_name)
    if os.path.exists(ffmpeg_path) and os.path.isfile(ffmpeg_path):
        return ffmpeg_path

    cwd_ffmpeg = os.path.join(os.getcwd(), ffmpeg_name)
    if os.path.exists(cwd_ffmpeg) and os.path.isfile(cwd_ffmpeg):
        return cwd_ffmpeg

    return "ffmpeg"


def check_ffmpeg_exists() -> bool:
    ffmpeg_path = find_ffmpeg_executable()
    if ffmpeg_path != "ffmpeg":
        return os.path.exists(ffmpeg_path) and os.path.isfile(ffmpeg_path)
    return shutil.which("ffmpeg") is not None


def get_ffmpeg_download_url():
    if sys.platform.startswith("win"):
        return "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip"
    if sys.platform == "darwin":
        return "https://evermeet.cx/ffmpeg/getrelease/zip"
    return None


def download_ffmpeg_quietly(base_path: str) -> bool:
    """Download FFmpeg quietly in the background."""
    try:
        if sys.platform.startswith("win"):
            url = "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip"
            temp_zip = os.path.join(tempfile.gettempdir(), "ffmpeg_download.zip")

            urllib.request.urlretrieve(url, temp_zip)

            temp_extract = os.path.join(tempfile.gettempdir(), "ffmpeg_extract")
            os.makedirs(temp_extract, exist_ok=True)

            with zipfile.ZipFile(temp_zip, "r") as zip_ref:
                zip_ref.extractall(temp_extract)

            for root, _, files in os.walk(temp_extract):
                for file in files:
                    if file == "ffmpeg.exe":
                        shutil.copy2(os.path.join(root, file), os.path.join(base_path, "ffmpeg.exe"))
                    elif file == "ffprobe.exe":
                        shutil.copy2(os.path.join(root, file), os.path.join(base_path, "ffprobe.exe"))

            os.remove(temp_zip)
            shutil.rmtree(temp_extract, ignore_errors=True)
            return True

        if sys.platform == "darwin":
            ffmpeg_url = "https://evermeet.cx/ffmpeg/getrelease/zip"
            ffprobe_url = "https://evermeet.cx/ffmpeg/getrelease/ffprobe/zip"

            temp_dir = tempfile.gettempdir()
            ffmpeg_zip = os.path.join(temp_dir, "ffmpeg_mac.zip")
            ffprobe_zip = os.path.join(temp_dir, "ffprobe_mac.zip")

            urllib.request.urlretrieve(ffmpeg_url, ffmpeg_zip)
            urllib.request.urlretrieve(ffprobe_url, ffprobe_zip)

            temp_extract_ffmpeg = os.path.join(temp_dir, "ffmpeg_extract")
            temp_extract_ffprobe = os.path.join(temp_dir, "ffprobe_extract")
            os.makedirs(temp_extract_ffmpeg, exist_ok=True)
            os.makedirs(temp_extract_ffprobe, exist_ok=True)

            try:
                with zipfile.ZipFile(ffmpeg_zip, "r") as zip_ref:
                    zip_ref.extractall(temp_extract_ffmpeg)
                with zipfile.ZipFile(ffprobe_zip, "r") as zip_ref:
                    zip_ref.extractall(temp_extract_ffprobe)
            except zipfile.BadZipFile:
                shutil.move(ffmpeg_zip, os.path.join(temp_extract_ffmpeg, "ffmpeg"))
                shutil.move(ffprobe_zip, os.path.join(temp_extract_ffprobe, "ffprobe"))

            ffmpeg_src = None
            ffprobe_src = None

            for root, _, files in os.walk(temp_extract_ffmpeg):
                if "ffmpeg" in files:
                    ffmpeg_src = os.path.join(root, "ffmpeg")
                    break
            if not ffmpeg_src and os.path.exists(os.path.join(temp_extract_ffmpeg, "ffmpeg")):
                ffmpeg_src = os.path.join(temp_extract_ffmpeg, "ffmpeg")

            for root, _, files in os.walk(temp_extract_ffprobe):
                if "ffprobe" in files:
                    ffprobe_src = os.path.join(root, "ffprobe")
                    break
            if not ffprobe_src and os.path.exists(os.path.join(temp_extract_ffprobe, "ffprobe")):
                ffprobe_src = os.path.join(temp_extract_ffprobe, "ffprobe")

            ffmpeg_dst = os.path.join(base_path, "ffmpeg")
            ffprobe_dst = os.path.join(base_path, "ffprobe")

            if ffmpeg_src and os.path.exists(ffmpeg_src):
                shutil.move(ffmpeg_src, ffmpeg_dst)
                os.chmod(ffmpeg_dst, 0o755)
            if ffprobe_src and os.path.exists(ffprobe_src):
                shutil.move(ffprobe_src, ffprobe_dst)
                os.chmod(ffprobe_dst, 0o755)

            if os.path.exists(ffmpeg_zip):
                os.remove(ffmpeg_zip)
            if os.path.exists(ffprobe_zip):
                os.remove(ffprobe_zip)
            shutil.rmtree(temp_extract_ffmpeg, ignore_errors=True)
            shutil.rmtree(temp_extract_ffprobe, ignore_errors=True)
            return True

        # Linux: ask the user to install FFmpeg manually
        return False

    except Exception as exc:  # noqa: BLE001
        logger.warning("FFmpeg download failed: %s", exc)
        return False

