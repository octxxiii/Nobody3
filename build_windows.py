#!/usr/bin/env python3
"""
Windows용 MSI 설치 파일 빌드 스크립트
"""

import os
import sys
import subprocess
import urllib.request
import zipfile
import shutil
from pathlib import Path

def download_ffmpeg_windows():
    """Windows용 FFmpeg 다운로드 및 설치"""
    print("Windows용 FFmpeg 다운로드 중...")
    
    ffmpeg_url = "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip"
    ffmpeg_zip = "ffmpeg-windows.zip"
    
    # FFmpeg 다운로드
    urllib.request.urlretrieve(ffmpeg_url, ffmpeg_zip)
    
    # 압축 해제
    with zipfile.ZipFile(ffmpeg_zip, 'r') as zip_ref:
        zip_ref.extractall("temp_ffmpeg")
    
    # FFmpeg 바이너리 복사
    ffmpeg_dir = Path("ffmpeg/windows")
    ffmpeg_dir.mkdir(parents=True, exist_ok=True)
    
    # 압축 해제된 폴더에서 실행 파일 찾기
    for root, dirs, files in os.walk("temp_ffmpeg"):
        for file in files:
            if file in ["ffmpeg.exe", "ffprobe.exe"]:
                src = os.path.join(root, file)
                dst = ffmpeg_dir / file
                shutil.copy2(src, dst)
                print(f"복사됨: {file}")
    
    # 임시 파일 정리
    os.remove(ffmpeg_zip)
    shutil.rmtree("temp_ffmpeg")
    
    print("FFmpeg 다운로드 완료!")

def install_dependencies():
    """필요한 패키지 설치"""
    print("의존성 패키지 설치 중...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    subprocess.run([sys.executable, "-m", "pip", "install", "cx_Freeze"])

def build_executable():
    """실행 파일 빌드"""
    print("실행 파일 빌드 중...")
    subprocess.run([sys.executable, "setup.py", "build"])

def create_msi():
    """MSI 설치 파일 생성"""
    print("MSI 설치 파일 생성 중...")
    
    # WiX Toolset이 필요합니다
    try:
        subprocess.run(["candle", "-?"], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("경고: WiX Toolset이 설치되지 않았습니다.")
        print("MSI 파일을 생성하려면 WiX Toolset을 설치해주세요:")
        print("https://wixtoolset.org/releases/")
        return
    
    # WXS 파일 생성
    wxs_content = '''<?xml version="1.0" encoding="UTF-8"?>
<Wix xmlns="http://schemas.microsoft.com/wix/2006/wi">
    <Product Id="*" Name="OctXXIII" Language="1033" Version="2.0.0" 
             Manufacturer="nobody" UpgradeCode="12345678-1234-1234-1234-123456789012">
        
        <Package InstallerVersion="200" Compressed="yes" InstallScope="perMachine" />
        
        <MajorUpgrade DowngradeErrorMessage="A newer version is already installed." />
        <MediaTemplate EmbedCab="yes" />
        
        <Feature Id="ProductFeature" Title="OctXXIII" Level="1">
            <ComponentGroupRef Id="ProductComponents" />
        </Feature>
        
        <Directory Id="TARGETDIR" Name="SourceDir">
            <Directory Id="ProgramFilesFolder">
                <Directory Id="INSTALLFOLDER" Name="OctXXIII" />
            </Directory>
            <Directory Id="ProgramMenuFolder">
                <Directory Id="ApplicationProgramsFolder" Name="OctXXIII"/>
            </Directory>
        </Directory>
        
        <ComponentGroup Id="ProductComponents" Directory="INSTALLFOLDER">
            <Component Id="MainExecutable" Guid="*">
                <File Id="OctXXIII.exe" Source="build/exe.win-amd64-3.x/OctXXIII.exe" KeyPath="yes">
                    <Shortcut Id="ApplicationStartMenuShortcut" Directory="ApplicationProgramsFolder" 
                              Name="OctXXIII" WorkingDirectory="INSTALLFOLDER" Advertise="yes" />
                </File>
            </Component>
            <!-- 추가 파일들을 여기에 포함 -->
        </ComponentGroup>
    </Product>
</Wix>'''
    
    with open("OctXXIII.wxs", "w", encoding="utf-8") as f:
        f.write(wxs_content)
    
    # MSI 빌드
    subprocess.run(["candle", "OctXXIII.wxs"])
    subprocess.run(["light", "OctXXIII.wixobj", "-o", "OctXXIII.msi"])
    
    print("MSI 파일이 생성되었습니다: OctXXIII.msi")

def main():
    """메인 빌드 프로세스"""
    print("=== Windows용 OctXXIII 빌드 시작 ===")
    
    if sys.platform != "win32":
        print("이 스크립트는 Windows에서만 실행할 수 있습니다.")
        return
    
    try:
        download_ffmpeg_windows()
        install_dependencies()
        build_executable()
        create_msi()
        
        print("\n=== 빌드 완료! ===")
        print("생성된 파일:")
        print("- build/exe.win-amd64-3.x/ (실행 파일)")
        print("- OctXXIII.msi (설치 파일)")
        
    except Exception as e:
        print(f"빌드 중 오류 발생: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())