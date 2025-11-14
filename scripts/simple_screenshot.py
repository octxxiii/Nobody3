"""Simple screenshot capture using mss library."""

import sys
import time
import subprocess
from pathlib import Path

try:
    import mss
    from PIL import Image
except ImportError:
    print("Installing mss...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "mss", "Pillow"])
    import mss
    from PIL import Image

project_root = Path(__file__).parent.parent
screenshots_dir = project_root / "docs" / "screenshots"
screenshots_dir.mkdir(parents=True, exist_ok=True)


def capture_screen(filename, monitor=1):
    """Capture entire screen or specific monitor."""
    with mss.mss() as sct:
        # Capture monitor
        sct_img = sct.grab(sct.monitors[monor])
        img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
        
        filepath = screenshots_dir / filename
        img.save(str(filepath), "PNG")
        print(f"✓ Captured: {filename} ({img.size[0]}x{img.size[1]})")
        return True


def main():
    """Main function."""
    print("=" * 60)
    print("Nobody 3 Screenshot Capture")
    print("=" * 60)
    print("\nThis script will help you capture screenshots.")
    print("Please follow these steps:\n")
    
    print("1. Run Nobody 3 in another window:")
    print("   python -m Nobody.main\n")
    
    input("2. Press Enter when Nobody 3 is running and visible...")
    
    screenshots = [
        ("main_interface.png", "Main window with browser and table"),
        ("format_selection.png", "Format selection table"),
        ("mini_player.png", "Mini player window"),
        ("settings_dialog.png", "Settings dialog"),
    ]
    
    print("\nCapturing screenshots...")
    print("-" * 60)
    
    for filename, description in screenshots:
        print(f"\n{description}")
        input(f"Position the window and press Enter to capture {filename}...")
        capture_screen(filename)
        time.sleep(0.5)
    
    print("\n" + "=" * 60)
    print("All screenshots captured!")
    print(f"Screenshots saved to: {screenshots_dir}")
    
    # List files
    captured = list(screenshots_dir.glob("*.png"))
    if captured:
        print(f"\nCaptured {len(captured)} file(s):")
        for f in captured:
            size_kb = f.stat().st_size / 1024
            print(f"  - {f.name} ({size_kb:.1f} KB)")


if __name__ == "__main__":
    main()

