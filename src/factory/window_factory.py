from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

def addButton(text, func, layout):
    obj = QPushButton(text)
    obj.clicked.connect(func)
    layout.addWidget(obj)
    return obj


def addLabel(text, layout):
    obj = QLabel()
    obj.setText(text)
    layout.addWidget(obj)
    return obj

def addLineEditDouble(layout):
    obj = QLineEdit()
    obj.setValidator(QDoubleValidator())
    layout.addWidget(obj)
    return obj