from tensorflow.python.framework import ops
import pickle
import h5py

import cv2 as cv
import numpy as np
#import pytesseract
import tensorflow.keras as keras


from tensorflow.keras.models import load_model

import tensorflow as tf


class ScreenFinder:
    model = None
    graph = None

    def __init__(self):
        # keras.backend.clear_session()
        # self.graph = tf.compat.v1.get_default_graph()

        pickle_in = open("./Models/model_trained.p", "rb")
        self.model = pickle.load(pickle_in)

        #self.model = load_model('model_trained.p')

    def find(self, screenShot, image, precision):
        searchedImage = cv.imread(image, cv.IMREAD_UNCHANGED)

        result = cv.matchTemplate(
            screenShot, searchedImage, cv.TM_CCOEFF_NORMED)

        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)

        if max_val >= precision:
            return True

        return False

    def findAndLoc(self, screenShot, image, precision):
        searchedImage = cv.imread(image, cv.IMREAD_UNCHANGED)

        result = cv.matchTemplate(
            screenShot, searchedImage, cv.TM_CCOEFF_NORMED)

        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)

        if max_val >= precision:
            return (True, max_loc)

        return (False, (-1, -1,))

    def findCountAndLoc(self, screenShot, image, precision):
        searchedImage = cv.imread(image, cv.IMREAD_UNCHANGED)

        result = cv.matchTemplate(
            screenShot, searchedImage, cv.TM_CCOEFF_NORMED)

        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)

        # the np.where() return the values below precision
        locations = np.where(result >= precision)
        # we can zip those up into position tuples
        locations = list(zip(*locations[::-1]))

        if max_val >= precision:
            return (True, len(locations), max_loc)

        return (False, 0, (-1, -1,),)

    def searchForOne(self, screenShot, image, precision):
        searchedImage = cv.imread(image, cv.IMREAD_UNCHANGED)

        result = cv.matchTemplate(
            screenShot, searchedImage, cv.TM_CCOEFF_NORMED)

        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)

        if max_val >= precision:
            # print("FOUND CHAMPION!")

            # get dimensions of the needle image
            searchedImage_w = searchedImage.shape[1]
            searchedImage_h = searchedImage.shape[0]

            top_left = (max_loc[0],
                        max_loc[1])

            bottom_right = (top_left[0] + searchedImage_w,
                            top_left[1] + searchedImage_h)

            cv.rectangle(screenShot, top_left, bottom_right, color=(
                0, 255, 0), thickness=2, lineType=cv.LINE_4)

        return screenShot

    def searchForAll(self, screenShot, image, precision):
        searchedImage = cv.imread(image, cv.IMREAD_UNCHANGED)

        result = cv.matchTemplate(
            screenShot, searchedImage, cv.TM_CCOEFF_NORMED)

        # the np.where() return the values below precision
        locations = np.where(result >= precision)
        # we can zip those up into position tuples
        locations = list(zip(*locations[::-1]))

        if locations:
            needle_w = searchedImage.shape[1]
            needle_h = searchedImage.shape[0]
            line_color = (0, 255, 0)
            line_type = cv.LINE_4

            for loc in locations:
                top_left = loc
                bottom_right = (top_left[0] + needle_w, top_left[1] + needle_h)

                cv.rectangle(screenShot, top_left,
                             bottom_right, line_color, line_type)

        return screenShot

    def countHowMany(self, screenShot, image, precision):
        searchedImage = cv.imread(image, cv.IMREAD_UNCHANGED)

        result = cv.matchTemplate(
            screenShot, searchedImage, cv.TM_CCOEFF_NORMED)

        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
        # the np.where() return the values below precision
        locations = np.where(result >= precision)
        # we can zip those up into position tuples
        locations = list(zip(*locations[::-1]))

        return (len(locations), max_loc, )

    def getPosOf(self, screenShot, image, precision):
        searchedImage = cv.imread(image, cv.IMREAD_UNCHANGED)

        result = cv.matchTemplate(
            screenShot, searchedImage, cv.TM_CCOEFF_NORMED)

        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)

        if max_val >= precision:
            return max_loc

        return False

    def getPercentOfHpBar(self, strip):
        totalPixels = 0

        for col in strip:
            for row in col:
                totalPixels += 1

        mask = cv.inRange(strip, (0, 0, 0), (30, 30, 30))

        strip = cv.bitwise_and(strip, strip, mask=mask)
        strip = cv.cvtColor(strip, cv.COLOR_RGB2GRAY)

        coloredPixels = cv.countNonZero(strip)

        # coloredPixels = cv.countNonZero(strip)
        return 1 - (coloredPixels/totalPixels)

    def getNumberFromArea(self, area):
        area = cv.resize(area, (32, 32))

        area = cv.cvtColor(area, cv.COLOR_RGB2GRAY)

        ret, thresh1 = cv.threshold(area, 50, 255, cv.THRESH_BINARY_INV)

        coloredPixels = cv.countNonZero(thresh1)

        if(coloredPixels < 500):
            thresh1 = cv.equalizeHist(thresh1)
            thresh1 = thresh1/255

            thresh1 = thresh1.reshape(1, 32, 32, 1)

            # with self.graph.as_default():
            response = self.model.predict_classes(thresh1)

            return str(response[0])

        return ""

    # def getTextFromScreenshot(self, readArea, ScreenShot):
    #     textArea = ScreenShot[readArea.y:readArea.y +
    #                           readArea.h, readArea.x: readArea.x+readArea.w]

    #     gray = cv.cvtColor(textArea, cv.COLOR_RGB2GRAY)

    #     # gray, img_bin = cv.threshold(
    #     #    textArea, 128, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)

    #     gray = cv.bitwise_not(gray)

    #     kernel = np.ones((2, 1), np.uint8)
    #     textArea = cv.erode(gray, kernel, iterations=1)
    #     textArea = cv.dilate(textArea, kernel, iterations=1)
    #     custom_config = r'--oem 3 --psm 6'

    #     text = pytesseract.image_to_string(textArea, config=custom_config)

    #     text = text.replace('O', '0')
    #     text = text.replace('o', '0')

    #     text = text.replace('i', '1')
    #     text = text.replace('I', '1')
    #     text = text.replace('l', '1')

    #     text = text.replace('z', '2')

    #     text = text.replace('H', '3')

    #     text = text.replace('A', '4')
    #     text = text.replace('d', '4')

    #     text = text.replace('S', '5')

    #     text = text.replace('T', '7')

    #     text = text.replace('B', '8')
    #     text = text.replace('g', '8')

    #     text = text.replace('/', '')
    #     text = text.replace('/', ',')

    #     return text
