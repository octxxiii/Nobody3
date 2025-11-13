#!/usr/bin/env python3
"""
macOS????ë²ˆë“¤ ë°?DMG ?¤ì¹˜ ?Œì¼ ë¹Œë“œ ?¤í¬ë¦½íŠ¸
"""

import os
import sys
import subprocess
import urllib.request
import tarfile
import shutil
from pathlib import Path
import platform

def download_ffmpeg_macos():
    """macOS??FFmpeg ?¤ìš´ë¡œë“œ ë°??¤ì¹˜"""
    print("macOS??FFmpeg ?¤ìš´ë¡œë“œ ì¤?..")
    
    # Apple Silicon vs Intel ?•ì¸
    arch = platform.machine()
    if arch == "arm64":
        ffmpeg_url = "https://evermeet.cx/ffmpeg/getrelease/zip"
        ffprobe_url = "https://evermeet.cx/ffmpeg/getrelease/ffprobe/zip"
    else:
        ffmpeg_url = "https://evermeet.cx/ffmpeg/getrelease/zip"
        ffprobe_url = "https://evermeet.cx/ffmpeg/getrelease/ffprobe/zip"
    
    ffmpeg_dir = Path("ffmpeg/macos")
    ffmpeg_dir.mkdir(parents=True, exist_ok=True)
    
    # FFmpeg ?¤ìš´ë¡œë“œ
    print("FFmpeg ë°”ì´?ˆë¦¬ ?¤ìš´ë¡œë“œ ì¤?..")
    urllib.request.urlretrieve(ffmpeg_url, "ffmpeg.zip")
    urllib.request.urlretrieve(ffprobe_url, "ffprobe.zip")
    
    # ?•ì¶• ?´ì œ
    import zipfile
    with zipfile.ZipFile("ffmpeg.zip", 'r') as zip_ref:
        zip_ref.extractall("temp_ffmpeg")
    with zipfile.ZipFile("ffprobe.zip", 'r') as zip_ref:
        zip_ref.extractall("temp_ffprobe")
    
    # ë°”ì´?ˆë¦¬ ë³µì‚¬
    shutil.move("temp_ffmpeg/ffmpeg", ffmpeg_dir / "ffmpeg")
    shutil.move("temp_ffprobe/ffprobe", ffmpeg_dir / "ffprobe")
    
    # ?¤í–‰ ê¶Œí•œ ë¶€??
    os.chmod(ffmpeg_dir / "ffmpeg", 0o755)
    os.chmod(ffmpeg_dir / "ffprobe", 0o755)
    
    # ?„ì‹œ ?Œì¼ ?•ë¦¬
    os.remove("ffmpeg.zip")
    os.remove("ffprobe.zip")
    shutil.rmtree("temp_ffmpeg")
    shutil.rmtree("temp_ffprobe")
    
    print("FFmpeg ?¤ìš´ë¡œë“œ ?„ë£Œ!")

def install_dependencies():
    """?„ìš”???¨í‚¤ì§€ ?¤ì¹˜"""
    print("?˜ì¡´???¨í‚¤ì§€ ?¤ì¹˜ ì¤?..")
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    subprocess.run([sys.executable, "-m", "pip", "install", "cx_Freeze"])
    subprocess.run([sys.executable, "-m", "pip", "install", "dmgbuild"])

def build_executable():
    """?¤í–‰ ?Œì¼ ë¹Œë“œ"""
    print("?¤í–‰ ?Œì¼ ë¹Œë“œ ì¤?..")
    subprocess.run([sys.executable, "setup.py", "build"])

