import json
import pygame
from shapely.geometry import Polygon, Point
from shapely.affinity import *

import node


class Node:

    DEFAULT_GRID_SIZE = 60

    def __init__(self, xPos, yPos, zPos =0, gridSize=60):
        self._x = xPos
        self._y = yPos
        self._z = zPos
        self._gridSize = gridSize
        self._visited = False
        self._fCost = -1

    def getX(self):
        return self._x

    def getY(self):
        return self._y

    def cmp_node_fcost(self, other):
        if self._fCost < other._fCost:
            return -1
        elif self._fCost == other._fCost:
            return 0
        else:
            return 1





    def calculateGridPos(self):
        self._row = self._y//self._gridSize
        self._col = self._x//self._gridSize
        return int(self._col), int(self._row)

    def calculateDistance(self, xPos, yPos):

        gridCol, gridRow = self.calculateGridPos()
        midX = int((float(gridCol)+0.5)* self._gridSize)
        midY = int((float(gridRow)+0.5)* self._gridSize)

        distance = ((xPos - midX )**2 + (yPos-midY)**2)**(1/2)

        return distance

    def findNeighhbours(self, character):
        gridCol, gridRow = self.calculateGridPos()
        leftCol = max(0, gridCol-1)
        rightCol = int(gridCol+1)
        topRow = max(0, gridRow-1)
        bottomRow = gridRow+1
        neighbours = []

        for i in range(leftCol, rightCol+1):

            for j in range(topRow, bottomRow+1):

                    neighbour = character.getNode(i, j)
                    if neighbour != None and neighbour not in neighbours:
                        neighbours.append(neighbour)    # node.Node((i+0.5)*self._gridSize, (j+0.5)*self._gridSize))
        return neighbours

    def getFCost(self):
        return self._fCost

    def calculateFCost(self, startPos:Point, destPos:Point):
        gCost = self.calculateDistance(startPos.x, startPos.y)
        hCost= self.calculateDistance(destPos.x, destPos.y)
        self._fCost = gCost + hCost

        return self._fCost
