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
    changed_curr = pyqtSignal(ConversationNode)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Create a QGraphicsScene
        self.scene = QGraphicsScene()
        #keep your copy of the root node.
        self.root = None
        self.curr = None
        self.radius = 25
        self.message_box = None

        # Set the scene
        self.setScene(self.scene)

    def connect_message_box(self, message_box):
        self.message_box = message_box
        self.changed_curr.connect(self.message_box._setCurrentMessage)
        
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
        self.changed_curr.emit(self.curr)

    def populateScene(self, root, curr):
        self.clear()
        
        def calculate_subtree_width(node):
            if not node.children:
                return 1
            return sum(calculate_subtree_width(child) for child in node.children)

        def draw_tree(node, x, y, layer_width):
            # Draw the node at (x, y)
            self.addCircle(x, y, node)
            
            # If leaf node, stop recursion
            if not node.children:
                return
            
            # Initial offset for the children
            offset = x - layer_width / 2

            for child in node.children:
                child_width = calculate_subtree_width(child) * self.radius * 3
                child_x = offset + child_width / 2
                child_y = y + self.radius * 3
                
                # Draw line between parent and child
                self.addLine(x, y, child_x, child_y)
                
                # Draw the subtree rooted at child
                draw_tree(child, child_x, child_y, child_width)
                
                # Update the offset
                offset += child_width

        root_width = calculate_subtree_width(root) * self.radius * 3
        draw_tree(root, 0, 0, root_width)




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
