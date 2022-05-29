import json
import pygame
from shapely.geometry import Polygon, Point
from shapely.affinity import *


class Item:


    _model = None

    def __init__(self, item_name, xPos, yPos, zPos, rotation, objectWidth, objectHeight, zLength, colour=(200, 200, 0)):
        self._item_name = item_name
        self._x = xPos
        self._y = yPos
        self._z = zPos
        self._direction = rotation
        self._objectWidth = objectWidth
        self._objectHeight = objectHeight
        self._zLength = zLength
        self._colour = colour
        self._model = None


    def testOfScreen(self, screenWidth, screenHeight, screenPolygon=None):
        if screenPolygon == None:
            for(x,y) in list(self.getPolygon().exterior.coords):
                if (x > screenWidth) | (x < 0) | (y > screenHeight) | (y < 0):
                    return True
        else:
            for (x, y) in list(self.getPolygon().exterior.coords):
                p = Point(x,y)
                if not p.within(screenPolygon):
                    return True
        return False
    def scale(self, scale_factor):
        self._objectWidth *= scale_factor
        self._objectHeight *= scale_factor
        self._zLength *= scale_factor


    def getPolygon(self):
        p = Polygon(
            [(self._x, self._y), (self._x + self._objectWidth, self._y), (self._x, self._y + self._objectHeight),
             (self._x + self._objectWidth, self._y + self._objectHeight)])
        result = rotate(p, self._direction )
        return result

       # return Polygon([(self._x, self._y), (self._x + self._objectHeight, self._y), (self._x, self._y + self._objectHeight),
                       # (self._x + self._objectHeight, self._y + self._objectHeight)])

    def testOverlap(self, otherPolygon):
        return self.getPolygon().overlaps(otherPolygon)

    def getColour(self):
        return self._colour



    def getX(self):
        return self._x

    def getY(self):
        return self._y

    def getZLength(self):
        return self._zLength

    def setX(self, newX):
        self._x = newX

    def setY(self, newY):
        self._y = newY

    def setZ(self, newZ):
        self._z = newZ

    def getItemMidpoint(self):
        return self.getPolygon().centroid

    def setItemMidpoint(self, midpoint:Polygon.centroid):
        self._x = max(0, midpoint.x - (self._objectWidth // 2))
        self._y = max(0, midpoint.y - (self._objectHeight // 2))

    def getWidth(self):
        return self._objectWidth

    def getHeight(self):
        return self._objectHeight

    def getRotation(self):
        return self._direction
    def setRotation(self, newRotation):
        self._direction = newRotation

    def getName(self):
        return self._item_name

    def toJSONStyle_dict(self):
        MULTIPLIER = 0.01
        my_data = {}
        my_data["id"] = self._item_name
        my_data["model"] = self._model

        my_data["position"] = [self._x*MULTIPLIER, self._z*MULTIPLIER , self._y*MULTIPLIER]
        my_data["rotation"] = [0, self._direction, 0]
        my_data["size"] = [self._objectWidth*MULTIPLIER, self._zLength*MULTIPLIER, self._objectHeight*MULTIPLIER]

        return my_data
