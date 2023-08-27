from PyQt6.QtWidgets import QPlainTextEdit
from PyQt6.QtCore import Qt

class AutoExpandingTextEdit(QPlainTextEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        single_line_height = self.fontMetrics().height()
        self.min_height = 50
        self.setFixedHeight(single_line_height + 4)  # Added padding of 4
        self.textChanged.connect(self.updateSize)
        self.max_lines = 5  # Set max number of lines
        self.updateSize()
        
    def updateSize(self):
        # Get number of lines
        num_lines = self.blockCount()
        
        # Calculate new height
        single_line_height = self.fontMetrics().height()
        new_height = min(num_lines, self.max_lines) * (single_line_height + 4)  # Added padding of 4
        
        new_height = max(self.min_height, new_height)
        # Update the height and scrollbar policy
        if self.height() != new_height:
            self.setFixedHeight(new_height)
            if num_lines > self.max_lines:
                self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
            else:
                self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
