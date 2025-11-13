#!/usr/bin/env python3
"""
Windows??MSI ?¤ì¹˜ ?Œì¼ ë¹Œë“œ ?¤í¬ë¦½íŠ¸
"""

import os
import sys
import subprocess
import urllib.request
import zipfile
import shutil
from pathlib import Path

def download_ffmpeg_windows():
    """Windows??FFmpeg ?¤ìš´ë¡œë“œ ë°??¤ì¹˜"""
    print("Windows??FFmpeg ?¤ìš´ë¡œë“œ ì¤?..")
    
    ffmpeg_url = "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip"
    ffmpeg_zip = "ffmpeg-windows.zip"
    
    # FFmpeg ?¤ìš´ë¡œë“œ
    urllib.request.urlretrieve(ffmpeg_url, ffmpeg_zip)
    
    # ?•ì¶• ?´ì œ
    with zipfile.ZipFile(ffmpeg_zip, 'r') as zip_ref:
        zip_ref.extractall("temp_ffmpeg")
    
    # FFmpeg ë°”ì´?ˆë¦¬ ë³µì‚¬
    ffmpeg_dir = Path("ffmpeg/windows")
    ffmpeg_dir.mkdir(parents=True, exist_ok=True)
    
    # ?•ì¶• ?´ì œ???´ë”?ì„œ ?¤í–‰ ?Œì¼ ì°¾ê¸°
    for root, dirs, files in os.walk("temp_ffmpeg"):
        for file in files:
            if file in ["ffmpeg.exe", "ffprobe.exe"]:
                src = os.path.join(root, file)
                dst = ffmpeg_dir / file
                shutil.copy2(src, dst)
                print(f"ë³µì‚¬?? {file}")
    
    # ?„ì‹œ ?Œì¼ ?•ë¦¬
    os.remove(ffmpeg_zip)
    shutil.rmtree("temp_ffmpeg")
    
    print("FFmpeg ?¤ìš´ë¡œë“œ ?„ë£Œ!")

def install_dependencies():
    """?„ìš”???¨í‚¤ì§€ ?¤ì¹˜"""
    print("?˜ì¡´???¨í‚¤ì§€ ?¤ì¹˜ ì¤?..")
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    subprocess.run([sys.executable, "-m", "pip", "install", "cx_Freeze"])

def build_executable():
    """?¤í–‰ ?Œì¼ ë¹Œë“œ"""
    print("?¤í–‰ ?Œì¼ ë¹Œë“œ ì¤?..")
    subprocess.run([sys.executable, "setup.py", "build"])

def create_msi():
    """MSI ?¤ì¹˜ ?Œì¼ ?ì„±"""
    print("MSI ?¤ì¹˜ ?Œì¼ ?ì„± ì¤?..")
    
    # WiX Toolset???„ìš”?©ë‹ˆ??
    try:
        subprocess.run(["candle", "-?"], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("ê²½ê³ : WiX Toolset???¤ì¹˜?˜ì? ?Šì•˜?µë‹ˆ??")
        print("MSI ?Œì¼???ì„±?˜ë ¤ë©?WiX Toolset???¤ì¹˜?´ì£¼?¸ìš”:")
        print("https://wixtoolset.org/releases/")
        return
    
    # WXS ?Œì¼ ?ì„±
    wxs_content = '''<?xml version="1.0" encoding="UTF-8"?>
<Wix xmlns="http://schemas.microsoft.com/wix/2006/wi">
    <Product Id="*" Name="Nobody 3" Language="1033" Version="1.0.0" 
             Manufacturer="nobody" UpgradeCode="12345678-1234-1234-1234-123456789012">
        
        <Package InstallerVersion="200" Compressed="yes" InstallScope="perMachine" />
        
        <MajorUpgrade DowngradeErrorMessage="A newer version is already installed." />
        <MediaTemplate EmbedCab="yes" />
        
        <Feature Id="ProductFeature" Title="Nobody 3" Level="1">
            <ComponentGroupRef Id="ProductComponents" />
        </Feature>
        
        <Directory Id="TARGETDIR" Name="SourceDir">
            <Directory Id="ProgramFilesFolder">
                <Directory Id="INSTALLFOLDER" Name="Nobody 3" />
            </Directory>
            <Directory Id="ProgramMenuFolder">
                <Directory Id="ApplicationProgramsFolder" Name="Nobody 3"/>
            </Directory>
        </Directory>
        
        <ComponentGroup Id="ProductComponents" Directory="INSTALLFOLDER">
            <Component Id="MainExecutable" Guid="*">
                <File Id="Nobody 3.exe" Source="build/exe.win-amd64-3.x/Nobody 3.exe" KeyPath="yes">
                    <Shortcut Id="ApplicationStartMenuShortcut" Directory="ApplicationProgramsFolder" 
                              Name="Nobody 3" WorkingDirectory="INSTALLFOLDER" Advertise="yes" />
                </File>
            </Component>
            <!-- ì¶”ê? ?Œì¼?¤ì„ ?¬ê¸°???¬í•¨ -->
        </ComponentGroup>
    </Product>
</Wix>'''
    
    with open("Nobody 3.wxs", "w", encoding="utf-8") as f:
        f.write(wxs_content)
    
    # MSI ë¹Œë“œ
    subprocess.run(["candle", "Nobody 3.wxs"])
    subprocess.run(["light", "Nobody 3.wixobj", "-o", "Nobody 3.msi"])
    
    print("MSI ?Œì¼???ì„±?˜ì—ˆ?µë‹ˆ?? Nobody 3.msi")

def main():
    """ë©”ì¸ ë¹Œë“œ ?„ë¡œ?¸ìŠ¤"""
    print("=== Windows??Nobody 3 ë¹Œë“œ ?œì‘ ===")
    
    if sys.platform != "win32":
        print("???¤í¬ë¦½íŠ¸??Windows?ì„œë§??¤í–‰?????ˆìŠµ?ˆë‹¤.")
        return
    
    try:
        download_ffmpeg_windows()
        install_dependencies()
        build_executable()
        create_msi()
        
        print("\n=== ë¹Œë“œ ?„ë£Œ! ===")
        print("?ì„±???Œì¼:")
        print("- build/exe.win-amd64-3.x/ (?¤í–‰ ?Œì¼)")
        print("- Nobody 3.msi (?¤ì¹˜ ?Œì¼)")
        
    except Exception as e:
        print(f"ë¹Œë“œ ì¤??¤ë¥˜ ë°œìƒ: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
