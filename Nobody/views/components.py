"""UI 컴포넌트 (CheckBoxHeader, VideoHandler, MainThreadSignalEmitter)"""

from PyQt5.QtWidgets import QHeaderView, QCheckBox, QTableWidgetItem
from PyQt5.QtCore import QObject, Qt, pyqtSignal, pyqtSlot


class CheckBoxHeader(QHeaderView):
    """체크박스가 있는 테이블 헤더"""
    def __init__(self, parent=None):
        super().__init__(Qt.Horizontal, parent)
        self.setSectionResizeMode(QHeaderView.Fixed)
        self.setDefaultAlignment(Qt.AlignCenter)
        self.setCheckBox()

    def setCheckBox(self):
        self.cb = QCheckBox(self)
        self.cb.setChecked(False)
        self.sectionResized.connect(self.resizeCheckBox)
        self.cb.clicked.connect(self.selectAll)
        self.cb.setStyleSheet("QCheckBox { margin-left: 6px; margin-right: 6px; }")

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.resizeCheckBox()

    def resizeCheckBox(self):
        rect = self.sectionViewportPosition(0)
        self.cb.setGeometry(rect, 0, self.sectionSize(0), self.height())
        self.parent().setColumnWidth(0, self.cb.sizeHint().width())

    def selectAll(self):
        check_state = self.cb.isChecked()
        for row in range(self.parent().rowCount()):
            item = self.parent().item(row, 0)
            if item and isinstance(item, QTableWidgetItem):
                item.setCheckState(Qt.Checked if check_state else Qt.Unchecked)

    def updateState(self):
        all_checked = self.parent().rowCount() > 0
        for row in range(self.parent().rowCount()):
            item = self.parent().item(row, 0)
            if item is None or item.checkState() != Qt.Checked:
                all_checked = False
                break
        self.cb.setChecked(all_checked)


class VideoHandler(QObject):
    """비디오 핸들러"""
    @pyqtSlot(float)
    def handleVideoDuration(self, duration):
        from ..utils.logging import logger
        logger.debug(f"Video duration: {duration}")


class MainThreadSignalEmitter(QObject):
    """메인 스레드 시그널 에미터"""
    warning_message = pyqtSignal(str)

    def __init__(self):
        super().__init__()

    def emit_warning(self, message):
        self.warning_message.emit(message)


# 전역 인스턴스
main_thread_signal_emitter = MainThreadSignalEmitter()

