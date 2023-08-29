'''
**WIP** - This is a work in progress.

Contains functions for displaying the graph of the conversation tree.
'''
from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsEllipseItem, QGraphicsLineItem, QApplication, QGraphicsObject
from PyQt6.QtCore import Qt, QRectF, QPointF, pyqtSignal
from PyQt6.QtGui import QBrush, QColor, QPainter
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

class ClickableCircle(QGraphicsObject):
    clicked = pyqtSignal(ConversationNode)

    def __init__(self, rect, node):
        super().__init__()
        self.node = node
        self.rect = rect
        self.brush = QBrush(QColor("blue"))

    def boundingRect(self):
        return self.rect

    def paint(self, painter: QPainter, option, widget):
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(self.brush)
        
        pen = painter.pen()
        pen.setColor(QColor("black"))  # Set the circle's border color here
        painter.setPen(pen)
        
        painter.drawEllipse(self.rect)

    def mousePressEvent(self, event):
        print(f"Circle clicked! Conversation ID: {self.node}")
        self.clicked.emit(self.node)
    def setFillColor(self, color_name):
        self.brush.setColor(QColor(color_name))
        self.update()  # Trigger repaint

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
            circle.setFillColor("green")
        elif node == self.root:
            circle.setFillColor("red")
        else:
            circle.setFillColor("grey")
        circle.node = node
        circle.clicked.connect(self.onCircleClicked)
        self.scene.addItem(circle)

    def onCircleClicked(self, node):
        self.curr = node
        self.update(self.root, self.curr)

    def populateScene(self, root, curr):
        self.clear()

        _pass = "line"
        while _pass != "done":
            queue = deque()
            seen = set()
            queue.append((root, None, None))
            r = self.radius
            dx, dy = 3*r, 3*r
            depth = -1
            while queue:
                print(queue)
                #draw all the circles
                width = len(queue)
                depth += 1
                mean = (width - 1) * (3*r)/2
                #draw the parents circles
                for i in range(len(queue)):
                    node, px, py = queue.popleft()
                    if node not in seen:
                        seen.add(node)
                        #calculate position of new node.
                        x = 0 if px is None else i*dx - mean
                        y = 0 if py is None else py + dy
                        
                        if _pass == "line":
                            if px is not None and py is not None:
                                self.addLine(x, y, px, py)
                        else:
                            self.addCircle(x, y, node)


                        for child in node.children:
                            #parents x, parents y
                            px = x
                            py = y
                            queue.append((child, px, py))
            if _pass == "line":
                _pass = "circle"
            else:
                _pass = "done"


    def addLine(self, x1, y1, x2, y2):
        r = self.radius
        line = QGraphicsLineItem()
        line.setLine(x1+r, y1+r, x2+r, y2+r)
        self.scene.addItem(line)
    def clear(self):
        self.scene.clear()
if __name__ == "__main__":
    app = QApplication(sys.argv)
    view = TreeGraph()
    view.show()
    sys.exit(app.exec())
