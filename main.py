# Import pygame

import sys
import pygame
import random
import pandas as pd
import csv
import json

from matplotlib import pyplot as plt
from shapely.geometry import Polygon

import lshapedroom
import room
import character
import item

import lookat
import sit
import plant
import storage
import floatingstorage
import grasp

MAX_ANGLE = 359
ROOM_LEFT = 300
ROOM_TOP = 150
DEBUG = True

WRITE_FILE = True

if "debug" in sys.argv:
    DEBUG = True


if __name__ == "__main__":

    OUTPUTDIRECTORY = "C:\\Users\\180123614\\Documents\\"
    FILENAME = "output.json"



    WRange = random.randint(366, 671)
    HRange = random.randint(549, 853)
    # Set window size
    #size = width, height = 1200, 600
    size = width, height = HRange, WRange


    W= WRange #671
    H= HRange #853

    # Prepare loop condition
    running = False
    HUMANS = 6
    ROOM_MAX = 1
    roomNo = 1 #['Bedroom','Livingroom','Bathroom']

    # Event loop
    while not running and roomNo <= ROOM_MAX:

        RoomWidth = random.randint(W // 1.5, W)
        RoomHeight = random.randint(H // 1.5, H)

        #myRoom = room.Room(str(roomNo), 0, 0, RoomWidth, RoomHeight)
        myRoom = random.choice([room.Room(str(roomNo), 0, 0, RoomWidth, RoomHeight), lshapedroom.Lshapedroom(str(roomNo), 0, 0, RoomWidth, RoomHeight)])

        myRoom.addRobot()
        myRoom.addHumans(random.randint(1, HUMANS))
        myRoom.addObjects()


        if WRITE_FILE != False:
            myRoom.planRoutes()

            steps = myRoom.longestRoute

            myRoom.visualise(OUTPUTDIRECTORY + "room.jpg")
            myRoom.write_json_to_file(OUTPUTDIRECTORY + FILENAME, steps)






        if DEBUG is not True:
            sys.exit(0)


        #pygame.display.flip()
        roomNo += 1





        print(myRoom.generate_JSON_string())




