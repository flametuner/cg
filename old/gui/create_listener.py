from listeners import ClickListener
from gui.log_view import Logger
import util

DISTANCE = 200

class PrePainter:

    def get_pre_object(self):
        pass

class SelectPointsListener(ClickListener, PrePainter):

    def __init__(self, clicks, callback):
        super().__init__()
        
        self.clicks  = clicks
        self.callback = callback
        self.i = 0
        if self.clicks < 3:
            Logger.log("Click on Canvas to define point[%i]" % self.i)
        else:
            Logger.log("Click on Canvas to define point[%i], to finalize click again on the initial point" % self.i)
        self.i += 1
        self.points = []

    def onClick(self, x, y):
        if self.clicks < 3:
            Logger.log("Canvas (x=%i, y=%i) selected" % (x, y))
            self.points.append((x, y))

        if self.i < self.clicks or (self.clicks >= 3 and (self.i <= 3 or util.distanceSquared(x, y, self.points[0][0], self.points[0][1]) > DISTANCE)): 
            if self.clicks >= 3:
                Logger.log("Canvas (x=%i, y=%i) selected" % (x, y))
                self.points.append((x, y))
            Logger.log("Click on Canvas to define point[%i]" % self.i)
            self.i += 1
        else:
            self.callback(self.points)

    def get_pre_object(self):
        return self.points

class SelectCurvePointsListener(ClickListener, PrePainter):

    def __init__(self, callback):
        super().__init__()
        
        self.callback = callback
        Logger.log("Click on Canvas and Drag to define a bezier line, to finalize press Enter")
        self.points = []
        self.current_point = (-1, -1)

    def onClick(self, x, y):
        self.current_point = (x, y)
        Logger.log("Canvas (x=%i, y=%i) selected" % (x, y))

    def onRelease(self, x, y):
        if (x, y) == self.current_point:
            Logger.log("You must drag the mouse to get a bezier curve.")
            return
        if len(self.points) % 4 == 0:
            self.points.append(self.current_point)
            self.points.append((x, y))
        else:
            self.points.append((x, y))
            self.points.append(self.current_point)
        self.current_point = (-1, -1)

        Logger.log("Release (x=%i, y=%i) selected" % (x, y))
        if len(self.points) == 4:
            self.callback(self.points)

    def finish(self):
        if len(self.points) < 4:
            Logger.log("You must define 2 lines at least")
            return
        self.callback(self.points)

    def get_pre_object(self):
        return self.points