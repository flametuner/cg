import numpy as np
from math import sin, cos, sqrt


def distanceSquared(x1, y1, x2, y2):
    return (x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1)


def distance(x1, y1, x2, y2):
    return sqrt(distanceSquared(x1, y1, x2, y2))


def distanceLine(x1, y1, x2, y2, px, py):
    l2 = distanceSquared(x1, y1, x2, y2)
    if l2 == 0:
        return distance(px, py, x2, y2)
    t = ((px-x1)*(x2-x1)+(py-y1)*(y2-y1)) / l2
    t = max(0, min(1, t))
    return distance(px, py, x1 + t * (x2 - x1), y1 + t * (y2 - y1))
    # return abs((x2-x1)*(y1-py)-(x1-px)*(y2-y1)) / distance(x1, y1, x2, y2)


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
