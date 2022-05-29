import json
import random

import pygame
from shapely.geometry import Polygon
from shapely.affinity import *
import character
import item
import numpy
import lookat
import sit
import plant
import storage
import floatingstorage
import grasp
from room import Room



class Lshapedroom(Room):



    #walls = [(0,0), (400, 0), (400, 200), (200, 200), (200, 400), (0, 400)]
    # geometry.Point p  p.x, p.y
    def __init__(self, room_name, xPos, yPos, roomWidth, roomHeight):
        super().__init__(room_name, xPos, yPos, roomWidth, roomHeight)

        self._walls = []
        self.__generateLWalls()

    def getFloorPolygon(self):
        p = Polygon(
            self._walls)

        return p

    def __generateLWalls(self):
        vShortLength = random.randint(int(self._roomHeight*0.3),int(self._roomHeight*0.7) ) #40-70% of the full height
        hShortLength = random.randint(int(self._roomWidth*0.3),int(self._roomWidth*0.7) )
        chosen_corner = random.choice([0,1,2,3])

        # origin corner
        if chosen_corner == 0:
            self._walls = [(0, vShortLength), (0, self._roomHeight), (self._roomWidth, self._roomHeight),
                           (self._roomWidth, 0), (hShortLength, 0),
                           (hShortLength, vShortLength)]
        # First Corner Clockwise
        elif chosen_corner == 1:
            self._walls = [(0, 0), (0, vShortLength), (hShortLength, vShortLength),
                           (hShortLength, self._roomHeight), (self._roomWidth, self._roomHeight),
                           (self._roomWidth, 0)]
        # Second Corner Clockwise
        elif chosen_corner == 2:
            self._walls = [(0, 0), (self._roomWidth, 0),     (self._roomWidth, vShortLength),
                           (hShortLength, vShortLength), (hShortLength, self._roomHeight),
                           (0, self._roomHeight)]
        # Third Corner Clockwise
        elif chosen_corner == 3:
            self._walls = [(0, 0), (0, self._roomHeight), (self._roomWidth, self._roomHeight), (self._roomWidth, vShortLength),
                           (hShortLength, vShortLength), (hShortLength, 0)]


    def _get_walls_JSON_list(self):
        JSON_Walls = []
        for w in range(len(self._walls)):

            thiscorner = w
            nextcorner = (w + 1) % len(self._walls)

            # self._walls[thiscorner][0]
            # self._walls[nextcorner][1]

            wall = {}
            # wall["center"] = [(self._walls[thiscorner][0] + self._walls[nextcorner][0] / 2.0)*Room.MULTIPLIER, Room.UNITY_WALL_HEIGHT / 2.0,
            #                   (self._walls[thiscorner][1] + self._walls[nextcorner][1] / 2.0)*Room.MULTIPLIER]


            if self._walls[thiscorner][1] == self._walls[nextcorner][1]:
                wall["size"] = [abs(self._walls[thiscorner][0] - self._walls[nextcorner][0]) * Room.MULTIPLIER,
                                Room.UNITY_WALL_HEIGHT,
                                Room.UNITY_WALL_THICKNESS]


                z_shift = Room.UNITY_WALL_THICKNESS / 2.0
                if self._walls[thiscorner][0] == 0:
                    z_shift *= -1

                wall["center"] = [((self._walls[thiscorner][0] +  self._walls[nextcorner][0] ) /2.0) * Room.MULTIPLIER ,
                                  Room.UNITY_WALL_HEIGHT / 2.0,
                                  ( (self._walls[thiscorner][1] + self._walls[nextcorner][1]) / 2.0) * Room.MULTIPLIER + z_shift]
            elif self._walls[thiscorner][0] == self._walls[nextcorner][0]:

                wall["size"] = [Room.UNITY_WALL_THICKNESS,
                                Room.UNITY_WALL_HEIGHT,
                                abs(self._walls[thiscorner][1] - self._walls[nextcorner][1]) * Room.MULTIPLIER]

                x_shift = Room.UNITY_WALL_THICKNESS / 2.0
                if self._walls[thiscorner][1] == 0:
                    x_shift *= -1


                wall["center"] = [((self._walls[thiscorner][0] + self._walls[nextcorner][0]) / 2.0) * Room.MULTIPLIER + x_shift,
                                  Room.UNITY_WALL_HEIGHT / 2.0,
                                  ((self._walls[thiscorner][1] + self._walls[nextcorner][1]) / 2.0) * Room.MULTIPLIER]




            JSON_Walls.append(wall)


        return JSON_Walls



    def _drawFloor(self, screen):
            pygame.draw.polygon(screen, (0, 255, 0), self._walls)

