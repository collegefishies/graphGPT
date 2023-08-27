from PyQt6.QtWidgets import QWidget, QVBoxLayout, QStyle, QStyleOption
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter
from PyQt6.QtWidgets import QSizePolicy

from . import MessageWidget

class MessageBoxWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.message_widgets = []
        
        # Create a QVBoxLayout to stack MessageWidget instances
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        self.setLayout(self.layout)
        
        # Set background color using stylesheet
        # Lighter in dark mode, darker in light mode
        self.setAutoFillBackground(True)
        self.setStyleSheet("""
            MessageBoxWidget {
                background-color: rgba(0, 0, 0, 20%);  /* for dark mode */
            }
        """)
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)


    def addMessage(self, message):
        message_widget = MessageWidget(message)
        self.message_widgets.append(message_widget)
        self.layout.addWidget(message_widget)

    def popMessage(self):
        if len(self.message_widgets) > 0:
            message_widget = self.message_widgets.pop()
            self.layout.removeWidget(message_widget)
            message_widget.deleteLater()
            return message_widget
        
    # This method ensures the custom stylesheet works properly
    def paintEvent(self, e):
        option = QStyleOption()
        option.initFrom(self)
        painter = QPainter(self)
        self.style().drawPrimitive(QStyle.PrimitiveElement.PE_Widget, option, painter, self)
