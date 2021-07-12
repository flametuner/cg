import numpy as np
from math import sin, cos


def get_defined_matrix(proportionX=1, proportionY=1):
    return np.array([[proportionX, 0, 0],
                     [0, proportionY, 0],
                     [0, 0, 1]])


def get_move_matrix(dx, dy):
    return np.array([[1, 0, 0],
                     [0, 1, 0],
                     [dx, dy, 1]])


def get_scale_matrix(factor, centerPoint):
    T1 = np.array([[1, 0, 0],
                   [0, 1, 0],
                   [-centerPoint[0], -centerPoint[1], 1]])
    R = np.array([[factor, 0, 0],
                  [0, factor, 0],
                  [0, 0, 1]])
    T2 = np.array([[1, 0, 0],
                   [0, 1, 0],
                   [centerPoint[0], centerPoint[1], 1]])
    return T1.dot(R).dot(T2)


def get_rotate_matrix(angle, centerPoint):
    T1 = np.array([[1, 0, 0],
                   [0, 1, 0],
                   [-centerPoint[0], -centerPoint[1], 1]])
    R = np.array([[cos(angle), -sin(angle), 0],
                  [sin(angle), cos(angle), 0],
                  [0, 0, 1]])
    T2 = np.array([[1, 0, 0],
                   [0, 1, 0],
                   [centerPoint[0], centerPoint[1], 1]])
    return T1.dot(R).dot(T2)
