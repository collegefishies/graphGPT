'''
    Input box that auto-expands to fit user input.
'''
from PyQt6.QtWidgets import QPlainTextEdit
from PyQt6.QtCore import Qt

class AutoExpandingTextEdit(QPlainTextEdit):
    """Custom QPlainTextEdit that auto-expands to a maximum number of lines."""

    def __init__(self, *args, **kwargs):
        """Initialize the text edit widget."""
        super().__init__(*args, **kwargs)
        self._set_initial_properties()
        self.textChanged.connect(self.updateSize)

    def _set_initial_properties(self):
        """Set initial properties for the widget."""
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.min_height = 50
        self.max_lines = 5
        single_line_height = self.fontMetrics().height()
        self.setFixedHeight(single_line_height + 4)  # 4 px padding
        self.updateSize()

    def updateSize(self):
        """Update the widget size based on the number of lines of text."""
        num_lines = self.blockCount()
        single_line_height = self.fontMetrics().height()
        new_height = min(num_lines, self.max_lines) * (single_line_height + 4)
        new_height = max(self.min_height, new_height)
        
        if self.height() != new_height:
            self._update_height_and_scrollbar(new_height, num_lines)

    def _update_height_and_scrollbar(self, new_height, num_lines):
        """Update the widget height and vertical scrollbar policy."""
        self.setFixedHeight(new_height)
        scrollbar_policy = Qt.ScrollBarPolicy.ScrollBarAsNeeded if num_lines > self.max_lines else Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        self.setVerticalScrollBarPolicy(scrollbar_policy)
