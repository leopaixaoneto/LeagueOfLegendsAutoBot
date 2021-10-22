import numpy as np


class SearchArea:

    x = 0
    y = 0
    w = 0
    h = 0
    imageToSearch = ""

  # constructor
    def __init__(self, x, y, w, h, imageToSearch):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.imageToSearch = imageToSearch

    def cropByScreenshot(self, ScreenShot):
        return ScreenShot[self.y:self.y+self.h, self.x:self.x+self.w]
