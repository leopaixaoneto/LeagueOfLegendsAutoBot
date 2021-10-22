from cMonitor import ClientMonitoring
from time import sleep

import os.path
import threading
from Console.consoleControler import ConsoleControler


class ClientThread(threading.Thread):

    lock = None
    globalFlag = True
    bMustRunMe = True
    consoleCtr = None
    clientMonitor = ClientMonitoring()
    clientLCUControler = None

    def __init__(self, consoleCtr, lock):
        threading.Thread.__init__(self)
        self.consoleCtr = consoleCtr
        self.lock = lock

    def checkClient(self, bMessage):
        if bMessage:
            self.consoleCtr.addInfo(
                "Procurando Client do League of Legends", ConsoleControler.INFO)
            self.consoleCtr.printPanel()

        if self.clientMonitor.checkIfClientIsOpen():
            if bMessage:
                self.consoleCtr.addInfo("Cliente está Aberto!",
                                        ConsoleControler.GOOD)
                self.consoleCtr.printPanel()

            return True
        else:

            return False

    def forceOpenClient(self, bMessage):
        if bMessage:
            self.consoleCtr.addInfo(
                "Forçando Abertura do League Of Legends", ConsoleControler.INFO)
            self.consoleCtr.printPanel()

        self.clientMonitor.forceClientWindowOpen()

    def makeLogin(self, bMessage):
        if self.checkClient(False):
            if bMessage:
                self.consoleCtr.addInfo("Efetuando Login!",
                                        ConsoleControler.GOOD)
                self.consoleCtr.printPanel()

            self.clientMonitor.makeLogin()

            return True
        else:
            return False

    def isLogged(self, bMessage):
        if bMessage:
            self.consoleCtr.addInfo("Verificando se está logado!",
                                    ConsoleControler.INFO)
            self.consoleCtr.printPanel()

        if os.path.exists('C:/Riot Games/League of Legends/lockfile'):

            self.consoleCtr.addInfo("Logado!",
                                    ConsoleControler.GOOD)
            self.consoleCtr.printPanel()

            return True

        else:

            self.consoleCtr.addInfo("Não logado!",
                                    ConsoleControler.ERROR)
            self.consoleCtr.printPanel()

            return False

    def closeClient(self):
        self.clientMonitor.forceClientWindowClose()

    def run(self):
        while(self.globalFlag):
            while(self.bMustRunMe):
                if not self.checkClient(True):
                    self.forceOpenClient(True)
                    sleep(4)
                else:
                    if not self.isLogged(False):
                        self.makeLogin(True)
                        sleep(5)
                    else:
                        self.consoleCtr.printInConsole("Iniciando Thread de LCU!",
                                                       ConsoleControler.INFO)
                        self.lock.acquire()
                        self.bMustRunMe = False
                        self.clientLCUControler.bMustRun = True
                        self.lock.release()

                    sleep(2)

            sleep(5)

            # if not self.checkClient(False):
            #     self.lock.acquire()
            #     self.bMustRunMe = True
            #     self.clientLCUControler.bMustRun = False
            #     self.clientLCUControler.globalFlag = False
            #     self.lock.release()
            #     sleep(1)
