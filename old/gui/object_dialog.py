from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtGui import QColor


class ObjectDialog(QDialog):
    def __init__(self, canBeFilled=False):
        super(QDialog, self).__init__()
        # self.setupUi(self)

        self.color = None

        w = QWidget(self)

        self.resize(300, 150)
        w.resize(300, 150)

        l = QGridLayout()
        w.setLayout(l)

        self.name_lbl = QLabel()
        self.name_lbl.setText("Object Name:")
        self.nameinput = QLineEdit()

        self.color_selector = QPushButton('Select color', self)
        self.color_selector.clicked.connect(self.on_click)

        self.styleChoice = QLabel(self)

        self.ok_btn = QPushButton('Ok', self)
        self.ok_btn.clicked.connect(lambda: self.finish(True))

        self.cancel_btn = QPushButton('Cancel', self)
        self.cancel_btn.clicked.connect(lambda: self.finish(False))
        
        self.filled_btn = QCheckBox('Filled')
        # self.filled_btn.clicked.connect(lambda: self.finish(False))

        l.addWidget(self.name_lbl, 0, 0, 1, 1)
        l.addWidget(self.nameinput, 0, 1, 1, 2)
        l.addWidget(self.color_selector, 1, 0, 1, 1)

        if canBeFilled:
            l.addWidget(self.styleChoice, 1, 1, 1, 1)
            l.addWidget(self.filled_btn, 1, 2, 1, 1)
        else:
            l.addWidget(self.styleChoice, 1, 1, 1, 2)

        l.addWidget(self.ok_btn, 2, 2, 1, 1)
        l.addWidget(self.cancel_btn, 2, 1, 1, 1)
        self.updateColor(QColor(0, 0, 0))  # Black
        self.status = False
        # set initials values to widgets

    def finish(self, status):
        self.status = status
        self.filled = self.filled_btn.isChecked()
        self.done(status)

    def updateColor(self, color):
        self.color = color
        self.styleChoice.setStyleSheet(
            "QWidget { background-color: %s}" % self.color.name())

    @pyqtSlot()
    def on_click(self):
        self.openColorDialog()

    def openColorDialog(self):
        color = QColorDialog.getColor()

        if color.isValid():
            self.updateColor(color)

    def getResults(self):
        self.exec_()
        return self.nameinput.text(), self.color, self.status, self.filled
