from time import sleep
import time

import sys
import cv2 as cv

import asyncio

import threading
from Console.consoleControler import ConsoleControler

from windowCapture.WindowsCapture import WindowCapture

from ShopSystem.buyOrder import BuyOrder
from ShopSystem.itemSample import getBuyOrderList

from windowCapture.searchAreaSample import goldDigits
from windowCapture.searchAreaSample import searchAreaDic
from windowCapture.searchAreaSample import readAreaDic
from windowCapture.searchAreaSample import clickPointDic
from windowCapture.screenFinder import ScreenFinder
from windowCapture.vectorCalc import VectorCalc
from ChampionRules.Caitlyn import Caitlyn

import win32gui
import win32ui
import win32con

import pyautogui
import pydirectinput


class InGameThread(threading.Thread):

    # Testing
    champion = Caitlyn()
    build = getBuyOrderList("ad1")

    # Screen Infos:
    allyMinionsFinded = False
    allyMinions = 0
    allyMinionLoc = (0, 0,)

    enemyMinionsFinded = False
    enemyMinions = 0
    enemyMinionLoc = (0, 0,)

    enemyChampionFinded = False
    enemyChampionLoc = (0, 0,)

    enemyTowerFind = False
    enemyTowerLoc = (0, 0,)

    # Start of Time Routine Area
    lastCheckHP = 0
    lastCheckMinions = 0
    lastCheckCamera = 0
    lastCheckSkills = 0
    lastCheckEAT = 0
    lastCheckBuyItens = 0

    # End of Time Routine Area

    # Start of Hp Area
    hp = 0
    status = "Alive"
    previousHP = 0

    # alterar centro da imagem
    middleX = 450
    middleY = 335

    lock = None
    globalFlag = True
    bMustRunMe = False
    consoleCtr = None
    wincap = None
    screenFinder = None
    screenshot = None
    veCalc = VectorCalc()
    lcuThread = None

    def __init__(self, consoleCtr, lock):
        threading.Thread.__init__(self)
        self.consoleCtr = consoleCtr
        self.lock = lock
        # self.lcuThread = lcuThread

        aux = time.time()

        self.lastCheckHP = aux
        self.lastCheckMinions = aux
        self.lastCheckCamera = aux
        self.lastCheckEAT = aux

    def initAllData(self):
        # Testing
        self.champion = Caitlyn()
        self.build = getBuyOrderList("ad1")

        # Screen Infos:
        self.allyMinionsFinded = False
        self.allyMinions = 0
        self.allyMinionLoc = (0, 0,)

        self.enemyMinionsFinded = False
        self.enemyMinions = 0
        self.enemyMinionLoc = (0, 0,)

        self.enemyChampionFinded = False
        self.enemyChampionLoc = (0, 0,)

        self.enemyTowerFind = False
        self.enemyTowerLoc = (0, 0,)

        # Start of Time Routine Area
        self.lastCheckHP = 0
        self.lastCheckMinions = 0
        self.lastCheckCamera = 0
        self.lastCheckSkills = 0
        self.lastCheckEAT = 0
        self.lastCheckBuyItens = 0

    def makeNewScreenShot(self):
        try:
            self.screenshot = self.wincap.get_screenshot()
            return True
        except Exception as identifier:
            print("Erro ao tentar tirar uma nova screenShot")
            # print(identifier)
            return False

# --------------------------------- Get POS AREA ---------------------------------------
    def getPosOfAllyMinion(self, bMustNewScreenShot=True):
        if bMustNewScreenShot:
            self.makeNewScreenShot()

        var = self.screenFinder.getPosOf(searchAreaDic["allyMinion"].cropByScreenshot(
            self.screenshot), searchAreaDic["allyMinion"].imageToSearch, 0.9)

        if(var == False):
            return (-1, -1)

        return (var[0] + searchAreaDic["allyMinion"].x, var[1] + searchAreaDic["allyMinion"].y)

    def getPosOfEnemyMinion(self, bMustNewScreenShot=True):
        if bMustNewScreenShot:
            self.makeNewScreenShot()

        var = self.screenFinder.getPosOf(searchAreaDic["enemyMinion"].cropByScreenshot(
            self.screenshot), searchAreaDic["enemyMinion"].imageToSearch, 0.9)

        return (var[0] + searchAreaDic["enemyMinion"].x, var[1] + searchAreaDic["enemyMinion"].y)

