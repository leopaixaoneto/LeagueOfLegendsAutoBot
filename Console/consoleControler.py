import pyfiglet
import datetime
from clint.arguments import Args
from clint.textui import puts, colored, indent
from Console.infoLine import InfoLine

import os

import ctypes


class ConsoleControler:
    BOLD = '\033[1m'
    ENDC = '\033[0m'

    version = ""
    infoVector = []
    botTitle = "                                     RodolBot"
    MaxLinesPerPanel = 19

    INFO = 0
    ERROR = 1
    CAUTION = 2
    GOOD = 3

    def __init__(self, version):
        self.version = version
        self.setWindowTitle(f"Rodolbot ({version})")

    def printTitle(self):
        Title = pyfiglet.figlet_format(self.botTitle)
        print(Title)

    def printVersion(self):
        puts(colored.cyan(
            f'  {self.BOLD}version: [{self.version}]{self.ENDC}'))

        print()

    def printInfo(self):
        for info in self.infoVector:
            colorfunc = None

            if info.colorType == self.INFO:
                puts(colored.cyan(
                    f'    {self.BOLD}[{info.Time}]: {self.ENDC}') + colored.white(info.Text))

            if info.colorType == self.ERROR:
                puts(colored.cyan(
                    f'    {self.BOLD}[{info.Time}]: {self.ENDC}') + colored.red(info.Text))

            if info.colorType == self.CAUTION:
                puts(colored.cyan(
                    f'    {self.BOLD}[{info.Time}]: {self.ENDC}') + colored.yellow(info.Text))

            if info.colorType == self.GOOD:
                puts(colored.cyan(
                    f'    {self.BOLD}[{info.Time}]: {self.ENDC}') + colored.green(info.Text))

        print()

    def printPanel(self):
        os.system('cls')
        self.printTitle()
        self.printVersion()
        self.printInfo()
        pass

    def addInfo(self, info, colorType):
        newInfo = InfoLine(info, self.getActualHour(), colorType)

        self.infoVector.insert(len(self.infoVector), newInfo)

        if len(self.infoVector) > self.MaxLinesPerPanel:
            self.infoVector.pop(0)

        # print()

    def printInConsole(self, info, type):
        color = self.INFO

        if(type == "INFO"):
            color = self.INFO

        if(type == "ERROR"):
            color = self.ERROR

        if(type == "GOOD"):
            color = self.GOOD

        self.addInfo(info, color)
        self.printPanel()

    def getActualHour(self):
        return datetime.datetime.now().strftime("%H:%M:%S")

    def setWindowTitle(self, title):
        ctypes.windll.kernel32.SetConsoleTitleW(title)
