import sys, os
from PyQt6 import QtWidgets, QtGui
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog
from widgets import ChatBoxWidget, TreeGraph
from ConversationNode import ConversationNode

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_attributes()
        self.init_ui()

    def init_attributes(self):
        self.filename = None
        self.changed = False

    def init_ui(self):
        self.set_geometry_and_title()
        self.create_menu_bar()
        self.create_central_widget()

    def set_geometry_and_title(self):
        self.setGeometry(0, 0, 748, 440)
        self.update_title()

    def create_menu_bar(self):
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("File")
        self.add_actions_to_menu(file_menu)

    def add_actions_to_menu(self, menu):
        actions = [
            ("New", "Ctrl+N", self.new_file),
            ("Open", "Ctrl+O", self.open_file_dialog),
            ("Save", "Ctrl+S", self.save_file),
            ("Save As", "Ctrl+Shift+S", self.save_file_dialog)
        ]
        for action_text, shortcut, action_function in actions:
            action = QtGui.QAction(action_text, self)
            action.setShortcut(shortcut)
            action.triggered.connect(action_function)
            menu.addAction(action)

    def create_central_widget(self):
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)

        layout = QtWidgets.QHBoxLayout()
        central_widget.setLayout(layout)

        self.chat_box = ChatBoxWidget()
        layout.addWidget(self.chat_box)

        self.tree_graph = TreeGraph()
        self.tree_graph.connect_message_box(self.chat_box.message_box)
        layout.addWidget(self.tree_graph)
        self.connect_signals()

    def connect_signals(self):
        self.chat_box.message_box.changed_signal.connect(self.tree_graph.update)

    def new_file(self):
        self.filename = None
        self.chat_box.message_box.deleteConversation()
        self.chat_box.message_box._initConv()
        self.tree_graph.clear()
        self.changed = False
        self.update_title()


    def open_file_dialog(self):
        filename, _ = self.show_file_dialog("Open File", "Open")
        if filename:
            self.load_file(filename)
            self.set_window_title()

    def save_file_dialog(self):
        filename, _ = self.show_file_dialog("Save File", "Save")
        if filename:
            self.filename = filename
            self.save_file()
            self.set_window_title()

    def show_file_dialog(self, title, action_type):
        dialog = QFileDialog()
        options = dialog.options()
        file_types = "Conversation Files (*.conv);;All Files (*)"
        if action_type == "Open":
            return QFileDialog.getOpenFileName(self, title, "", file_types, options=options)
        else:
            return QFileDialog.getSaveFileName(self, title, "", file_types, options=options)

    def load_file(self, filename):
        self.filename = filename
        short_filename = self.extract_filename(filename)
        self.setWindowTitle(f"graphGPT - {short_filename}")

        root, curr = ConversationNode.load_conversation_tree(filename)
        self.chat_box.message_box._populate(root, curr)
        self.changed = False
        self.update_title()

    def update_title(self):
        title = "graphGPT - *Untitled*"
        if self.filename:
            short_filename = self.extract_filename(self.filename)
            title = f"graphGPT - {short_filename}"
            if self.changed:
                title += "*"
        self.setWindowTitle(title)

    def set_window_title(self):
        short_filename = self.extract_filename(self.filename)
        self.setWindowTitle(f"graphGPT - {short_filename}")

    def save_conversation(self):
        widgets = self.chat_box.message_box.message_widgets
        root = widgets[0].node if widgets else None
        curr = self.chat_box.message_box.current_message.node if widgets else None
        root.save_conversation_tree(self.filename, curr)

    def save_file(self):
        self.changed = False
        if not self.filename:
            self.save_file_dialog()
        else:
            self.set_window_title()
            self.save_conversation()

    @staticmethod
    def extract_filename(full_path):
        return full_path.split("/")[-1]


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":

    print("##### Main Start #####")
    main()
