#!/usr/bin/env python3
"""Download FFmpeg binaries for Windows."""

import os
import requests
import zipfile
from pathlib import Path

def download_ffmpeg():
    """Download and extract FFmpeg binaries."""
    
    # First, get the latest release info from GitHub API
    api_url = "https://api.github.com/repos/BtbN/FFmpeg-Builds/releases/latest"
    
    print("Getting latest FFmpeg release info...")
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        release_data = response.json()
        
        # Find the Windows GPL build
        download_url = None
        for asset in release_data.get('assets', []):
            if 'win64-gpl' in asset['name'] and asset['name'].endswith('.zip'):
                download_url = asset['browser_download_url']
                print(f"Found: {asset['name']}")
                break
        
        if not download_url:
            print("Could not find Windows GPL build in latest release")
            return False
            
    except Exception as e:
        print(f"Failed to get release info: {e}")
        # Fallback to a known working URL
        download_url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
        print("Using fallback URL from gyan.dev")
    
    print(f"Downloading FFmpeg from: {download_url}")
    try:
        response = requests.get(download_url, stream=True)
        response.raise_for_status()
        
        # Save zip file
        zip_path = Path("ffmpeg.zip")
        with open(zip_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"Downloaded: {zip_path} ({zip_path.stat().st_size / (1024*1024):.2f} MB)")
        
        # Extract zip file
        print("Extracting FFmpeg...")
        with zipfile.ZipFile(zip_path, 'r') as zf:
            # Find ffmpeg.exe and ffprobe.exe in the zip
            for member in zf.namelist():
                if member.endswith('ffmpeg.exe') or member.endswith('ffprobe.exe'):
                    # Extract to current directory
                    filename = os.path.basename(member)
                    print(f"Extracting: {filename}")
                    with zf.open(member) as source, open(filename, "wb") as target:
                        target.write(source.read())
        
        # Clean up zip file
        zip_path.unlink()
        print("FFmpeg download and extraction completed!")
        
        # Verify files exist
        if os.path.exists("ffmpeg.exe") and os.path.exists("ffprobe.exe"):
            print("✓ ffmpeg.exe and ffprobe.exe are ready")
            return True
        else:
            print("✗ Failed to extract ffmpeg executables")
            return False
            
    except requests.RequestException as e:
        print(f"Download failed: {e}")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    success = download_ffmpeg()
    exit(0 if success else 1)