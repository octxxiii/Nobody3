"""Nobody 애플리케이션 진입점"""

import os
import sys
import platform

# 프로젝트 루트를 Python 경로에 추가
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtWebEngineWidgets import QWebEngineSettings, QWebEngineView

# Nobody 모듈에서 VideoDownloader 임포트
from Nobody.views import VideoDownloader


def main():
    """애플리케이션 메인 함수"""
    app = QApplication(sys.argv)
    app.setStyle("fusion")  # Fusion 스타일을 설정합니다.
    
    # 플랫폼별 아이콘 설정 (프로젝트 루트에서 찾기)
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

    # Enable hardware acceleration
    QWebEngineSettings.globalSettings().setAttribute(QWebEngineSettings.WebGLEnabled, True)
    QWebEngineSettings.globalSettings().setAttribute(QWebEngineSettings.Accelerated2dCanvasEnabled, True)

    mainWindow = VideoDownloader()
    mainWindow.show()
    view = QWebEngineView()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

