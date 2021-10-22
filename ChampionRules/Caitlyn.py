from windowCapture.vectorCalc import VectorCalc


class Caitlyn:

    veCalc = VectorCalc()
    middleX = 450
    middleY = 335

    def autoAttack(self, allyMinions, allyMinionsLoc, enemyMinions, enemyMinionsLoc, enemyChampionLoc):
        championDist = self.veCalc.dist(
            self.middleX, self.middleY, enemyChampionLoc[0], enemyChampionLoc[1])

        allyMinionDist = self.veCalc.dist(
            self.middleX, self.middleY, allyMinionsLoc[0], allyMinionsLoc[1])

        if(championDist < 250 and (allyMinions-enemyMinions) > 0 and allyMinionDist < 300):
            return True
        return False

    def qCheck(self, allyMinions, allyMinionsLoc, enemyMinions, enemyMinionsLoc, enemyChampionLoc):
        if(self.veCalc.dist(self.middleX, self.middleY, enemyChampionLoc[0], enemyChampionLoc[1]) < 300 and allyMinions > 0):
            return True
        return False

    def rCheck(self, allyMinions, allyMinionsLoc, enemyMinions, enemyMinionsLoc, enemyChampionLoc):
        if(self.veCalc.dist(self.middleX, self.middleY, enemyChampionLoc[0], enemyChampionLoc[1]) > 375 and allyMinions > 0):
            return True
        return False