# ----------------------------FIND COUNT LOC AREA ------------------------------------

    def findCountAndLocEnemyMinions(self, bMustNewScreenShot=True, searchArea=None):
        if not searchArea is None:
            searchArea = searchAreaDic["enemyMinion"].cropByScreenshot(
                self.screenshot)

        if bMustNewScreenShot:
            self.makeNewScreenShot()
        return self.screenFinder.findCountAndLoc(searchArea, searchAreaDic["enemyMinion"].imageToSearch, 0.9)

    def findCountAndLocAllyMinions(self, bMustNewScreenShot=True, searchArea=None):
        if not searchArea is None:
            searchArea = searchAreaDic["allyMinion"].cropByScreenshot(
                self.screenshot)

        if bMustNewScreenShot:
            self.makeNewScreenShot()

        return self.screenFinder.findCountAndLoc(searchArea, searchAreaDic["allyMinion"].imageToSearch, 0.9)

    def findCountAndLocEnemyChampions(self, bMustNewScreenShot=True):
        if bMustNewScreenShot:
            self.makeNewScreenShot()

        return self.screenFinder.findCountAndLoc(searchAreaDic["enemyChampion"].cropByScreenshot(
            self.screenshot), searchAreaDic["enemyChampion"].imageToSearch, 0.9)


# --------------------------------- COUNT AREA ---------------------------------------

    def countEnemyMinions(self, bMustNewScreenShot=True):
        if bMustNewScreenShot:
            self.makeNewScreenShot()

        return self.screenFinder.countHowMany(searchAreaDic["enemyMinion"].cropByScreenshot(
            self.screenshot), searchAreaDic["enemyMinion"].imageToSearch, 0.9)

    def countEnemyChampions(self, bMustNewScreenShot=True):
        if bMustNewScreenShot:
            self.makeNewScreenShot()

        return self.screenFinder.countHowMany(searchAreaDic["enemyChampion"].cropByScreenshot(
            self.screenshot), searchAreaDic["enemyChampion"].imageToSearch, 0.9)

    def countGold(self, bMustNewScreenShot=True):
        if bMustNewScreenShot:
            self.makeNewScreenShot()

        firstDigit = self.screenFinder.getNumberFromArea(
            goldDigits["first"].cropByScreenshot(self.screenshot))
        secondDigit = self.screenFinder.getNumberFromArea(
            goldDigits["second"].cropByScreenshot(self.screenshot))
        thirdDigit = self.screenFinder.getNumberFromArea(
            goldDigits["third"].cropByScreenshot(self.screenshot))
        fourthDigit = self.screenFinder.getNumberFromArea(
            goldDigits["fourth"].cropByScreenshot(self.screenshot))

        return int(f"{firstDigit}{secondDigit}{thirdDigit}{fourthDigit}")

    def countActualHp(self, bMustNewScreenShot=True):
        x = readAreaDic["hpPercentBar"].x
        y = readAreaDic["hpPercentBar"].y
        w = readAreaDic["hpPercentBar"].w
        h = readAreaDic["hpPercentBar"].h

        try:
            screenshot = self.wincap.get_screenshotAtPos(x, y, w, h)
            percent = self.screenFinder.getPercentOfHpBar(screenshot)
            return percent*100
        except Exception as ex:
            print(ex)
            return 100

    def countAllyMinions(self, bMustNewScreenShot=True):
        if bMustNewScreenShot:
            self.makeNewScreenShot()

        return self.screenFinder.countHowMany(searchAreaDic["allyMinion"].cropByScreenshot(
            self.screenshot), searchAreaDic["allyMinion"].imageToSearch, 0.9)

