from windowCapture.searchAreaSample import goldDigits
import cv2 as cv
from windowCapture.screenFinder import ScreenFinder
from windowCapture.WindowsCapture import WindowCapture
from windowCapture.searchAreaSample import searchAreaDic
from clientThread import ClientThread

from Console.consoleControler import ConsoleControler

from lcuHandlerThread import LcuHandlerThread

from inGameThread import InGameThread

import threading
from time import sleep


lock = threading.Lock()

consoleCtr = ConsoleControler("0.5a")


# ingameCtr.run()

clientCtr = ClientThread(consoleCtr, lock)

lcuHandlerCtr = LcuHandlerThread(consoleCtr, lock)

ingameCtr = InGameThread(consoleCtr, lock)

clientCtr.clientLCUControler = lcuHandlerCtr

lcuHandlerCtr.clientThread = clientCtr
lcuHandlerCtr.inGameThread = ingameCtr

ingameCtr.lcuThread = lcuHandlerCtr

# clientCtr.start()
# lcuHandlerCtr.start()
#lcuHandlerCtr.bMustRun = True
ingameCtr.start()
ingameCtr.bMustRunMe = True

# screenFinder = ScreenFinder()

# wincap = WindowCapture('League of Legends (TM) Client')


# while(True):

#     screenshot = wincap.get_screenshot()

#     firstDigit = screenFinder.getNumberFromArea(
#         goldDigits["first"].cropByScreenshot(screenshot))
#     secondDigit = screenFinder.getNumberFromArea(
#         goldDigits["second"].cropByScreenshot(screenshot))
#     thirdDigit = screenFinder.getNumberFromArea(
#         goldDigits["third"].cropByScreenshot(screenshot))
#     fourthDigit = screenFinder.getNumberFromArea(
#         goldDigits["fourth"].cropByScreenshot(screenshot))

#     # print(firstDigit)
#     print(f"{firstDigit}{secondDigit}{thirdDigit}{fourthDigit}")

#     image = goldDigits["first"].cropByScreenshot(screenshot)

#     cv.imshow("Janela", image)
#     if cv.waitKey(1) == ord('q'):
#         cv.destroyAllWindows()
#         break


#lcuCtr = LcuHandlerThread(consoleCtr, clientCtr, ingameCtr, lock)

#clientCtr.clientLCUControler = lcuCtr
