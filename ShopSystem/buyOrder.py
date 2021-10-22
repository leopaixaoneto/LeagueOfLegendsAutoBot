from ShopSystem.Item import Item


class BuyOrder:

    order = []
    actualItem = -1

  # constructor
    def __init__(self, order=[]):
        self.order = order
        self.actualItem = self.order[0]

    def nextItem(self):
        for item in self.order:
            self.actualItem = self.goUnder(item)
            if(not self.actualItem.bIsBought):
                return self.actualItem

    def goUnder(self, item):
        if(len(item.recipe) > 0):
            for subItem in item.recipe:
                if(len(subItem.recipe) > 0):
                    #print("entrando mais")
                    nextItem = self.goUnder(subItem)
                    if(not nextItem.bIsBought):
                        return nextItem

                elif(not subItem.bIsBought):
                    #print("retornando subItem não comprado")
                    return subItem

            #print("Comprou todas as recipes, retornando item que chego")
            return item

        else:
            #print("retornando o item que chego")
            return item

    def boughtItem(self):
        self.actualItem.bIsBought = True
