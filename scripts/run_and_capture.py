"""Run Nobody 3 and capture screenshots automatically."""

import sys
import time
import subprocess
from pathlib import Path

project_root = Path(__file__).parent.parent
screenshots_dir = project_root / "docs" / "screenshots"
screenshots_dir.mkdir(parents=True, exist_ok=True)

print("=" * 60)
print("Nobody 3 - Automated Screenshot Capture")
print("=" * 60)
print("\nThis script will:")
print("1. Start Nobody 3 application")
print("2. Wait for it to load")
print("3. Provide instructions for manual capture")
print("\n" + "=" * 60)

# Start the application
print("\nStarting Nobody 3...")
app_process = subprocess.Popen(
    [sys.executable, "-m", "Nobody.main"],
    cwd=str(project_root)
)

print("Application started!")
print("\nPlease wait 5 seconds for the application to load...")
time.sleep(5)

print("\n" + "=" * 60)
print("SCREENSHOT CAPTURE INSTRUCTIONS")
print("=" * 60)
print("\nNow that Nobody 3 is running, please:")
print("\n1. Press Windows + Shift + S to open Snipping Tool")
print("2. Capture each of the following screens:")
print("\n   a) Main Interface")
print("      - Save as: docs/screenshots/main_interface.png")
print("\n   b) Format Selection (after searching a URL)")
print("      - Save as: docs/screenshots/format_selection.png")
print("\n   c) Mini Player (click mini player button)")
print("      - Save as: docs/screenshots/mini_player.png")
print("\n   d) Settings Dialog (click info button)")
print("      - Save as: docs/screenshots/settings_dialog.png")
print("\n3. After capturing all screenshots, press Enter here to continue...")

input("\nPress Enter when all screenshots are captured...")

# Check for screenshots
captured = list(screenshots_dir.glob("*.png"))
if captured:
    print(f"\n✓ Found {len(captured)} screenshot(s):")
    for f in captured:
        size_kb = f.stat().st_size / 1024
        print(f"  - {f.name} ({size_kb:.1f} KB)")
    
    missing = []
    required = ["main_interface.png", "format_selection.png", "mini_player.png", "settings_dialog.png"]
    for req in required:
        if not (screenshots_dir / req).exists():
            missing.append(req)
    
    if missing:
        print(f"\n⚠ Missing {len(missing)} screenshot(s):")
        for m in missing:
            print(f"  - {m}")
    else:
        print("\n✓ All required screenshots are present!")
        print("\nYou can now commit and push:")
        print("  git add docs/screenshots/*.png")
        print("  git commit -m 'docs: add screenshots'")
        print("  git push origin main")
else:
    print("\n⚠ No screenshots found in docs/screenshots/")
    print("Please capture the screenshots manually using Windows + Shift + S")

print("\nApplication is still running. Close it when done.")
print("=" * 60)

