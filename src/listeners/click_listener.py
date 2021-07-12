
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