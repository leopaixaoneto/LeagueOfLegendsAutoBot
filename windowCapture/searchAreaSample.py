from windowCapture.searchArea import SearchArea
from windowCapture.readArea import ReadArea
from windowCapture.clickArea import ClickArea

searchAreaDic = {
    "loadingScreen": SearchArea(0, 367, 82, 46, "Screenshots/loadingScreen.jpg"),
    "enemyMinion": SearchArea(271, 25, 680, 500, "Screenshots/enemyMinionHealth.jpg"),
    "allyMinion": SearchArea(271, 25, 680, 500, "Screenshots/allyMinionHealth.jpg"),
    "enemyTower": SearchArea(271, 0, 680, 525, "Screenshots/t1Tower.jpg"),
    # 271,25,680,500
    "TowerAgro": SearchArea(0, 25, 950, 500, "Screenshots/towerAgro.jpg"),
    "enemyChampion": SearchArea(231, 25, 720, 525, "Screenshots/enemyChampionHealth.jpg"),
    "centralizedCam": SearchArea(218, 750, 16, 14, "Screenshots/notCentralizedCam.jpg"),
    "levelUp-Q": SearchArea(377, 674, 14, 7, "Screenshots/hasLevelUpSkill.jpg"),
    "levelUp-W": SearchArea(418, 674, 14, 7, "Screenshots/hasLevelUpSkill.jpg"),
    "levelUp-E": SearchArea(461, 674, 14, 7, "Screenshots/hasLevelUpSkill.jpg"),
    "levelUp-R": SearchArea(502, 674, 14, 7, "Screenshots/hasLevelUpSkill.jpg"),
    "basing": SearchArea(368, 565, 25, 8, "Screenshots/basingBar.jpg"),
    "base": SearchArea(0, 175, 500, 390, "Screenshots/baseSample.jpg"),
    "shop": SearchArea(265, 650, 45, 30, "Screenshots/shoppyCoin.jpg"),
    "arsenal": SearchArea(105, 40, 60, 20, "Screenshots/arsenalItems.jpg"),
}


readAreaDic = {
    "gold": ReadArea(665, 745, 50, 15),
    "hpPercentBar": ReadArea(337, 745, 260, 1),
}


clickPointDic = {
    "openArsenalMenu": ClickArea(220, 50),
    "selectArsenalItems": ClickArea(220, 95),
    "retreatToT1Bot": ClickArea(137, 753),
    "retreatToBase": ClickArea(16, 754)
}


goldDigits = {
    "first": ReadArea(669, 747, 7, 11),
    "second": ReadArea(678, 747, 7, 11),
    "third": ReadArea(687, 747, 7, 11),
    "fourth": ReadArea(696, 747, 7, 11)
}
