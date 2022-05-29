import json
import random

import pygame
from shapely.geometry import Polygon
from shapely.affinity import *
import item
import plant
import storage

class Floatingstorage(storage.Storage):


    def __init__(self, item_name, xPos, yPos, zPos, rotation, objectWidth, objectHeight,zLength,storageCode):
        super().__init__(item_name, xPos, yPos, zPos, rotation, objectWidth, objectHeight,zLength, storageCode)

    def getSuggestedLocation(self, roomWidth, roomHeight):
        x = random.randint(min(roomWidth//5, roomWidth-(roomWidth//5)-self._objectWidth), max(roomWidth//5, roomWidth-(roomWidth//5)-self._objectWidth))
        y = random.randint(min(roomHeight//5, roomHeight-(roomHeight//5)-self._objectHeight), max(roomHeight//5, roomHeight-(roomHeight//5)-self._objectHeight))
        r = random.randint(1, 180)

        return x, y, r

    def getPolygon(self):
        p = Polygon(
            [(self._x, self._y), (self._x + self._objectWidth, self._y), (self._x, self._y + self._objectHeight),
             (self._x + self._objectWidth, self._y + self._objectHeight)])
        result = rotate(p, self._direction )
        return result
