import math


class VectorCalc():

    def __init__(self):
        super().__init__()

    def inverseVector(self, cx, cy, tx, ty):

        size = self.dist(cx, cy, tx, ty)
        if(size > 100):
            size = 100

        angleBetween = abs(math.degrees(self.angle_between(cx, cy, tx, ty)))
        # print(angleBetween)
        angleBetween = math.radians(angleBetween)
        # print(angleBetween)

        offset_x = math.cos(angleBetween) * size
        offset_y = math.sin(angleBetween) * size

        x = cx - offset_x
        y = cy + offset_y

        #print(f"degreesBetween: {math.degrees(angleBetween)}")
        #print(f"X: {tx} || Y: {ty}")
        #print(f"X: {x} || Y: {y}")

        return (x, y, )

    def angle_between(self, x1, y1, x2, y2):
        return math.atan2(y2-y1, x2-x1)

    def dist(self, x1, y1, x2, y2):
        return math.sqrt(((x1-x2)**2)+((y1-y2)**2))
