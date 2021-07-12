from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from gui.log_view import Logger
from typing import List, NamedTuple
from objects import *
from viewport import Viewport
from gui.create_listener import *
from gui.object_dialog import *
from math import sqrt
from clipping import *
from copy import deepcopy
import numpy as np
import alerts

STEP = 10
ANGLE = 0.1
ZOOM = 0.2
BORDER = 30


class Canvas(QLabel):

    # Constructor
    def __init__(self, window, parent=None, objectList=None, inputs=None):
        super().__init__(parent)

        # Object style sheet
        stylesheet = '''
            QLabel {
                background-color: white;
                border: 1px solid black
            }
        '''
        self.setStyleSheet(stylesheet)

        self.viewport = Viewport(0, 0, self.width(), self.height(), window)

        self.updateStep()
        self.center = None
        self.clickListener = None
        self.objectList = objectList
        self.inputs = inputs
        if self.inputs != None:
            pass
        if self.objectList != None:
            self.objectList.itemClicked.connect(self.setFocus)

    # Classes functions
    def updateStep(self):
        point_1 = self.viewport.mapToWindow(0, 0)
        point_2 = self.viewport.mapToWindow(1, 1)
        self.step_x = point_2[0] - point_1[0]
        self.step_y = point_2[1] - point_1[1]

        point_zero = self.viewport.mapToWorld(0, 0)
        point_x = self.viewport.mapToWorld(1, 0)
        point_y = self.viewport.mapToWorld(0, 1)
        self.world_step_matrix = np.array([[point_x[0] - point_zero[0], point_x[1] - point_zero[1]],
                                           [point_y[0] - point_zero[0], point_y[1] - point_zero[1]]])
        transform = np.array([1, 1]).dot(self.world_step_matrix)
        self.step_distance = sqrt(
            (transform[0] ** 2) + (transform[1] ** 2))

    def updateCenter(self, xy=None):
        if xy != None:
            self.center = (xy[0], xy[1])
            Logger.log(
                "Center selected (", self.center[0], self.center[1], ")")
            if self.inputs != None:
                self.inputs[0].setText(str(self.center[0]))
                self.inputs[1].setText(str(self.center[1]))
        else:
            self.center = None
            if self.inputs != None:
                self.inputs[0].setText('Object')
                self.inputs[1].setText('Object')
        if self.inputs != None:
            self.inputs[0].setReadOnly(self.center == None)
            self.inputs[1].setReadOnly(self.center == None)
        self.setFocus()
        self.update()

    def executeSelectedItems(self, func, *args):
        if self.objectList == None:
            return
        for item in self.objectList.selectedItems():
            func(self.viewport.window.displayfile[str(item.text())], *args)
        self.update()

    def initCreation(self, clicks):
        if self.clickListener != None:
            Logger.log("Last selection canceled")
        if clicks <= 3:
            self.clickListener = SelectPointsListener(clicks, self.createNewObject)
        else:
            alerts.showCurveDialog()
            self.clickListener = SelectCurvePointsListener(self.createCurve)

    def createNewObject(self, points):
        dlg = ObjectDialog(len(points) > 2)
        text, color, ok, filled = dlg.getResults()
        self.clickListener = None
        # text, ok = QInputDialog.getText(
        #     self.parentWidget(), 'Input Dialog', 'Type the object name:')
        if ok and color and text:
            mappedPoints = self.viewport.mapPointsToWorld(points)
            obj = transformToObject(text, mappedPoints, color, filled)

            self.viewport.window.addObject(obj)
            if self.objectList != None:
                self.objectList.clear()
                self.objectList.addItems(
                    self.viewport.window.displayfile.keys())

            Logger.log(obj)
        else:
            Logger.log("Canceled")

    def createCurve(self, points):
        self.clickListener = None
        dlg = ObjectDialog()
        text, color, ok, filled = dlg.getResults()
        if ok and color and text:
            mappedPoints = self.viewport.mapPointsToWorld(points)
            pointList = []
            for point in mappedPoints:
                pointList.append(Point(point[0], point[1]))
            obj = Curve2D([BezierPoints(pointList[0], pointList[1], pointList[2], pointList[3])], text, color)

            self.viewport.window.addObject(obj)
            if self.objectList != None:
                self.objectList.clear()
                self.objectList.addItems(
                    self.viewport.window.displayfile.keys())

            Logger.log(obj)
        else:
            Logger.log("Canceled")

    # Paint event
    def paintEvent(self, event):
        if self.width() != self.viewport.Xvpmax or self.height() != self.viewport.Yvpmax:
            self.viewport.Xvpmax = self.width()
            self.viewport.Yvpmax = self.height()
            self.viewport.window.updateProportion(self.width(), self.height())
            self.updateStep()
        painter = QPainter(self)
        pen = QPen()

        pen.setWidth(2)
        pen.setColor(QColor(0, 0, 0))
        painter.setPen(pen)
        borderCoords = (self.step_x * BORDER, -self.step_y * BORDER)
        border = {
            "xmin": self.viewport.window.Xwmin + borderCoords[0],
            "xmax": self.viewport.window.Xwmax - borderCoords[0],
            "ymin": self.viewport.window.Ywmin + borderCoords[1],
            "ymax": self.viewport.window.Ywmax - borderCoords[1],
        }
        for obj in self.viewport.window.get_window_displayfile():
            obj_pen = QPen()
            obj_pen.setWidth(2)
            obj_pen.setColor(obj.color)
            painter.setBrush(QBrush(obj.color, Qt.SolidPattern))
            painter.setPen(obj_pen)
            # In case it is a point
            if isinstance(obj, Point):
                clippedObj = pointClipping(obj, border)
                if clippedObj != None:
                    xvp, yvp = self.viewport.transformToViewport(
                        clippedObj.locX, clippedObj.locY)
                    painter.drawPoint(xvp, yvp)

            # In case it is a line
            elif isinstance(obj, Line):
                clippedObj = lineClippingCohenSutherland(obj, border)
                if clippedObj != None:
                    p1_x, p1_y = self.viewport.transformToViewport(
                        clippedObj.p1.locX, clippedObj.p1.locY)
                    p2_x, p2_y = self.viewport.transformToViewport(
                        clippedObj.p2.locX, clippedObj.p2.locY)
                    painter.drawLine(p1_x, p1_y,
                                    p2_x, p2_y)

            # In case it is a wireframe
            else:
                points = []
                for lines in obj.lineList:
                    clippedObj = lineClippingCohenSutherland(lines, border)
                    if clippedObj != None:
                        p1_x, p1_y = self.viewport.transformToViewport(
                            clippedObj.p1.locX, clippedObj.p1.locY)
                        p2_x, p2_y = self.viewport.transformToViewport(
                            clippedObj.p2.locX, clippedObj.p2.locY)
                        if not obj.filled:
                            painter.drawLine(p1_x, p1_y,
                                            p2_x, p2_y)
                        else:
                            if len(points) == 0 or points[-1] != QPoint(p1_x, p1_y):
                                points.append(QPoint(p1_x, p1_y))
                            points.append(QPoint(p2_x, p2_y))
                if obj.filled:
                    poly = QPolygon(points)
                    painter.drawPolygon(poly)
            painter.setPen(pen)

        old_pen = pen
        pen = QPen()
        pen.setWidth(1)
        pen.setColor(QColor(255, 0, 0))
        painter.setPen(pen)

        if self.clickListener != None:
            preObject = self.clickListener.get_pre_object()
            if len(preObject) > 0:
                last = preObject[0]
                painter.drawPoint(last[0], last[1])
                for i in range(1, len(preObject)):
                    current = preObject[i]
                    painter.drawLine(last[0], last[1],
                                    current[0], current[1])
                    last = current

        if self.center != None:
            pen.setWidth(3)
            painter.setPen(pen)
            M = np.array([self.center[0], self.center[1], 1]).dot(
                self.viewport.window.current_matrix)
            xvp, yvp = self.viewport.transformToViewport(
                M[0], M[1])
            painter.drawPoint(xvp, yvp)

        painter.setPen(old_pen)

        p1_x, p1_y = self.viewport.transformToViewport(
            border["xmin"], border["ymin"])
        p2_x, p2_y = self.viewport.transformToViewport(
            border["xmin"], border["ymax"])
        p3_x, p3_y = self.viewport.transformToViewport(
            border["xmax"], border["ymax"])
        p4_x, p4_y = self.viewport.transformToViewport(
            border["xmax"], border["ymin"])

        painter.drawLine(p1_x, p1_y, p2_x, p2_y)
        painter.drawLine(p2_x, p2_y, p3_x, p3_y)
        painter.drawLine(p3_x, p3_y, p4_x, p4_y)
        painter.drawLine(p4_x, p4_y, p1_x, p1_y)

        painter.end()

    # Mouse Events
    def mousePressEvent(self, e):
        self.setFocus()
        self.lastPoint = (e.x(), e.y())
        if self.clickListener:
            self.clickListener.onClick(e.x(), e.y())
            self.update()
        else:
            if e.button() == Qt.RightButton:
                # Get Closes Object
                pointTuple = self.viewport.mapToWorld(e.x(), e.y())
                point = Point(pointTuple[0], pointTuple[1])
                min_distance = float('inf')
                closest = None
                for obj in self.viewport.window.displayfile.values():
                    current = obj.distance(point)
                    if current < min_distance:
                        min_distance = current
                        closest = obj

                if QApplication.keyboardModifiers() != Qt.ControlModifier:
                    for item in self.objectList.selectedItems():
                        item.setSelected(False)
                if min_distance < 3 * self.step_distance:
                    item = self.objectList.findItems(
                        closest.name, Qt.MatchExactly)[0]
                    item.setSelected(not item.isSelected())
                self.setFocus()
            elif e.button() == Qt.LeftButton:
                pass
                # Move object
            elif e.button() == Qt.MiddleButton:
                if self.center == None:
                    self.updateCenter(self.viewport.mapToWorld(e.x(), e.y()))
                else:
                    self.updateCenter()

    def mouseMoveEvent(self, e):
        if self.clickListener:
            return
        direction_x = (e.x() - self.lastPoint[0])
        direction_y = (e.y() - self.lastPoint[1])
        self.lastPoint = (e.x(), e.y())
        modifiers = QApplication.keyboardModifiers()
        if modifiers == Qt.ShiftModifier:
            # world_direction = self.viewport.window.get_world_position(direction_x, direction_y)
            transform = np.array([direction_x, direction_y]).dot(
                self.world_step_matrix)
            self.executeSelectedItems(
                Drawable.move, transform[0], transform[1])
        else:
            direction_x *= self.step_x
            direction_y *= self.step_y
            self.viewport.window.move(
                -direction_x, -direction_y)
            self.update()

    def mouseReleaseEvent(self, e):
        if self.clickListener:
            self.clickListener.onRelease(e.x(), e.y())
            self.update()

    def wheelEvent(self, e):
        if self.clickListener:
            return
        # Objects
        y = e.angleDelta().y()
        s = y / abs(y)
        modifiers = QApplication.keyboardModifiers()
        if modifiers == Qt.ControlModifier:
            self.executeSelectedItems(Drawable.scale, 1 + s * ZOOM)
        # Window
        elif modifiers == Qt.ShiftModifier:
            if self.objectList == None or len(self.objectList.selectedItems()) == 0:
                # center = self.viewport.mapToWindow(e.pos().x(), e.pos().y())
                self.viewport.window.rotate(s * ANGLE)
                self.update()
                self.updateStep()
            else:
                self.executeSelectedItems(
                    Drawable.rotate, s * ANGLE, self.center)
        else:
            center = self.viewport.mapToWindow(e.pos().x(), e.pos().y())
            self.viewport.window.zoom(-s * ZOOM, center)
            self.update()
            self.updateStep()

    # Key Events

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Return:
            self.clickListener.finish()
    #         if e.key() == Qt.Key_Up:
    #         elif e.key() == Qt.Key_Down:
    #         elif e.key() == Qt.Key_Left:
    #         elif e.key() == Qt.Key_Right:
    #         elif e.key() == Qt.Key_Equal:
    #         elif e.key() == Qt.Key_Minus:
    #     if e.key() == Qt.Key_Control:
    #     if e.key() == Qt.Key_Shift:

    # def keyReleaseEvent(self, e):
    #     if e.key() == Qt.Key_Control:
    #     if e.key() == Qt.Key_Shift:


def transformToObject(name, points, color, filled):
    if len(points) == 1:
        return Point(points[0][0], points[0][1], name, color)

    pointList = []
    for point in points:
        pointList.append(Point(point[0], point[1]))
    if len(pointList) == 2:
        return Line(pointList[0], pointList[1], name, color)

    lineList = []
    lastPoint = None
    for point in pointList:
        if lastPoint != None:
            lineList.append(Line(lastPoint, point))
        lastPoint = deepcopy(point)
    lineList.append(Line(deepcopy(pointList[-1]), deepcopy(pointList[0])))

    return Wireframe(lineList, name, color, filled)


class ViewportPoint(NamedTuple):
    x: int
    y: int


class ViewportObject(NamedTuple):
    '''Class to hold data of a object ready to be draw at viewport'''
    name: str
    points: List[ViewportPoint]
    color: QColor
    thickness: int
