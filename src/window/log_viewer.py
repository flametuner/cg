from PyQt5.QtWidgets import *

class Logger:
    logger = None
    initialized = False

    @staticmethod
    def init(loggerInstance):
        Logger.initialized = True
        Logger.logger = loggerInstance

    @staticmethod
    def log(*arg):
        if Logger.initialized:
            Logger.logger.log(' '.join(map(str, arg)))

class LogView(QPlainTextEdit):

    def __init__(self, parent = None):
        super().__init__(parent)
        self.setReadOnly(True)

    def log(self, message):
        self.appendPlainText(str(message))
        self.verticalScrollBar().setValue(self.verticalScrollBar().maximum())