import json
import random

import pygame
from shapely.geometry import Polygon
from shapely.affinity import *
import item

class Plant(item.Item):



    def __init__(self, item_name, xPos, yPos, zPos, rotation, objectWidth, objectHeight,zLength):
        super().__init__(item_name, xPos, yPos, zPos, rotation, objectWidth, objectHeight,zLength)
        self._colour = (0, 200, 25)
        self._model = 'Plant'

    def setStorage(self, storageObject):
        self.storageObject = storageObject
        self.setItemMidpoint(self.storageObject.getItemMidpoint())

    def getSuggestedLocation(self, roomWidth, roomHeight):
        MARGIN = 40
        TOP_LEFT = 315
        TOP_MID = 0
        TOP_RIGHT = 45
        RIGHT_MID = 90
        BOTTOM_RIGHT = 135
        BOTTOM_MID = 180
        BOTTOM_LEFT = 225
        LEFT_MID = 270
        plant_Positions = [TOP_LEFT, TOP_MID, TOP_RIGHT, RIGHT_MID, BOTTOM_RIGHT, BOTTOM_MID, BOTTOM_LEFT, LEFT_MID]

        x = -1
        y = -1
        chosen_plantPositions = random.choice(plant_Positions)
        if chosen_plantPositions == TOP_LEFT:

            x = 0 + MARGIN
            y = 0 + MARGIN


        elif chosen_plantPositions == TOP_MID:

            x = (roomWidth - self._objectWidth) // 2

            y = 0 + MARGIN

        elif chosen_plantPositions == TOP_RIGHT:
            x = roomWidth - self._objectWidth - MARGIN
            y = 0 + MARGIN

        elif chosen_plantPositions == RIGHT_MID:
            x = roomWidth - self._objectWidth - MARGIN
            y = (roomHeight - self._objectHeight) // 2

        elif chosen_plantPositions == BOTTOM_RIGHT:
            x = roomWidth - self._objectWidth - MARGIN
            y = roomHeight - self._objectHeight - MARGIN

        elif chosen_plantPositions == BOTTOM_MID:
            x = (roomWidth - self._objectWidth)//2
            y = roomHeight - self._objectHeight - MARGIN

        elif chosen_plantPositions == BOTTOM_LEFT:
            x = 0 + MARGIN
            y = roomHeight - self._objectHeight - MARGIN

        elif chosen_plantPositions == LEFT_MID:
            x = 0 + MARGIN
            y = (roomHeight - self._objectHeight)//2

        return x, y, chosen_plantPositions

    def getPolygon(self):


        return Polygon([(self._x, self._y), (self._x + self._objectWidth, self._y), (self._x, self._y + self._objectHeight),
                        (self._x + self._objectWidth, self._y + self._objectHeight)])



