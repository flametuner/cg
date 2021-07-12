from PyQt5.QtGui import QPainter, QPolygon
from dataclasses import dataclass
from PyQt5.QtCore import QPoint
from .drawable import Drawable
from ..wireframe import Wireframe
from util.clipping_util import lineClippingCohenSutherland


@dataclass
class DrawableWireframe(Wireframe, Drawable):

    filled: bool = False

    def draw(self, painter: QPainter, viewport, border):
        self.updateColor(painter)

        points = []
        for lines in self.lines:
            clippedObj = lineClippingCohenSutherland(lines, border)
            if clippedObj != None:
                p1 = viewport.transformToViewport(clippedObj.p1)
                p2 = viewport.transformToViewport(clippedObj.p2)
                if not self.filled:
                    painter.drawLine(p1.x, p1.y,
                                        p2.x, p2.y)
                else:
                    if len(points) == 0 or points[-1] != QPoint(p1.x, p1.y):
                        points.append(QPoint(p1.x, p1.y))
                    points.append(QPoint(p2.x, p2.y))
        if self.filled:
            poly = QPolygon(points)
            painter.drawPolygon(poly)
