'''
	The executable for the GUI interface
'''
import sys, os
from PyQt6 import QtWidgets, QtGui
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog
from widgets import ChatBoxWidget, TreeGraph
from ConversationNode import ConversationNode

class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()

		#set attributes
		self.filename = None
		self.changed = False

		#set window properties
		self.setGeometry(0, 0, 748, 440)
		self.update_title()
		self.init_ui()

	def init_ui(self):
		self.create_menu_bar()
		self.create_central_widget()

	def create_menu_bar(self):
		menu_bar = self.menuBar()
		file_menu = menu_bar.addMenu("File")

		actions = [
			("Open", "Ctrl+O", self.open_file_dialog),
			("Save", "Ctrl+S", self.save_file),
			("Save As", "Ctrl+Shift+S", self.save_file_dialog)
		]

		for action_text, shortcut, action_function in actions:
			action = QtGui.QAction(action_text, self)
			action.setShortcut(shortcut)
			action.triggered.connect(action_function)
			file_menu.addAction(action)

	def create_central_widget(self):
		central_widget = QtWidgets.QWidget()
		self.setCentralWidget(central_widget)

		layout = QtWidgets.QHBoxLayout()
		central_widget.setLayout(layout)

		self.chat_box = ChatBoxWidget()
		layout.addWidget(self.chat_box)

		tree_graph = TreeGraph()
		layout.addWidget(tree_graph)

	def open_file_dialog(self):
		dialog = QFileDialog()
		options = dialog.options()
		filename, _ = QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*);;Conversation Files (*.conv)", options=options)
		if filename:
			self.load_file(filename)
			self.set_window_title()

	def save_file_dialog(self):
		dialog = QFileDialog()
		options = dialog.options()
		filename, _ = QFileDialog.getSaveFileName(self, "Save File", "", "All Files (*);;Conversation Files (*.conv)", options=options)
		if filename:
			self.filename = filename
			self.save_file()
			self.set_window_title()
			


	def load_file(self, filename):
		self.filename = filename
		#update title
		#use short filename
		filename = filename.split("/")[-1]
		self.setWindowTitle(f"graphGPT - {filename}")

		#load the conversation nodes
		root, curr = ConversationNode.load_conversation_tree(filename)

		#populate the widgets
		self.chat_box.message_box._populate(root, curr)
		self.changed = False
		self.update_title()


	def update_title(self):
		if self.filename and self.changed:
			filename = self.filename.split("/")[-1]
			self.setWindowTitle(f"graphGPT - {filename}*")
		else:
			self.setWindowTitle(f"graphGPT - *Untitled*")

	def set_window_title(self):
		filename = self.filename.split("/")[-1]
		self.setWindowTitle(f"graphGPT - {filename}")

	def save_conversation(self):
		widgets = self.chat_box.message_box.message_widgets
		root = widgets[0].node if widgets else None
		curr = self.chat_box.message_box.current_message.node if widgets else None
		root.save_conversation_tree(self.filename, curr)

	def save_file(self):
		print("in savefile")
		self.changed = False
		print(self.filename)
		if self.filename is None:
			self.save_file_dialog()
		else:
			self.set_window_title()
			self.save_conversation()


def main():
	app = QApplication(sys.argv)
	window = MainWindow()
	window.show()
	sys.exit(app.exec())

if __name__ == "__main__":
	print("##### Main Start #####")
	print(os.getcwd())
	main()
