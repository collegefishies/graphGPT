"""

This module contains the MessageBoxWidget class, which serves as a container
for MessageWidget instances in a chat application.

Classes:
    - MessageBoxWidget: A QWidget subclass that holds and manages multiple MessageWidgets.
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QStyle, QStyleOption, QSizePolicy
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter
from . import MessageWidget
from ConversationNode import ConversationNode
class MessageBoxWidget(QWidget):
    """A container widget for multiple MessageWidgets.

    This class serves as the vertical container for MessageWidgets to display messages
    in a chat application.

    Methods:
        - addMessage: Adds a new MessageWidget with the given message.
        - popMessage: Removes and returns the oldest MessageWidget.
    """
    
    def __init__(self, *args, **kwargs):
        """Initialize the MessageBoxWidget."""
        super().__init__(*args, **kwargs)
        self.message_widgets = []
        self.current_message = None
        self._initUI()
        
    def _initUI(self):
        """Initialize the user interface components."""
        self._setupLayout()
        self._setupStyleSheet()
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)

    def _setupLayout(self):
        """Setup the QVBoxLayout to house MessageWidgets."""
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(self.layout)

    def _setupStyleSheet(self):
        """Setup the stylesheet for this widget."""
        self.setAutoFillBackground(True)
        self.setStyleSheet("""
            MessageBoxWidget {
                background-color: rgba(0, 0, 0, 0.2);
            }
        """)
        
    def addMessage(self, message):
        """Add a new MessageWidget with the given message."""
        message_widget = MessageWidget(message)
        node = ConversationNode(message)
        message_widget.defineNode(node)

        #connect the nodes
        if self.current_message:
            parent_node = self.current_message.node
            child_node = message_widget.node
            parent_node.add(child_node)

        self.message_widgets.append(message_widget)
        self.layout.addWidget(message_widget)
        self.current_message = message_widget

        #print the root node
        root_node = self.message_widgets[0].node
        print(root_node)

    def popMessage(self):
        """Remove and return the oldest MessageWidget."""
        if self.message_widgets:
            message_widget = self.message_widgets.pop()
            self.layout.removeWidget(message_widget)
            message_widget.deleteLater()

            #update self.current_message
            self.current_message = self.message_widgets[0] if self.message_widgets else None

            return message_widget

    def paintEvent(self, e):
        """Ensure the custom stylesheet works properly."""
        option = QStyleOption()
        option.initFrom(self)
        painter = QPainter(self)
        self.style().drawPrimitive(QStyle.PrimitiveElement.PE_Widget, option, painter, self)
