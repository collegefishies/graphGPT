from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QHBoxLayout
from PyQt6.QtGui import QPixmap, QIcon

class MessageWidget(QWidget):
    def __init__(self, message, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Initialize parameters
        self.min_height = 50  # Minimum height of the message label
        self.message_padding = 10  # Padding at the top and bottom of the message
        
        # Create elements
        self.user_icon = QLabel("👤")
        
        self.message_label = QLabel(message)
        self.message_label.setWordWrap(True)
        self.message_label.setMinimumHeight(self.min_height)
        self.message_label.setContentsMargins(0, self.message_padding, 0, self.message_padding)
        
        self.button = QPushButton("Button")
        self.button.setFixedSize(40, 40)
        
        # Create horizontal layout
        layout = QHBoxLayout()
        layout.addWidget(self.user_icon)
        layout.addWidget(self.message_label, 1)  # The '1' makes this widget expand to fill available space
        layout.addWidget(self.button)
        
        self.setLayout(layout)
