#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cross-platform build script for Nobody 3
Creates executables for Windows, macOS, and Linux
"""

import os
import sys
import platform
import subprocess
import shutil
import zipfile
import tarfile
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def check_pyinstaller():
    """Check if PyInstaller is installed."""
    try:
        import PyInstaller
        print("✓ PyInstaller is installed")
        return True
    except ImportError:
        print("✗ PyInstaller is not installed")
        print("Installing PyInstaller...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
        return True

def create_spec_file():
    """Create PyInstaller spec file."""
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['Nobody/main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('resources.qrc', '.'),
        ('icon.ico', '.'),
        ('st2.icns', '.'),
    ],
    hiddenimports=[
        'PyQt5.QtCore',
        'PyQt5.QtGui',
        'PyQt5.QtWidgets',
        'PyQt5.QtWebEngineWidgets',
        'PyQt5.QtWebEngineCore',
        'PyQt5.QtMultimedia',
        'PyQt5.QtWebChannel',
        'yt_dlp',
        'requests',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Nobody3',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

# For macOS, create app bundle
if platform.system() == 'Darwin':
    app = BUNDLE(
        exe,
        name='Nobody3.app',
        icon='st2.icns',
        bundle_identifier='com.nobody.Nobody3',
    )
'''
    
    spec_path = project_root / "Nobody3.spec"
    with open(spec_path, 'w', encoding='utf-8') as f:
        f.write(spec_content)
    
    print(f"✓ Created spec file: {spec_path}")
    return spec_path

def copy_ffmpeg():
    """Copy FFmpeg binaries to dist folder."""
    current_platform = platform.system()
    ffmpeg_src = None
    
    if current_platform == "Windows":
        ffmpeg_exe = project_root / "ffmpeg.exe"
        ffprobe_exe = project_root / "ffprobe.exe"
        if ffmpeg_exe.exists() and ffprobe_exe.exists():
            ffmpeg_src = [ffmpeg_exe, ffprobe_exe]
    elif current_platform == "Darwin":
        # macOS - check for ffmpeg in common locations
        for path in ["/usr/local/bin/ffmpeg", "/opt/homebrew/bin/ffmpeg", "ffmpeg"]:
            if shutil.which("ffmpeg"):
                break
    else:
        # Linux
        if shutil.which("ffmpeg"):
            pass
    
    return ffmpeg_src

def build_windows():
    """Build Windows executable."""
    print("\n=== Building Windows executable ===")
    
    if platform.system() != "Windows":
        print("⚠ Skipping Windows build (not on Windows)")
        return None
    
    spec_file = create_spec_file()
    
    # Modify spec for Windows
    with open(spec_file, 'r', encoding='utf-8') as f:
        spec_content = f.read()
    
    spec_content = spec_content.replace(
        "icon='st2.icns',",
        "icon='icon.ico',"
    )
    spec_content = spec_content.replace(
        "if platform.system() == 'Darwin':",
        "if False:  # Windows build"
    )
    
    with open(spec_file, 'w', encoding='utf-8') as f:
        f.write(spec_content)
    
    # Build
    subprocess.run([
        sys.executable, "-m", "PyInstaller",
        "--clean",
        "--noconfirm",
        str(spec_file)
    ], check=True)
    
    # Copy FFmpeg
    dist_dir = project_root / "dist"
    if (project_root / "ffmpeg.exe").exists():
        shutil.copy2(project_root / "ffmpeg.exe", dist_dir / "ffmpeg.exe")
    if (project_root / "ffprobe.exe").exists():
        shutil.copy2(project_root / "ffprobe.exe", dist_dir / "ffprobe.exe")
    
    exe_path = dist_dir / "Nobody3.exe"
    if exe_path.exists():
        print(f"✓ Windows executable created: {exe_path}")
        return exe_path
    return None

def build_macos():
    """Build macOS app bundle."""
    print("\n=== Building macOS app bundle ===")
    
    if platform.system() != "Darwin":
        print("⚠ Skipping macOS build (not on macOS)")
        return None
    
    spec_file = create_spec_file()
    
    # Build
    subprocess.run([
        sys.executable, "-m", "PyInstaller",
        "--clean",
        "--noconfirm",
        str(spec_file)
    ], check=True)
    
    app_path = project_root / "dist" / "Nobody3.app"
    if app_path.exists():
        print(f"✓ macOS app bundle created: {app_path}")
        return app_path
    return None

def build_linux():
    """Build Linux executable."""
    print("\n=== Building Linux executable ===")
    
    if platform.system() != "Linux":
        print("⚠ Skipping Linux build (not on Linux)")
        return None
    
    spec_file = create_spec_file()
    
    # Modify spec for Linux
    with open(spec_file, 'r', encoding='utf-8') as f:
        spec_content = f.read()
    
    spec_content = spec_content.replace(
        "if platform.system() == 'Darwin':",
        "if False:  # Linux build"
    )
    
    with open(spec_file, 'w', encoding='utf-8') as f:
        f.write(spec_content)
    
    # Build
    subprocess.run([
        sys.executable, "-m", "PyInstaller",
        "--clean",
        "--noconfirm",
        str(spec_file)
    ], check=True)
    
    exe_path = project_root / "dist" / "Nobody3"
    if exe_path.exists():
        print(f"✓ Linux executable created: {exe_path}")
        return exe_path
    return None

def create_zip(output_path, source_path, platform_name):
    """Create zip archive."""
    print(f"\n=== Creating {platform_name} archive ===")
    
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        if source_path.is_file():
            zipf.write(source_path, source_path.name)
        else:
            for root, dirs, files in os.walk(source_path):
                for file in files:
                    file_path = Path(root) / file
                    arcname = file_path.relative_to(source_path.parent)
                    zipf.write(file_path, arcname)
    
    print(f"✓ Created archive: {output_path}")
    return output_path

def create_tar_gz(output_path, source_path, platform_name):
    """Create tar.gz archive."""
    print(f"\n=== Creating {platform_name} archive ===")
    
    with tarfile.open(output_path, 'w:gz') as tar:
        if source_path.is_file():
            tar.add(source_path, arcname=source_path.name)
        else:
            tar.add(source_path, arcname=source_path.name, recursive=True)
    
    print(f"✓ Created archive: {output_path}")
    return output_path

def main():
    """Main build process."""
    print("=" * 60)
    print("Nobody 3 - Cross-Platform Build Script")
    print("=" * 60)
    
    # Check PyInstaller
    if not check_pyinstaller():
        return 1
    
    # Create dist directory
    dist_dir = project_root / "dist"
    dist_dir.mkdir(exist_ok=True)
    
    # Create releases directory
    releases_dir = project_root / "releases"
    releases_dir.mkdir(exist_ok=True)
    
    current_platform = platform.system()
    built_files = []
    
    # Build for current platform
    if current_platform == "Windows":
        exe_path = build_windows()
        if exe_path:
            # Create zip with FFmpeg
            zip_path = releases_dir / "Nobody3-Windows.zip"
            create_zip(zip_path, dist_dir, "Windows")
            built_files.append(zip_path)
    
    elif current_platform == "Darwin":
        app_path = build_macos()
        if app_path:
            # Create zip
            zip_path = releases_dir / "Nobody3-macOS.zip"
            create_zip(zip_path, app_path, "macOS")
            built_files.append(zip_path)
    
    elif current_platform == "Linux":
        exe_path = build_linux()
        if exe_path:
            # Create tar.gz
            tar_path = releases_dir / "Nobody3-Linux.tar.gz"
            create_tar_gz(tar_path, exe_path, "Linux")
            built_files.append(tar_path)
    
    # Summary
    print("\n" + "=" * 60)
    print("Build Summary")
    print("=" * 60)
    if built_files:
        print("✓ Successfully built:")
        for f in built_files:
            print(f"  - {f}")
    else:
        print("⚠ No files were built")
    
    print("\nNote: To build for other platforms, run this script on each platform.")
    print("Or use Docker/VM to build for different platforms.")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

