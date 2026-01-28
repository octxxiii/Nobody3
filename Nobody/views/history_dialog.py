"""Download history dialog."""

from datetime import datetime
from PyQt5.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QLineEdit,
    QLabel,
    QMessageBox,
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon

from ..models.history import DownloadHistory
from ..config.constants import DARK_THEME_STYLESHEET
from ..utils.logging import logger


class HistoryDialog(QDialog):
    """Dialog for viewing and managing download history."""

    redownload_requested = pyqtSignal(str, str, str)  # url, title, format_id

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Download History")
        self.setModal(True)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.history = DownloadHistory()
        self.setup_ui()

    def setup_ui(self):
        """Set up the dialog UI."""
        layout = QVBoxLayout(self)

        # Search bar
        search_layout = QHBoxLayout()
        search_label = QLabel("Search:")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by title or URL...")
        self.search_input.textChanged.connect(self._on_search_changed)
        search_clear = QPushButton("Clear")
        search_clear.clicked.connect(self.search_input.clear)
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_input, 1)
        search_layout.addWidget(search_clear)
        layout.addLayout(search_layout)

        # History table
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(
            ["Title", "URL", "Format", "Date", "Path"]
        )
        self.table.horizontalHeader().setSectionResizeMode(
            0, QHeaderView.Stretch
        )
        self.table.horizontalHeader().setSectionResizeMode(
            1, QHeaderView.Stretch
        )
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(4, QHeaderView.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setAlternatingRowColors(True)
        self.table.doubleClicked.connect(self._on_row_double_clicked)
        layout.addWidget(self.table, 1)

        # Buttons
        button_layout = QHBoxLayout()
        self.redownload_button = QPushButton("Redownload")
        self.redownload_button.clicked.connect(self._on_redownload)
        self.delete_button = QPushButton("Delete")
        self.delete_button.clicked.connect(self._on_delete_selected)
        self.clear_all_button = QPushButton("Clear All")
        self.clear_all_button.clicked.connect(self._on_clear_all)
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.accept)

        button_layout.addWidget(self.redownload_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.clear_all_button)
        button_layout.addStretch()
        button_layout.addWidget(close_button)
        layout.addLayout(button_layout)

        self.setStyleSheet(DARK_THEME_STYLESHEET)
        self.setMinimumSize(800, 500)
        self._refresh_table()

    def _refresh_table(self, entries=None):
        """Refresh the history table.
        
        Args:
            entries: Optional list of entries to display. If None, shows all.
        """
        if entries is None:
            entries = self.history.get_recent_entries(limit=500)

        self.table.setRowCount(len(entries))
        for row, entry in enumerate(entries):
            # Title
            title_item = QTableWidgetItem(entry.get("title", "Unknown"))
            self.table.setItem(row, 0, title_item)

            # URL
            url_item = QTableWidgetItem(entry.get("url", ""))
            self.table.setItem(row, 1, url_item)

            # Format
            format_item = QTableWidgetItem(entry.get("format_id", "Unknown"))
            self.table.setItem(row, 2, format_item)

            # Date
            timestamp = entry.get("timestamp", "")
            if timestamp:
                try:
                    dt = datetime.fromisoformat(timestamp)
                    date_str = dt.strftime("%Y-%m-%d %H:%M:%S")
                except Exception:
                    date_str = timestamp
            else:
                date_str = "Unknown"
            date_item = QTableWidgetItem(date_str)
            self.table.setItem(row, 3, date_item)

            # Path
            path_item = QTableWidgetItem(entry.get("download_path", ""))
            self.table.setItem(row, 4, path_item)

    def _on_search_changed(self, text: str):
        """Handle search input changes."""
        if not text.strip():
            self._refresh_table()
        else:
            results = self.history.search_entries(text)
            self._refresh_table(results)

    def _on_row_double_clicked(self, index):
        """Handle double-click on a row to redownload."""
        row = index.row()
        entry = self._get_entry_for_row(row)
        if entry:
            self._redownload_entry(entry)

    def _on_redownload(self):
        """Handle redownload button click."""
        selected_rows = self.table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.information(
                self, "No Selection", "Please select an item to redownload."
            )
            return

        for index in selected_rows:
            entry = self._get_entry_for_row(index.row())
            if entry:
                self._redownload_entry(entry)

    def _on_delete_selected(self):
        """Handle delete button click."""
        selected_rows = self.table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.information(
                self, "No Selection", "Please select items to delete."
            )
            return

        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            f"Delete {len(selected_rows)} item(s)?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if reply == QMessageBox.Yes:
            # Delete in reverse order to maintain indices
            rows_to_delete = sorted(
                [idx.row() for idx in selected_rows], reverse=True
            )
            # Get entries in display order (most recent first)
            current_entries = []
            for row in range(self.table.rowCount()):
                entry = self._get_entry_for_row(row)
                if entry:
                    current_entries.append(entry)

            # Find and delete from history
            deleted = 0
            for row_idx in rows_to_delete:
                if 0 <= row_idx < len(current_entries):
                    entry = current_entries[row_idx]
                    # Find entry in history by matching URL and timestamp
                    for hist_idx, hist_entry in enumerate(self.history.entries):
                        if (hist_entry.get("url") == entry.get("url") and
                                hist_entry.get("timestamp") == entry.get("timestamp")):
                            if self.history.delete_entry(hist_idx):
                                deleted += 1
                            break

            if deleted > 0:
                self._refresh_table()
                QMessageBox.information(
                    self, "Deleted", f"Deleted {deleted} item(s)."
                )

    def _on_clear_all(self):
        """Handle clear all button click."""
        reply = QMessageBox.question(
            self,
            "Confirm Clear All",
            "Clear all download history? This cannot be undone.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if reply == QMessageBox.Yes:
            if self.history.clear_history():
                self._refresh_table()
                QMessageBox.information(
                    self, "Cleared", "All history has been cleared."
                )

    def _get_entry_for_row(self, row: int) -> dict:
        """Get history entry for a table row.
        
        Args:
            row: Table row index
            
        Returns:
            History entry dictionary or None
        """
        if row < 0 or row >= self.table.rowCount():
            return None

        url_item = self.table.item(row, 1)
        date_item = self.table.item(row, 3)
        if not url_item or not date_item:
            return None

        url = url_item.text()
        timestamp_str = date_item.text()

        # Find matching entry in history
        for entry in self.history.entries:
            if entry.get("url") == url:
                entry_timestamp = entry.get("timestamp", "")
                if entry_timestamp:
                    try:
                        dt = datetime.fromisoformat(entry_timestamp)
                        entry_date_str = dt.strftime("%Y-%m-%d %H:%M:%S")
                        if entry_date_str == timestamp_str:
                            return entry
                    except Exception:
                        if entry_timestamp == timestamp_str:
                            return entry
                else:
                    return entry

        return None

    def _redownload_entry(self, entry: dict):
        """Emit signal to redownload an entry.
        
        Args:
            entry: History entry dictionary
        """
        url = entry.get("url", "")
        title = entry.get("title", "")
        format_id = entry.get("format_id", "")

        if url and format_id:
            self.redownload_requested.emit(url, title, format_id)
            self.accept()
        else:
            QMessageBox.warning(
                self,
                "Invalid Entry",
                "Selected entry is missing required information.",
            )
