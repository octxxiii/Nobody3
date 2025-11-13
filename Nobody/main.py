"""Entry point for the Nobody 3 application."""

import os
import sys
import platform

# Ensure project root is on sys.path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtWebEngineWidgets import QWebEngineSettings, QWebEngineView

from Nobody.views import VideoDownloader


def main():
    """Launch the GUI application."""
    app = QApplication(sys.argv)
    app.setStyle("fusion")

    icon_paths = []
    if platform.system() == "Windows":
        icon_paths = [
            os.path.join(project_root, "icon.ico"),
            os.path.join(project_root, "st2.icns"),
        ]
    else:
        icon_paths = [
            os.path.join(project_root, "icon.icns"),
            os.path.join(project_root, "st2.icns"),
        ]

    for icon_path in icon_paths:
        if os.path.exists(icon_path):
            app.setWindowIcon(QIcon(icon_path))
            break

    QWebEngineSettings.globalSettings().setAttribute(QWebEngineSettings.WebGLEnabled, True)
    QWebEngineSettings.globalSettings().setAttribute(QWebEngineSettings.Accelerated2dCanvasEnabled, True)

    mainWindow = VideoDownloader()
    mainWindow.show()
    QWebEngineView()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

