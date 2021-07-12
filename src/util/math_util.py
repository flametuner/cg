from math import sqrt

from objects.point import Point


def distanceSquared(p1, p2):
    return (p2.x - p1.x) * (p2.x - p1.x) + (p2.y - p1.y) * (p2.y - p1.y)


def distance(p1, p2):
    return sqrt(distanceSquared(p1, p2))


def distanceLine(line, point):
    l2 = distanceSquared(line.p1, line.p2)
    if l2 == 0:
        return distance(point, line.p2)
    x1 = line.p1.x
    y1 = line.p1.y
    x2 = line.p2.x
    y2 = line.p2.y
    px = point.x
    py = point.y
    t = ((px-x1)*(x2-x1)+(py-y1)*(y2-y1)) / l2
    t = max(0, min(1, t))
    return distance(point, Point(x1 + t * (x2 - x1), y1 + t * (y2 - y1)))
