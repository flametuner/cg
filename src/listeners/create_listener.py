from .click_listener import ClickListener
from window.log_viewer import Logger
from objects.point import Point
from util.math_util import distanceSquared
from factory.object_factory import ObjectType

DISTANCE = 200

class PrePainter:

    def get_pre_object(self):
        pass

class SelectPointsListener(ClickListener, PrePainter):

    def __init__(self, objectType, callback):
        super().__init__()
        
        self.objectType  = objectType
        self.callback = callback
        self.i = 0
        if self.objectType != ObjectType.WIREFRAME:
            Logger.log("Click on Canvas to define point[%i]" % self.i)
        else:
            Logger.log("Click on Canvas to define point[%i], to finalize click again on the initial point" % self.i)
        self.i += 1
        self.points: [Point] = []

    def onClick(self, x, y):
        if self.objectType != ObjectType.WIREFRAME:
            Logger.log("Canvas (x=%i, y=%i) selected" % (x, y))
            self.points.append(Point(x, y))
        clicks = self.objectType.value
        if self.i < clicks or (self.objectType == ObjectType.WIREFRAME and (self.i <= 3 or distanceSquared(Point(x, y), self.points[0]) > DISTANCE)): 
            if self.objectType == ObjectType.WIREFRAME:
                Logger.log("Canvas (x=%i, y=%i) selected" % (x, y))
                self.points.append(Point(x, y))
            Logger.log("Click on Canvas to define point[%i]" % self.i)
            self.i += 1
        else:
            self.callback(self.objectType, self.points)

    def get_pre_object(self):
        return self.points

class SelectCurvePointsListener(ClickListener, PrePainter):

    def __init__(self, callback):
        super().__init__()
        
        self.callback = callback
        Logger.log("Click on Canvas and Drag to define a bezier line, to finalize press Enter")
        self.points = []
        self.current_point = Point(-1, -1)

    def onClick(self, x, y):
        self.current_point = Point(x, y)
        Logger.log("Canvas (x=%i, y=%i) selected" % (x, y))

    def onRelease(self, x, y):
        if Point(x, y) == self.current_point:
            Logger.log("You must drag the mouse to get a bezier curve.")
            return
        if len(self.points) % 4 == 0:
            self.points.append(self.current_point)
            self.points.append(Point(x, y))
        else:
            self.points.append(Point(x, y))
            self.points.append(self.current_point)
        self.current_point = Point(-1, -1)

        Logger.log("Release (x=%i, y=%i) selected" % (x, y))
        if len(self.points) == 4:
            self.callback(ObjectType.CURVE2D, self.points)

    def finish(self):
        if len(self.points) < 4:
            Logger.log("You must define 2 lines at least")
            return
        self.callback(ObjectType.CURVE2D, self.points)

    def get_pre_object(self):
        return self.points