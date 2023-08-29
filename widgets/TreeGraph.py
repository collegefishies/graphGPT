'''
**WIP** - This is a work in progress.

Contains functions for displaying the graph of the conversation tree.
'''
from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsEllipseItem, QGraphicsLineItem, QApplication
from PyQt6.QtCore import Qt, QRectF, QPointF, pyqtSignal
from PyQt6.QtGui import QBrush, QColor
from collections import deque
from ConversationNode import ConversationNode
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
    clicked = pyqtSignal(ConversationNode)

    def __init__(self, rect, node):
        super().__init__(rect)
        self.node = node

    def mousePressEvent(self, event):
        print(f"Circle clicked! Conversation ID: {self.node}")
        self.clicked.emit(self.node)

class TreeGraph(QGraphicsView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Create a QGraphicsScene
        self.scene = QGraphicsScene()
        #keep your copy of the root node.
        self.root = None
        self.curr = None
        self.radius = 25


        # Set the scene
        self.setScene(self.scene)

    def update(self, root, curr):
        print("Update called.")
        self.root = root
        self.curr = curr
        self.populateScene(root, curr)


    def addCircle(self, x, y, node):
        r = self.radius
        circle = ClickableCircle(QRectF(x, y, 2*r, 2*r), node)
        if node == self.curr:
            circle.setBrush(QBrush(QColor("green")))
        elif node == self.root:
            circle.setBrush(QBrush(QColor("red")))
        else:
            circle.setBrush(QBrush(QColor("grey")))
        circle.node = node
        circle.clicked.connect(self.onCircleClicke)
        self.scene.addItem(circle)

    def onCircleClicked(self, node):
        self.curr = node
        self.update(self.root, self.curr)

    def populateScene(self, root, curr):
        self.clear()

        queue = deque()
        seen = set()
        queue.appendleft((root, 0, 0))
        r = self.radius
        dx, dy = 3*r, 3*r

        while queue:
            node, x, y = queue.popleft()

            self.addCircle(x, y, node)
            i = 0
            N = len(node.children)
            mean = (N-1)*(3*r)/2
            for i,child in enumerate(node.children):
                if child not in seen:
                    seen.add(child)
                    #draw line from parent to child
                    line = QGraphicsLineItem()
                    line.setLine(x + r, y + r, x + i*dx + r-mean, y + dy + r)
                    self.scene.addItem(line)
                    queue.append((child, x + i*dx-mean, y + dy))


    def clear(self):
        self.scene.clear()
if __name__ == "__main__":
    app = QApplication(sys.argv)
    view = TreeGraph()
    view.show()
    sys.exit(app.exec())
