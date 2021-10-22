class Item:

    name = ""
    x = 0
    y = 0
    price = 0
    bIsBought = False
    recipe = []

  # constructor
    def __init__(self, x, y, price, recipe=[], name=""):
        self.x = x
        self.y = y
        self.price = price
        self.recipe = recipe
        self.name = name

    def toString(self):
        return f"[ITEM: {self.name} || x: {self.x} || y: {self.y} || price: {self.price} || bought: {self.bIsBought}]"
