from PyQt5.QtGui import QPainter
from dataclasses import dataclass

from .drawable import Drawable
from ..line import Line
from util.clipping_util import lineClippingCohenSutherland


@dataclass
class DrawableLine(Line, Drawable):

    def draw(self, painter: QPainter, viewport, border):
        self.updateColor(painter)

        clippedObj = lineClippingCohenSutherland(self, border)
        if clippedObj != None:
            p1 = viewport.transformToViewport(
                clippedObj.p1)
            p2 = viewport.transformToViewport(
                clippedObj.p2)
            painter.drawLine(p1.x, p1.y,
                             p2.x, p2.y)
