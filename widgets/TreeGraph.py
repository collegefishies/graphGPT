'''
**WIP** - This is a work in progress.

Contains functions for displaying the graph of the conversation tree.
'''
from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsEllipseItem, QGraphicsLineItem, QApplication, QGraphicsObject, QGraphicsDropShadowEffect
from PyQt6.QtCore import Qt, QRectF, QPointF, pyqtSignal
from PyQt6.QtGui import QBrush, QColor, QPainter, QPainterPath
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

        # Add drop shadow effect            
        self.shadow = QGraphicsDropShadowEffect()
        self.shadow.setBlurRadius(15)  # Adjust the blur radius as you like
        self.shadow.setXOffset(2)      # Horizontal offset
        self.shadow.setYOffset(2)      # Vertical offset
        self.shadow.setColor(QColor("gray"))  # Shadow color
        self.setGraphicsEffect(self.shadow)

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
    def setFillColor(self, color):
        if isinstance(color, str):
            self.brush.setColor(QColor(color))
        elif isinstance(color, tuple):
            if len(color) == 3:
                self.brush.setColor(QColor(color[0], color[1], color[2]))
            elif len(color) == 4:
                self.brush.setColor(QColor(color[0], color[1], color[2], color[3]))
        elif isinstance(color, QColor):
            self.brush.setColor(color)
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
        circle.shadow.setXOffset(5)      # Horizontal offset
        circle.shadow.setYOffset(5)      # Vertical offset
        
        if node == self.curr:
            circle.setFillColor("green")
            
        elif node == self.root:
            circle.setFillColor("red")
        else:
            circle.setFillColor((200,200,200,255))
            circle.shadow.setXOffset(2)      # Horizontal offset
            circle.shadow.setYOffset(2)      # Vertical offset
        
        circle.node = node
        circle.clicked.connect(self.onCircleClicked)
        self.scene.addItem(circle)

    def onCircleClicked(self, node):
        self.curr = node
        self.update(self.root, self.curr)
        self.changed_curr.emit(self.curr)

    def calculate_subtree_width(self,node):
        if not node.children:
            return 1
        return sum(self.calculate_subtree_width(child) for child in node.children)
    def addBezierCurve(self, x1, y1, x2, y2):
        r = self.radius
        path = QPainterPath()
        path.moveTo(x1 + r, y1 + r)
        ctrl_x, ctrl_y = (x1 + x2) / 2, y1 + r
        path.quadTo(ctrl_x + r, ctrl_y, x2 + r, y2 + r)
        self.scene.addPath(path)
    def draw_tree(self, node, x, y, layer_width, draw_lines=True):
        if not node.children:
            if not draw_lines:
                self.addCircle(x, y, node)
            return

        offset = x - layer_width / 2
        for child in node.children:
            child_width = self.calculate_subtree_width(child) * self.radius * 3
            child_x = offset + child_width / 2
            child_y = y + self.radius * 3

            if draw_lines:
                # Draw Bezier curve between parent and child
                self.addBezierCurve(x, y, child_x, child_y)
            else:
                # Draw the node at (x, y)
                self.addCircle(x, y, node)

            # Draw the subtree rooted at child
            self.draw_tree(child, child_x, child_y, child_width, draw_lines)

            offset += child_width

    def populateScene(self, root, curr):
        self.clear()
        

        root_width = self.calculate_subtree_width(root) * self.radius * 3
        self.draw_tree(root, 0, 0, root_width, True)
        self.draw_tree(root, 0, 0, root_width, False)



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
