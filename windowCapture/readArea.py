
class ReadArea:

    x = 0
    y = 0
    w = 0
    h = 0

  # constructor

    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def cropByScreenshot(self, ScreenShot):
        return ScreenShot[self.y:self.y+self.h, self.x:self.x+self.w]
