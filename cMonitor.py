
from threading import Thread
from windowCapture.WindowsCapture import WindowCapture
from win32con import VK_CAPITAL


import os
import pyautogui

import json


class ClientMonitoring:

    bDontMustRunMe = False

    def __init__(self):
        bDontMustRunMe = True

    def checkIfClientIsOpen(self):
        if not self.bDontMustRunMe:
            bIsOpen = False

            try:
                wincap = WindowCapture("Riot Client")
                # League of Legends
                bIsOpen = True
            except:
                pass

            try:
                leagueOfLegendsClient = WindowCapture(
                    "League of Legends")
                bIsOpen = True
            except:
                pass

            return bIsOpen
        else:
            print("checkIfClientIsOpen doesn't process because bDontMustRunMe is True")

    def forceClientWindowOpen(self):
        if not self.bDontMustRunMe:
            t = Thread(target=lambda: os.system(
                '"C:\Riot Games\Riot Client\RiotClientServices.exe" --launch-product=league_of_legends --launch-patchline=live'))
            t.daemon = True
            t.start()
        else:
            print("forceClientWindowOpen doesn't process because bDontMustRunMe is True")

    def forceClientWindowClose(self):
        if not self.bDontMustRunMe:
            bRiotClientClosed = False
            bLeagueOfLegendsClosed = False

            try:
                riotClient = WindowCapture("Riot Client")
                riotClient.closeProcess()
            except:
                pass

            try:
                leagueOfLegendsClient = WindowCapture(
                    "League of Legends")
                leagueOfLegendsClient.closeProcess()
            except:
                pass

            try:
                riotClient = WindowCapture("Riot Client")
            except:
                bRiotClientClosed = True

            try:
                leagueOfLegendsClient = WindowCapture(
                    "League of Legends")
            except:
                bLeagueOfLegendsClosed = True

            return bRiotClientClosed == True and bLeagueOfLegendsClosed == True

        else:
            print("forceClientWindowClose doesn't process because bDontMustRunMe is True")

    def focusClient(self):
        try:
            wincap = WindowCapture("Riot Client")
            wincap.focusWindow()
        except:
            pass

        return True

    def makeLogin(self):
        self.focusClient()
        # if GetKeyState(VK_CAPITAL):
        #     pyautogui.press('capslock')
        login = ""
        password = ""

        with open('credentials.json') as json_file:
            data = json.load(json_file)
            login = data['login']
            password = data['password']

        pyautogui.typewrite(login)
        pyautogui.press('tab')
        pyautogui.typewrite(password)
        pyautogui.press('enter')