# --------------------------------- CHECK AREA ---------------------------------------

    def checkForAllyMinions(self, bMustNewScreenShot=True):
        if bMustNewScreenShot:
            self.makeNewScreenShot()
        return self.screenFinder.find(searchAreaDic["allyMinion"].cropByScreenshot(
            self.screenshot), searchAreaDic["allyMinion"].imageToSearch, 0.9)

    def checkForEnemyMinions(self, bMustNewScreenShot=True):
        if bMustNewScreenShot:
            self.makeNewScreenShot()
        return self.screenFinder.find(searchAreaDic["enemyMinion"].cropByScreenshot(
            self.screenshot), searchAreaDic["enemyMinion"].imageToSearch, 0.9)

    def checkForEnemyChampions(self, bMustNewScreenShot=True):
        if bMustNewScreenShot:
            self.makeNewScreenShot()
        return self.screenFinder.find(searchAreaDic["enemyChampion"].cropByScreenshot(
            self.screenshot), searchAreaDic["enemyChampion"].imageToSearch, 0.9)

    def checkForEnemyTower(self, bMustNewScreenShot=True):
        if bMustNewScreenShot:
            self.makeNewScreenShot()

        return self.screenFinder.find(searchAreaDic["enemyTower"].cropByScreenshot(self.screenshot), searchAreaDic["enemyTower"].imageToSearch, 0.7)

    def checkIfIsInBase(self, bMustNewScreenShot=True):
        if bMustNewScreenShot:
            self.makeNewScreenShot()
        return self.screenFinder.find(searchAreaDic["base"].cropByScreenshot(
            self.screenshot), searchAreaDic["base"].imageToSearch, 0.85)

    def checkIfIsBasing(self, bMustNewScreenShot=True):
        if bMustNewScreenShot:
            self.makeNewScreenShot()
        return self.screenFinder.find(searchAreaDic["basing"].cropByScreenshot(
            self.screenshot), searchAreaDic["basing"].imageToSearch, 0.95)

    def checkIfShopIsOpen(self, bMustNewScreenShot=True):
        if bMustNewScreenShot:
            self.makeNewScreenShot()
        return self.screenFinder.find(searchAreaDic["shop"].cropByScreenshot(
            self.screenshot), searchAreaDic["shop"].imageToSearch, 0.85)

    def checkIfArsenalIsRight(self, bMustNewScreenShot=True):
        if bMustNewScreenShot:
            self.makeNewScreenShot()
        return self.screenFinder.find(searchAreaDic["arsenal"].cropByScreenshot(
            self.screenshot), searchAreaDic["arsenal"].imageToSearch, 0.8)

    def checkForLevelUpAvaibility(self, q=True, e=True, w=True, r=True, bMustNewScreenShot=True):
        if bMustNewScreenShot:
            self.makeNewScreenShot()
        result = False
        if q:
            result = (result or self.checkLevelUpAvaibilityQ())
        if w:
            result = (result or self.checkLevelUpAvaibilityW())
        if e:
            result = (result or self.checkLevelUpAvaibilityE())
        if r:
            result = (result or self.checkLevelUpAvaibilityR())

        return result

    def checkLevelUpAvaibilityQ(self, bMustNewScreenShot=True):
        if bMustNewScreenShot:
            self.makeNewScreenShot()
        return self.screenFinder.find(searchAreaDic["levelUp-Q"].cropByScreenshot(
            self.screenshot), searchAreaDic["levelUp-Q"].imageToSearch, 0.8)

    def checkLevelUpAvaibilityW(self, bMustNewScreenShot=True):
        if bMustNewScreenShot:
            self.makeNewScreenShot()
        return self.screenFinder.find(searchAreaDic["levelUp-W"].cropByScreenshot(
            self.screenshot), searchAreaDic["levelUp-W"].imageToSearch, 0.8)

    def checkLevelUpAvaibilityE(self, bMustNewScreenShot=True):
        if bMustNewScreenShot:
            self.makeNewScreenShot()
        return self.screenFinder.find(searchAreaDic["levelUp-E"].cropByScreenshot(
            self.screenshot), searchAreaDic["levelUp-E"].imageToSearch, 0.8)

    def checkLevelUpAvaibilityR(self, bMustNewScreenShot=True):
        if bMustNewScreenShot:
            self.makeNewScreenShot()
        return self.screenFinder.find(searchAreaDic["levelUp-R"].cropByScreenshot(
            self.screenshot), searchAreaDic["levelUp-R"].imageToSearch, 0.8)

    def checkIfCameraIsCentralized(self, bMustNewScreenShot=True):
        if bMustNewScreenShot:
            self.makeNewScreenShot()
        return self.screenFinder.find(searchAreaDic["centralizedCam"].cropByScreenshot(
            self.screenshot), searchAreaDic["centralizedCam"].imageToSearch, 0.90)

    def checkIfIsInLoadingScreen(self, bMustNewScreenShot=True):
        if bMustNewScreenShot:
            self.makeNewScreenShot()
        return self.screenFinder.find(searchAreaDic["loadingScreen"].cropByScreenshot(
            self.screenshot), searchAreaDic["loadingScreen"].imageToSearch, 0.90)

    def checkIfPlayerIsDead(self, bMustNewScreenShot=True):
        actualHP = int(self.hp)

        if(actualHP < 1):
            if(not self.status == "Dead"):
                self.consoleCtr.printInConsole(
                    f"Player Morreu!", "ERROR")
            self.status = "Dead"

        else:
            self.status = "Alive"

