import random
from perlin_noise import PerlinNoise
import numpy as np


class Walker:
    """_summary_"""

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.position = np.array([x, y])
        

