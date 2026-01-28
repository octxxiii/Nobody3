"""Address bar widget for browser."""

from PyQt5.QtCore import Qt, pyqtSignal, QUrl
from PyQt5.QtWidgets import QLineEdit, QHBoxLayout, QWidget, QPushButton, QLabel
from PyQt5.QtGui import QIcon

from ..utils.logging import logger


class AddressBar(QLineEdit):
    """Address bar widget with URL validation and navigation."""

    url_entered = pyqtSignal(str)  # Emitted when user presses Enter
    url_changed = pyqtSignal(str)  # Emitted when URL changes

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setPlaceholderText("Enter URL or search...")
        self.returnPressed.connect(self._on_return_pressed)
        self.textChanged.connect(self._on_text_changed)
        self._last_valid_url = ""

    def _on_return_pressed(self):
        """Handle Enter key press."""
        text = self.text().strip()
        if text:
            # If it looks like a URL, emit as-is
            if text.startswith(("http://", "https://")):
                self.url_entered.emit(text)
            # If it starts with '?', treat as search
            elif text.startswith("?"):
                self.url_entered.emit(text[1:])
            # Otherwise, try to make it a URL
            else:
                # Check if it contains a dot (might be a domain)
                if "." in text and " " not in text:
                    url = f"https://{text}"
                    self.setText(url)
                    self.url_entered.emit(url)
                else:
                    # Treat as search query
                    self.url_entered.emit(text)

    def _on_text_changed(self, text: str):
        """Handle text changes."""
        self.url_changed.emit(text)

    def set_url(self, url: str):
        """Set the address bar URL.
        
        Args:
            url: URL to display
        """
        if url != self.text():
            self.setText(url)
            self._last_valid_url = url

    def get_url(self) -> str:
        """Get current URL from address bar.
        
        Returns:
            Current URL string
        """
        return self.text().strip()


class BrowserToolbar(QWidget):
    """Browser toolbar with address bar and navigation buttons."""

    url_entered = pyqtSignal(str)
    back_requested = pyqtSignal()
    forward_requested = pyqtSignal()
    refresh_requested = pyqtSignal()
    home_requested = pyqtSignal()
    zoom_in_requested = pyqtSignal()
    zoom_out_requested = pyqtSignal()
    zoom_reset_requested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.address_bar = AddressBar(self)
        self.address_bar.url_entered.connect(self.url_entered.emit)
        self.setup_ui()

    def setup_ui(self):
        """Set up the toolbar UI."""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)

        # Navigation buttons
        self.back_button = QPushButton("👈")
        self.back_button.setFixedSize(30, 30)
        self.back_button.setToolTip("Back")
        self.back_button.clicked.connect(self.back_requested.emit)

        self.forward_button = QPushButton("👉")
        self.forward_button.setFixedSize(30, 30)
        self.forward_button.setToolTip("Forward")
        self.forward_button.clicked.connect(self.forward_requested.emit)

        self.refresh_button = QPushButton("🔄")
        self.refresh_button.setFixedSize(30, 30)
        self.refresh_button.setToolTip("Refresh (Ctrl+R)")
        self.refresh_button.clicked.connect(self.refresh_requested.emit)

        self.home_button = QPushButton()
        self.home_button.setFixedSize(30, 30)
        self.home_button.setIcon(QIcon(":/homeIcon"))
        self.home_button.setToolTip("Home")
        self.home_button.clicked.connect(self.home_requested.emit)

        # Zoom controls
        self.zoom_out_button = QPushButton("−")
        self.zoom_out_button.setFixedSize(25, 25)
        self.zoom_out_button.setToolTip("Zoom Out (Ctrl+-)")
        self.zoom_out_button.clicked.connect(self._on_zoom_out)

        self.zoom_label = QLabel("100%")
        self.zoom_label.setFixedWidth(40)
        self.zoom_label.setAlignment(Qt.AlignCenter)

        self.zoom_in_button = QPushButton("+")
        self.zoom_in_button.setFixedSize(25, 25)
        self.zoom_in_button.setToolTip("Zoom In (Ctrl++)")
        self.zoom_in_button.clicked.connect(self._on_zoom_in)

        self.zoom_reset_button = QPushButton("0")
        self.zoom_reset_button.setFixedSize(25, 25)
        self.zoom_reset_button.setToolTip("Reset Zoom (Ctrl+0)")
        self.zoom_reset_button.clicked.connect(self._on_zoom_reset)

        # Address bar
        layout.addWidget(self.back_button)
        layout.addWidget(self.forward_button)
        layout.addWidget(self.refresh_button)
        layout.addWidget(self.home_button)
        layout.addWidget(self.address_bar, 1)  # Stretch address bar
        layout.addWidget(self.zoom_out_button)
        layout.addWidget(self.zoom_label)
        layout.addWidget(self.zoom_in_button)
        layout.addWidget(self.zoom_reset_button)

    def set_url(self, url: str):
        """Set the address bar URL.
        
        Args:
            url: URL to display
        """
        self.address_bar.set_url(url)

    def get_url(self) -> str:
        """Get current URL from address bar.
        
        Returns:
            Current URL string
        """
        return self.address_bar.get_url()

    def update_navigation_state(self, can_go_back: bool, can_go_forward: bool):
        """Update navigation button states.
        
        Args:
            can_go_back: Whether browser can go back
            can_go_forward: Whether browser can go forward
        """
        self.back_button.setEnabled(can_go_back)
        self.forward_button.setEnabled(can_go_forward)

    def update_zoom(self, zoom_factor: float):
        """Update zoom display.
        
        Args:
            zoom_factor: Current zoom factor (0.25 to 5.0)
        """
        zoom_percent = int(zoom_factor * 100)
        self.zoom_label.setText(f"{zoom_percent}%")

    def _on_zoom_in(self):
        """Handle zoom in button click."""
        self.zoom_in_requested.emit()

    def _on_zoom_out(self):
        """Handle zoom out button click."""
        self.zoom_out_requested.emit()

    def _on_zoom_reset(self):
        """Handle zoom reset button click."""
        self.zoom_reset_requested.emit()

    def update_zoom_label(self, zoom_factor: float):
        """Update zoom label.
        
        Args:
            zoom_factor: Current zoom factor (1.0 = 100%)
        """
        self.zoom_label.setText(f"{int(zoom_factor * 100)}%")
