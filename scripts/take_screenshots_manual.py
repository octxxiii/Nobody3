"""Manual screenshot capture helper script.

This script helps you take screenshots manually by providing instructions
and a simple interface to save screenshots with the correct names.
"""

import sys
from pathlib import Path

try:
    from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QFileDialog
    from PyQt5.QtCore import Qt
    from PyQt5.QtGui import QPixmap, QScreen
except ImportError:
    print("PyQt5 is required. Install with: pip install PyQt5")
    sys.exit(1)


class ScreenshotHelper(QMainWindow):
    """Helper window for taking screenshots."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Nobody 3 Screenshot Helper")
        self.setGeometry(100, 100, 400, 300)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Instructions
        instructions = QLabel("""
        <h3>Screenshot Helper</h3>
        <p><b>Steps:</b></p>
        <ol>
        <li>Run Nobody 3 application</li>
        <li>Navigate to the screen you want to capture</li>
        <li>Click the button below to capture the current screen</li>
        <li>Save with the appropriate filename</li>
        </ol>
        <p><b>Required screenshots:</b></p>
        <ul>
        <li>main_interface.png</li>
        <li>format_selection.png</li>
        <li>mini_player.png</li>
        <li>settings_dialog.png</li>
        </ul>
        """)
        instructions.setWordWrap(True)
        layout.addWidget(instructions)
        
        # Capture button
        self.capture_btn = QPushButton("Capture Current Screen")
        self.capture_btn.clicked.connect(self.capture_screen)
        layout.addWidget(self.capture_btn)
        
        # Status label
        self.status_label = QLabel("Ready to capture")
        layout.addWidget(self.status_label)
        
    def capture_screen(self):
        """Capture the current screen."""
        screen = QApplication.primaryScreen()
        pixmap = screen.grabWindow(0)  # Capture entire screen
        
        # Get save location
        screenshots_dir = Path(__file__).parent.parent / "docs" / "screenshots"
        screenshots_dir.mkdir(parents=True, exist_ok=True)
        
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Save Screenshot",
            str(screenshots_dir / "screenshot.png"),
            "PNG Files (*.png);;All Files (*)"
        )
        
        if filename:
            pixmap.save(filename, "PNG")
            self.status_label.setText(f"Saved: {filename}")
            print(f"✓ Screenshot saved: {filename}")


def main():
    """Main function."""
    app = QApplication(sys.argv)
    window = ScreenshotHelper()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

