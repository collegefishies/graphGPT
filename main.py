from PyQt6 import QtWidgets, QtGui
from PyQt6.QtWidgets import QApplication, QMainWindow
from widgets import ChatBoxWidget, MessageBoxWidget, MessageWidget, InputBox, TreeGraph
import sys

messages = ["Hello", "World", "This", "Is", "A", "Test", "Message"]

def main():
	app = QApplication(sys.argv)
	win = QMainWindow()
	win.setGeometry(0, 0, 748, 440)
	win.setWindowTitle("My first app")

	# Create a central QWidget and set it to the main window
	central_widget = QtWidgets.QWidget()
	win.setCentralWidget(central_widget)

	# Create a QVBoxLayout and set it to the central widget
	hlayout = QtWidgets.QHBoxLayout()
	central_widget.setLayout(hlayout)

	# Create an instance of ChatBoxWidget and set it to the central widget
	chat_box = ChatBoxWidget()
	hlayout.addWidget(chat_box)

	#Create the Tree Graph
	tree_graph = TreeGraph()
	hlayout.addWidget(tree_graph)
	
	win.show()
	sys.exit(app.exec())



if __name__ == "__main__":
	print("#####Main Start#####")
	main()