"""Video table management utilities."""

import re
from typing import List, Tuple, Optional

import requests
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QComboBox, QTableWidget, QTableWidgetItem

from ..utils.logging import logger
from .components import CheckBoxHeader

FormatInfo = Tuple[str, Optional[str], str, int]


class VideoTableManager:
    """Encapsulates QTableWidget setup and updates for VideoDownloader."""

    def __init__(self, host, table: QTableWidget):
        self.host = host
        self.table = table
        self.header: CheckBoxHeader | None = None

    def initialize(self):
        """Initial table setup."""
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["", "Thumbnail", "Title", "Format"])
        header = CheckBoxHeader()
        self.table.setHorizontalHeader(header)
        header.cb.clicked.connect(header.selectAll)
        self.table.horizontalHeader().setSectionResizeMode(1, self.table.horizontalHeader().ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(2, self.table.horizontalHeader().Stretch)
        self.table.horizontalHeader().setVisible(True)
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setShowGrid(False)
        self.table.setColumnWidth(0, 100)
        self.table.setColumnWidth(1, 150)
        self.table.setColumnWidth(2, 300)
        self.table.setColumnWidth(3, 180)
        self.table.itemChanged.connect(self._handle_item_changed)
        self.header = header

    def update_video_list(
        self,
        title: str,
        thumbnail_url: str,
        video_url: str,
        formats_info_list: List[FormatInfo],
    ):
        """Add a new video row with thumbnail and format dropdown."""
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)
        self.host.video_info_list.append((title, video_url))

        checkbox_item = QTableWidgetItem()
        checkbox_item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
        checkbox_item.setCheckState(Qt.Unchecked)
        self.table.setItem(row_position, 0, checkbox_item)

        title_item = QTableWidgetItem(title)
        title_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable)
        self.table.setItem(row_position, 2, title_item)

        if thumbnail_url:
            self._load_thumbnail(row_position, thumbnail_url)

        format_combo = QComboBox()
        filtered_formats = self._filter_formats(formats_info_list)

        current_category = None
        if not filtered_formats:
            format_combo.addItem("No available formats", None)
        else:
            for display_text, format_id, type_label, _ in filtered_formats:
                if type_label != current_category:
                    if format_combo.count() > 0 and current_category is not None:
                        pass
                    format_combo.addItem(f"--- {type_label} --- ")
                    format_combo.model().item(format_combo.count() - 1).setEnabled(False)
                    current_category = type_label
                format_combo.addItem(display_text, userData=format_id)

        self._select_default_format(format_combo)
        self.table.setCellWidget(row_position, 3, format_combo)

    def apply_filters(self):
        """Reapply format filters to existing rows."""
        row_count = self.table.rowCount()
        for row in range(row_count):
            format_combo = self.table.cellWidget(row, 3)
            if not format_combo or not isinstance(format_combo, QComboBox):
                continue

            current_format_id = format_combo.currentData()
            all_formats: List[FormatInfo] = []
            for i in range(format_combo.count()):
                if not format_combo.model().item(i).isEnabled():
                    continue
                item_text = format_combo.itemText(i)
                item_data = format_combo.itemData(i)
                type_label = "Unknown"
                if "[Video]" in item_text:
                    type_label = "Video"
                elif "[Video-only]" in item_text:
                    type_label = "Video-only"
                elif "[Audio-only]" in item_text:
                    type_label = "Audio-only"
                filesize = 0
                match = re.search(r"(\d+)MB", item_text)
                if match:
                    filesize = int(match.group(1)) * 1024 * 1024
                all_formats.append((item_text, item_data, type_label, filesize))

            filtered_formats = self._filter_formats(all_formats)
            format_combo.clear()
            current_category = None
            found_current = False
            for display_text, format_id, type_label, _ in filtered_formats:
                if type_label != current_category:
                    format_combo.addItem(f"--- {type_label} --- ")
                    format_combo.model().item(format_combo.count() - 1).setEnabled(False)
                    current_category = type_label
                format_combo.addItem(display_text, userData=format_id)
                if format_id == current_format_id:
                    format_combo.setCurrentIndex(format_combo.count() - 1)
                    found_current = True

            if not found_current and format_combo.count() > 0:
                for i in range(format_combo.count()):
                    if format_combo.model().item(i).isEnabled():
                        format_combo.setCurrentIndex(i)
                        break

    # Internal helpers -------------------------------------------------

    def _handle_item_changed(self, item):
        if item.column() == 0 and self.header:
            self.header.updateState()

    def _load_thumbnail(self, row_position: int, thumbnail_url: str):
        try:
            response = requests.get(thumbnail_url, timeout=10)
            response.raise_for_status()
            pixmap = QPixmap()
            if pixmap.loadFromData(response.content):
                pixmap_resized = pixmap.scaled(30, 30, Qt.KeepAspectRatio)
                thumbnail_item = QTableWidgetItem()
                thumbnail_item.setData(Qt.DecorationRole, pixmap_resized)
                self.table.setItem(row_position, 1, thumbnail_item)
        except requests.exceptions.Timeout:
            logger.warning("Thumbnail request timed out: %s", thumbnail_url)
        except requests.exceptions.RequestException as exc:
            logger.warning("Thumbnail download failed: %s - %s", thumbnail_url, exc)
        except Exception as exc:  # pragma: no cover - defensive
            logger.error("Thumbnail processing error: %s", exc)

    def _filter_formats(self, formats_info_list: List[FormatInfo]) -> List[FormatInfo]:
        if not formats_info_list:
            return formats_info_list

        filtered = []
        settings = self.host.app_settings
        for display_text, format_id, type_label, filesize in formats_info_list:
            if type_label == "Video" and not settings.show_video_formats:
                continue
            if type_label == "Audio-only" and not settings.show_audio_only:
                continue
            if type_label == "Video-only" and not settings.show_video_formats:
                continue

            if type_label in ["Video", "Video-only"] and settings.max_quality > 0:
                resolution_match = re.search(r"(\d+)x(\d+)", display_text)
                if resolution_match:
                    height = int(resolution_match.group(2))
                    if height > settings.max_quality:
                        continue
            filtered.append((display_text, format_id, type_label, filesize))
        return filtered

    def _select_default_format(self, combo: QComboBox):
        if combo.count() == 0:
            return
        preferred_format = self.host.app_settings.default_format.lower()
        best_match_index = -1
        partial_match_index = -1
        for i in range(combo.count()):
            if not combo.model().item(i).isEnabled():
                continue
            item_text = combo.itemText(i).lower()
            item_data = combo.itemData(i)
            if item_data:
                format_id_str = str(item_data).lower()
                if preferred_format in format_id_str:
                    best_match_index = i
                    break
            if preferred_format in ["mp3", "mp4", "webm", "m4a"]:
                if f".{preferred_format}" in item_text or f" {preferred_format} " in item_text:
                    if best_match_index == -1:
                        best_match_index = i
                elif preferred_format in item_text and partial_match_index == -1:
                    partial_match_index = i
            elif preferred_format in item_text and partial_match_index == -1:
                partial_match_index = i

        target_index = best_match_index
        if target_index == -1:
            target_index = partial_match_index
        if target_index == -1:
            for i in range(combo.count()):
                if combo.model().item(i).isEnabled():
                    target_index = i
                    break

        if target_index != -1:
            combo.setCurrentIndex(target_index)

    def delete_selected_videos(self):
        rows_to_remove = []
        for row in range(self.table.rowCount()):
            item = self.table.item(row, 0)
            if item and item.checkState() == Qt.Checked:
                rows_to_remove.append(row)

        for row in reversed(rows_to_remove):
            self.table.removeRow(row)
            if 0 <= row < len(self.host.video_info_list):
                del self.host.video_info_list[row]

    def get_selected_videos(self):
        selected_videos = []
        for row in range(self.table.rowCount()):
            item = self.table.item(row, 0)
            if item and item.checkState() == Qt.Checked:
                url = self.host.video_info_list[row][1]
                combo = self.table.cellWidget(row, 3)
                format_id = None
                if isinstance(combo, QComboBox):
                    format_id = combo.currentData()
                selected_videos.append((row, url, format_id))
        return selected_videos

