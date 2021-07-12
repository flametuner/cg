from objects import Drawable
from util import *
import numpy as np
from copy import deepcopy


class Window:
    def __init__(self, Xwmin, Ywmin, Xwmax, Ywmax):
        self.displayfile: dict[str, Drawable] = {}
        self.Xwmin = -1
        self.Ywmin = -1
        self.Xwmax = 1
        self.Ywmax = 1
        self.proportion = get_defined_matrix()
        self.current_matrix = get_defined_matrix()  # 4x3

    def updateProportion(self, x, y):
        self.Xwmin = -x/2
        self.Ywmin = -y/2
        self.Xwmax = x/2
        self.Ywmax = y/2
        # proportion_inverted = np.linalg.inv(self.proportion)
        # self.proportion = get_defined_matrix(x, y)
        # self.current_matrix = self.current_matrix.dot(
        #     proportion_inverted).dot(self.proportion)

    def addObject(self, obj: Drawable):
        self.displayfile[obj.name] = obj

    def move(self, addX, addY):
        self.current_matrix = self.current_matrix.dot(
            get_move_matrix(-addX, -addY))

    def zoom(self, ZOOM, center=None):
        if center == None:
            center = (0, 0)
        total_zoom = 1 - ZOOM
        self.current_matrix = self.current_matrix.dot(
            get_scale_matrix(total_zoom, center))

    def rotate(self, angle, center=None):
        if center == None:
            center = (0, 0)
        self.current_matrix = self.current_matrix.dot(
            get_rotate_matrix(-angle, center))

    def get_world_position(self, windowCoords):
        matrix = np.array([windowCoords[0],  windowCoords[1], 1])
        inverted = np.linalg.inv(self.current_matrix)
        result = matrix.dot(inverted)
        return (result[0], result[1])

    def get_window_displayfile(self):
        window_displayfile = []
        for obj in self.displayfile.values():
            copy = deepcopy(obj)
            copy.matrix_operation(self.current_matrix)
            window_displayfile.append(copy)
        return window_displayfile
