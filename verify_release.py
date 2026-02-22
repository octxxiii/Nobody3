#!/usr/bin/env python3
"""Verify the release ZIP file contents."""

import zipfile
import os
from pathlib import Path

def verify_release():
    """Verify the release ZIP file."""
    
    # Find the release ZIP file
    releases_dir = Path("releases")
    zip_files = list(releases_dir.glob("Nobody3-Windows-v1.0.2-*.zip"))
    
    if not zip_files:
        print("ERROR: No release ZIP file found!")
        return False
    
    zip_path = zip_files[0]
    print(f"Verifying: {zip_path.name}")
    print(f"Size: {zip_path.stat().st_size / (1024*1024):.2f} MB")
    
    # Expected files
    expected_files = {
        'Nobody3.exe': 'Main application executable',
        'ffmpeg.exe': 'FFmpeg video processing tool',
        'ffprobe.exe': 'FFprobe media analysis tool',
        'RELEASE_NOTES_v1.0.2.md': 'Release notes'
    }
    
    try:
        with zipfile.ZipFile(zip_path, 'r') as zf:
            zip_contents = zf.namelist()
            print(f"\nZIP Contents ({len(zip_contents)} files):")
            
            for item in zip_contents:
                print(f"  {item}")
            
            # Check for expected files
            print(f"\nVerification Results:")
            all_found = True
            
            for expected_file, description in expected_files.items():
                found = any(expected_file in item for item in zip_contents)
                status = "OK" if found else "MISSING"
                print(f"  [{status}] {expected_file} - {description}")
                if not found:
                    all_found = False
            
            # Check file sizes
            print(f"\nFile Sizes:")
            for item in zip_contents:
                if not item.endswith('/'):  # Skip directories
                    info = zf.getinfo(item)
                    size_mb = info.file_size / (1024*1024)
                    print(f"  {os.path.basename(item)}: {size_mb:.2f} MB")
            
            if all_found:
                print(f"\nRelease verification PASSED!")
                print(f"{zip_path.name} is ready for distribution!")
                return True
            else:
                print(f"\nRelease verification FAILED!")
                print(f"Some expected files are missing.")
                return False
                
    except Exception as e:
        print(f"ERROR: Error verifying ZIP file: {e}")
        return False

if __name__ == "__main__":
    success = verify_release()
    exit(0 if success else 1)