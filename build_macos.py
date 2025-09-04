#!/usr/bin/env python3
"""
macOS용 앱 번들 및 DMG 설치 파일 빌드 스크립트
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
    """macOS용 FFmpeg 다운로드 및 설치"""
    print("macOS용 FFmpeg 다운로드 중...")
    
    # Apple Silicon vs Intel 확인
    arch = platform.machine()
    if arch == "arm64":
        ffmpeg_url = "https://evermeet.cx/ffmpeg/getrelease/zip"
        ffprobe_url = "https://evermeet.cx/ffmpeg/getrelease/ffprobe/zip"
    else:
        ffmpeg_url = "https://evermeet.cx/ffmpeg/getrelease/zip"
        ffprobe_url = "https://evermeet.cx/ffmpeg/getrelease/ffprobe/zip"
    
    ffmpeg_dir = Path("ffmpeg/macos")
    ffmpeg_dir.mkdir(parents=True, exist_ok=True)
    
    # FFmpeg 다운로드
    print("FFmpeg 바이너리 다운로드 중...")
    urllib.request.urlretrieve(ffmpeg_url, "ffmpeg.zip")
    urllib.request.urlretrieve(ffprobe_url, "ffprobe.zip")
    
    # 압축 해제
    import zipfile
    with zipfile.ZipFile("ffmpeg.zip", 'r') as zip_ref:
        zip_ref.extractall("temp_ffmpeg")
    with zipfile.ZipFile("ffprobe.zip", 'r') as zip_ref:
        zip_ref.extractall("temp_ffprobe")
    
    # 바이너리 복사
    shutil.move("temp_ffmpeg/ffmpeg", ffmpeg_dir / "ffmpeg")
    shutil.move("temp_ffprobe/ffprobe", ffmpeg_dir / "ffprobe")
    
    # 실행 권한 부여
    os.chmod(ffmpeg_dir / "ffmpeg", 0o755)
    os.chmod(ffmpeg_dir / "ffprobe", 0o755)
    
    # 임시 파일 정리
    os.remove("ffmpeg.zip")
    os.remove("ffprobe.zip")
    shutil.rmtree("temp_ffmpeg")
    shutil.rmtree("temp_ffprobe")
    
    print("FFmpeg 다운로드 완료!")

def install_dependencies():
    """필요한 패키지 설치"""
    print("의존성 패키지 설치 중...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    subprocess.run([sys.executable, "-m", "pip", "install", "cx_Freeze"])
    subprocess.run([sys.executable, "-m", "pip", "install", "dmgbuild"])

def build_executable():
    """실행 파일 빌드"""
    print("실행 파일 빌드 중...")
    subprocess.run([sys.executable, "setup.py", "build"])

def create_app_bundle():
    """macOS 앱 번들 생성"""
    print("앱 번들 생성 중...")
    
    app_name = "OctXXIII.app"
    build_dir = Path("build")
    
    # 빌드된 실행 파일 찾기
    exe_dirs = list(build_dir.glob("exe.*"))
    if not exe_dirs:
        raise Exception("빌드된 실행 파일을 찾을 수 없습니다.")
    
    exe_dir = exe_dirs[0]
    
    # 앱 번들 구조 생성
    app_dir = Path(app_name)
    contents_dir = app_dir / "Contents"
    macos_dir = contents_dir / "MacOS"
    resources_dir = contents_dir / "Resources"
    
    # 기존 앱 번들 제거
    if app_dir.exists():
        shutil.rmtree(app_dir)
    
    # 디렉토리 생성
    macos_dir.mkdir(parents=True)
    resources_dir.mkdir(parents=True)
    
    # 실행 파일 및 라이브러리 복사
    for item in exe_dir.iterdir():
        if item.is_file():
            shutil.copy2(item, macos_dir)
        else:
            shutil.copytree(item, macos_dir / item.name)
    
    # Info.plist 생성
    info_plist = '''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>OctXXIII</string>
    <key>CFBundleIdentifier</key>
    <string>com.nobody.octxxiii</string>
    <key>CFBundleName</key>
    <string>OctXXIII</string>
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
    
    # 실행 권한 부여
    os.chmod(macos_dir / "OctXXIII", 0o755)
    
    print(f"앱 번들이 생성되었습니다: {app_name}")

def create_dmg():
    """DMG 설치 파일 생성"""
    print("DMG 파일 생성 중...")
    
    # dmgbuild 설정 파일 생성
    dmg_settings = '''
import os.path

# 기본 설정
format = "UDBZ"
size = "100M"
files = ["OctXXIII.app"]
symlinks = {"Applications": "/Applications"}
badge_icon = "icon.icns" if os.path.exists("icon.icns") else None

# 윈도우 설정
window_rect = ((100, 100), (640, 480))
icon_locations = {
    "OctXXIII.app": (150, 200),
    "Applications": (500, 200)
}

# 배경 설정
background = "builtin-arrow"
show_status_bar = False
show_tab_view = False
show_toolbar = False
show_pathbar = False
show_sidebar = False
sidebar_width = 180

# 아이콘 뷰 설정
default_view = "icon-view"
show_icon_preview = False
include_icon_view_settings = "auto"
include_list_view_settings = "auto"

# 아이콘 크기
icon_size = 128
text_size = 16
'''
    
    with open("dmg_settings.py", "w") as f:
        f.write(dmg_settings)
    
    # DMG 생성
    try:
        subprocess.run([
            "dmgbuild", 
            "-s", "dmg_settings.py",
            "OctXXIII", 
            "OctXXIII.dmg"
        ], check=True)
        print("DMG 파일이 생성되었습니다: OctXXIII.dmg")
    except subprocess.CalledProcessError:
        print("DMG 생성 실패. 수동으로 생성하세요:")
        print("hdiutil create -volname 'OctXXIII' -srcfolder OctXXIII.app -ov -format UDZO OctXXIII.dmg")

def sign_app():
    """앱 서명 (선택사항)"""
    print("앱 서명을 건너뜁니다. (개발자 계정이 필요)")
    print("서명하려면 다음 명령을 사용하세요:")
    print("codesign --deep --force --verify --verbose --sign 'Developer ID Application: Your Name' OctXXIII.app")

def main():
    """메인 빌드 프로세스"""
    print("=== macOS용 OctXXIII 빌드 시작 ===")
    
    if sys.platform != "darwin":
        print("이 스크립트는 macOS에서만 실행할 수 있습니다.")
        return 1
    
    try:
        download_ffmpeg_macos()
        install_dependencies()
        build_executable()
        create_app_bundle()
        create_dmg()
        sign_app()
        
        print("\n=== 빌드 완료! ===")
        print("생성된 파일:")
        print("- OctXXIII.app (앱 번들)")
        print("- OctXXIII.dmg (설치 파일)")
        
    except Exception as e:
        print(f"빌드 중 오류 발생: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())