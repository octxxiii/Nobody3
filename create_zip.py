"""Create release ZIP file."""
import zipfile
import os
from datetime import datetime

date = datetime.now().strftime('%Y%m%d')
zip_name = f'releases/Nobody3-Windows-v1.0.2-{date}.zip'

files = [
    'dist/Nobody3/Nobody3.exe',
    'dist/Nobody3/ffmpeg.exe',
    'dist/Nobody3/ffprobe.exe',
    'RELEASE_NOTES_v1.0.2.md'
]

# Ensure releases directory exists
os.makedirs('releases', exist_ok=True)

# Remove existing zip if exists
if os.path.exists(zip_name):
    os.remove(zip_name)
    print(f"Removed existing: {zip_name}")

# Create zip file
with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zf:
    for file in files:
        if os.path.exists(file):
            zf.write(file, os.path.basename(file))
            print(f"Added: {file}")
        else:
            print(f"Warning: {file} not found")

print(f"\nCreated: {zip_name}")
print(f"Size: {os.path.getsize(zip_name) / (1024*1024):.2f} MB")

