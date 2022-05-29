
import json
import random

import pygame
from shapely.geometry import Polygon
from shapely.affinity import *
import item

class Sit(item.Item):

    def __init__(self, item_name, xPos, yPos, zPos, rotation, objectWidth, objectHeight, zLength):
        super().__init__(item_name, xPos, yPos, zPos, rotation, objectWidth, objectHeight, zLength)
        self._colour = (0, 0, 255)
        self._model = "Chair"

    def getPolygon(self):

        if self.getRotation() %180 == 0:
            return Polygon([(self._x, self._y), (self._x + self._objectWidth, self._y), (self._x, self._y + self._objectHeight),
                        (self._x + self._objectWidth, self._y + self._objectHeight)])
        else:
            return Polygon(
                [(self._x, self._y), (self._x + self._objectHeight, self._y), (self._x, self._y + self._objectWidth),
                 (self._x + self._objectHeight, self._y + self._objectWidth)])




