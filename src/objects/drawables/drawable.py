from dataclasses import dataclass
from PyQt5.QtGui import QColor, QPainter, QPen, QBrush
from PyQt5.QtCore import Qt
from abc import abstractmethod
from objects.line import Line


@dataclass
class Drawable:
    ''' Wireframe class '''
    name: str
    color: QColor = QColor(0, 0, 0)

    @abstractmethod
    def draw(self, painter: QPainter, viewport, border):
        pass

    def updateColor(self, painter: QPainter):
        obj_pen = QPen()
        obj_pen.setWidth(2)
        obj_pen.setColor(self.color)
        painter.setBrush(QBrush(self.color, Qt.SolidPattern))
        painter.setPen(obj_pen)
