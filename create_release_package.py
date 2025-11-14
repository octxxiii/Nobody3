#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Create release package with executable and FFmpeg
"""

import os
import sys
import platform
import shutil
import zipfile
from pathlib import Path

def create_windows_package():
    """Create Windows release package."""
    print("=== Creating Windows Release Package ===")
    
    dist_dir = Path("dist")
    releases_dir = Path("releases")
    releases_dir.mkdir(exist_ok=True)
    
    # Check if executable exists
    exe_path = dist_dir / "Nobody3.exe"
    if not exe_path.exists():
        print("[ERROR] Nobody3.exe not found in dist/")
        return False
    
    # Create package directory
    package_name = "Nobody3-Windows"
    package_dir = releases_dir / package_name
    if package_dir.exists():
        shutil.rmtree(package_dir)
    package_dir.mkdir(parents=True)
    
    # Copy executable
    shutil.copy2(exe_path, package_dir / "Nobody3.exe")
    print("[OK] Copied Nobody3.exe")
    
    # Copy FFmpeg if exists
    for ffmpeg_file in ["ffmpeg.exe", "ffprobe.exe"]:
        src = dist_dir / ffmpeg_file
        if src.exists():
            shutil.copy2(src, package_dir / ffmpeg_file)
            print(f"[OK] Copied {ffmpeg_file}")
        else:
            # Try root directory
            src = Path(ffmpeg_file)
            if src.exists():
                shutil.copy2(src, package_dir / ffmpeg_file)
                print(f"[OK] Copied {ffmpeg_file} from root")
    
    # Create README
    readme_content = """Nobody 3 - Windows Release

사용 방법:
1. Nobody3.exe를 더블클릭하여 실행
2. FFmpeg가 포함되어 있어 별도 설치 불필요

시스템 요구사항:
- Windows 10 이상
- 인터넷 연결

문제 해결:
- 실행이 안 되면 관리자 권한으로 실행해보세요
- 바이러스 백신 프로그램이 차단할 수 있습니다
"""
    
    with open(package_dir / "README.txt", "w", encoding="utf-8") as f:
        f.write(readme_content)
    
    # Create zip file
    zip_path = releases_dir / f"{package_name}.zip"
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in package_dir.rglob("*"):
            if file.is_file():
                arcname = file.relative_to(package_dir)
                zipf.write(file, arcname)
    
    print(f"[OK] Created {zip_path}")
    return True

def create_macos_package():
    """Create macOS release package."""
    print("=== Creating macOS Release Package ===")
    
    dist_dir = Path("dist")
    releases_dir = Path("releases")
    releases_dir.mkdir(exist_ok=True)
    
    # Check if app bundle exists
    app_path = dist_dir / "Nobody3.app"
    if not app_path.exists():
        print("[ERROR] Nobody3.app not found in dist/")
        return False
    
    # Create zip file
    zip_path = releases_dir / "Nobody3-macOS.zip"
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in app_path.rglob("*"):
            if file.is_file():
                arcname = file.relative_to(dist_dir)
                zipf.write(file, arcname)
    
    print(f"[OK] Created {zip_path}")
    return True

def create_linux_package():
    """Create Linux release package."""
    print("=== Creating Linux Release Package ===")
    
    dist_dir = Path("dist")
    releases_dir = Path("releases")
    releases_dir.mkdir(exist_ok=True)
    
    # Check if executable exists
    exe_path = dist_dir / "Nobody3"
    if not exe_path.exists():
        print("[ERROR] Nobody3 executable not found in dist/")
        return False
    
    # Create package directory
    package_name = "Nobody3-Linux"
    package_dir = releases_dir / package_name
    if package_dir.exists():
        shutil.rmtree(package_dir)
    package_dir.mkdir(parents=True)
    
    # Copy executable
    shutil.copy2(exe_path, package_dir / "Nobody3")
    os.chmod(package_dir / "Nobody3", 0o755)
    print("[OK] Copied Nobody3")
    
    # Create tar.gz
    import tarfile
    tar_path = releases_dir / f"{package_name}.tar.gz"
    with tarfile.open(tar_path, 'w:gz') as tar:
        tar.add(package_dir, arcname=package_name)
    
    print(f"[OK] Created {tar_path}")
    return True

def main():
    """Main function."""
    current_platform = platform.system()
    
    print("=" * 60)
    print("Nobody 3 - Release Package Creator")
    print("=" * 60)
    
    success = False
    if current_platform == "Windows":
        success = create_windows_package()
    elif current_platform == "Darwin":
        success = create_macos_package()
    elif current_platform == "Linux":
        success = create_linux_package()
    else:
        print(f"⚠ Unsupported platform: {current_platform}")
    
    if success:
        print("\n[SUCCESS] Package creation completed!")
    else:
        print("\n[FAILED] Package creation failed!")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

