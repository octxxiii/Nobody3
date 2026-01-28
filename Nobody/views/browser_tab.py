"""Browser tab widget for multi-tab browsing."""

from PyQt5.QtCore import Qt, pyqtSignal, QUrl
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QLabel
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings

from ..utils.logging import logger


class BrowserTab(QWidget):
    """Single browser tab containing a QWebEngineView."""

    url_changed = pyqtSignal(QUrl)
    title_changed = pyqtSignal(str)
    load_finished = pyqtSignal(bool)
    close_requested = pyqtSignal()

    def __init__(self, parent=None, url: QUrl = None):
        super().__init__(parent)
        self.url = url or QUrl("https://www.youtube.com")
        self.setup_ui()

    def setup_ui(self):
        """Set up the tab UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        try:
            self.browser = QWebEngineView(self)
            self.browser.setUrl(self.url)
            self.browser.urlChanged.connect(self.url_changed.emit)
            self.browser.titleChanged.connect(self.title_changed.emit)
            self.browser.loadFinished.connect(self.load_finished.emit)

            # Configure settings
            settings = self.browser.settings()
            settings.setAttribute(QWebEngineSettings.JavascriptEnabled, True)
            settings.setAttribute(QWebEngineSettings.PluginsEnabled, True)
            settings.setAttribute(QWebEngineSettings.LocalStorageEnabled, True)

            layout.addWidget(self.browser)
        except Exception as e:
            logger.error(f"Failed to create browser in tab: {e}")
            error_label = QLabel(f"Browser initialization failed: {e}")
            error_label.setStyleSheet("color: red; padding: 20px;")
            layout.addWidget(error_label)

    def set_url(self, url: QUrl):
        """Set the URL for this tab.
        
        Args:
            url: URL to load
        """
        if hasattr(self, 'browser') and self.browser:
            self.browser.setUrl(url)
            self.url = url

    def get_url(self) -> QUrl:
        """Get current URL.
        
        Returns:
            Current URL
        """
        if hasattr(self, 'browser') and self.browser:
            return self.browser.url()
        return self.url

    def reload(self):
        """Reload the current page."""
        if hasattr(self, 'browser') and self.browser:
            self.browser.reload()

    def back(self):
        """Navigate back."""
        if hasattr(self, 'browser') and self.browser:
            self.browser.back()

    def forward(self):
        """Navigate forward."""
        if hasattr(self, 'browser') and self.browser:
            self.browser.forward()

    def can_go_back(self) -> bool:
        """Check if can go back.
        
        Returns:
            True if can go back
        """
        if hasattr(self, 'browser') and self.browser:
            return self.browser.history().canGoBack()
        return False

    def can_go_forward(self) -> bool:
        """Check if can go forward.
        
        Returns:
            True if can go forward
        """
        if hasattr(self, 'browser') and self.browser:
            return self.browser.history().canGoForward()
        return False

    def close_tab(self):
        """Close this tab."""
        if hasattr(self, 'browser') and self.browser:
            self.browser.deleteLater()
        self.deleteLater()


class BrowserTabWidget(QWidget):
    """Tab widget container with tab bar and content area."""

    current_changed = pyqtSignal(int)
    tab_close_requested = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.tabs = []
        self.current_index = -1
        self.setup_ui()

    def setup_ui(self):
        """Set up the tab widget UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Tab bar
        self.tab_bar = QWidget()
        self.tab_bar_layout = QHBoxLayout(self.tab_bar)
        self.tab_bar_layout.setContentsMargins(5, 5, 5, 0)
        self.tab_bar_layout.setSpacing(2)
        layout.addWidget(self.tab_bar)

        # Content area
        self.content_stack = QWidget()
        self.content_layout = QVBoxLayout(self.content_stack)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.content_stack, 1)

        # New tab button
        self.new_tab_button = QPushButton("+")
        self.new_tab_button.setFixedSize(30, 30)
        self.new_tab_button.setToolTip("New Tab (Ctrl+T)")
        self.tab_bar_layout.addWidget(self.new_tab_button)

        self.current_tab_changed = pyqtSignal(int)

    def add_tab(self, url: QUrl = None, title: str = "New Tab") -> BrowserTab:
        """Add a new tab.
        
        Args:
            url: Initial URL (optional)
            title: Tab title (optional)
            
        Returns:
            Index of new tab
        """
        tab = BrowserTab(self.content_stack, url)
        tab_index = len(self.tabs)
        self.tabs.append(tab)

        # Create tab button
        tab_button = QPushButton(title)
        tab_button.setCheckable(True)
        tab_button.setFixedHeight(30)
        tab_button.clicked.connect(lambda: self.set_current_tab(tab_index))
        close_button = QPushButton("×")
        close_button.setFixedSize(20, 20)
        close_button.clicked.connect(
            lambda: self.close_tab(tab_index)
        )

        tab_header = QWidget()
        tab_header_layout = QHBoxLayout(tab_header)
        tab_header_layout.setContentsMargins(5, 0, 5, 0)
        tab_header_layout.setSpacing(2)
        tab_header_layout.addWidget(tab_button)
        tab_header_layout.addWidget(close_button)

        self.tab_bar_layout.addWidget(tab_header)
        self.content_layout.addWidget(tab)

        # Connect signals
        tab.title_changed.connect(
            lambda t: self._update_tab_title(tab_index, t)
        )

        # Set as current if first tab
        if tab_index == 0:
            self.set_current_tab(0)
        else:
            tab.hide()

        return tab

    def set_current_tab(self, index: int):
        """Set the current active tab.
        
        Args:
            index: Tab index
        """
        if 0 <= index < len(self.tabs):
            # Hide all tabs
            for tab in self.tabs:
                tab.hide()

            # Show current tab
            self.tabs[index].show()
            self.current_index = index

            # Update tab buttons
            for i, widget in enumerate(self.tab_bar_layout.children()):
                if isinstance(widget, QWidget):
                    buttons = widget.findChildren(QPushButton)
                    if buttons:
                        buttons[0].setChecked(i == index)

            self.current_changed.emit(index)

    def close_tab(self, index: int):
        """Close a tab.
        
        Args:
            index: Tab index to close
        """
        if 0 <= index < len(self.tabs):
            # Don't close if it's the last tab
            if len(self.tabs) == 1:
                return

            # Remove tab
            tab = self.tabs.pop(index)
            tab.close_tab()

            # Remove tab button
            widget = self.tab_bar_layout.itemAt(index).widget()
            if widget:
                widget.deleteLater()

            # Adjust current index
            if self.current_index >= index:
                self.current_index -= 1
                if self.current_index < 0:
                    self.current_index = 0

            # Set new current tab
            if self.tabs:
                self.set_current_tab(self.current_index)

            self.tab_close_requested.emit(index)

    def get_current_tab(self) -> BrowserTab:
        """Get the current active tab.
        
        Returns:
            Current BrowserTab or None
        """
        if 0 <= self.current_index < len(self.tabs):
            return self.tabs[self.current_index]
        return None

    def _update_tab_title(self, index: int, title: str):
        """Update tab title.
        
        Args:
            index: Tab index
            title: New title
        """
        if 0 <= index < len(self.tabs):
            widget = self.tab_bar_layout.itemAt(index).widget()
            if widget:
                buttons = widget.findChildren(QPushButton)
                if buttons:
                    # Truncate long titles
                    display_title = title[:20] + "..." if len(title) > 20 else title
                    buttons[0].setText(display_title)
