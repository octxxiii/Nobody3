"""Simple screenshot capture using Windows API."""

import sys
from pathlib import Path

try:
    import win32gui
    import win32ui
    import win32con
    from PIL import Image
except ImportError:
    print("Required packages not installed.")
    print("Install with: pip install pywin32 Pillow")
    sys.exit(1)


def capture_window_by_title(title_pattern):
    """Capture a window by its title pattern."""
    def enum_handler(hwnd, windows):
        if win32gui.IsWindowVisible(hwnd):
            window_title = win32gui.GetWindowText(hwnd)
            if title_pattern.lower() in window_title.lower():
                windows.append((hwnd, window_title))
        return True
    
    windows = []
    win32gui.EnumWindows(enum_handler, windows)
    
    if not windows:
        return None
    
    hwnd = windows[0][0]
    
    # Get window dimensions
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    width = right - left
    height = bottom - top
    
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
    
    # Cleanup
    dcObj.DeleteDC()
    cDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, wDC)
    win32gui.DeleteObject(dataBitMap.GetHandle())
    
    return img


def main():
    """Main function."""
    print("Screenshot Capture Tool")
    print("=" * 50)
    print("\nInstructions:")
    print("1. Run Nobody 3 application")
    print("2. Navigate to each screen you want to capture")
    print("3. Press Enter when ready to capture")
    print("\nRequired screenshots:")
    print("- main_interface.png")
    print("- format_selection.png")
    print("- mini_player.png")
    print("- settings_dialog.png")
    print("\n" + "=" * 50)
    
    screenshots_dir = Path(__file__).parent.parent / "docs" / "screenshots"
    screenshots_dir.mkdir(parents=True, exist_ok=True)
    
    screenshots = [
        ("main_interface.png", "Nobody 3"),
        ("format_selection.png", "Nobody 3"),
        ("mini_player.png", "Nobody 3"),
        ("settings_dialog.png", "Nobody 3"),
    ]
    
    for filename, title_pattern in screenshots:
        input(f"\nReady to capture {filename}? (Press Enter when the window is ready)")
        
        img = capture_window_by_title(title_pattern)
        if img:
            filepath = screenshots_dir / filename
            img.save(filepath, "PNG")
            print(f"✓ Saved: {filepath}")
        else:
            print(f"✗ Could not find window with title containing '{title_pattern}'")
            print("  Please make sure Nobody 3 is running and visible")
    
    print("\n" + "=" * 50)
    print("All screenshots captured!")
    print(f"Screenshots saved to: {screenshots_dir}")


if __name__ == "__main__":
    main()