# -----------------------  Check And Get Pos Area ---------------------------------

    def findAndLocEnemyTower(self, bMustNewScreenShot=True, searchArea=None):
        if searchArea.any():
            searchArea = searchAreaDic["enemyTower"].cropByScreenshot(
                self.screenshot)

        if bMustNewScreenShot:
            self.makeNewScreenShot()

        return self.screenFinder.findAndLoc(
            searchArea, searchAreaDic["enemyTower"].imageToSearch, 0.7)

    def findandlocEnemyChampion(self, bMustNewScreenShot=True, searchArea=None):
        if searchArea.any():
            searchArea = searchAreaDic["enemyTower"].cropByScreenshot(
                self.screenshot)

        if bMustNewScreenShot:
            self.makeNewScreenShot()

        return self.screenFinder.findAndLoc(
            searchArea, searchAreaDic["enemyChampion"].imageToSearch, 0.9)


# --------------------------------- DO AREA ---------------------------------------


    def doMouseClick(self, x, y, duration, buttonName="left"):
        pydirectinput.moveTo(x, y)

        pydirectinput.mouseDown(button=buttonName)
        sleep(duration)
        pydirectinput.mouseUp(button=buttonName)

    def doMouseClickWithName(self, name, duration, buttonName="left"):
        pydirectinput.moveTo(
            clickPointDic[name].x, clickPointDic[name].y)

        pydirectinput.mouseDown(button=buttonName)
        sleep(duration)
        pydirectinput.mouseUp(button=buttonName)

    def doUseSkillWMousePos(self, mx, my, skill):
        pydirectinput.moveTo(mx, my)
        pydirectinput.keyDown(skill)
        sleep(0.5)
        pydirectinput.keyUp(skill)

    def doFixArsenal(self):
        self.doMouseClickWithName("openArsenalMenu", 0.2)

        sleep(.1)

        self.doMouseClickWithName("selectArsenalItems", 0.2)

    def doOpenShop(self):
        pydirectinput.press('p')

    def doSkillLevelUp(self, skill):
        pydirectinput.keyDown('ctrl')
        pydirectinput.keyDown(skill)
        sleep(0.5)
        pydirectinput.keyUp(skill)
        pydirectinput.keyUp('ctrl')

    def doFirstBuy(self):
        gold = self.countGold(True)
        self.consoleCtr.addInfo(
            f"TO COM GOLD: {gold}", ConsoleControler.GOOD)
        self.consoleCtr.printPanel()
        self.bMustRunMe = False

    def doActiveCentralizedCamera(self):
        pydirectinput.press('y')

    def doRetreat(self, tNumber):
        self.doMouseClickWithName(
            "retreatToT1Bot", 0.2, buttonName='right')

    def doRetreatToBase(self, tNumber):
        self.doMouseClickWithName(
            "retreatToBase", 0.2, buttonName='right')

    def doReturnToBase(self):
        pydirectinput.press('b')

    def doRoutine(self, routine, args, expectedValue, tries=3, timeBetweenTries=1):
        while (tries > 0):
            if routine(*args) != expectedValue:
                tries = tries - 1
                sleep(timeBetweenTries)
            else:
                return True
        return False

    def doBuyItem(self, item):
        self.doMouseClick(item.x, item.y, 0.2)
        self.doMouseClick(item.x, item.y, 0.2)

    # --------------------------------- ROUTINE AREA ---------------------------------------

    def routineLoadingScreen(self):

        while not self.doRoutine(self.checkIfIsInLoadingScreen, (True,), False, timeBetweenTries=0.2):
            self.consoleCtr.printInConsole(
                "Em LoadingScreen!", "INFO")

        self.consoleCtr.printInConsole(
            "Partida em Andamento!", "GOOD")

        return True

    def routineCentralizeCamera(self, bMessage=False):

        if(time.time() - self.lastCheckCamera > 4.0):

            while(self.checkIfCameraIsCentralized()):
                self.doActiveCentralizedCamera()
                if bMessage:
                    self.consoleCtr.printInConsole(
                        "Ativando Centralizar Camera", "INFO")
                sleep(.2)

            self.lastCheckCamera = time.time()

    def routineSearchMinionsChampionsTowers(self, bMessage=False):
        if(time.time() - self.lastCheckEAT > 0.1):
            eatSearchArea = searchAreaDic["enemyTower"].cropByScreenshot(
                self.screenshot)

            self.enemyTowerFind, self.enemyTowerLoc = self.findAndLocEnemyTower(
                searchArea=eatSearchArea)

            self.allyMinionFinded, self.allyMinions, self.allyMinionLoc = self.findCountAndLocAllyMinions(
                searchArea=eatSearchArea)

            self.enemyMinionFinded, self.enemyMinions, self.enemyMinionLoc = self.findCountAndLocEnemyMinions(
                searchArea=eatSearchArea)

            self.enemyChampionFinded, self.enemyChampionLoc = self.findandlocEnemyChampion(
                searchArea=eatSearchArea)

            if self.enemyTowerFind:
                self.enemyTowerLoc = (self.enemyTowerLoc[0] + searchAreaDic["enemyTower"].x,
                                      self.enemyTowerLoc[1] + searchAreaDic["enemyTower"].y,)

            if self.enemyChampionFinded:
                self.enemyChampionLoc = (self.enemyChampionLoc[0] + searchAreaDic["enemyChampion"].x,
                                         self.enemyChampionLoc[1] + searchAreaDic["enemyChampion"].y,)

            if self.allyMinionFinded:
                self.allyMinionLoc = (self.allyMinionLoc[0] + searchAreaDic["enemyTower"].x,
                                      self.allyMinionLoc[1] + searchAreaDic["enemyTower"].y,)

            if self.enemyMinionFinded:
                self.enemyMinionLoc = (self.enemyMinionLoc[0] + searchAreaDic["enemyTower"].x,
                                       self.enemyMinionLoc[1] + searchAreaDic["enemyTower"].y,)

            if bMessage:
                self.consoleCtr.printInConsole(
                    f"AllyMinions: {self.allyMinions} || EnemyMinions: {self.enemyMinions} || EnemyChampions: {self.enemyChampionFinded} || EnemyTower: {self.enemyTowerFind}", "INFO")

            # print(
            #     f"aFinded: {allyMinionFinded} || aCount: {self.allyMinions}  || aLoc: {self.allyMinionLoc} ||")

            # print(
            #     f"eFinded: {enemyMinionFinded} || eCount: {self.enemyMinions}  || eLoc: {self.enemyMinionLoc} ||")

            self.lastCheckEAT = time.time()

    def routineAttackWithMinions(self):

        if(time.time() - self.lastCheckMinions > 0.1):
            if(not self.status == "Dead" and not self.status == "Basing"):
                if(self.enemyTowerFind and self.allyMinions > 1):
                    if(self.veCalc.dist(self.middleX, self.middleY, self.enemyTowerLoc[0], self.enemyTowerLoc[1]) < 400 and self.allyMinions > 0):
                        self.doMouseClick(
                            self.enemyTowerLoc[0]+90, self.enemyTowerLoc[1]+100, 0.2)

                elif((self.allyMinions > 1)):
                    posx, posy = self.allyMinionLoc
                    if(posx == -1 and posy == -1):
                        print("nani?")
                        return

                    self.doMouseClick(posx, posy, 0.2)

                elif ((self.allyMinions <= 1) and (self.enemyMinions > 0) or (self.allyMinions <= 1) and (self.enemyTowerFind)):
                    try:
                        # TODO TRATATIVA PARA RECUAR
                        self.routineGoToSafeZone()

                        self.consoleCtr.printInConsole(
                            "Retirada muitos minions inimigos!", "INFO")

                    except Exception as ex:
                        print(ex)
                        pass

                self.lastCheckMinions = time.time()

    def routineUseSkillsInEnemyChampions(self, bMessage):
        if (not self.enemyTowerFind and self.enemyChampionFinded):
            if(not self.status == "Dead" and not self.status == "Basing"):

                if(self.champion.autoAttack(self.allyMinions, self.allyMinionLoc, self.enemyMinions, self.enemyMinionLoc, self.enemyChampionLoc)):
                    self.doMouseClick(
                        self.enemyChampionLoc[0]+90, self.enemyChampionLoc[1]+100, 0.2)

                elif(self.champion.qCheck(self.allyMinions, self.allyMinionLoc, self.enemyMinions, self.enemyMinionLoc, self.enemyChampionLoc)):
                    self.doUseSkillWMousePos(
                        self.enemyChampionLoc[0]+90, self.enemyChampionLoc[1]+100, "q")

                elif(self.champion.rCheck(self.allyMinions, self.allyMinionLoc, self.enemyMinions, self.enemyMinionLoc, self.enemyChampionLoc)):
                    self.doUseSkillWMousePos(
                        self.enemyChampionLoc[0]+90, self.enemyChampionLoc[1]+100, "r")

    def routineCheckActualHP(self, bMessage):
        self.previousHP = self.hp
        self.hp = self.countActualHp()
        self.checkIfPlayerIsDead()
        elapsed_time = time.time() - self.lastCheckHP

        if(elapsed_time > 0.1):
            if(not self.status == "Dead" and not self.status == "Basing"):
                if(bMessage):
                    self.consoleCtr.printInConsole(
                        f"Hp: {int(self.hp)}%", "INFO")

                hpDif = self.previousHP - self.hp
                hpDifPerTime = hpDif / elapsed_time

                if hpDifPerTime > 5:
                    if(bMessage):
                        self.consoleCtr.printInConsole(
                            f"TOMANDO MUITO DANO! RECUANDO", "ERROR")

                    self.routineGoToSafeZone()

                elif self.hp < 25:

                    if(bMessage):
                        self.consoleCtr.printInConsole(
                            f"VIDA ABAIXO DE 25% RETORNANDO BASE", "ERROR")

                    self.routineGoToBase()

                self.lastCheckHP = time.time()

    def routineCheckLevelUp(self, bMessage=True):
        if(time.time() - self.lastCheckSkills > 5):
            if(self.checkForLevelUpAvaibility()):
                pydirectinput.keyDown('ctrl')
                done = False

                if(self.checkLevelUpAvaibilityR() and done == False):
                    self.consoleCtr.printInConsole(
                        f"AUMENTANDO NÍVEL DE HABILIDADE - R", "GOOD")
                    pydirectinput.press('r')
                    done = True

                if(self.checkLevelUpAvaibilityQ() and done == False):
                    self.consoleCtr.printInConsole(
                        f"AUMENTANDO NÍVEL DE HABILIDADE - Q", "GOOD")
                    pydirectinput.press('q')

                if(self.checkLevelUpAvaibilityW() and done == False):
                    self.consoleCtr.printInConsole(
                        f"AUMENTANDO NÍVEL DE HABILIDADE - W", "GOOD")
                    pydirectinput.press('w')

                if(self.checkLevelUpAvaibilityE() and done == False):
                    self.consoleCtr.printInConsole(
                        f"AUMENTANDO NÍVEL DE HABILIDADE - E", "GOOD")
                    pydirectinput.press('e')

                sleep(.2)
                self.lastCheckSkills = time.time()
            pydirectinput.keyUp('ctrl')

    def routineCheckIfIsCompletlySafe(self, bMessage=True):
        threat = 0
        threat += self.countEnemyMinions()[0]
        threat += self.countEnemyChampions()[0]

        if self.checkForEnemyTower():
            threat += 1

        if threat <= 0:
            return True

        return False

    def routineCheckIfIsSafe(self, bMessage=True):
        threat = 0
        threat += self.countEnemyMinions()[0]
        threat += 4 * self.countEnemyChampions()[0]
        threat -= self.countAllyMinions()[0]

        if self.checkForEnemyTower():
            threat += 99

        if threat <= 0:
            return True

        return False

    def routineGoToBase(self, bMessage=True):
        inBase = self.checkIfIsInBase()
        self.status = "Basing"

        while not inBase:
            if(inBase):
                break

            if(self.checkIfPlayerIsDead()):
                self.status = "Dead"
                self.consoleCtr.printInConsole(
                    f"Player morreu!", "INFO")

                break

            if(self.checkIfPlayerIsDead()):
                self.consoleCtr.printInConsole(
                    f"Player está morto!", "INFO")
                self.status = "Dead"
                break

            if self.routineCheckIfIsCompletlySafe():

                self.consoleCtr.printInConsole(
                    f"Player está safe", "GOOD")
                if not self.checkIfIsBasing():
                    self.consoleCtr.printInConsole(
                        f"Player não dando base", "INFO")

                    if(not self.checkIfIsInBase()):
                        self.doReturnToBase()
                        self.consoleCtr.printInConsole(
                            f"Dando Base", "INFO")

            else:
                self.consoleCtr.printInConsole(
                    f"Player não safe", "ERROR")
                self.doRetreatToBase(1)

            inBase = self.checkIfIsInBase()

        self.consoleCtr.printInConsole(
            f"Na base", "GOOD")

        self.status = "InBase"

    def routineGoToSafeZone(self, bMessage=True):
        self.status = "Retrieting"

        actualSafe = False

        while(not actualSafe):
            self.doRetreat(1)
            actualSafe = self.routineCheckIfIsSafe()

        self.status = "Alive"

    def routineCheckIfInBaseOrNeedToBuy(self, bMessage=True):

        result = self.checkIfIsInBase()

        if(result):
            self.status = "InBase"

        if(time.time() - self.lastCheckBuyItens > 150.0 or self.status == "InBase"):

            hasMoney = False

            if(bMessage):
                self.consoleCtr.printInConsole(
                    f"Checando gold para comprar itens", "INFO")

                self.consoleCtr.printInConsole(
                    f"Gold:{self.countGold()}", "INFO")

                self.consoleCtr.printInConsole(
                    f"Actual Item Price: {self.build.actualItem.price}", "INFO")

                self.consoleCtr.printInConsole(
                    f"Estou Base?: {self.checkIfIsInBase()}", "INFO")

            if(self.build.actualItem.price < int(self.countGold())):
                if(not self.checkIfIsInBase()):
                    self.routineGoToBase()

                hasMoney = True

            while(hasMoney):
                whatToBuy = self.build.nextItem()
                try:
                    gold = int(self.countGold())
                    if(bMessage):
                        self.consoleCtr.printInConsole(
                            f"Gold: {int(gold)}", "INFO")

                    if(whatToBuy.price < gold):
                        if(not self.checkIfShopIsOpen()):
                            self.consoleCtr.printInConsole(
                                f"num ta aberto", "INFO")
                            self.doOpenShop()
                            if(not self.checkIfArsenalIsRight()):
                                self.doFixArsenal()
                        else:
                            self.consoleCtr.printInConsole(
                                f"SHOPY ABERTU", "INFO")

                        sleep(.1)
                        self.doBuyItem(whatToBuy)
                        sleep(2.0)

                        if(gold > int(self.countGold())):
                            self.consoleCtr.printInConsole(
                                f"COMPRADO!", "INFO")
                            self.build.boughtItem()

                        if(bMessage):
                            self.consoleCtr.printInConsole(
                                f"GoldAtual: {int(self.countGold())}", "INFO")

                    else:
                        hasMoney = False

                    sleep(.5)

                except Exception as ex:
                    hasMoney = False
                    print(ex)
                    pass

            self.consoleCtr.printInConsole(
                f"Checando se o shopping ainda ta open", "INFO")
            if(self.checkIfShopIsOpen()):
                self.consoleCtr.printInConsole(
                    f"Ta aberto! Fechando", "INFO")
                self.doOpenShop()

            self.lastCheckBuyItens = time.time()

        if(self.status == "InBase"):
            self.doRetreat(1)
            sleep(16)

    def routineInLane(self):
        while(self.bMustRunMe):

            # Rotina Principal para atualizar dados do estado atual da tela
            self.routineSearchMinionsChampionsTowers(False)

            # #Rotinas para atacar inimigo ou avançar na lane
            self.routineUseSkillsInEnemyChampions(True)
            self.routineAttackWithMinions()

            # Rotinas de Checagens principais
            self.routineCentralizeCamera(True)
            self.routineCheckActualHP(True)
            self.routineCheckLevelUp(True)
            self.routineCheckIfInBaseOrNeedToBuy()

            # cv.imshow('Test', self.screenshot)
            # if cv.waitKey(1) == ord('k'):
            #     cv.destroyAllWindows()
            #     self.bMustRunMe = False
            #     self.globalFlag = False
            #     break

            sleep(0.5)

            # --------------------------------- MAIN RUN AREA ---------------------------------------

    def run(self):

        self.screenFinder = ScreenFinder()

        while(self.globalFlag):

            test = True
            # self.initAllData()

            while(self.bMustRunMe):
                self.consoleCtr.printInConsole(
                    "Esperando", "GOOD")
                sleep(1)

                while test:
                    try:
                        self.wincap = WindowCapture(
                            'League of Legends (TM) Client')
                        sleep(10)
                        self.wincap.setPosToOrigin()
                        self.doMouseClick(100, 500, 0.4)
                        test = False
                    except Exception as identifier:
                        # print(identifier)
                        #print("num achei saporra de league janela")
                        pass

                    sleep(5)

                try:
                    self.makeNewScreenShot()

                    if (self.routineLoadingScreen()):
                        self.consoleCtr.printInConsole(
                            "Iniciando Rotina de Gameplay!", "GOOD")

                        self.routineInLane()

                    else:
                        self.consoleCtr.printInConsole(
                            "Me Caguei! Me limpa Léu!", "GOOD")

                except Exception as ex:
                    print("exceção aqui!!!")
                    print(ex)

            # self.consoleCtr.printInConsole(
            #     f"Game Finalizado!", "INFO")

            sleep(1)
