from PyQt5.QtGui import QPainter
from dataclasses import dataclass
from .drawable import Drawable
from ..point import Point
from util.clipping_util import pointClipping


@dataclass
class DrawablePoint(Point, Drawable):

    def draw(self, painter: QPainter, viewport, border):
        self.updateColor(painter)

        clippedObj = pointClipping(self, border)
        if clippedObj != None:
            vp_point = viewport.transformToViewport(clippedObj)
            painter.drawPoint(vp_point.x, vp_point.y)
