import numpy as np


class Const:
    def __init__(self):
        self.PI = 3.141592653589793
        self.INV_PI = 1 / self.PI
        self.TWO_PI = 2 * self.PI
        self.INV_TWO_PI = 0.5 / self.PI
        self.PI_OVER_2 = 0.5 * self.PI
        self.PI_OVER_3 = self.PI / 3
        self.PI_OVER_4 = self.PI / 4
        self.PI_OVER_6 = self.PI / 6
        self.SQRT3_OVER_2 = np.sqrt(3)/2

CONST = Const()


