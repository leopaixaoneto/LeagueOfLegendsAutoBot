import cv2 as cv
import os
from time import sleep
from time import time

from windowCapture.WindowsCapture import WindowCapture
from windowCapture.searchAreaSample import searchAreaDic
from windowCapture.searchAreaSample import readAreaDic
from windowCapture.searchAreaSample import clickPointDic
from windowCapture.screenFinder import ScreenFinder

import win32gui
import win32ui
import win32con

import pyautogui
import pydirectinput


wincap = WindowCapture('League of Legends (TM) Client')
screenFinder = ScreenFinder()
wincap.setPosToOrigin()
loop_time = time()


while(True):

    # get an updated image of the game
    screenshot = wincap.get_screenshot()

    # press 'q' with the output window focused to exit.
    # waits 1 ms every loop to process key presses
    # screenshot = screenFinder.searchForAll(
    #     screenshot, imageDic["enemyMinion"], 0.9)

    # screenshot = screenFinder.searchForOne(
    #     screenshot, imageDic["enemyChampion"], 0.95)

    # screenshot = screenFinder.searchForOne(
    #     screenshot, imageDic["levelUpCheck"], 0.95)

    # screenshot = screenFinder.searchForOne(
    #     screenshot, imageDic["centralizedCam"], 0.95)

    # screenshotFinal = screenFinder.searchForOne(searchAreaDic["base"].cropByScreenshot(
    #     screenshot), searchAreaDic["base"].imageToSearch, 0.85)

    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break

    bImInBase = screenFinder.find(searchAreaDic["base"].cropByScreenshot(
        screenshot), searchAreaDic["base"].imageToSearch, 0.85)

    sleep(0.1)

    if bImInBase:
        print("Estou na Base")

        actualGold = screenFinder.getTextFromScreenshot(
            readAreaDic["gold"], screenshot)

        # pyautogui.typewrite("p")

        screenshot = wincap.get_screenshot()

        bImInBase = screenFinder.find(searchAreaDic["shop"].cropByScreenshot(
            screenshot), searchAreaDic["shop"].imageToSearch, 0.85)

        if bImInBase:
            print("Estou com o mercado aberto")

            bImInBase = screenFinder.find(searchAreaDic["arsenal"].cropByScreenshot(
                screenshot), searchAreaDic["arsenal"].imageToSearch, 0.7)

            if bImInBase:
                print("Estou com o arsenal certo")
            else:
                x = clickPointDic["openArsenalMenu"].x
                y = clickPointDic["openArsenalMenu"].y
                pydirectinput.click(x, y)

                sleep(.5)

                x = clickPointDic["selectArsenalItems"].x
                y = clickPointDic["selectArsenalItems"].y
                pydirectinput.click(x, y)

        else:
            print("Abrindo mercado")
            pydirectinput.press('p')

    cv.imshow('Computer Vision', screenshot)

    # print(actualGold)

    # print("não estou na base")p

    # debug the loop rate
    # print('FPS {}'.format(1 / (time() - loop_time)))
    loop_time = time()


# def list_window_names():
#     def winEnumHandler(hwnd, ctx):
#         if win32gui.IsWindowVisible(hwnd):
#             print(hex(hwnd), win32gui.GetWindowText(hwnd))
#     win32gui.EnumWindows(winEnumHandler, None)

# list_window_names()
