"""Entry point for the Nobody 3 application."""

import os
import sys
import platform

# Ensure project root is on sys.path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# WebEngine environment variables to prevent crashes
# Service Worker 관련 에러를 방지하기 위한 플래그 추가
chromium_flags = [
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

# Windows-specific WebEngine environment variables
if platform.system() == "Windows":
    # Disable GPU acceleration if causing issues
    os.environ.setdefault("QTWEBENGINE_DISABLE_SANDBOX", "1")
    # Use software rendering to avoid GPU driver issues
    os.environ.setdefault("QT_OPENGL", "software")
    # Disable ANGLE to use software rendering
    os.environ.setdefault("QT_ANGLE_PLATFORM", "d3d11")
    # Windows-specific GPU flags
    chromium_flags.extend([
        "--disable-gpu",
        "--disable-software-rasterizer",
    ])

# Apply Chromium flags for all platforms
flags_str = " ".join(chromium_flags)
os.environ.setdefault("QTWEBENGINE_CHROMIUM_FLAGS", flags_str)
# Disable WebEngine logging to reduce overhead
# (하지만 에러는 여전히 표시됨)
# os.environ.setdefault("QTWEBENGINE_DISABLE_LOGGING", "1")
# 주석 처리: 에러 추적을 위해 로깅 유지

# Initialize logging early for error tracking
try:
    from Nobody.utils.logging import logger
    logger_available = True
except Exception:
    logger_available = False
    logger = None

# Import after environment variables are set
from PyQt5.QtWidgets import QApplication  # noqa: E402
from PyQt5.QtGui import QIcon  # noqa: E402
from PyQt5.QtWebEngineWidgets import QWebEngineSettings  # noqa: E402

from Nobody.views import VideoDownloader  # noqa: E402


def main():
    """Launch the GUI application."""
    # Log startup information
    if logger_available:
        logger.info("Starting Nobody 3 application...")
        logger.info(f"Platform: {platform.system()} {platform.release()}")
        logger.info(f"Python: {sys.version}")
        flags = os.environ.get('QTWEBENGINE_CHROMIUM_FLAGS', 'None')
        logger.info(f"Chromium flags: {flags}")

    try:
        app = QApplication(sys.argv)
        app.setStyle("fusion")
        app.setApplicationName("Nobody 3")
        app.setOrganizationName("Nobody")

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

        # Try to load application icon
        icon_paths = [
            os.path.join(base_path, "st2.icns"),
            os.path.join(project_root, "st2.icns"),
            os.path.join(base_path, "icon.ico"),
            os.path.join(project_root, "icon.ico"),
        ]

        icon_loaded = False
        for icon_path in icon_paths:
            if os.path.exists(icon_path):
                try:
                    app.setWindowIcon(QIcon(icon_path))
                    icon_loaded = True
                    if logger_available:
                        logger.debug(f"Loaded icon from: {icon_path}")
                    break
                except Exception as icon_error:
                    if logger_available:
                        logger.warning(
                            f"Failed to load icon {icon_path}: {icon_error}"
                        )

        if not icon_loaded and logger_available:
            logger.warning("No application icon found, using default")

        # Configure WebEngine settings
        try:
            settings = QWebEngineSettings.globalSettings()
            settings.setAttribute(QWebEngineSettings.WebGLEnabled, True)
            settings.setAttribute(
                QWebEngineSettings.Accelerated2dCanvasEnabled, True
            )
            if 'logger' in locals():
                logger.debug("WebEngine settings configured")
        except Exception as settings_error:
            if 'logger' in locals():
                logger.error(
                    f"Failed to configure WebEngine settings: {settings_error}"
                )
            # Continue anyway - WebEngine may still work with defaults

        # Create and show main window
        try:
            if logger_available:
                logger.info("Initializing main window...")
            mainWindow = VideoDownloader()
            mainWindow.show()
            if logger_available:
                logger.info("Application started successfully")
            sys.exit(app.exec_())
        except Exception as window_error:
            if logger_available:
                logger.critical(
                    f"Failed to create main window: {window_error}",
                    exc_info=True
                )
            else:
                print(
                    f"Critical error: Failed to create main window: "
                    f"{window_error}"
                )
            # Show user-friendly error message
            try:
                from PyQt5.QtWidgets import QMessageBox
                error_msg = QMessageBox()
                error_msg.setIcon(QMessageBox.Critical)
                error_msg.setWindowTitle("Application Error")
                error_msg.setText("Failed to start the application.")
                error_msg.setInformativeText(
                    f"Error: {str(window_error)}\n\n"
                    "Please check the log file for more details."
                )
                error_msg.exec_()
            except Exception:
                # Ignore errors when showing error dialog
                pass
            sys.exit(1)

    except Exception as app_error:
        # Catch-all for any other errors during initialization
        error_msg = (
            f"Critical error during application initialization: {app_error}\n"
            f"Platform: {platform.system()}\n"
            f"Python: {sys.version}"
        )
        if logger_available:
            logger.critical(error_msg, exc_info=True)
        else:
            print(error_msg)
        sys.exit(1)


if __name__ == "__main__":
    main()
