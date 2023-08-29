"""

This module contains the ChatBoxWidget class, which serves as the central
widget to house the message display area and the text input area for a chat
application.

Classes:
    - ChatBoxWidget: The main QWidget subclass that composes MessageBoxWidget and InputBox.
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout
from . import InputBox, MessageBoxWidget
from ChatGPT import response
class ChatBoxWidget(QWidget):
    """A widget that combines MessageBoxWidget and InputBox into a chat interface.

    Methods:
        - addNewMessage: Adds a new message to the MessageBoxWidget from InputBox.
        - popMessage: Removes and returns the oldest message from MessageBoxWidget.
    """
    
    def __init__(self, *args, **kwargs):
        """Initialize the ChatBoxWidget."""
        super().__init__(*args, **kwargs)
        self._initUI()
        
    def _initUI(self):
        """Initialize the user interface components."""
        self.message_box = MessageBoxWidget()
        self.input_box = InputBox()
        self._setupLayout()

    def _setupLayout(self):
        """Setup QVBoxLayout to house MessageBoxWidget and InputBox."""
        layout = QVBoxLayout()
        layout.addWidget(self.message_box, 1)
        layout.addWidget(self.input_box, 0)
        self.setLayout(layout)

    def addNewMessage(self):
        """Add a new message to the MessageBoxWidget."""
        new_message = self.input_box.text_edit.toPlainText()
        if new_message:
            self.message_box.addMessage(new_message)
            self.input_box.text_edit.clear()

    def popMessage(self):
        """Remove and return the oldest message from MessageBoxWidget."""
        return self.message_box.popMessage()
