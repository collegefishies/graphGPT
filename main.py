from PyQt6 import QtWidgets, QtGui
from PyQt6.QtWidgets import QApplication, QMainWindow
from widgets import AutoExpandingTextEdit, InputBox
import sys


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

    # Create and set the InputBox
    input_box = InputBox()
    vlayout.addWidget(input_box)

    # Create and set the AutoExpandingTextEdit
    text_edit = AutoExpandingTextEdit()
    text_edit.setPlaceholderText("Type a message...")
    text_edit.setFixedHeight(50)
    vlayout.addWidget(text_edit)

    win.show()
    sys.exit(app.exec())



if __name__ == "__main__":
	print("#####Main Start#####")
	main()