from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from dataclasses import astuple


import numpy as np
from math import sqrt
from typing import List, NamedTuple

from .alerts import showCurveDialog
from .object_dialog import *
from .log_viewer import Logger
from factory.object_factory import ObjectType, createObject
from objects.object import Object
from objects.point import Point
from objects.bezier_curve import BezierPoints
from objects.drawables.drawable import Drawable
from components.viewport import Viewport
from listeners.create_listener import *
from util.clipping_util import pointClipping

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
        self.updateBorder()
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
        point_1 = self.viewport.mapToWindow(Point(0, 0))
        point_2 = self.viewport.mapToWindow(Point(1, 1))
        self.step_x = point_2.x - point_1.x
        self.step_y = point_2.y - point_1.y

        point_zero = self.viewport.mapToWorld(Point(0, 0))
        point_x = self.viewport.mapToWorld(Point(1, 0))
        point_y = self.viewport.mapToWorld(Point(0, 1))
        self.world_step_matrix = np.array([[point_x.x - point_zero.x, point_x.y - point_zero.y],
                                           [point_y.x - point_zero.x, point_y.y - point_zero.y]])
        transform = np.array([1, 1]).dot(self.world_step_matrix)
        self.step_distance = sqrt(
            (transform[0] ** 2) + (transform[1] ** 2))

    def updateBorder(self):
        borderCoords = Point(self.step_x * BORDER, -self.step_y * BORDER)
        self.border = {
            "xmin": self.viewport.window.Xwmin + borderCoords.x,
            "xmax": self.viewport.window.Xwmax - borderCoords.x,
            "ymin": self.viewport.window.Ywmin + borderCoords.y,
            "ymax": self.viewport.window.Ywmax - borderCoords.y,
        }

    def updateCenter(self, xy=None):
        if xy != None:
            self.center = xy
            Logger.log(
                "Center selected (", self.center.x, self.center.y, ")")
            if self.inputs != None:
                self.inputs[0].setText(str(self.center.x))
                self.inputs[1].setText(str(self.center.y))
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

    # Paint event
    def paintEvent(self, event):
        if self.width() != self.viewport.Xvpmax or self.height() != self.viewport.Yvpmax:
            self.viewport.Xvpmax = self.width()
            self.viewport.Yvpmax = self.height()
            self.viewport.window.updateProportion(self.width(), self.height())
            self.updateStep()
            self.updateBorder()
        painter = QPainter(self)

        for obj in self.viewport.window.get_window_displayfile():
            if isinstance(obj, Drawable):
                obj.draw(painter, self.viewport, self.border)

        pen = QPen()
        pen.setWidth(1)
        pen.setColor(QColor(255, 0, 0))
        painter.setPen(pen)
        # Draw Pre Object
        if self.clickListener != None:
            # TODO Fazer Draw próprio
            preObject = self.clickListener.get_pre_object()
            if len(preObject) > 0:
                last = preObject[0]
                painter.drawPoint(last.x, last.y)
                for i in range(1, len(preObject)):
                    current = preObject[i]
                    painter.drawLine(last.x, last.y,
                                     current.x, current.y)
                    last = current

        # Draw world center
        if self.center != None:
            pen.setWidth(3)
            painter.setPen(pen)
            M = np.array([self.center.x, self.center.y, 1]).dot(
                self.viewport.window.current_matrix)

            obj = pointClipping(Point(M[0], M[1]), self.border)

            if obj != None:
                vp_point = self.viewport.transformToViewport(obj)
                painter.drawPoint(vp_point.x, vp_point.y)

        pen = QPen()

        pen.setWidth(1)
        pen.setColor(QColor(0, 0, 0))
        painter.setPen(pen)

        # Draw borders
        p1 = self.viewport.transformToViewport(
            Point(self.border["xmin"], self.border["ymin"]))
        p2 = self.viewport.transformToViewport(
            Point(self.border["xmin"], self.border["ymax"]))
        p3 = self.viewport.transformToViewport(
            Point(self.border["xmax"], self.border["ymax"]))
        p4 = self.viewport.transformToViewport(
            Point(self.border["xmax"], self.border["ymin"]))
        painter.drawLine(p1.x, p1.y, p2.x, p2.y)
        painter.drawLine(p2.x, p2.y, p3.x, p3.y)
        painter.drawLine(p3.x, p3.y, p4.x, p4.y)
        painter.drawLine(p4.x, p4.y, p1.x, p1.y)

        painter.end()

    # Mouse Events
    def mousePressEvent(self, e):
        self.setFocus()
        self.lastPoint = Point(e.x(), e.y())
        if self.clickListener:
            self.clickListener.onClick(e.x(), e.y())
            self.update()
        else:
            if e.button() == Qt.RightButton:
                # Get Closes Object
                point = self.viewport.mapToWorld(Point(e.x(), e.y()))
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
                    self.updateCenter(
                        self.viewport.mapToWorld(Point(e.x(), e.y())))
                else:
                    self.updateCenter()

    def mouseMoveEvent(self, e):
        if self.clickListener:
            return
        direction_x = e.x() - self.lastPoint.x
        direction_y = e.y() - self.lastPoint.y
        self.lastPoint = Point(e.x(), e.y())
        modifiers = QApplication.keyboardModifiers()
        if modifiers == Qt.ShiftModifier:
            transform = np.array([direction_x, direction_y]).dot(
                self.world_step_matrix)
            self.executeSelectedItems(
                Object.move, transform[0], transform[1])
        else:
            direction_x *= self.step_x
            direction_y *= self.step_y
            self.viewport.window.move(
                direction_x, direction_y)
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
            self.executeSelectedItems(Object.scale, 1 + s * ZOOM)
        # Window
        elif modifiers == Qt.ShiftModifier:
            if self.objectList == None or len(self.objectList.selectedItems()) == 0:
                # center = self.viewport.mapToWindow(e.pos().x(), e.pos().y())
                self.viewport.window.rotate(s * ANGLE)
                self.update()
                self.updateStep()
            else:
                center = astuple(self.center) if self.center != None else None
                self.executeSelectedItems(
                    Object.rotate, s * ANGLE, center)
        else:
            center = self.viewport.mapToWindow(Point(e.pos().x(), e.pos().y()))
            self.viewport.window.zoom(-s * ZOOM, astuple(center))
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

    def executeSelectedItems(self, func, *args):
        if self.objectList == None:
            return
        for item in self.objectList.selectedItems():
            func(self.viewport.window.displayfile[str(item.text())], *args)
        self.update()

    def initCreation(self, object_type):
        if self.clickListener != None:
            Logger.log("Last selection canceled")
        if object_type == ObjectType.CURVE2D:
            showCurveDialog()
            self.clickListener = SelectCurvePointsListener(
                self.openObjectDialog)
        else:
            self.clickListener = SelectPointsListener(
                object_type, self.openObjectDialog)

    def openObjectDialog(self, objType, pointList):
        dlg = ObjectDialog(len(pointList) > 2)
        text, color, ok, filled = dlg.getResults()
        self.clickListener = None
        # text, ok = QInputDialog.getText(
        #     self.parentWidget(), 'Input Dialog', 'Type the object name:')
        if ok and color and text:
            mappedPoints = self.viewport.mapPointsToWorld(pointList)
            op = {
                'filled': filled
            }

            obj = createObject(text, color, objType, mappedPoints, op)

            self.viewport.window.addObject(obj)
            if self.objectList != None:
                self.objectList.clear()
                self.objectList.addItems(
                    self.viewport.window.displayfile.keys())

            Logger.log(obj)
        else:
            Logger.log("Canceled")
