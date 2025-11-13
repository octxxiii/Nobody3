"""FFmpeg 관련 유틸리티"""

import os
import shutil
import sys
import urllib.request
import zipfile
import tempfile
from .logging import logger


def find_ffmpeg_executable() -> str:
    """Find FFmpeg executable path relative to the application.
    
    Checks in the following order:
    1. Same directory as the executable (for frozen/packaged apps)
    2. Current working directory
    3. System PATH
    
    Returns the path to ffmpeg executable or 'ffmpeg' if not found.
    """
    # Get the directory where the executable is located
    if getattr(sys, 'frozen', False):
        # Running as a compiled executable
        base_path = os.path.dirname(sys.executable)
    else:
        # Running as a script
        # 프로젝트 루트 (Nobody3 디렉터리) 찾기
        # Nobody/utils/ffmpeg.py -> Nobody -> Nobody3
        current_file = os.path.abspath(__file__)
        nobody_dir = os.path.dirname(os.path.dirname(current_file))  # Nobody/
        base_path = os.path.dirname(nobody_dir)  # Nobody3/ (프로젝트 루트)
    
    # Check for ffmpeg in the executable directory
    if sys.platform.startswith("win"):
        ffmpeg_name = "ffmpeg.exe"
    else:
        ffmpeg_name = "ffmpeg"
    
    # Try executable directory first
    ffmpeg_path = os.path.join(base_path, ffmpeg_name)
    if os.path.exists(ffmpeg_path) and os.path.isfile(ffmpeg_path):
        return ffmpeg_path
    
    # Try current working directory
    cwd_ffmpeg = os.path.join(os.getcwd(), ffmpeg_name)
    if os.path.exists(cwd_ffmpeg) and os.path.isfile(cwd_ffmpeg):
        return cwd_ffmpeg
    
    # Fall back to system PATH (just return 'ffmpeg')
    return 'ffmpeg'


def check_ffmpeg_exists() -> bool:
    """Check if FFmpeg executable exists in the application directory.
    
    Returns True if ffmpeg is found, False otherwise.
    """
    ffmpeg_path = find_ffmpeg_executable()
    # If it returns a path (not just 'ffmpeg'), check if it exists
    if ffmpeg_path != 'ffmpeg':
        return os.path.exists(ffmpeg_path) and os.path.isfile(ffmpeg_path)
    # If it's just 'ffmpeg', check system PATH
    return shutil.which('ffmpeg') is not None


def get_ffmpeg_download_url():
    """Get FFmpeg download URL based on platform."""
    if sys.platform.startswith("win"):
        return "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip"
    elif sys.platform == "darwin":
        # macOS uses the same URL for both architectures
        return "https://evermeet.cx/ffmpeg/getrelease/zip"
    else:
        # Linux - return None for now, user should install via package manager
        return None


def download_ffmpeg_quietly(base_path: str) -> bool:
    """Download FFmpeg quietly in the background.
    
    Args:
        base_path: Directory where the executable is located
        
    Returns:
        True if download and extraction succeeded, False otherwise
    """
    try:
        if sys.platform.startswith("win"):
            # Windows: Download from GitHub releases
            url = "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip"
            temp_zip = os.path.join(tempfile.gettempdir(), "ffmpeg_download.zip")
            
            # Download with progress callback (but don't show it)
            def reporthook(blocknum, blocksize, totalsize):
                # Silent download - no output
                pass
            
            urllib.request.urlretrieve(url, temp_zip, reporthook)
            
            # Extract to temp directory
            temp_extract = os.path.join(tempfile.gettempdir(), "ffmpeg_extract")
            os.makedirs(temp_extract, exist_ok=True)
            
            with zipfile.ZipFile(temp_zip, 'r') as zip_ref:
                zip_ref.extractall(temp_extract)
            
            # Find ffmpeg.exe and ffprobe.exe in extracted files
            for root, dirs, files in os.walk(temp_extract):
                for file in files:
                    if file == "ffmpeg.exe":
                        src = os.path.join(root, file)
                        dst = os.path.join(base_path, "ffmpeg.exe")
                        shutil.copy2(src, dst)
                    elif file == "ffprobe.exe":
                        src = os.path.join(root, file)
                        dst = os.path.join(base_path, "ffprobe.exe")
                        shutil.copy2(src, dst)
            
            # Cleanup
            os.remove(temp_zip)
            shutil.rmtree(temp_extract, ignore_errors=True)
            return True
            
        elif sys.platform == "darwin":
            # macOS: Download from evermeet.cx
            # evermeet.cx provides zip files that contain the binaries
            ffmpeg_url = "https://evermeet.cx/ffmpeg/getrelease/zip"
            ffprobe_url = "https://evermeet.cx/ffmpeg/getrelease/ffprobe/zip"
            
            temp_dir = tempfile.gettempdir()
            ffmpeg_zip = os.path.join(temp_dir, "ffmpeg_mac.zip")
            ffprobe_zip = os.path.join(temp_dir, "ffprobe_mac.zip")
            
            # Download both
            urllib.request.urlretrieve(ffmpeg_url, ffmpeg_zip)
            urllib.request.urlretrieve(ffprobe_url, ffprobe_zip)
            
            # Extract
            temp_extract_ffmpeg = os.path.join(temp_dir, "ffmpeg_extract")
            temp_extract_ffprobe = os.path.join(temp_dir, "ffprobe_extract")
            os.makedirs(temp_extract_ffmpeg, exist_ok=True)
            os.makedirs(temp_extract_ffprobe, exist_ok=True)
            
            # Extract zip files
            try:
                with zipfile.ZipFile(ffmpeg_zip, 'r') as zip_ref:
                    zip_ref.extractall(temp_extract_ffmpeg)
                with zipfile.ZipFile(ffprobe_zip, 'r') as zip_ref:
                    zip_ref.extractall(temp_extract_ffprobe)
            except zipfile.BadZipFile:
                # If not a zip file, try as direct binary download
                shutil.move(ffmpeg_zip, os.path.join(temp_extract_ffmpeg, "ffmpeg"))
                shutil.move(ffprobe_zip, os.path.join(temp_extract_ffprobe, "ffprobe"))
            
            # Find and move binaries (handle both zip extraction and direct download)
            ffmpeg_src = None
            ffprobe_src = None
            
            # Look for ffmpeg binary
            for root, dirs, files in os.walk(temp_extract_ffmpeg):
                if "ffmpeg" in files and not files[files.index("ffmpeg")].endswith('.zip'):
                    ffmpeg_src = os.path.join(root, "ffmpeg")
                    break
            if not ffmpeg_src and os.path.exists(os.path.join(temp_extract_ffmpeg, "ffmpeg")):
                ffmpeg_src = os.path.join(temp_extract_ffmpeg, "ffmpeg")
            
            # Look for ffprobe binary
            for root, dirs, files in os.walk(temp_extract_ffprobe):
                if "ffprobe" in files and not files[files.index("ffprobe")].endswith('.zip'):
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
            
            # Cleanup
            if os.path.exists(ffmpeg_zip):
                os.remove(ffmpeg_zip)
            if os.path.exists(ffprobe_zip):
                os.remove(ffprobe_zip)
            shutil.rmtree(temp_extract_ffmpeg, ignore_errors=True)
            shutil.rmtree(temp_extract_ffprobe, ignore_errors=True)
            return True
            
        else:
            # Linux - not supported for auto-download
            return False
            
    except Exception as e:
        # Silent failure - just return False
        logger.warning(f"FFmpeg 다운로드 실패: {e}")
        return False

