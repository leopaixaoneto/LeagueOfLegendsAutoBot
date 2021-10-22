from lcu_driver import Connector

import json

from collections import namedtuple
from json import JSONEncoder
from time import sleep
from random import randint

from inGameThread import InGameThread

from Console.consoleControler import ConsoleControler

import threading


class LcuHandlerThread(threading.Thread):

    summoner = None
    bMustRun = False
    lock = None
    consoleCtr = None
    connector = Connector()
    con = None
    clientThread = None
    inGameThread = None
    printC = None

    def __init__(self, consoleCtr, lock):
        threading.Thread.__init__(self)
        self.consoleCtr = consoleCtr
        # self.clientThread = clientThread
        self.lock = lock
        self.printC = self.consoleCtr.printInConsole

    def customStudentDecoder(self, studentDict):
        return namedtuple('X', studentDict.keys())(*studentDict.values())

    def jsonToObject(self, obj):
        return json.loads(obj, object_hook=self.customStudentDecoder)

    @connector.ready
    async def connect(self, connection):
        # print('LCU API is ready to be used.')
        self.con = connection

        self.lock.acquire()
        self.globalFlag = True
        self.lock.release()

        self.consoleCtr.addInfo(
            'LCU INICIADA!', ConsoleControler.GOOD)
        self.consoleCtr.printPanel()

    async def confirmConnection(self, connection, bMessage=True):
        # check if the user is already logged into his account
        summoner = await connection.request('get', '/lol-summoner/v1/current-summoner')
        if ((summoner.status != 200) and (summoner.status != 404) and (summoner.status != 400)):
            return False
        else:
            return True

    async def makeLogin(self, connection, bMessage=True):

        login = ""
        password = ""

        with open('credentials.json') as json_file:
            data = json.load(json_file)
            login = data['login']
            password = data['password']

        await connection.request('post', '/lol-login/v1/session',
                                 data={
                                     "password": login,
                                     "username": password
                                 }
                                 )

    async def loadSummonerInfo(self, connection, bMessage=True):
        # check if the user is already logged into his account
        response = await connection.request('get', '/lol-summoner/v1/current-summoner')
        self.summoner = json.loads(await response.content.read())

    async def set_random_icon(self, connection, bMessage=True):
        # random number of a chinese icon
        random_number = randint(50, 78)

        # make the request to set the icon
        icon = await connection.request('put', '/lol-summoner/v1/current-summoner/icon',
                                        data={'profileIconId': random_number})

        # if HTTP status code is 201 the icon was applied successfully
        if icon.status == 201:
            self.consoleCtr.addInfo(
                'Icone alterado com sucesso!', ConsoleControler.GOOD)
            self.consoleCtr.printPanel()
        else:
            self.consoleCtr.addInfo(
                'Ocorreu um erro ao tentar mudar o ícone!', ConsoleControler.ERROR)
            self.consoleCtr.printPanel()
            # print('Unknown problem, the icon was not set.')

    async def createCoopMatch(self, connection, bMessage=True):
        if bMessage:
            self.consoleCtr.addInfo(
                'Criando partida Co-Op vs IA Intrudução', ConsoleControler.INFO)
            self.consoleCtr.printPanel()

        # queueId:830 = coopVsIaIntro
        await connection.request('post', '/lol-lobby/v2/lobby',
                                 data={'queueId': 830})

    async def createPraticeMatch(self, connection, bMessage=True):
        if(bMessage):
            self.consoleCtr.printInConsole(
                f"Criando uma partida de treinamento!", "INFO")

        await connection.request('post', '/lol-lobby/v2/lobby',
                                 data={
                                     "customGameLobby": {
                                         "configuration": {
                                             "gameMode": "PRACTICETOOL", "gameMutator": "", "gameServerRegion": "", "mapId": 11, "mutators": {"id": 1}, "spectatorPolicy": "AllAllowed", "teamSize": 5
                                         },
                                         "lobbyName": "Name",
                                         "lobbyPassword": ""
                                     },
                                     "isCustom": True
                                 }
                                 )

    async def bIsInLobby(self, connection, bMessage=True):
        if(bMessage):
            self.consoleCtr.printInConsole(
                f"Verificando se está em um lobby!", "INFO")

        response = await connection.request('get', '/lol-lobby/v2/lobby')

        read = json.loads(await response.content.read())
        # print("o que saiu do read: {}".format(read["readyCheck"]["state"]))

        try:
            if read["message"] == "LOBBY_NOT_FOUND":
                return False
        except:
            return True

        return True

    async def startCustomChampionSelect(self, connection, bMessage=True):
        if(bMessage):
            self.consoleCtr.printInConsole(
                f"Iniciando game Custom", "INFO")
        await connection.request('post', '/lol-lobby/v1/lobby/custom/start-champ-select')

    async def startQueu(self, connection, bMessage=True):
        if(bMessage):
            self.consoleCtr.printInConsole(
                f"Iniciando Fila", "INFO")

        await connection.request('post', '/lol-lobby/v2/lobby/matchmaking/search')

    async def acceptMatch(self, connection, bMessage=True):
        await connection.request('post', '/lol-matchmaking/v1/ready-check/accept')

    async def bHasMatchMakingErrors(self, connection, bMessage=True):
        response = await connection.request('get', '/lol-matchmaking/v1/search/errors')
        read = json.loads(await response.content.read())
        try:
            if(read[0]["errorType"] == 'QUEUE_DODGER'):
                return True
        except:
            return False

    async def matchQueuStatus(self, connection, bMessage=True):
        response = await connection.request('get', '/lol-matchmaking/v1/search')

        read = json.loads(await response.content.read())
        # print("o que saiu do read: {}".format(read["readyCheck"]["state"]))

        try:
            if (not read["isCurrentlyInQueue"]):
                return "NoInQueu"
            else:
                return read["searchState"]
        except:
            pass

        try:
            if(read["errors"][0]["errorType"] == 'QUEUE_DODGER'):
                return "NoInQueu"
        except:
            pass

        try:
            if(read['message'] == 'No matchmaking search exists.'):
                return "NoInQueu"
        except:
            pass

    async def timerChampSelect(self, connection, bMessage=True):
        response = await connection.request('get', '/lol-champ-select/v1/session/timer')
        read = json.loads(await response.content.read())
        # if(bMessage):
        # self.consoleCtr.printInConsole(
        #     f"Timer?: {read}", "INFO")

        try:
            return read["phase"]
        except:
            return "NOTHING"

    async def getPlayerChampSelectPos(self, connection, bMessage=True):
        if(bMessage):
            self.consoleCtr.printInConsole(
                f"Verificando a posição de pick", "INFO")

        response = await connection.request('get', '/lol-champ-select/v1/pin-drop-notification')
        read = json.loads(await response.content.read())

        try:
            for summoner in read["pinDropSummoners"]:
                if summoner["isLocalSummoner"] == True:
                    return summoner["slotId"]
        except:
            return "NOTHING"

    async def bIsChampionSelected(self, connection, bMessage=True):
        if(bMessage):
            self.consoleCtr.printInConsole(
                f"Verificando se ja foi selecionado um campeão", "INFO")

        response = await connection.request('get', '/lol-champ-select/v1/current-champion')
        read = await response.content.read()
        if(str(read) == "b'0'"):
            return False
        return True

    async def selectChampionInChampSelect(self, connection, bMessage=True):
        if(bMessage):
            self.consoleCtr.printInConsole(
                f"Pickando Champion!", "INFO")

        slot = await self.getPlayerChampSelectPos(connection)
        # print("PINTO SLOT: {}".format(slot))
        # 145 -> Kai'sa
        # 51 -> Caitlynyyyyyyyyyyyyyyyyyyyyyyy
        # 42 -> Corki
        # slot+2 -> custom with bots
        print(slot)
        await connection.request('patch', '/lol-champ-select/v1/session/actions/{}'.format(slot+2),
                                 data={
            "actorCellId": slot+2,
            "championId": 51,
            "completed": True,
            "id": slot+2,
            "isAllyAction": True,
            "isInProgress": True,
            "type": "pick"
        })

        # print({"actorCellId": slot,
        #        "championId": 51,
        #        "completed": True,
        #        "id": slot,
        #        "isAllyAction": True,
        #        "isInProgress": True,
        #        "type": "pick"})

    async def selectSpellsInChampSelect(self, connection, bMessage=True):
        if(bMessage):
            self.consoleCtr.printInConsole(
                f"Selecionando Spells!", "INFO")

        await connection.request('patch', '/lol-champ-select/v1/session/my-selection',
                                 data={
                                     "selectedSkinId": 0,
                                     "spell1Id": 7,
                                     "spell2Id": 4,
                                     "wardSkinId": 0})

    async def checkIfGameWasFinished(self, connection, bMessage=True):
        response = await connection.request('get', '/lol-end-of-game/v1/eog-stats-block')
        read = json.loads(await response.content.read())
        try:
            if(read["message"] == "No end of game stats available."):
                return False
        except:
            return True

    async def endOfGameDismissStats(self, connection, bMessage=True):
        if(bMessage):
            self.consoleCtr.printInConsole(
                f"Ignorando informações pós partida!", "INFO")

        await connection.request('post', '/lol-end-of-game/v1/state/dismiss-stats')

    async def declinePlayAgain(self, connection, bMessage=True):
        if(bMessage):
            self.consoleCtr.printInConsole(
                f"Declinando jogar novamente!", "INFO")

        await connection.request('post', '/lol-lobby/v2/play-again-decline')

    async def routine(self, connection):
        # check if the user is already logged into his account
        summoner = await connection.request('get', '/lol-summoner/v1/current-summoner')
        if summoner.status != 200:
            print(
                'Please login into your account to change your icon and restart the script...')
        else:

            response = self.jsonToObject(await summoner.content.read())
            # self.consoleCtr.addInfo(
            #     f'Nome da conta: {response.displayName}', ConsoleControler.GOOD)

            # TODO print(response.displayName)

            #! COMEÇO PARA CRIAR COOP VS IA

            # while(not await self.bIsInLobby(connection)):
            #     await self.createCoopMatch(connection, True)

            # self.consoleCtr.printInConsole(
            #     f"Criando lobby Co-op VS IA - Introdução", "INFO")

            # while(await self.bHasMatchMakingErrors(connection)):
            #     # print("Esperando Penalidade")
            #     sleep(1)

            # while(await self.timerChampSelect(connection) != "BAN_PICK"):

            #     # iniciar a fila
            #     while(await self.matchQueuStatus(connection) == 'NoInQueu'):
            #         await self.startQueu(connection)

            #     # esperar até achar a fila
            #     # while (await self.matchQueuStatus(connection) != 'Found'):
            #     #     # print("Esperando fila!")
            #     #     sleep(1)

            #     # ACEITAR PARTIDA
            #     if(await self.matchQueuStatus(connection) == 'Found'):
            #         await self.acceptMatch(connection)

            #! FIM PARA CRIAR COOP VS IA

            # criar custom game lobby
            while(not await self.bIsInLobby(connection)):
                await self.createPraticeMatch(connection)

            # iniciar custom game
            await self.startCustomChampionSelect(connection)

            # loop para esperar até liberar para pickar
            while (await self.timerChampSelect(connection) != "BAN_PICK"):
                sleep(1)

            # selecionar campeão
            while(not await self.bIsChampionSelected(connection)):
                await self.selectChampionInChampSelect(connection)
                sleep(1)

            await self.selectSpellsInChampSelect(connection)
            # print("Spells selecionadas - OK")

            # iniciando thread de inGame
            self.lock.acquire()
            self.inGameThread.bMustRunMe = True
            self.lock.release()

            # Loop para esperar o jogo acabar
            while (not await self.checkIfGameWasFinished(connection)):
                self.consoleCtr.printInConsole(
                    f"Esperando jogo acabar!", "INFO")
                sleep(5)

            self.consoleCtr.printInConsole(
                f"Jogo Acabou!", "INFO")
            await self.declinePlayAgain(connection)

            # pausandoThread de inGame
            self.lock.acquire()
            self.inGameThread.bMustRunMe = False
            self.inGameThread.initAllData()
            self.lock.release()


