from objects.drawables.drawable import Drawable
from objects.point import Point
from objects.matrix_object import MatrixObject
import numpy as np
from copy import deepcopy
from util.matrix_util import *

class Window(MatrixObject):
    def __init__(self, Xwmin, Ywmin, Xwmax, Ywmax):
        self.displayfile: dict[str, Drawable] = {}
        self.Xwmin = -1
        self.Ywmin = -1
        self.Xwmax = 1
        self.Ywmax = 1
        self.proportion = get_defined_matrix()
        self.current_matrix = get_defined_matrix()  # 4x3

    def matrix_operation(self, matrix):
        self.current_matrix = self.current_matrix.dot(matrix)

    def center_point(self):
        return 0, 0

    def updateProportion(self, x, y):
        self.Xwmin = -x/2
        self.Ywmin = -y/2
        self.Xwmax = x/2
        self.Ywmax = y/2

    def addObject(self, obj: Drawable):
        self.displayfile[obj.name] = obj

    def zoom(self, ZOOM, center=None):
        total_zoom = 1 - ZOOM
        self.scale(total_zoom, center)

    def get_world_position(self, windowCoords):
        matrix = np.array([windowCoords.x,  windowCoords.y, 1])
        inverted = np.linalg.inv(self.current_matrix)
        result = matrix.dot(inverted)
        return Point(result[0], result[1])

    def get_window_displayfile(self):
        window_displayfile = []
        for obj in self.displayfile.values():
            copy = deepcopy(obj)
            copy.matrix_operation(self.current_matrix)
            window_displayfile.append(copy)
        return window_displayfile
