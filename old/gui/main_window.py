from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from gui.canvas import *
from gui.log_view import Logger, LogView
from objects import *
from listeners import *
from window import *

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
        buttonWidget = QWidget()
        buttonLayout = QVBoxLayout()
        buttonWidget.setLayout(buttonLayout)
        buttonWidget.setMaximumWidth(350)

        self.objects_lbl = QLabel()
        self.objects_lbl.setText("Objects")

        self.objectList = QListWidget()
        self.objectList.setSelectionMode(QAbstractItemView.ExtendedSelection)

        # Elements
        self.create_lbl = QLabel()
        self.create_lbl.setText("Create Objects")

        self.newPoint = QPushButton("New Point")
        self.newLine = QPushButton("New Line")
        self.newPolygon = QPushButton("New Wireframe")
        self.newCurve = QPushButton("New Curve")

        centerLayout = QHBoxLayout()
        centerWidget = QWidget()
        centerWidget.setLayout(centerLayout)

        self.center_lbl = QLabel()
        self.center_lbl.setText("Rotation center:")

        self.center_x_lbl = QLabel()
        self.center_x_lbl.setText("X:")

        # self.center_x_input = QDoubleSpinBox()
        self.center_x_input = QLineEdit()
        self.center_x_input.setValidator(QDoubleValidator())

        self.center_y_lbl = QLabel()
        self.center_y_lbl.setText("Y:")

        self.center_y_input = QLineEdit()
        self.center_y_input.setValidator(QDoubleValidator())

        self.apply_center_btn = QPushButton()
        self.apply_center_btn.setText("Apply")

        centerLayout.addWidget(self.center_x_lbl)
        centerLayout.addWidget(self.center_x_input)
        centerLayout.addWidget(self.center_y_lbl)
        centerLayout.addWidget(self.center_y_input)
        centerLayout.addWidget(self.apply_center_btn)

        btnCenterLayout = QHBoxLayout()
        btnCenterWidget = QWidget()
        btnCenterWidget.setLayout(btnCenterLayout)

        self.world_center_btn = QPushButton()
        self.world_center_btn.setText("World Center")

        self.obj_center_btn = QPushButton()
        self.obj_center_btn.setText("Object Center")

        btnCenterLayout.addWidget(self.world_center_btn)
        btnCenterLayout.addWidget(self.obj_center_btn)

        self.canvas = Canvas(self.window, w, self.objectList, (self.center_x_input, self.center_y_input))

        self.canvas.updateCenter()

        self.apply_center_btn.clicked.connect(lambda: self.canvas.updateCenter((float(self.center_x_input.text()), float(self.center_y_input.text()))))

        self.world_center_btn.clicked.connect(lambda: self.canvas.updateCenter((0, 0)))

        self.obj_center_btn.clicked.connect(lambda: self.canvas.updateCenter())

        self.newPoint.clicked.connect(lambda: self.canvas.initCreation(1))

        self.newLine.clicked.connect(lambda: self.canvas.initCreation(2))

        self.newPolygon.clicked.connect(lambda: self.canvas.initCreation(3))

        self.newCurve.clicked.connect(lambda: self.canvas.initCreation(4))

        buttonLayout.addWidget(self.objects_lbl)
        buttonLayout.addWidget(self.objectList)
        buttonLayout.addWidget(self.create_lbl)
        buttonLayout.addWidget(self.newPoint)
        buttonLayout.addWidget(self.newLine)
        buttonLayout.addWidget(self.newPolygon)
        buttonLayout.addWidget(self.newCurve)
        buttonLayout.addWidget(self.center_lbl)
        buttonLayout.addWidget(centerWidget)
        buttonLayout.addWidget(btnCenterWidget)

        l.addWidget(buttonWidget, 0, 0, 1, 1)
        l.addWidget(self.canvas, 0, 1, 5, 5)
        l.addWidget(Logger.logger, 6, 0, 6, 6)

        self.setCentralWidget(w)

    def updateObjectList(self, l):
        self.objectList.clear()
        self.objectList.addItems(l)

    # def initUi(self):
    #     self.setObjectName('MainWindow')
    #     # self.resize(850, 650)

    #     # Tools setup
    #     self.tools_menu_box = QGroupBox(self)
    #     self.tools_menu_box.setGeometry(QRect(10, 20, 171, 581))
    #     self.tools_menu_box.setTitle("Tools Menu")

    #     self.objects_lbl = QLabel(self.tools_menu_box)
    #     self.objects_lbl.setGeometry(QRect(10, 30, 57, 15))
    #     self.objects_lbl.setText("Objects")

    #     self.objects_list_view = QListView(self.tools_menu_box)
    #     self.objects_list_view.setGeometry(QRect(10, 50, 151, 121))

    #     self.items_model = QStandardItemModel()
    #     self.objects_list_view.setModel(self.items_model)

    #     self.objects_list_view.setContextMenuPolicy(
    #         Qt.CustomContextMenu)
    #     # self.objects_list_view.customContextMenuRequested.connect(
    #     #     self.custom_context_menu)

    #     self.objects_list_view_context_menu = QMenu(
    #         self.objects_list_view)
    #     self.color_change_action = QAction()
    #     self.color_change_action.setText('Change color')
    #     self.objects_list_view_context_menu.addAction(self.color_change_action)

    #     self.open_transformation_dialog_action = QAction()
    #     self.open_transformation_dialog_action.setText('Transform...')
    #     self.objects_list_view_context_menu.addAction(
    #         self.open_transformation_dialog_action)

    #     self.objects_list_view.addAction(self.color_change_action)
    #     self.objects_list_view.addAction(
    #         self.open_transformation_dialog_action)

    #     self.window_lbl = QLabel(self.tools_menu_box)
    #     self.window_lbl.setGeometry(QRect(10, 180, 71, 16))
    #     self.window_lbl.setText("Window")

    #     self.step_lbl = QLabel(self.tools_menu_box)
    #     self.step_lbl.setGeometry(QRect(10, 200, 31, 16))
    #     self.step_lbl.setText("Step:")

    #     self.step_input = QLineEdit(self.tools_menu_box)
    #     self.step_input.setText('10')
    #     self.step_input.setGeometry(QRect(50, 200, 41, 23))
    #     self.step_input.setValidator(QIntValidator(0, 500))

    #     self.view_up_btn = QPushButton(self.tools_menu_box)
    #     self.view_up_btn.setGeometry(QRect(30, 227, 41, 23))
    #     self.view_up_btn.setText("Up")

    #     self.view_left_btn = QPushButton(self.tools_menu_box)
    #     self.view_left_btn.setGeometry(QRect(10, 250, 41, 23))
    #     self.view_left_btn.setText("Left")

    #     self.view_right_btn = QPushButton(self.tools_menu_box)
    #     self.view_right_btn.setGeometry(QRect(52, 250, 41, 23))
    #     self.view_right_btn.setText("Right")

    #     self.view_down_btn = QPushButton(self.tools_menu_box)
    #     self.view_down_btn.setGeometry(QRect(30, 273, 41, 23))
    #     self.view_down_btn.setText("Down")

    #     self.in_btn = QPushButton(self.tools_menu_box)
    #     self.in_btn.setGeometry(QRect(95, 230, 31, 23))
    #     self.in_btn.setText("In")

    #     self.out_btn = QPushButton(self.tools_menu_box)
    #     self.out_btn.setGeometry(QRect(95, 270, 31, 23))
    #     self.out_btn.setText("Out")

    #     self.z_plus_btn = QPushButton(self.tools_menu_box)
    #     self.z_plus_btn.setGeometry(QRect(127, 230, 31, 23))
    #     self.z_plus_btn.setText("+")

    #     self.z_minus_btn = QPushButton(self.tools_menu_box)
    #     self.z_minus_btn.setGeometry(QRect(127, 270, 31, 23))
    #     self.z_minus_btn.setText("-")

    #     # Canvas setup
    #     self.viewport = ViewPort(self)
    #     self.viewport.setGeometry(QRect(200, 30, 600, 600))

    #     # Setting up menu bar
    #     self.menubar = QMenuBar(self)
    #     self.menubar.setGeometry(QRect(0, 0, 800, 20))

    #     self.menu_file = QMenu(self.menubar)
    #     self.menu_file.setTitle("File")
    #     self.setMenuBar(self.menubar)
    #     self.menubar.addAction(self.menu_file.menuAction())

    #     self.action_add_object = QAction(self)
    #     self.action_add_object.setText("Add object")
    #     self.menu_file.addAction(self.action_add_object)

    #     self.action_export_all_objects = QAction(self)
    #     self.action_export_all_objects.setText("Export all")
    #     self.menu_file.addAction(self.action_export_all_objects)

    #     self.action_import_wavefront = QAction(self)
    #     self.action_import_wavefront.setText("Import objects")
    #     self.menu_file.addAction(self.action_import_wavefront)
