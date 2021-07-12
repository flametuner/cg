from PyQt5.QtWidgets import QMessageBox

def showInfoDialog():
    msgBox = QMessageBox()
    msgBox.setIcon(QMessageBox.Information)
    msgBox.setText("""
    To navigate in the Window use the following commands:

    LEFT CLICK and MOVE on the Canvas to 'pan'
    Use the SCROLL to 'zoom in' and 'out'
    Use SHIFT + SCROLL without selected objects to 'rotate' the window

    To interact with Objects use the following commands:

    RIGHT CLICK to 'select' one object on Canvas
    CTRL + RIGHT CLICK to 'select' multiple objects on Canvas
    CTRL + LEFT CLICK and MOVE to 'move' the object
    CTRL + SCROLL to 'scale' the object
    SHIFT + SCROLL to 'rotate' the object

    To select the center point of the rotation you can either:

    CLICK on the left rotation buttons
    MIDDLE CLICK to select a custom center

    """)
    msgBox.setWindowTitle("Commands")
    msgBox.setStandardButtons(QMessageBox.Ok)

    msgBox.exec()

def showCurveDialog():
    msgBox = QMessageBox()
    msgBox.setIcon(QMessageBox.Information)
    msgBox.setText("""
    Click and drag to get each bezier line.

    After you have 2 lines, we can create a curve.

    Multicurves aren't supported yet.
    """)
    msgBox.setWindowTitle("Commands")
    msgBox.setStandardButtons(QMessageBox.Ok)

    msgBox.exec()