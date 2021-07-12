from objects.point import Point

class Viewport:
    def __init__(self, Xvpmin, Yvpmin, Xvpmax, Yvpmax, window):
        self.Xvpmin = Xvpmin
        self.Yvpmin = Yvpmin
        self.Xvpmax = Xvpmax
        self.Yvpmax = Yvpmax
        self.window = window

    def transformToViewport(self, point: Point):
        xvp = (point.x - self.window.Xwmin) * (self.Xvpmax - self.Xvpmin) / (self.window.Xwmax - self.window.Xwmin)
        yvp = (1 - (point.y - self.window.Ywmin)/(self.window.Ywmax - self.window.Ywmin)) * (self.Yvpmax - self.Yvpmin)
        return Point(xvp, yvp)

    def mapToWindow(self, point: Point):
        xw = (point.x * (self.window.Xwmax - self.window.Xwmin) / (self.Xvpmax - self.Xvpmin)) + self.window.Xwmin
        yw = ((1 - (point.y / (self.Yvpmax - self.Yvpmin))) * (self.window.Ywmax - self.window.Ywmin)) + self.window.Ywmin
        return Point(xw, yw)

    def mapToWorld(self, point):
        return self.window.get_world_position(self.mapToWindow(point))

    def mapPointsToWorld(self, points):
        mappedPoints = map(self.mapToWorld, points)
        return list(mappedPoints)