import sys
import os
from cx_Freeze import setup, Executable
import platform

# 현재 플랫폼 확인
is_windows = platform.system() == "Windows"
is_mac = platform.system() == "Darwin"

# 기본 설정
build_exe_options = {
    "packages": ["PyQt5", "yt_dlp", "requests", "urllib3", "certifi"],
    "excludes": ["tkinter", "unittest", "email", "http", "xml", "pydoc"],
    "include_files": [
        "resources_rc.py",
    ],
    "optimize": 2,
}

# FFmpeg 바이너리 포함
if is_windows:
    # Windows용 FFmpeg 바이너리 경로
    ffmpeg_files = [
        ("ffmpeg/windows/ffmpeg.exe", "ffmpeg.exe"),
        ("ffmpeg/windows/ffprobe.exe", "ffprobe.exe"),
    ]
    build_exe_options["include_files"].extend(ffmpeg_files)
    
elif is_mac:
    # macOS용 FFmpeg 바이너리 경로
    ffmpeg_files = [
        ("ffmpeg/macos/ffmpeg", "ffmpeg"),
        ("ffmpeg/macos/ffprobe", "ffprobe"),
    ]
    build_exe_options["include_files"].extend(ffmpeg_files)

# 실행 파일 설정
if is_windows:
    executables = [
        Executable(
            "Nobody33.py",
            base="Win32GUI",
            target_name="OctXXIII.exe",
            icon="icon.ico" if os.path.exists("icon.ico") else None
        )
    ]
else:
    executables = [
        Executable(
            "Nobody3.py",
            target_name="OctXXIII",
            icon="icon.icns" if os.path.exists("icon.icns") else None
        )
    ]

setup(
    name="OctXXIII",
    version="2.0",
    description="YouTube/Music Converter & Player with Mini Player",
    author="nobody",
    options={"build_exe": build_exe_options},
    executables=executables
)