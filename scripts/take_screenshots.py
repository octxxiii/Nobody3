"""Automated screenshot capture script for Nobody 3."""

import sys
import os
import time
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtCore import QTimer
    from PyQt5.QtGui import QPixmap, QScreen
    from Nobody.main import main as app_main
    from Nobody.views.main_window import VideoDownloader
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Please install required dependencies: pip install -r requirements.txt")
    sys.exit(1)


def capture_screenshot(window, filename, delay=2):
    """Capture a screenshot of the window after a delay."""
    def take_screenshot():
        # Wait for window to be fully rendered
        QApplication.processEvents()
        time.sleep(delay)
        
        # Get the screen
        screen = QApplication.primaryScreen()
        
        # Capture the window
        pixmap = screen.grabWindow(window.winId())
        
        # Save the screenshot
        screenshots_dir = Path(__file__).parent.parent / "docs" / "screenshots"
        screenshots_dir.mkdir(parents=True, exist_ok=True)
        
        filepath = screenshots_dir / filename
        pixmap.save(str(filepath), "PNG")
        print(f"✓ Screenshot saved: {filepath}")
        
    return take_screenshot


def main():
    """Main function to capture screenshots."""
    app = QApplication(sys.argv)
    
    # Create main window
    window = VideoDownloader()
    window.show()
    
    # Wait for window to be ready
    QApplication.processEvents()
    time.sleep(1)
    
    screenshots = [
        ("main_interface.png", 2),
        ("format_selection.png", 1),
        ("mini_player.png", 1),
        ("settings_dialog.png", 1),
    ]
    
    print("Starting screenshot capture...")
    print("Please interact with the application as needed.")
    print("Screenshots will be captured automatically.\n")
    
    # Capture main interface
    timer1 = QTimer()
    timer1.setSingleShot(True)
    timer1.timeout.connect(capture_screenshot(window, "main_interface.png", 0))
    timer1.start(2000)
    
    # Capture format selection (after clicking format button)
    def capture_format():
        # Open format settings dialog
        window.formatSettingsButton.click()
        QApplication.processEvents()
        time.sleep(1)
        # Capture the dialog or table
        screen = QApplication.primaryScreen()
        pixmap = screen.grabWindow(window.winId())
        screenshots_dir = Path(__file__).parent.parent / "docs" / "screenshots"
        screenshots_dir.mkdir(parents=True, exist_ok=True)
        pixmap.save(str(screenshots_dir / "format_selection.png"), "PNG")
        print(f"✓ Screenshot saved: {screenshots_dir / 'format_selection.png'}")
    
    timer2 = QTimer()
    timer2.setSingleShot(True)
    timer2.timeout.connect(capture_format)
    timer2.start(4000)
    
    # Capture mini player
    def capture_mini_player():
        # Switch to mini player mode
        if hasattr(window, 'mini_player_controller'):
            window.mini_player_controller.toggle_mini_player()
            QApplication.processEvents()
            time.sleep(1)
            screen = QApplication.primaryScreen()
            if hasattr(window, 'mini_player_controller') and window.mini_player_controller.mini_player:
                pixmap = screen.grabWindow(window.mini_player_controller.mini_player.winId())
            else:
                pixmap = screen.grabWindow(window.winId())
            screenshots_dir = Path(__file__).parent.parent / "docs" / "screenshots"
            screenshots_dir.mkdir(parents=True, exist_ok=True)
            pixmap.save(str(screenshots_dir / "mini_player.png"), "PNG")
            print(f"✓ Screenshot saved: {screenshots_dir / 'mini_player.png'}")
    
    timer3 = QTimer()
    timer3.setSingleShot(True)
    timer3.timeout.connect(capture_mini_player)
    timer3.start(6000)
    
    # Capture settings dialog
    def capture_settings():
        # Open settings dialog
        if hasattr(window, 'settingsButton'):
            window.settingsButton.click()
        QApplication.processEvents()
        time.sleep(1)
        screen = QApplication.primaryScreen()
        pixmap = screen.grabWindow(window.winId())
        screenshots_dir = Path(__file__).parent.parent / "docs" / "screenshots"
        screenshots_dir.mkdir(parents=True, exist_ok=True)
        pixmap.save(str(screenshots_dir / "settings_dialog.png"), "PNG")
        print(f"✓ Screenshot saved: {screenshots_dir / 'settings_dialog.png'}")
        print("\nAll screenshots captured!")
        print("You can close the application now.")
    
    timer4 = QTimer()
    timer4.setSingleShot(True)
    timer4.timeout.connect(capture_settings)
    timer4.start(8000)
    
    print("Application will run for 10 seconds to capture screenshots...")
    print("You can manually interact with the application if needed.\n")
    
    # Run for enough time to capture all screenshots
    QTimer.singleShot(10000, app.quit)
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

