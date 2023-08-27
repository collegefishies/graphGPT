from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsEllipseItem, QGraphicsLineItem, QApplication
from PyQt6.QtCore import Qt, QRectF, QPointF
from PyQt6.QtGui import QBrush, QColor
import sys

class ClickableCircle(QGraphicsEllipseItem):
    def mousePressEvent(self, event):
        print(f"Circle clicked! Conversation ID: {self.conversation_id}")

class TreeGraph(QGraphicsView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Create a QGraphicsScene
        self.scene = QGraphicsScene()

        # Create nodes (circles)
        circle1 = ClickableCircle(QRectF(0, 0, 50, 50))
        circle1.setBrush(QBrush(QColor("blue")))
        circle1.conversation_id = 1

        circle2 = ClickableCircle(QRectF(100, 100, 50, 50))
        circle2.setBrush(QBrush(QColor("red")))
        circle2.conversation_id = 2

        # # Create edge (line)
        # line = QGraphicsLineItem(QPointF(25, 25), QPointF(125, 125))

        # Add items to scene
        self.scene.addItem(circle1)
        self.scene.addItem(circle2)
        # self.scene.addItem(line)

        # Set the scene
        self.setScene(self.scene)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    view = TreeGraph()
    view.show()
    sys.exit(app.exec())
