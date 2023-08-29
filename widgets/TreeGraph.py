'''
**WIP** - This is a work in progress.

Contains functions for displaying the graph of the conversation tree.
'''
from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsEllipseItem, QGraphicsLineItem, QApplication
from PyQt6.QtCore import Qt, QRectF, QPointF
from PyQt6.QtGui import QBrush, QColor
from collections import deque
import sys

class Node:
    def __init__(self):
        self.val = None
        self.parent = None
        self.children = []

    def add_child(self, x):
        assert isinstance(x, Node)
        x.parent = self
        self.children.append(x)

class ClickableCircle(QGraphicsEllipseItem):
    def mousePressEvent(self, event):
        print(f"Circle clicked! Conversation ID: {self.conversation_id}")

class TreeGraph(QGraphicsView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Create a QGraphicsScene
        self.scene = QGraphicsScene()
        #keep your copy of the root node.
        self.root = None
        self.curr = None


        # Set the scene
        self.setScene(self.scene)

        # self.addCircle(25, 75, 4)
    def update(self, root, curr):
        print("Update called.")
        self.root = root
        self.curr = curr
        self.populateScene(root, curr)

    def addCircle(self, x, y, conversation_id):
        circle = ClickableCircle(QRectF(x, y, 50, 50))
        if conversation_id == self.root:
            circle.setBrush(QBrush(QColor("red")))
        elif conversation_id == self.curr:
            circle.setBrush(QBrush(QColor("green")))
        else:
            circle.setBrush(QBrush(QColor("grey")))
        circle.conversation_id = conversation_id
        self.scene.addItem(circle)

    def populateScene(self, root, curr):
        self.clear()

        queue = deque()
        seen = set()
        queue.appendleft((root, 0, 0))
        dx, dy = 75, 75

        while queue:
            node, x, y = queue.popleft()

            self.addCircle(x, y, node)
            i = 0
            for i,child in enumerate(node.children):
                if child not in seen:
                    seen.add(child)
                    #draw line from parent to child
                    line = QGraphicsLineItem()
                    line.setLine(x + 25, y + 25, x + i*dx + 25, y + dy + 25)
                    self.scene.addItem(line)
                    queue.append((child, x + i*dx, y + dy))


    def clear(self):
        self.scene.clear()
if __name__ == "__main__":
    app = QApplication(sys.argv)
    view = TreeGraph()
    view.show()
    sys.exit(app.exec())
