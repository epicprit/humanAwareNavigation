import json
import random

import pygame
from shapely.geometry import Polygon
from shapely.affinity import *
import item
import storage


class Grasp(item.Item):

    def __init__(self, item_name, xPos, yPos, zPos, rotation, objectWidth, objectHeight, zLength):
        super().__init__(item_name, xPos, yPos, zPos, rotation, objectWidth, objectHeight, zLength)
        self._colour = (255, 165, 0)
        self.storageObject = None
        self._model = random.choice(['Boots', 'Bowl', 'Mug'])


    def setStorage(self, storageObject):
        self.storageObject = storageObject
        self.setItemMidpoint(self.storageObject.getItemMidpoint())

    def confirmStorage(self, location= storage.Storage.ON_TOP):
        if self.storageObject != None:
            self.storageObject.addItem(self, location)


