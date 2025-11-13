import sys
import os
from cx_Freeze import setup, Executable
import platform

# ?�재 ?�랫???�인
is_windows = platform.system() == "Windows"
is_mac = platform.system() == "Darwin"

# 기본 ?�정
build_exe_options = {
    "packages": ["PyQt5.QtCore", "PyQt5.QtGui", "PyQt5.QtWidgets", "PyQt5.QtWebEngineWidgets", "PyQt5.QtWebChannel", "PyQt5.QtMultimedia", "yt_dlp", "requests", "urllib3", "http", "urllib", "ssl", "certifi"],
    "excludes": ["tkinter", "unittest", "pydoc", "PyQt5.QtQml", "PyQt5.QtQuick"],
    "include_files": [
        "resources_rc.py",
    ],
    "optimize": 2,
    "build_exe": "build_new",
}

# FFmpeg 바이?�리 ?�함 (?�택?�항)
if is_windows:
    # Windows??FFmpeg 바이?�리 경로
    ffmpeg_files = []
    if os.path.exists("ffmpeg/windows/ffmpeg.exe"):
        ffmpeg_files.append(("ffmpeg/windows/ffmpeg.exe", "ffmpeg.exe"))
    if os.path.exists("ffmpeg/windows/ffprobe.exe"):
        ffmpeg_files.append(("ffmpeg/windows/ffprobe.exe", "ffprobe.exe"))
    if ffmpeg_files:
        build_exe_options["include_files"].extend(ffmpeg_files)
    else:
        print("경고: FFmpeg 바이?�리�?찾을 ???�습?�다. ?�함?��? ?�고 빌드?�니??")
    
elif is_mac:
    # macOS??FFmpeg 바이?�리 경로
    ffmpeg_files = []
    if os.path.exists("ffmpeg/macos/ffmpeg"):
        ffmpeg_files.append(("ffmpeg/macos/ffmpeg", "ffmpeg"))
    if os.path.exists("ffmpeg/macos/ffprobe"):
        ffmpeg_files.append(("ffmpeg/macos/ffprobe", "ffprobe"))
    if ffmpeg_files:
        build_exe_options["include_files"].extend(ffmpeg_files)
    else:
        print("경고: FFmpeg 바이?�리�?찾을 ???�습?�다. ?�함?��? ?�고 빌드?�니??")

# ?�행 ?�일 ?�정
# ?�이�??�일 ?�선?�위: icon.ico/icon.icns > st2.icns
if is_windows:
    icon_path = None
    if os.path.exists("icon.ico"):
        icon_path = "icon.ico"
    elif os.path.exists("st2.icns"):
        icon_path = "st2.icns"
    
    executables = [
        Executable(
            "Nobody/main.py",
            base="Win32GUI",
            target_name="Nobody 3.exe",
            icon=icon_path
        )
    ]
else:
    icon_path = None
    if os.path.exists("icon.icns"):
        icon_path = "icon.icns"
    elif os.path.exists("st2.icns"):
        icon_path = "st2.icns"
    
    executables = [
        Executable(
            "Nobody/main.py",
            target_name="Nobody 3",
            icon=icon_path
        )
    ]

setup(
    name="Nobody 3",
    version="1.0",
    description="YouTube/Music Converter & Player",
    author="nobody",
    options={"build_exe": build_exe_options},
    executables=executables
)
