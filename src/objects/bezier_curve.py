from dataclasses import dataclass, field
from statistics import mean
import numpy as np
from .point import Point
from .line import Line
from .object import Object


@dataclass
class BezierPoints(Object):

    P1: Point
    P2: Point
    P3: Point
    P4: Point

    def as_list(self):
        return [self.P1, self.P2, self.P3, self.P4]


@dataclass
class Curve2D(Object):
    ''' Bezier curve '''

    bezierPointList: list = field(default_factory=list)
    lines: list = field(default_factory=list)

    def __post_init__(self):
        self.calculate_lines()

    def matrix_operation(self, matrix):
        for bezier in self.bezierPointList:
            for point in bezier.as_list():
                point.matrix_operation(matrix)
        self.calculate_lines()

    def calculate_lines(self, step=0.01):
        lines_to_return = []
        for bezier in self.bezierPointList:
            lines_to_return.extend(
                self._calculate_for_setup(bezier, step))
        self.lines = lines_to_return

    def _calculate_for_setup(self, bezier, step):
        MB = np.array([[-1,  3, -3,  1],
                       [3, -6,  3,  0],
                       [-3,  3,  0,  0],
                       [1,  0,  0,  0]])
        GB = np.array([[bezier.P1.x, bezier.P1.y],
                       [bezier.P2.x, bezier.P2.y],
                       [bezier.P3.x, bezier.P3.y],
                       [bezier.P4.x, bezier.P4.y]])

        lines = []
        t_values = list(np.arange(0, 1, step)) + [1]
        p_start = t_values[0]
        T0 = self._t_vec(p_start)
        for i, p_end in enumerate(t_values, 1):
            T1 = self._t_vec(p_end)

            start_x, start_y = T0.dot(MB).dot(GB)
            end_x, end_y = T1.dot(MB).dot(GB)

            line = Line(
                Point(start_x, start_y),
                Point(end_x, end_y)
            )

            lines.append(line)

            T0 = T1
            p_start = p_end

        return lines

    def _t_vec(self, t_value):
        values = [1, t_value]
        for i in range(1, 3):
            values.append(values[i] * t_value)

        values.reverse()
        return np.array(values)

    def as_point_list(self):
        return [point for bezierPoint in self.bezierPointList for point in bezierPoint.as_list()]

    def distance(self, point):
        min_distance = float('inf')
        for line in self.lines:
            current = line.distance(point)
            if current < min_distance:
                min_distance = current
        return min_distance
