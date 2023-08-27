from PyQt6 import QtWidgets, QtGui
from PyQt6.QtWidgets import QApplication, QMainWindow
from widgets import AutoExpandingTextEdit, InputBox, MessageWidget
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
	vlayout = QtWidgets.QVBoxLayout()
	central_widget.setLayout(vlayout)

	# Create and add the MessageWidget
	for msg in messages:
		message_widget = MessageWidget(msg)
		vlayout.addWidget(message_widget)

	# Create and set the InputBox
	input_box = InputBox()
	vlayout.addWidget(input_box)

	win.show()
	sys.exit(app.exec())



if __name__ == "__main__":
	print("#####Main Start#####")
	main()