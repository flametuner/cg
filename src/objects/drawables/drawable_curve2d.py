from PyQt5.QtGui import QPainter, QPolygon
from dataclasses import dataclass
from PyQt5.QtCore import QPoint
from .drawable import Drawable
from ..bezier_curve import Curve2D
from util.clipping_util import lineClippingCohenSutherland


@dataclass
class DrawableCurve2D(Curve2D, Drawable):

    def draw(self, painter: QPainter, viewport, border):
        self.updateColor(painter)

        for lines in self.lines:
            clippedObj = lineClippingCohenSutherland(lines, border)
            if clippedObj != None:
                p1 = viewport.transformToViewport(clippedObj.p1)
                p2 = viewport.transformToViewport(clippedObj.p2)
                painter.drawLine(p1.x, p1.y,
                                 p2.x, p2.y)
