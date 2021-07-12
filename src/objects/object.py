from dataclasses import dataclass
from abc import abstractmethod
from statistics import mean
from util.matrix_util import *
from objects.matrix_object import MatrixObject

@dataclass
class Object(MatrixObject):

    def matrix_operation(self, matrix):
        for p in self.as_point_list():
            p.matrix_operation(matrix)

    def center_point(self):
        points = self.as_point_list()
        return mean(map(lambda point: point.x, points)), mean(map(lambda point: point.y, points))

    @abstractmethod
    def distance(self, point):
        pass

    @abstractmethod
    def as_point_list(self):
        pass
