import numpy as np
from abc import abstractmethod
from util import *
from PyQt5.QtGui import QColor
from statistics import mean

class Drawable:

    def __init__(self, name, color):
        self.name = name
        self.color = color

    @abstractmethod
    def matrix_operation(self, matrix):
        pass

    @abstractmethod
    def center_point(self):
        pass

    @abstractmethod
    def distance(self, point):
        pass

    def move(self, dx, dy):
        self.matrix_operation(get_move_matrix(dx, dy))

    def scale(self, factor, centerPoint=None):
        if centerPoint == None:
            centerPoint = self.center_point()
        self.matrix_operation(get_scale_matrix(factor, centerPoint))

    def rotate(self, angle, centerPoint=None):
        if centerPoint == None:
            centerPoint = self.center_point()
        self.matrix_operation(get_rotate_matrix(angle, centerPoint))


class Point(Drawable):

    def __init__(self, locX, locY, name="", color=QColor(0, 0, 0)):
        super().__init__(name, color)
        self.locX = locX
        self.locY = locY

    def matrix_operation(self, matrix):
        P = np.array([self.locX, self.locY, 1])
        R = P.dot(matrix)
        self.locX = R[0]
        self.locY = R[1]

    def center_point(self):
        return self.locX, self.locY

    def distance(self, point):
        return distance(self.locX, self.locY, point.locX, point.locY)

    def __str__(self):
        return f'Point(name={self.name}, x={self.locX}, y={self.locY})'


class Line(Drawable):

    def __init__(self, p1, p2, name="", color=QColor(0, 0, 0)):
        super().__init__(name, color)
        self.p1 = p1
        self.p2 = p2

    def matrix_operation(self, matrix):
        self.p1.matrix_operation(matrix)
        self.p2.matrix_operation(matrix)

    def center_point(self):
        return (self.p1.locX + self.p2.locX) / 2, (self.p1.locY + self.p2.locY) / 2

    def distance(self, point):
        return distanceLine(self.p1.locX, self.p1.locY, self.p2.locX, self.p2.locY, point.locX, point.locY)

    def __str__(self):
        if self.name:
            return f'Line(name={self.name}, p1={self.p1}, p2={self.p2})'
        else:
            return f'Line(p1={self.p1}, p2={self.p2})'


class Wireframe(Drawable):

    def __init__(self, lineList, name="", color=QColor(0, 0, 0), filled=False):
        super().__init__(name, color)
        self.lineList = lineList
        self.filled = filled

    def matrix_operation(self, matrix):
        for line in self.lineList:
            line.p1.matrix_operation(matrix)
            line.p2.matrix_operation(matrix)

    def center_point(self):
        Cx = 0
        Cy = 0
        for line in self.lineList:
            Cx += line.p1.locX
            Cy += line.p1.locY
        n = len(self.lineList)
        return Cx / n, Cy / n

    def distance(self, point):
        min_distance = float('inf')
        for line in self.lineList:
            current = line.distance(point)
            if current < min_distance:
                min_distance = current
        return min_distance

    def __str__(self):
        return f'Wireframe(name={self.name}, lineList=a{self.lineList})'

class BezierPoints(Drawable):

    def __init__(self, P1, P2, P3, P4, name="", color=QColor(0, 0, 0)):
        super().__init__(name, color)
        self.P1 = P1
        self.P2 = P2
        self.P3 = P3
        self.P4 = P4
    
    def as_list(self):
        return [self.P1, self.P2, self.P3, self.P4]

class Curve2D(Drawable):
    ''' Bezier curve '''
    def __init__(self, pointList, name="", color=QColor(0, 0, 0)):
        super().__init__(name, color)
        self.bezierPointList = pointList
        self.lineList = []
        self.filled = False
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
        self.lineList = lines_to_return

    def _calculate_for_setup(self, bezier, step):
        MB = np.array([[-1,  3, -3,  1],
                       [3, -6,  3,  0],
                       [-3,  3,  0,  0],
                       [1,  0,  0,  0]])
        GB = np.array([[bezier.P1.locX, bezier.P1.locY],
                       [bezier.P2.locX, bezier.P2.locY],
                       [bezier.P3.locX, bezier.P3.locY],
                       [bezier.P4.locX, bezier.P4.locY]])

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

    def center_point(self):
        points = []
        for bezier in self.bezierPointList:
            points.extend(bezier.as_list())
        return mean(map(lambda point: point.locX, points)), mean(map(lambda point: point.locY, points))

    def distance(self, point):
        min_distance = float('inf')
        for line in self.lineList:
            current = line.distance(point)
            if current < min_distance:
                min_distance = current
        return min_distance

    def __str__(self):
        return f'Curve2D(name={self.name}, bezierPointList={self.bezierPointList})'