#* ################################ ARSENAL AREA #########################################

    async def itemSetRoutine(self, connection, bMessage=True):
        if(bMessage):
            self.consoleCtr.printInConsole(
                f"Carregando informações da conta!", "INFO")

            sumId = self.summoner['summonerId']
            response = await connection.request('get', f'/lol-item-sets/v1/item-sets/{sumId}/sets')
            read = json.loads(await response.content.read())

            bHasItemSet = False

            for iSet in read['itemSets']:
                if(iSet['uid'] == '2c7d42d0-cb45-11ea-925a-1fddc1659a58'):
                    bHasItemSet = True

            if(not bHasItemSet):
                with open('./ShopSystem/itemSet.json') as json_file:
                    rData = json.load(json_file)
                    await connection.request('post', f'/lol-item-sets/v1/item-sets/{sumId}/sets', data=rData)

#* ############################# END OF ARSENAL AREA #####################################


#! ################################ DISENCHANT AREA ######################################

    async def disenchantRoutine(self, connection, bMessage=True):
        response = await connection.request('get', '/lol-loot/v1/player-loot')
        read = json.loads(await response.content.read())

        for dItem in read:
            info = dItem["lootId"]
            if("CHAMPION_RENTAL" in info):
                await self.disenchantItem(connection, "CHAMPION_RENTAL_disenchant", [info], bMessage=bMessage)

            elif("MATERIAL_key_fragment" in info):
                await self.disenchantItem(connection, "MATERIAL_key_fragment_forge", [info], bMessage=bMessage)

            elif("CHEST_generic" in info):
                await self.disenchantItem(connection, f"{info}_OPEN", [info, "MATERIAL_key"], bMessage=bMessage)

            elif("CHEST_" in info):
                await self.disenchantItem(connection, f"{info}_OPEN", [info], bMessage=bMessage)

    async def disenchantItem(self, connection, recipeName, playerLootList, bMessage=True):
        if bMessage:
            self.consoleCtr.addInfo(
                f'Desencantando: {recipeName} || Utilizando: {playerLootList}', ConsoleControler.INFO)
            self.consoleCtr.printPanel()

        try:
            response = await connection.request('post', f'/lol-loot/v1/recipes/{recipeName}/craft',
                                                data=playerLootList)

        except Exception as ex:
            print(ex)

