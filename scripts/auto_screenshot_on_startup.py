"""Automatically take screenshots when app starts."""

import sys
import time
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap, QScreen

# Import after path setup
from Nobody.main import main as app_main

screenshots_dir = project_root / "docs" / "screenshots"
screenshots_dir.mkdir(parents=True, exist_ok=True)


def capture_screenshots():
    """Capture all required screenshots."""
    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)
    
    # Create and show main window
    window = VideoDownloader()
    window.show()
    window.raise_()
    window.activateWindow()
    
    QApplication.processEvents()
    time.sleep(3)  # Wait for window to fully render
    
    screenshots = []
    
    # 1. Main interface
    def capture_main():
        screen = QApplication.primaryScreen()
        pixmap = screen.grabWindow(window.winId())
        filepath = screenshots_dir / "main_interface.png"
        pixmap.save(str(filepath), "PNG")
        screenshots.append(filepath)
        print(f"✓ Captured: main_interface.png")
        QApplication.processEvents()
    
    # 2. Format selection (after search)
    def capture_format():
        # Simulate a search to show format table
        if hasattr(window, 'search_url'):
            window.search_url.setText("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
            QApplication.processEvents()
            time.sleep(1)
            if hasattr(window, 'on_search'):
                window.on_search()
                QApplication.processEvents()
                time.sleep(3)  # Wait for search to complete
        
        screen = QApplication.primaryScreen()
        pixmap = screen.grabWindow(window.winId())
        filepath = screenshots_dir / "format_selection.png"
        pixmap.save(str(filepath), "PNG")
        screenshots.append(filepath)
        print(f"✓ Captured: format_selection.png")
        QApplication.processEvents()
    
    # 3. Mini player
    def capture_mini_player():
        if hasattr(window, 'mini_player_controller'):
            window.mini_player_controller.toggle_mini_player()
            QApplication.processEvents()
            time.sleep(1)
            screen = QApplication.primaryScreen()
            if hasattr(window.mini_player_controller, 'mini_player') and window.mini_player_controller.mini_player:
                pixmap = screen.grabWindow(window.mini_player_controller.mini_player.winId())
            else:
                pixmap = screen.grabWindow(window.winId())
            filepath = screenshots_dir / "mini_player.png"
            pixmap.save(str(filepath), "PNG")
            screenshots.append(filepath)
            print(f"✓ Captured: mini_player.png")
        QApplication.processEvents()
    
    # 4. Settings dialog
    def capture_settings():
        if hasattr(window, 'settingsButton'):
            window.settingsButton.click()
            QApplication.processEvents()
            time.sleep(1)
            screen = QApplication.primaryScreen()
            pixmap = screen.grabWindow(window.winId())
            filepath = screenshots_dir / "settings_dialog.png"
            pixmap.save(str(filepath), "PNG")
            screenshots.append(filepath)
            print(f"✓ Captured: settings_dialog.png")
        QApplication.processEvents()
        app.quit()
    
    # Schedule captures
    QTimer.singleShot(3000, capture_main)
    QTimer.singleShot(6000, capture_format)
    QTimer.singleShot(10000, capture_mini_player)
    QTimer.singleShot(13000, capture_settings)
    QTimer.singleShot(15000, app.quit)
    
    print("=" * 60)
    print("Automated Screenshot Capture")
    print("=" * 60)
    print("\nCapturing screenshots in sequence...")
    print("Please wait...\n")
    
    app.exec_()
    
    print("\n" + "=" * 60)
    print("Screenshot capture completed!")
    print(f"Screenshots saved to: {screenshots_dir}")
    if screenshots:
        print(f"\nCaptured {len(screenshots)} screenshot(s):")
        for f in screenshots:
            if f.exists():
                size_kb = f.stat().st_size / 1024
                print(f"  - {f.name} ({size_kb:.1f} KB)")
    print("=" * 60)


if __name__ == "__main__":
    capture_screenshots()

