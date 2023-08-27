from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton
from PyQt6.QtWidgets import QSizePolicy
from . import AutoExpandingTextEdit
class InputBox(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Create an instance of AutoExpandingTextEdit
        self.text_edit = AutoExpandingTextEdit()
        self.text_edit.setPlaceholderText("Type a message...")
        
        # Create a QPushButton
        self.button = QPushButton("Send")
        self.button.clicked.connect(self.handleSend)
        
        # Create a horizontal layout
        layout = QHBoxLayout()
        
        # Add widgets to the layout
        layout.addWidget(self.text_edit)
        layout.addWidget(self.button)
        
        # Set the layout for this widget
        self.setLayout(layout)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

    def handleSend(self):
        self.parent().addNewMessage()