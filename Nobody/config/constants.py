"""애플리케이션 상수 정의"""

# Dark Theme 스타일 시트
DARK_THEME_STYLESHEET = """
        QDialog { background-color: #2D2D2D; }
        QPushButton { background-color: #333333; color: #FFFFFF; border: 2px solid #555555; border-radius: 5px; padding: 5px; }
        QPushButton:hover { background-color: #555555; }
        QPushButton:pressed { background-color: #444444; }
        QComboBox { background-color: #333333; color: #FFFFFF; border: 2px solid #555555; border-radius: 5px; padding: 3px; }
        QComboBox QAbstractItemView { background: #2D2D2D; selection-background-color: #3D3D3D; color: #FFFFFF; }
        QLineEdit, QTextEdit { background-color: #333333; color: #FFFFFF; border: 2px solid #555555; }
        QTableWidget { background-color: #2D2D2D; color: #FFFFFF; border: none; }
        QTableWidget::item { background-color: #333333; color: #FFFFFF; border: 1px solid #2D2D2D; }
        QLabel { color: #FFFFFF; }
        QHeaderView::section { background-color: #333333; color: #FFFFFF; padding: 4px; border: 1px solid #2D2D2D; }
        QProgressBar { border: 2px solid #333333; border-radius: 5px; background-color: #2D2D2D; text-align: center; }
        QProgressBar::chunk { background-color: #555555; }
"""

