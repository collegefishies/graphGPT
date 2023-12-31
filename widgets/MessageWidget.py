"""

This module contains the MessageWidget class, which represents a single
message in a chat application.

Classes:
    - MessageWidget: A QWidget subclass that displays a message alongside a user icon.
"""

from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QHBoxLayout, QSizePolicy
from ConversationNode import ConversationNode

class MessageWidget(QWidget):
    """A QWidget subclass to display a message in a chat application.

    The widget contains a user icon, message, and an optional button.

    Methods:
        - None
    """

    def __init__(self, message, *args, robot=False, **kwargs):
        """Initialize the MessageWidget with a given message."""
        super().__init__(*args, **kwargs)
        self.node = None
        self._initConstants()
        self._initUI(message, robot)

        
    def _initConstants(self):
        """Initialize constants used in the widget."""
        self.min_height = 50
        self.message_padding = 10
        
    def _initUI(self, message, robot):
        """Initialize the user interface components."""
        self._createUserIcon(robot)
        self._createMessageLabel(message)
        self._setupLayout()

    def _createUserIcon(self, robot):
        """Create user icon."""
        if not robot:
            self.user_icon = QLabel("👤")
        else:
            self.user_icon = QLabel("🤖")

    def defineNode(self, node):
        self.node = node
    def _createMessageLabel(self, message):
        """Create message label."""
        self.message_label = QLabel(message)
        self.message_label.setWordWrap(True)
        # self.message_label.setMinimumHeight(self.min_height)
        self.message_label.setContentsMargins(0, self.message_padding, 0, self.message_padding)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.message_label.setSizePolicy(sizePolicy)

    def _setupLayout(self):
        """Setup the QHBoxLayout for the widget."""
        layout = QHBoxLayout()
        layout.addWidget(self.user_icon)
        layout.addWidget(self.message_label, 1)
        self.setLayout(layout)
