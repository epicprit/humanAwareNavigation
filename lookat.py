import json
import random

import pygame
from shapely.geometry import Polygon
from shapely.affinity import *
import item

class Lookat(item.Item):

    def __init__(self, item_name, xPos, yPos, zPos, rotation, objectWidth, objectHeight,zLength):
        super().__init__(item_name, xPos, yPos, zPos, rotation, objectWidth, objectHeight,zLength)

        self._colour = (225, 20, 20)
        self._model = 'Clock'


    def getSuggestedLocation(self, roomWidth, roomHeight):

        NORTH = 0
        SOUTH = 180
        EAST = 90
        WEST = 270
        walls = [NORTH, SOUTH, WEST, EAST]

        #returns a direction, xLocation, yLocation,
        # if direction = NORTH, x, y as normal, width heght as normal
        #if direction is EAST, x, y as normal, width & height of the polygon will be swapped when drawn and represented in shapelypolygon & JSON

        #_______________
        #|
        #|
        #|
        #|
        MARGIN = -3
        CORNER_MARGIN = 20
        #room width = 600
        #rom ehight = 400

        x = -1
        y = -1
        chosen_wall = random.choice(walls)
        if chosen_wall == NORTH:
            #case 1 = NORTH WALL
            x = random.randint(CORNER_MARGIN, roomWidth-CORNER_MARGIN-self._objectWidth)
            y = MARGIN

        #case 2 = EAST WALL
        elif chosen_wall == EAST:
            x = roomWidth - self._objectHeight-MARGIN
            y = random.randint(CORNER_MARGIN, roomHeight - CORNER_MARGIN - self._objectWidth)


        elif chosen_wall == SOUTH:
            # case 3 = SOUTH WALL
            x = random.randint(CORNER_MARGIN, roomWidth - CORNER_MARGIN - self._objectWidth)
            y = roomHeight - self._objectHeight-MARGIN


        elif chosen_wall == WEST:
        #case 4 = WEST WALL
            x = MARGIN
            y = random.randint(CORNER_MARGIN, roomHeight-CORNER_MARGIN-self._objectWidth)



        return x, y, chosen_wall

    def getPolygon(self):

        if self.getRotation() %180 == 0:
            return Polygon([(self._x, self._y), (self._x + self._objectWidth, self._y), (self._x, self._y + self._objectHeight),
                        (self._x + self._objectWidth, self._y + self._objectHeight)])
        else:
            return Polygon(
                [(self._x, self._y), (self._x + self._objectHeight, self._y), (self._x, self._y + self._objectWidth),
                 (self._x + self._objectHeight, self._y + self._objectWidth)])
        #result = rotate(p, self._direction )


    def hangOnWall(self, x, y, wall):
        self._x, self._y, self.rotation = x, y, wall
        return p

    def toJSONStyle_dict(self):
        my_data = item.Item.toJSONStyle_dict(self)
        MULTIPLIER = 0.01
        my_data["position"][1] = self._z * MULTIPLIER
        return my_data






