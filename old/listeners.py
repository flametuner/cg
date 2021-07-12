
from PyQt5 import QtCore
from gui.log_view import Logger

class ClickListener:
    def __init__(self):
        self.x = -1
        self.y = -1

    def onClick(self, x, y):
        self.x = x
        self.y = y

    def onPress(self, x, y):
        self.x = x
        self.y = y

    def onRelease(self, x, y):
        self.x = x
        self.y = y

    def finish(self):
        pass


class ArrowKey:
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

class ArrowPressedListener:

    def onPress(self, key):
        pass