"""Automated screenshot capture for Nobody 3."""

import sys
import time
import subprocess
from pathlib import Path

# Add parent directory to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

try:
    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtCore import QTimer, QThread, pyqtSignal
    from PyQt5.QtGui import QPixmap
    import win32gui
    import win32ui
    import win32con
    from PIL import Image
except ImportError as e:
    print(f"Missing dependencies: {e}")
    print("Installing required packages...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pywin32", "Pillow"])
    import win32gui
    import win32ui
    import win32con
    from PIL import Image

screenshots_dir = project_root / "docs" / "screenshots"
screenshots_dir.mkdir(parents=True, exist_ok=True)


def find_window_by_title(title_pattern):
    """Find window by title pattern."""
    def enum_handler(hwnd, windows):
        if win32gui.IsWindowVisible(hwnd):
            window_title = win32gui.GetWindowText(hwnd)
            if title_pattern.lower() in window_title.lower():
                windows.append((hwnd, window_title))
        return True
    
    windows = []
    win32gui.EnumWindows(enum_handler, windows)
    return windows[0][0] if windows else None


def capture_window(hwnd, filename):
    """Capture a window by its handle."""
    try:
        # Get window dimensions
        left, top, right, bottom = win32gui.GetWindowRect(hwnd)
        width = right - left
        height = bottom - top
        
        if width <= 0 or height <= 0:
            return False
        
        # Capture window
        wDC = win32gui.GetWindowDC(hwnd)
        dcObj = win32ui.CreateDCFromHandle(wDC)
        cDC = dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, width, height)
        cDC.SelectObject(dataBitMap)
        cDC.BitBlt((0, 0), (width, height), dcObj, (0, 0), win32con.SRCCOPY)
        
        # Convert to PIL Image
        bmpinfo = dataBitMap.GetInfo()
        bmpstr = dataBitMap.GetBitmapBits(True)
        img = Image.frombuffer(
            'RGB',
            (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
            bmpstr, 'raw', 'BGRX', 0, 1
        )
        
        # Save
        filepath = screenshots_dir / filename
        img.save(str(filepath), "PNG")
        
        # Cleanup
        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(hwnd, wDC)
        win32gui.DeleteObject(dataBitMap.GetHandle())
        
        print(f"✓ Captured: {filename} ({width}x{height})")
        return True
    except Exception as e:
        print(f"✗ Failed to capture {filename}: {e}")
        return False


def main():
    """Main function."""
    print("=" * 60)
    print("Nobody 3 Automated Screenshot Capture")
    print("=" * 60)
    print("\nStarting application...")
    
    # Start the application
    app_process = subprocess.Popen(
        [sys.executable, "-m", "Nobody.main"],
        cwd=str(project_root),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    print("Waiting for application to start...")
    time.sleep(5)  # Wait for app to initialize
    
    # Find the main window
    hwnd = None
    for i in range(10):
        windows = []
        def enum_handler(hwnd, windows):
            if win32gui.IsWindowVisible(hwnd):
                title = win32gui.GetWindowText(hwnd)
                if "nobody" in title.lower() or "nobody 3" in title.lower():
                    windows.append((hwnd, title))
        win32gui.EnumWindows(enum_handler, windows)
        
        if windows:
            hwnd = windows[0][0]
            print(f"Found window: {windows[0][1]}")
            break
        time.sleep(1)
    
    if not hwnd:
        print("✗ Could not find Nobody 3 window")
        print("Please make sure the application started successfully")
        app_process.terminate()
        return
    
    # Bring window to front
    try:
        win32gui.SetForegroundWindow(hwnd)
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
        time.sleep(1)
    except:
        pass
    
    screenshots = [
        ("main_interface.png", 2),
        ("format_selection.png", 1),
        ("mini_player.png", 1),
        ("settings_dialog.png", 1),
    ]
    
    print("\nCapturing screenshots...")
    print("-" * 60)
    
    # Capture main interface
    if capture_window(hwnd, "main_interface.png"):
        time.sleep(1)
    
    # Try to capture other windows
    # Note: These might need manual interaction, so we'll capture what we can
    for filename, delay in screenshots[1:]:
        time.sleep(delay)
        # Try to find specific windows or capture main window again
        current_hwnd = find_window_by_title("nobody")
        if current_hwnd:
            capture_window(current_hwnd, filename)
        else:
            # Fallback: capture main window
            capture_window(hwnd, filename)
    
    print("-" * 60)
    print("\nScreenshot capture completed!")
    print(f"Screenshots saved to: {screenshots_dir}")
    
    # List captured files
    captured = list(screenshots_dir.glob("*.png"))
    if captured:
        print(f"\nCaptured {len(captured)} screenshot(s):")
        for f in captured:
            size_kb = f.stat().st_size / 1024
            print(f"  - {f.name} ({size_kb:.1f} KB)")
    else:
        print("\n⚠ No screenshots were captured.")
        print("You may need to take screenshots manually.")
    
    # Keep app running for a bit, then close
    print("\nApplication will close in 3 seconds...")
    time.sleep(3)
    app_process.terminate()
    
    print("\nDone!")


if __name__ == "__main__":
    main()

