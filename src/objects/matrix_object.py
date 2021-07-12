from dataclasses import dataclass
from abc import abstractmethod
from statistics import mean
from util.matrix_util import *


@dataclass
class MatrixObject:

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

    @abstractmethod
    def center_point(self):
        pass

    @abstractmethod
    def matrix_operation(self, matrix):
        pass
