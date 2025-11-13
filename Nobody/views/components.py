"""Common UI components (header, signal helpers)."""

from PyQt5.QtWidgets import QHeaderView, QCheckBox, QTableWidgetItem
from PyQt5.QtCore import QObject, Qt, pyqtSignal, pyqtSlot


class CheckBoxHeader(QHeaderView):
    """Header that hosts a tri-state checkbox for select-all."""

    def __init__(self, parent=None):
        super().__init__(Qt.Horizontal, parent)
        self.setSectionResizeMode(QHeaderView.Fixed)
        self.setDefaultAlignment(Qt.AlignCenter)
        self._check_box = QCheckBox(self)
        self._check_box.setChecked(False)
        self._check_box.clicked.connect(self.selectAll)
        self._check_box.setStyleSheet("QCheckBox { margin-left: 6px; margin-right: 6px; }")
        self.sectionResized.connect(self._resize_check_box)

    def resizeEvent(self, event):  # noqa: N802 (Qt naming)
        super().resizeEvent(event)
        self._resize_check_box()

    def _resize_check_box(self):
        rect = self.sectionViewportPosition(0)
        self._check_box.setGeometry(rect, 0, self.sectionSize(0), self.height())
        if self.parent() is not None:
            self.parent().setColumnWidth(0, self._check_box.sizeHint().width())

    def selectAll(self):  # noqa: N802 (Qt naming)
        check_state = self._check_box.isChecked()
        table = self.parent()
        if table is None:
            return
        for row in range(table.rowCount()):
            item = table.item(row, 0)
            if item and isinstance(item, QTableWidgetItem):
                item.setCheckState(Qt.Checked if check_state else Qt.Unchecked)

    def updateState(self):  # noqa: N802 (Qt naming)
        table = self.parent()
        if table is None or table.rowCount() == 0:
            self._check_box.setChecked(False)
            return
        for row in range(table.rowCount()):
            item = table.item(row, 0)
            if item is None or item.checkState() != Qt.Checked:
                self._check_box.setChecked(False)
                return
        self._check_box.setChecked(True)


class VideoHandler(QObject):
    """Utility class to handle signals from video elements."""

    @pyqtSlot(float)
    def handleVideoDuration(self, duration):  # noqa: N802 (Qt naming)
        from ..utils.logging import logger

        logger.debug("Video duration: %s", duration)


class MainThreadSignalEmitter(QObject):
    """Expose cross-thread warning signal for presenters."""

    warning_message = pyqtSignal(str)

    def emit_warning(self, message):
        self.warning_message.emit(message)


main_thread_signal_emitter = MainThreadSignalEmitter()

