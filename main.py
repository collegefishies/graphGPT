from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QApplication, QMainWindow
import sys


def main():
	app = QApplication(sys.argv)
	win = QMainWindow()
	win.setGeometry(200, 200, 300, 300)
	win.setWindowTitle("My first app")
	label = QtWidgets.QLabel(win)
	label.setText("Hello world!")
	label.move(50, 50)
	win.show()
	sys.exit(app.exec())


if __name__ == "__main__":
	main()