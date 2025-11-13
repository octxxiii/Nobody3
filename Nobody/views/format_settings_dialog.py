"""포맷 설정 다이얼로그"""

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, QComboBox,
                             QPushButton, QCheckBox, QGroupBox)
from PyQt5.QtCore import pyqtSignal
from ..models.settings import AppSettings


class FormatSettingsDialog(QDialog):
    """포맷 설정 다이얼로그"""
    settingsChanged = pyqtSignal()
    
    def __init__(self, parent=None, app_settings=None):
        super(FormatSettingsDialog, self).__init__(parent)
        self.app_settings = app_settings or AppSettings()
        self.setWindowTitle('포맷 설정')
        self.setModal(True)
        self.setFixedSize(450, 420)
        self.setupUI()
        
    def setupUI(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)
        
        # 기본 포맷 설정
        default_group = QGroupBox("기본 포맷")
        default_layout = QVBoxLayout()
        default_layout.setContentsMargins(10, 15, 10, 10)
        default_layout.setSpacing(8)
        
        default_label = QLabel("기본 선택 포맷:")
        self.default_format_combo = QComboBox()
        self.default_format_combo.addItems(['mp3', 'mp4', 'webm', 'm4a', 'best'])
        self.default_format_combo.setCurrentText(self.app_settings.default_format)
        self.default_format_combo.setMinimumHeight(30)
        
        default_layout.addWidget(default_label)
        default_layout.addWidget(self.default_format_combo)
        default_group.setLayout(default_layout)
        
        # 표시할 포맷 설정
        display_group = QGroupBox("표시할 포맷")
        display_layout = QVBoxLayout()
        display_layout.setContentsMargins(10, 15, 10, 10)
        display_layout.setSpacing(5)
        
        self.show_video_check = QCheckBox("비디오 포맷 표시")
        self.show_video_check.setChecked(self.app_settings.show_video_formats)
        self.show_video_check.setMinimumHeight(20)
        
        self.show_audio_check = QCheckBox("오디오 포맷 표시")
        self.show_audio_check.setChecked(self.app_settings.show_audio_formats)
        self.show_audio_check.setMinimumHeight(20)
        
        self.show_audio_only_check = QCheckBox("오디오 전용 포맷 표시")
        self.show_audio_only_check.setChecked(self.app_settings.show_audio_only)
        self.show_audio_only_check.setMinimumHeight(20)
        
        display_layout.addWidget(self.show_video_check)
        display_layout.addWidget(self.show_audio_check)
        display_layout.addWidget(self.show_audio_only_check)
        display_group.setLayout(display_layout)
        
        # 품질 설정
        quality_group = QGroupBox("최대 품질")
        quality_layout = QVBoxLayout()
        quality_layout.setContentsMargins(10, 15, 10, 10)
        quality_layout.setSpacing(8)
        
        quality_label = QLabel("최대 품질:")
        self.quality_combo = QComboBox()
        self.quality_combo.addItems(['480p', '720p', '1080p', '무제한'])
        quality_map = {480: 0, 720: 1, 1080: 2, 0: 3}
        self.quality_combo.setCurrentIndex(quality_map.get(self.app_settings.max_quality, 1))
        self.quality_combo.setMinimumHeight(30)
        
        quality_layout.addWidget(quality_label)
        quality_layout.addWidget(self.quality_combo)
        quality_group.setLayout(quality_layout)
        
        # 버튼
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(0, 10, 0, 0)
        button_layout.setSpacing(10)
        
        self.save_button = QPushButton("저장")
        self.cancel_button = QPushButton("취소")
        self.save_button.setMinimumHeight(35)
        self.cancel_button.setMinimumHeight(35)
        self.save_button.clicked.connect(self.save_settings)
        self.cancel_button.clicked.connect(self.reject)
        
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)
        
        # 레이아웃 구성
        layout.addWidget(default_group)
        layout.addWidget(display_group)
        layout.addWidget(quality_group)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
        # 다크 테마 스타일 적용
        self.setStyleSheet("""
            QDialog {
                background-color: #2D2D2D;
                color: #FFFFFF;
                font-size: 12px;
            }
            QGroupBox {
                color: #FFFFFF;
                font-weight: bold;
                font-size: 13px;
                border: 2px solid #555555;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 5px;
            }
            QGroupBox::title {
                color: #FFFFFF;
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 8px 0 8px;
                background-color: #2D2D2D;
            }
            QLabel {
                color: #FFFFFF;
                font-size: 12px;
                padding: 2px;
            }
            QCheckBox {
                color: #FFFFFF;
                font-size: 12px;
                spacing: 8px;
                padding: 1px;
                margin: 2px 0px;
            }
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
                border: 2px solid #555555;
                border-radius: 3px;
                background-color: #333333;
            }
            QCheckBox::indicator:checked {
                background-color: #666666;
                border: 2px solid #777777;
            }
            QComboBox {
                background-color: #333333;
                color: #FFFFFF;
                border: 2px solid #555555;
                border-radius: 5px;
                padding: 5px;
                font-size: 12px;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox::down-arrow {
                image: none;
                border: 1px solid #FFFFFF;
                width: 0px;
                height: 0px;
                border-top: 4px solid #FFFFFF;
                border-left: 4px solid transparent;
                border-right: 4px solid transparent;
            }
            QComboBox QAbstractItemView {
                background: #2D2D2D;
                selection-background-color: #555555;
                color: #FFFFFF;
                border: 1px solid #555555;
            }
            QPushButton {
                background-color: #333333;
                color: #FFFFFF;
                border: 2px solid #555555;
                border-radius: 5px;
                padding: 8px;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #555555;
                border: 2px solid #777777;
            }
            QPushButton:pressed {
                background-color: #444444;
            }
        """)
        
    def save_settings(self):
        """설정 저장"""
        self.app_settings.default_format = self.default_format_combo.currentText()
        self.app_settings.show_video_formats = self.show_video_check.isChecked()
        self.app_settings.show_audio_formats = self.show_audio_check.isChecked()
        self.app_settings.show_audio_only = self.show_audio_only_check.isChecked()
        
        quality_map = {0: 480, 1: 720, 2: 1080, 3: 0}
        self.app_settings.max_quality = quality_map[self.quality_combo.currentIndex()]
        
        self.app_settings.save_settings()
        self.settingsChanged.emit()
        self.accept()

