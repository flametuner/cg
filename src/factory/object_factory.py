
from enum import Enum
from copy import deepcopy

from objects.drawables.drawable_point import DrawablePoint
from objects.drawables.drawable_line import DrawableLine
from objects.drawables.drawable_wireframe import DrawableWireframe
from objects.drawables.drawable_curve2d import DrawableCurve2D
from objects.line import Line
from objects.bezier_curve import BezierPoints

class ObjectType(Enum):
    POINT = 1
    LINE = 2
    WIREFRAME = 3
    CURVE2D = 4


def createPoint(name, color, points, options):
    assert len(points) == 1
    return DrawablePoint(name, color, points[0].x, points[0].y)


def createLine(name, color, points, options):
    assert len(points) == 2
    return DrawableLine(name, color, points[0], points[1])


def createWireframe(name, color, points, options):
    assert len(points) > 2
    lineList = []
    lastPoint = None
    for point in points:
        if lastPoint != None:
            lineList.append(Line(lastPoint, point))
        lastPoint = deepcopy(point)
    lineList.append(Line(deepcopy(points[-1]), deepcopy(points[0])))

    return DrawableWireframe(name, color, lineList, options['filled'])


def createBezierCurve(name, color, points, options):
    assert len(points) % 4 == 0
    return DrawableCurve2D(name, color, [BezierPoints(points[0], points[1],
                                                      points[2], points[3])])


switcher = {
    1: createPoint,
    2: createLine,
    3: createWireframe,
    4: createBezierCurve
}


def createObject(name, color, type, points, options):
    return switcher[type.value](name, color, points, options)