#! ############################# END OF DISENCHANT AREA ##################################

    # fired when League Client is closed (or disconnected from websocket)
    @connector.close
    async def disconnect(self, _):
        self.consoleCtr.addInfo(
            "LCU Não Conectada", ConsoleControler.ERROR)
        self.consoleCtr.printPanel()

        self.lock.acquire()
        self.bMustRun = False
        self.clientThread.bMustRunMe = True
        self.lock.release()

    def run(self):
        self.consoleCtr.printInConsole("LCU STARTADA!",
                                       ConsoleControler.INFO)
        self.connector.start(self)
        # self.connector.start(self)

    @connector.mainLoop
    async def runLCU(self, connection):
        try:
            while not await self.confirmConnection(self.con):
                sleep(1)

            self.consoleCtr.printInConsole(
                'LCU CONECTADA!', "GOOD")

            # await self.makeLogin(self.con)

            await self.loadSummonerInfo(self.con)

            await self.itemSetRoutine(self.con)

            # await self.disenchantRoutine(self.con)

            while self.bMustRun:
                if await self.confirmConnection(self.con):
                    self.consoleCtr.printInConsole(
                        'NO LOOP DA LCU!', "INFO")

                    await self.routine(self.con)
                sleep(2)

            sleep(1)

        except Exception as ex:
            self.consoleCtr.addInfo(
                'LCU DESCONECTOU! ou alguma exceção', ConsoleControler.ERROR)
            self.consoleCtr.addInfo(
                'Iniciando verificações!', ConsoleControler.INFO)
            self.consoleCtr.printPanel()
            print(ex)
            pass
