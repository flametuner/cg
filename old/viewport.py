class Viewport:
    def __init__(self, Xvpmin, Yvpmin, Xvpmax, Yvpmax, window):
        self.Xvpmin = Xvpmin
        self.Yvpmin = Yvpmin
        self.Xvpmax = Xvpmax
        self.Yvpmax = Yvpmax
        self.window = window

    def transformToViewport(self, xw, yw):
        xvp = (xw - self.window.Xwmin) * (self.Xvpmax - self.Xvpmin) / (self.window.Xwmax - self.window.Xwmin)
        yvp = (1 - (yw - self.window.Ywmin)/(self.window.Ywmax - self.window.Ywmin)) * (self.Yvpmax - self.Yvpmin)
        return (xvp, yvp)

    def mapToWindow(self, xvp, yvp):
        xw = (xvp * (self.window.Xwmax - self.window.Xwmin) / (self.Xvpmax - self.Xvpmin)) + self.window.Xwmin
        yw = ((1 - (yvp / (self.Yvpmax - self.Yvpmin))) * (self.window.Ywmax - self.window.Ywmin)) + self.window.Ywmin
        return (xw, yw)

    def mapToWorld(self, xvp, yvp):
        return self.window.get_world_position(self.mapToWindow(xvp, yvp))

    def mapPointsToWorld(self, points):
        mappedPoints = []
        for point in points:
            mappedPoints.append(self.mapToWorld(point[0], point[1]))
        return mappedPoints