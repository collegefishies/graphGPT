"""

This module contains the InputBox class, which serves as the text input 
and control area for a chat application.

Classes:
    - InputBox: A QWidget subclass that holds an AutoExpandingTextEdit and control buttons.
"""

from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QSizePolicy
from . import AutoExpandingTextEdit

class InputBox(QWidget):
    """A custom QWidget that contains an AutoExpandingTextEdit and control buttons.
    
    Methods:
        - handleSend: Triggered to add a new message to the chat.
        - handleQueue: Triggered to add a new message to the chat with no response.
    """
    
    def __init__(self, *args, **kwargs):
        """Initialize the InputBox widget."""
        super().__init__(*args, **kwargs)
        self._initUI()
        
    def _initUI(self):
        """Initialize the user interface components."""
        self._createTextEdit()
        self._createButtons()
        self._setupLayout()

    def _createTextEdit(self):
        """Create an instance of AutoExpandingTextEdit."""
        self.text_edit = AutoExpandingTextEdit()
        self.text_edit.setPlaceholderText("Type a message...")

    def _createButtons(self):
        """Create Send and Pop buttons."""
        self.sendButton = QPushButton("Send")
        self.queueButton = QPushButton("Queue")
        self.sendButton.clicked.connect(self.handleSend)
        self.queueButton.clicked.connect(self.handleQueue)
        
    def _setupLayout(self):
        """Setup QHBoxLayout to house the text edit and buttons."""
        layout = QHBoxLayout()
        layout.addWidget(self.text_edit)
        layout.addWidget(self.queueButton)
        layout.addWidget(self.sendButton)
        self.setLayout(layout)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

    def handleSend(self):
        """Trigger to add a new message to the MessageBoxWidget."""
        self.parent().addNewMessage()

    def handleQueue(self):
        """Trigger to remove the oldest message from the MessageBoxWidget."""
        self.parent().queueMessage()
