"""Entry point for the Nobody 3 application."""

import os
import sys
import platform

# Ensure project root is on sys.path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Windows-specific WebEngine environment variables to prevent crashes
if platform.system() == "Windows":
    # Disable GPU acceleration if causing issues
    os.environ.setdefault("QTWEBENGINE_DISABLE_SANDBOX", "1")
    # Use software rendering to avoid GPU driver issues
    os.environ.setdefault("QT_OPENGL", "software")
    # Disable ANGLE to use software rendering
    os.environ.setdefault("QT_ANGLE_PLATFORM", "d3d11")
    # Additional WebEngine stability settings
    os.environ.setdefault("QTWEBENGINE_CHROMIUM_FLAGS", "--disable-gpu --disable-software-rasterizer")
    # Disable WebEngine logging to reduce overhead
    os.environ.setdefault("QTWEBENGINE_DISABLE_LOGGING", "1")

from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtWebEngineWidgets import QWebEngineSettings

from Nobody.views import VideoDownloader


def main():
    """Launch the GUI application."""
    app = QApplication(sys.argv)
    app.setStyle("fusion")

    # Get resource path for frozen (PyInstaller) environment
    if getattr(sys, 'frozen', False):
        # Running as compiled executable
        if hasattr(sys, '_MEIPASS'):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.dirname(sys.executable)
    else:
        # Running as script
        base_path = project_root
    
    icon_paths = [
        os.path.join(base_path, "st2.icns"),
        os.path.join(project_root, "st2.icns"),
        os.path.join(base_path, "icon.ico"),
        os.path.join(project_root, "icon.ico"),
    ]

    for icon_path in icon_paths:
        if os.path.exists(icon_path):
            app.setWindowIcon(QIcon(icon_path))
            break

    QWebEngineSettings.globalSettings().setAttribute(QWebEngineSettings.WebGLEnabled, True)
    QWebEngineSettings.globalSettings().setAttribute(QWebEngineSettings.Accelerated2dCanvasEnabled, True)

    mainWindow = VideoDownloader()
    mainWindow.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

