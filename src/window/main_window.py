from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from window.canvas import *
from window.log_viewer import Logger, LogView
from listeners.click_listener import *
from components.window import *
from objects.point import Point
from factory.object_factory import ObjectType
from factory.window_factory import *
# creating class for main window


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.window = Window(-400, -300, 400, 300)

        Logger.init(LogView())
        Logger.log("Hello World")

        # Configuration
        title = "Graphic Computing"

        top = 400
        left = 200
        width = 1280
        height = 720

        self.setWindowTitle(title)
        self.setGeometry(top, left, width, height)
        self.setWindowFlags(Qt.Window | Qt.MSWindowsFixedSizeDialogHint)

        # Layout
        w = QWidget()
        l = QGridLayout()
        w.setLayout(l)

        self.objectList = QListWidget()
        self.objectList.setSelectionMode(QAbstractItemView.ExtendedSelection)

        buttonWidget = QWidget()
        buttonLayout = QVBoxLayout()
        buttonWidget.setLayout(buttonLayout)
        buttonWidget.setMaximumWidth(350)

        # Center Layout
        centerLayout = QHBoxLayout()
        centerWidget = QWidget()
        centerWidget.setLayout(centerLayout)

        addLabel("X:", centerLayout)
        self.center_x_input = addLineEditDouble(centerLayout)

        addLabel("Y:", centerLayout)
        self.center_y_input = addLineEditDouble(centerLayout)

        addButton("Apply", lambda: self.canvas.updateCenter(Point(float(
            self.center_x_input.text()), float(self.center_y_input.text()))), centerLayout)

        # Center buttons layout
        btnCenterLayout = QHBoxLayout()
        btnCenterWidget = QWidget()
        btnCenterWidget.setLayout(btnCenterLayout)

        addButton("World Center", lambda: self.canvas.updateCenter(
            Point(0, 0)), btnCenterLayout)
        addButton("Object Center",
                  lambda: self.canvas.updateCenter(), btnCenterLayout)

        # Canvas
        self.canvas = Canvas(self.window, w, self.objectList,
                             (self.center_x_input, self.center_y_input))

        self.canvas.updateCenter()

        # Elements
        addLabel("Objects", buttonLayout)
        buttonLayout.addWidget(self.objectList)
        addLabel("Create Objects", buttonLayout)
        addButton("New Point", lambda: self.canvas.initCreation(
            ObjectType.POINT), buttonLayout)
        addButton("New Line", lambda: self.canvas.initCreation(
            ObjectType.LINE), buttonLayout)
        addButton("New Wireframe", lambda: self.canvas.initCreation(
            ObjectType.WIREFRAME), buttonLayout)
        addButton("New Curve", lambda: self.canvas.initCreation(
            ObjectType.CURVE2D), buttonLayout)
        addLabel("Rotation center:", buttonLayout)

        # self.center_x_input = QDoubleSpinBox()

        buttonLayout.addWidget(centerWidget)
        buttonLayout.addWidget(btnCenterWidget)

        l.addWidget(buttonWidget, 0, 0, 1, 1)
        l.addWidget(self.canvas, 0, 1, 5, 5)
        l.addWidget(Logger.logger, 6, 0, 6, 6)

        self.setCentralWidget(w)

    def updateObjectList(self, l):
        self.objectList.clear()
        self.objectList.addItems(l)
