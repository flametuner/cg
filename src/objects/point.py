from dataclasses import dataclass
from math import sqrt
import numpy as np
from .object import Object

@dataclass(unsafe_hash=True)
class Point(Object):
    ''' Point class '''
    x: float = 0
    y: float = 0

    def matrix_operation(self, matrix):
        P = np.array([self.x, self.y, 1])
        R = P.dot(matrix)
        self.x = R[0]
        self.y = R[1]

    def center_point(self):
        return self

    def distance(self, point):
        return sqrt((point.x - self.x) * (point.x - self.x) + (point.y - self.y) * (point.y - self.y))

    def as_point_list(self):
        return [self]
