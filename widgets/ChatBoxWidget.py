from PyQt6.QtWidgets import QWidget, QVBoxLayout
from . import InputBox, MessageBoxWidget

class ChatBoxWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Create an instance of MessageBoxWidget and InputBox
        self.message_box = MessageBoxWidget()
        self.input_box = InputBox()
        
        # Create a QVBoxLayout to house both MessageBoxWidget and InputBox
        layout = QVBoxLayout()
        
        # Add MessageBoxWidget and InputBox to the layout
        # Use stretch factors to control their sizes
        layout.addWidget(self.message_box, 1)  # Takes any extra vertical space
        layout.addWidget(self.input_box, 0)    # Takes only the space it needs
        
        # Set the layout for this widget
        self.setLayout(layout)

    def addNewMessage(self):
        new_message = self.input_box.text_edit.toPlainText()
        if len(new_message) > 0:
            self.message_box.addMessage(new_message)
            self.input_box.text_edit.clear()

    def popMessage(self):
        return self.message_box.popMessage()