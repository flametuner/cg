from gui.main_window import MainWindow
import sys
from PyQt5.QtWidgets import QApplication, QMessageBox
import numpy as np
from util import *
from alerts import showInfoDialog
# main method

if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    showInfoDialog()
    # looping for window

    sys.exit(app.exec())
