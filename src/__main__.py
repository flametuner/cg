import sys

from PyQt5.QtWidgets import QApplication

from window.main_window import MainWindow
from window.alerts import showInfoDialog

if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    showInfoDialog()
    # looping for window

    sys.exit(app.exec())
