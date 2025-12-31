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
    # Service Worker 관련 에러를 방지하기 위한 플래그 추가
    chromium_flags = [
        "--disable-gpu",
        "--disable-software-rasterizer",
        # Service Worker 백그라운드 네트워킹 비활성화
        "--disable-background-networking",
        # 백그라운드 타이머 스로틀링 비활성화
        "--disable-background-timer-throttling",
        # 가려진 창 백그라운드 처리 비활성화
        "--disable-backgrounding-occluded-windows",
        # 렌더러 백그라운드 처리 비활성화
        "--disable-renderer-backgrounding",
        # 번역 UI 비활성화 (Service Worker 사용 감소)
        "--disable-features=TranslateUI",
    ]
    flags_str = " ".join(chromium_flags)
    os.environ.setdefault("QTWEBENGINE_CHROMIUM_FLAGS", flags_str)
    # Disable WebEngine logging to reduce overhead
    # (하지만 에러는 여전히 표시됨)
    # os.environ.setdefault("QTWEBENGINE_DISABLE_LOGGING", "1")
    # 주석 처리: 에러 추적을 위해 로깅 유지

# Import after environment variables are set
from PyQt5.QtWidgets import QApplication  # noqa: E402
from PyQt5.QtGui import QIcon  # noqa: E402
from PyQt5.QtWebEngineWidgets import QWebEngineSettings  # noqa: E402

from Nobody.views import VideoDownloader  # noqa: E402


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

    settings = QWebEngineSettings.globalSettings()
    settings.setAttribute(QWebEngineSettings.WebGLEnabled, True)
    settings.setAttribute(
        QWebEngineSettings.Accelerated2dCanvasEnabled, True
    )

    mainWindow = VideoDownloader()
    mainWindow.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
