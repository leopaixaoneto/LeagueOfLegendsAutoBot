from ShopSystem.Item import Item
from ShopSystem.buyOrder import BuyOrder

itemList = {
    # Basic Items
    "LongSword": Item(70, 160, 350),
    "BfSword": Item(173, 160, 1300),
    "AgilityCape": Item(225, 160, 800),
    "PickAxe": Item(175, 260, 875),
    "Dagger": Item(380, 160, 300),
    "Boots": Item(330, 160, 300),

    # Medium Itens
    "Caufield": Item(122, 160, 400, [Item(70, 160, 350), Item(70, 160, 350)]),
    "BerserkerBoots": Item(430, 160, 500, [Item(330, 160, 300), Item(380, 160, 300)]),
    "vampiricCepter": Item(70, 260, 550, [Item(70, 160, 350)]),
    "Zelo": Item(275, 260, 300, [Item(225, 160, 800), Item(380, 160, 300)]),
    "Kircheis": Item(330, 260, 400, [Item(380, 160, 300)]),


    # Advanced Itens
    "BloodThursty": Item(120, 260, 950, [Item(173, 160, 1300), Item(70, 260, 550, [Item(70, 160, 350)]), Item(70, 160, 350)]),
    "Statikk": Item(380, 260, 500, [Item(275, 260, 300, [Item(225, 160, 800), Item(380, 160, 300)]), Item(330, 260, 400, [Item(380, 160, 300)])]),
    "Infinity": Item(225, 260, 425, [Item(173, 160, 1300), Item(175, 260, 875), Item(225, 160, 800)])
}


def getBuyOrderList(build):

    if build == "ad1":
        return BuyOrder(
            [
                # firstBuy
                Item(70, 160, 350),

                # BloodThursty (already bought the firstSword)
                Item(120, 260, 950,
                     [
                         Item(173, 160, 1300),
                         Item(70, 260, 550,
                              [
                                  Item(70, 160, 350)
                              ]
                              )
                     ]
                     ),

                # Berserker
                Item(430, 160, 500,
                     [
                         Item(330, 160, 300),
                         Item(380, 160, 300)
                     ]),

                # Statik
                Item(380, 260, 500,
                     [
                         Item(275, 260, 300,
                              [
                                  Item(225, 160, 800),
                                  Item(380, 160, 300)
                              ]
                              ),
                         Item(330, 260, 400,
                              [
                                  Item(380, 160, 300)
                              ]
                              )
                     ]
                     ),


                # Infinity
                Item(225, 260, 425, [
                    Item(173, 160, 1300),
                    Item(175, 260, 875),
                    Item(225, 160, 800)
                ]),

                # Infinity
                Item(225, 260, 425, [
                    Item(173, 160, 1300),
                    Item(175, 260, 875),
                    Item(225, 160, 800)
                ]),

                # Infinity
                Item(225, 260, 425, [
                    Item(173, 160, 1300),
                    Item(175, 260, 875),
                    Item(225, 160, 800)
                ])

            ]
        )

    if build == "ad2":
        return BuyOrder(
            [
                Item(120, 260, 950,
                     [
                         Item(173, 160, 1300),
                         Item(70, 160, 350),
                         Item(70, 260, 550,
                              [
                                  Item(70, 160, 350)
                              ]
                              ),
                     ]
                     )
            ]
        )
