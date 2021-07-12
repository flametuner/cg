from dataclasses import dataclass
from .point import Point
from .object import Object
from util.math_util import distanceLine


@dataclass
class Line(Object):
    ''' Line class '''
    p1: Point = Point()
    p2: Point = Point()

    def distance(self, point):
        return distanceLine(self, point)

    def as_point_list(self):
        return [self.p1, self.p2]