def create_app_bundle():
    """macOS ??ë²ˆë“¤ ?ì„±"""
    print("??ë²ˆë“¤ ?ì„± ì¤?..")
    
    app_name = "Nobody 3.app"
    build_dir = Path("build")
    
    # ë¹Œë“œ???¤í–‰ ?Œì¼ ì°¾ê¸°
    exe_dirs = list(build_dir.glob("exe.*"))
    if not exe_dirs:
        raise Exception("ë¹Œë“œ???¤í–‰ ?Œì¼??ì°¾ì„ ???†ìŠµ?ˆë‹¤.")
    
    exe_dir = exe_dirs[0]
    
    # ??ë²ˆë“¤ êµ¬ì¡° ?ì„±
    app_dir = Path(app_name)
    contents_dir = app_dir / "Contents"
    macos_dir = contents_dir / "MacOS"
    resources_dir = contents_dir / "Resources"
    
    # ê¸°ì¡´ ??ë²ˆë“¤ ?œê±°
    if app_dir.exists():
        shutil.rmtree(app_dir)
    
    # ?”ë ‰? ë¦¬ ?ì„±
    macos_dir.mkdir(parents=True)
    resources_dir.mkdir(parents=True)
    
    # ?¤í–‰ ?Œì¼ ë°??¼ì´ë¸ŒëŸ¬ë¦?ë³µì‚¬
    for item in exe_dir.iterdir():
        if item.is_file():
            shutil.copy2(item, macos_dir)
        else:
            shutil.copytree(item, macos_dir / item.name)
    
    # Info.plist ?ì„±
    info_plist = '''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>Nobody 3</string>
    <key>CFBundleIdentifier</key>
    <string>com.nobody.Nobody 3</string>
    <key>CFBundleName</key>
    <string>Nobody 3</string>
    <key>CFBundleVersion</key>
    <string>1.0</string>
    <key>CFBundleShortVersionString</key>
    <string>1.0</string>
    <key>CFBundleInfoDictionaryVersion</key>
    <string>6.0</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>NSHighResolutionCapable</key>
    <true/>
    <key>LSMinimumSystemVersion</key>
    <string>10.15</string>
</dict>
</plist>'''
    
    with open(contents_dir / "Info.plist", "w") as f:
        f.write(info_plist)
    
    # ?¤í–‰ ê¶Œí•œ ë¶€??
    os.chmod(macos_dir / "Nobody 3", 0o755)
    
    print(f"??ë²ˆë“¤???ì„±?˜ì—ˆ?µë‹ˆ?? {app_name}")

def create_dmg():
    """DMG ?¤ì¹˜ ?Œì¼ ?ì„±"""
    print("DMG ?Œì¼ ?ì„± ì¤?..")
    
    # dmgbuild ?¤ì • ?Œì¼ ?ì„±
    dmg_settings = '''
import os.path

# ê¸°ë³¸ ?¤ì •
format = "UDBZ"
size = "100M"
files = ["Nobody 3.app"]
symlinks = {"Applications": "/Applications"}
badge_icon = "icon.icns" if os.path.exists("icon.icns") else None

# ?ˆë„???¤ì •
window_rect = ((100, 100), (640, 480))
icon_locations = {
    "Nobody 3.app": (150, 200),
    "Applications": (500, 200)
}

# ë°°ê²½ ?¤ì •
background = "builtin-arrow"
show_status_bar = False
show_tab_view = False
show_toolbar = False
show_pathbar = False
show_sidebar = False
sidebar_width = 180

# ?„ì´ì½?ë·??¤ì •
default_view = "icon-view"
show_icon_preview = False
include_icon_view_settings = "auto"
include_list_view_settings = "auto"

# ?„ì´ì½??¬ê¸°
icon_size = 128
text_size = 16
'''
    
    with open("dmg_settings.py", "w") as f:
        f.write(dmg_settings)
    
    # DMG ?ì„±
    try:
        subprocess.run([
            "dmgbuild", 
            "-s", "dmg_settings.py",
            "Nobody 3", 
            "Nobody 3.dmg"
        ], check=True)
        print("DMG ?Œì¼???ì„±?˜ì—ˆ?µë‹ˆ?? Nobody 3.dmg")
    except subprocess.CalledProcessError:
        print("DMG ?ì„± ?¤íŒ¨. ?˜ë™?¼ë¡œ ?ì„±?˜ì„¸??")
        print("hdiutil create -volname 'Nobody 3' -srcfolder Nobody 3.app -ov -format UDZO Nobody 3.dmg")

def sign_app():
    """???œëª… (? íƒ?¬í•­)"""
    print("???œëª…??ê±´ë„ˆ?ë‹ˆ?? (ê°œë°œ??ê³„ì •???„ìš”)")
    print("?œëª…?˜ë ¤ë©??¤ìŒ ëª…ë ¹???¬ìš©?˜ì„¸??")
    print("codesign --deep --force --verify --verbose --sign 'Developer ID Application: Your Name' Nobody 3.app")

def main():
    """ë©”ì¸ ë¹Œë“œ ?„ë¡œ?¸ìŠ¤"""
    print("=== macOS??Nobody 3 ë¹Œë“œ ?œì‘ ===")
    
    if sys.platform != "darwin":
        print("???¤í¬ë¦½íŠ¸??macOS?ì„œë§??¤í–‰?????ˆìŠµ?ˆë‹¤.")
        return 1
    
    try:
        download_ffmpeg_macos()
        install_dependencies()
        build_executable()
        create_app_bundle()
        create_dmg()
        sign_app()
        
        print("\n=== ë¹Œë“œ ?„ë£Œ! ===")
        print("?ì„±???Œì¼:")
        print("- Nobody 3.app (??ë²ˆë“¤)")
        print("- Nobody 3.dmg (?¤ì¹˜ ?Œì¼)")
        
    except Exception as e:
        print(f"ë¹Œë“œ ì¤??¤ë¥˜ ë°œìƒ: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
