import json
import random

import pygame
import timeit
from numpy import histogram
from shapely.geometry import Polygon
from shapely.affinity import *
import character
import item
import numpy
import pandas as pd
import lookat
import sit
import plant
import storage
import floatingstorage
import grasp




class Room:

    # HUMANS = 1
    # OBJECTS = 2
    # PLANTS = 3
    MAX_ANGLE = 359
    MULTIPLIER = 0.01
    UNITY_WALL_HEIGHT = 2.4
    UNITY_WALL_THICKNESS = 0.1
    UNITY_FLOOR_THICKNESS = 0.1
    MARGIN = 50


    def __init__(self, room_name, xPos, yPos, roomWidth, roomHeight):
        self._room_name = room_name
        self._x = xPos
        self._y = yPos
        self._roomWidth = roomWidth
        self._roomHeight = roomHeight
        self._size = roomWidth, roomHeight
        self._characters = []
        self._items = []

    def getFloorPolygon(self):
        p = Polygon(
            [(0, 0), (self._roomWidth, 0), (self._roomWidth, self._roomHeight), (0, self._roomHeight)])

        return p

    def _drawFloor(self, screen):
        pygame.draw.rect(screen, (0, 255, 0), (0, 0, self._roomWidth, self._roomHeight))

    def _drawCeiling(self, screen):
        pygame.draw.rect(screen, (0, 255, 0), (0, 0, self._roomWidth, self._roomHeight))

    def visualise (self, filename='room.jpg'):
        pygame.init()
        pygame.display.set_caption('Room')
        screen = pygame.display.set_mode(self._size)
        # Clock
        clock = pygame.time.Clock()
        # Close window event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = True

        # Background Color
        screen.fill((0, 0, 0))

        # Show the image
        self._drawFloor(screen)


        for i in self._items:

            my_poly = []
            points = list(zip(*i.getPolygon().exterior.coords.xy))[:-1]
            points[2], points[3] = points[3], points[2]

            for (x1, y1) in points:
                my_poly.append((x1, y1))
            pygame.draw.polygon(screen, i.getColour(), my_poly)

        for c in self._characters:
            screen.blit(c.getImage(), (c.getX(), c.getY()))
        gridSize = 50
        for i in range (1 + (self._roomWidth//gridSize)):
            pygame.draw.line(screen, pygame.Color(0), (i*gridSize, 0), (i*gridSize,self._roomHeight), 1)

        for j in range (1 + (self._roomHeight//gridSize)):
            pygame.draw.line(screen, pygame.Color(0), (0, j*gridSize), (self._roomHeight, j*gridSize), 1)




        pygame.image.save(screen, filename)

    def write_json_to_file(self, filename:str, steps=20):
        json_data = self.generate_JSON_string(steps)
        # print(json_data)
        fd = open(filename, 'w')
        fd.write(json_data)
        fd.close()

    def generateNewGoals(self):
        for c in self._characters:
            c.generateNewGoal(self, 0.5)

    def moveCharacters(self):
         for c in self._characters:
             c.moveCharacter(self)

             c.planRoute(c.getGoal(), self)

    def planRoutes(self):
        self.longestRoute = -1

        for c in self._characters:
            c.planRoute(c.getGoal(), self)
            self.longestRoute = max(len(c.getRoute()), self.longestRoute)


    def addRobot(self):



        robotWidth = 30
        robotHeight = 30

        # Since rotation makes the image bigger we reduce the error of testing
        while len(self.getCharactersMatching("ROBOT")) == 0:
            robotPosx = random.randint(0, self._roomWidth - robotWidth - 20)
            robotPosy = random.randint(0, self._roomHeight - robotHeight - 20)
            robotPosz = 19
            Robot = character.Character("ROBOT", 'C:\\Users\\180123614\\Documents\\SocialRobotVRPritesh\\Assets\\Sprites\\robot.png', robotPosx, robotPosy, robotPosz,
                                        random.randint(0, Room.MAX_ANGLE), robotWidth, robotHeight, self)
            if not Robot.testOfScreen(self._roomWidth, self._roomHeight, self.getFloorPolygon()):
                self._characters.append(Robot)

    def draw_number(self, histogram):
        v = random.randint(0, sum(histogram))
        for i in range(len(histogram)):
            v -= histogram[i]
            if v <= 0:
                return i

    def get_furniture_quantity(self, room_type, furniture_type):
        data = {
            "Bedroom"   : { "storage" :  [5, 86, 75, 22, 10, 2],
                            "floatingstorage": [147, 47, 5],
                            "sit": [0, 131, 59, 10],
                            "plant": [53, 102, 39, 5, 1],
                            "lookat": [5, 16, 29, 33, 43, 22, 24, 11, 4, 3, 1, 2, 1, 0, 2, 0, 1, 0, 0, 1, 1, 1],
                            "grasp": [0, 1, 2, 2, 8, 29, 24, 33, 12, 20, 17, 10, 3, 8, 9, 3, 1, 5, 3, 2, 2, 2, 0, 0, 1, 0, 0, 1, 0, 0, 0,
                        1, 1]
                            },

         "Livingroom": {    "storage" :  [39, 64, 53, 33, 6, 3, 1, 1],
                            "floatingstorage": [16, 116, 49, 17, 2],
                            "sit": [0, 32, 67, 61, 25, 8, 4, 1, 0, 1, 1],
                            "plant": [35, 77, 46, 17, 13, 4, 4, 3, 1],
                            "lookat": [5, 12, 31, 30, 30, 22, 18, 19, 14, 3, 4, 1, 0, 2, 1, 3, 3, 0, 2],
                            "grasp": [5, 12, 31, 30, 30, 22, 18, 19, 14, 3, 4, 1, 0, 2, 1, 3, 3, 0, 2]
                            },

            "Bathroom"  : { "storage" :  [5, 25, 25, 37, 28, 14, 9, 3, 3, 1],
                            "floatingstorage": [127, 21, 2],
                            "sit": [40, 87, 22, 1],
                            "plant": [55, 62, 17, 11, 2, 0, 2, 1],
                            "lookat": [11, 22, 26, 34, 16, 22, 6, 7, 4, 2],
                            "grasp": [11, 22, 26, 34, 16, 22, 6, 7, 4, 2]
                            }
        }
        return self.draw_number(data[room_type][furniture_type])


    def hasObjectsIn(self, poly:Polygon, excludeditems=[]):

        for c in self._characters:
            if (c.testOverlap(poly)):
                if not c in excludeditems:
                    return True


        for i in self._items:
            if (i.testOverlap(poly)):
                return True

        return False


    def addObjects(self):
        current_no_Objects = 0
        min_objectSize = 10
        max_objectSize = 50

        types_of_rooms = ['Bedroom', 'Livingroom', 'Bathroom']
        room_type = random.choice(types_of_rooms)

        num_storages = self.get_furniture_quantity(room_type, "storage")
        num_floatingstorage = self.get_furniture_quantity(room_type, "floatingstorage")
        num_sits = self.get_furniture_quantity(room_type, "sit")
        num_plants = self.get_furniture_quantity(room_type, "plant")
        num_lookats = self.get_furniture_quantity(room_type, "lookat")
        num_grasps = self.get_furniture_quantity(room_type, "grasp")

        for storage_num in range(num_storages):
            # select height and width

            newItem = None

            collision = True

            # check the overlap before adding to items
            while collision:
                newItemWidth = random.randint(100, 200)
                storageWidth = newItemWidth
                newItemHeight = random.randint(20, 40)
                storageHeight = newItemHeight
                zLength = 100
                storageCode = storage.Storage.ON_TOP + storage.Storage.UNDERNEATH
                #storage.Storage.ON_TOP + storage.Storage.UNDERNEATH
                newItem = storage.Storage("STORAGE_" + str(storage_num + 1), 0, 0, 0, 0, newItemWidth, newItemHeight, zLength,
                                          storageCode)
                x, y, dir = newItem.getSuggestedLocation(self._roomWidth, self._roomHeight)

                if x > self._roomWidth or y > self._roomHeight:
                    break
                newItem.setX(x)
                newItem.setY(y)
                newItem.setRotation(dir)
                collision = False

                for i in self._items:
                    if (newItem.testOverlap(i.getPolygon())):
                        collision = True
                        #print("collision between floatingstorage and storage item")
                        break

                for c in self._characters:
                    if (newItem.testOverlap(c.getPolygon())):
                        collision = True
                        #print("collision between floatingstorage and character")
                        break

            if not newItem.testOfScreen(self._roomWidth, self._roomHeight, self.getFloorPolygon()):
                self._items.append(newItem)
                #storage_num += 1

        for floatingstorage_num in range(num_floatingstorage):

            newItem = None

            collision = True


            while collision:
                newItemWidth = random.randint(80, 120)
                newItemHeight = (newItemWidth * 10) // 16
                zLength = 100
                newItem = floatingstorage.Floatingstorage("FLSTORAGE_" + str(floatingstorage_num + 1), 0, 0, 0, 0,
                                                          newItemWidth, newItemHeight,  zLength,
                                                          storage.Storage.ON_TOP)
                x, y, dir = newItem.getSuggestedLocation(self._roomWidth, self._roomHeight)
                newItem.setX(x)
                newItem.setY(y)
                newItem.setRotation(dir)
                collision = False
                for c in self._characters:
                    if (newItem.testOverlap(c.getPolygon())):
                        collision = True
                        break
                        #print("collision between storage and character")

                for i in self._items:
                    if (newItem.testOverlap(i.getPolygon())):
                        collision = True
                        #print("collision between storage and storage item")
                        break


            if not newItem.testOfScreen(self._roomWidth, self._roomHeight, self.getFloorPolygon()):
                self._items.append(newItem)
                #floatingstorage_num += 1

        for sit_num in range(num_sits):
            # select height and width
            newItemWidth = 59 #random.randint(20, 30)
            newItemHeight = 57 #random.randint(20, 30)
            zLength = 100
            newItem = None

            collision = True

            # check the overlap before adding to items
            while collision:
                newItemX = random.randint(0, self._roomWidth - newItemWidth)
                newItemY = random.randint(0, self._roomHeight - newItemHeight)
                newItemR = random.randint(0, Room.MAX_ANGLE)
                newItem = sit.Sit("Sit_" + str(sit_num + 1), newItemX, newItemY, 0, newItemR, newItemWidth, newItemHeight, zLength)
                collision = False

                if (newItem.testOverlap(self._characters[0].getPolygon())):
                    collision = True


                for i in self._items:
                    if (newItem.testOverlap(i.getPolygon())):
                        collision = True

            if not newItem.testOfScreen(self._roomWidth, self._roomHeight, self.getFloorPolygon()):
                self._items.append(newItem)

        for plant_num in range(num_plants):


            newItem = None
            collision = True
            myStorage = None


            while collision:
                newItemWidth = random.randint(10, 20)
                newItemHeight = random.randint(10, 20)
                zLength = random.randint(10, 20)
                newItem = plant.Plant("Plant_" + str(plant_num + 1), 0, 0, 0, 0, newItemWidth, newItemHeight,zLength)
                position = "storage"
                if random.randint(0, 4) >= 2:
                    position = "floor"
                    myStorage = None
                    x, y, dir = newItem.getSuggestedLocation(self._roomWidth, self._roomHeight)
                    #print("chosen value {0} from 0 to {1}".format(x, self._roomWidth - newItemWidth))
                    newItem.setX(x)
                    newItem.setY(y)
                else:
                    # select a storage item from items
                    item_location = random.choice(storage.Storage.locations)
                    myStorage = storage.Storage.getEmptyStorage(self._items, item_location)
                    if myStorage == None:
                        break


                    dir = random.randint(0, 90)
                    newItem.setStorage(myStorage)
                    myStorage.addItem(newItem, item_location)

                #if x > self._roomWidth:
                    #print("x ({0})is too big, RoomWidth is only {1} ".format(x, self._roomWidth))

                newItem.setRotation(dir)
                collision = False

                for c in self._characters:
                    if (newItem.testOverlap(c.getPolygon())):
                        collision = True
                        #print("collision between Plant and Character")

                for i in self._items:
                    if (newItem.testOverlap(i.getPolygon()) and not isinstance(i, storage.Storage)):
                        collision = True
                        #print("collision between plant and non-storage item")

            if not newItem.testOfScreen(self._roomWidth, self._roomHeight, self.getFloorPolygon()):
                self._items.append(newItem)

        for lookat_num in range(num_lookats):
            # select height and width

            newItem = None

            collision = True

            # check the overlap before adding to items
            while collision:
                newItemWidth = random.randint(30, 150)
                newItemHeight = random.randint(5, 10)
                zLength = 100
                newItem = lookat.Lookat("LOOKAT_" + str(lookat_num + 1), 0, 120, 150,0, newItemWidth, newItemHeight,zLength)
                x, y, dir = newItem.getSuggestedLocation(self._roomWidth, self._roomHeight)
                newItem.setX(x)
                newItem.setY(y)
                newItem.setRotation(dir)
                collision = False
                for c in self._characters:
                    if (newItem.testOverlap(c.getPolygon())):
                        collision = True
                        #print("collision between lookAt and character")

                for i in self._items:
                    if (newItem.testOverlap(i.getPolygon())):
                        collision = True
                        #print("collision between lookAt and lookAT item")

            if not newItem.testOfScreen(self._roomWidth, self._roomHeight, self.getFloorPolygon()):
                self._items.append(newItem)

        for grasp_num in range(num_grasps):
            # select height and width

            newItem = None
            collision = True
            myStorage = None
            # check the overlap before adding to items
            while collision:
                newItemWidth = random.randint(5, 15)
                newItemHeight = random.randint(5, 10)
                zLength = 50

                x = random.randint(0, self._roomWidth - newItemWidth)
                y = random.randint(0, self._roomHeight - newItemHeight)

                # decide on prob distribution of floor vs storage 20:80
                position = "storage"
                item_location = None
                if random.randint(0, 4) >= 3:
                    position = "floor"
                    myStorage = None
                    x = random.randint(0, self._roomWidth - newItemWidth)
                    y = random.randint(0, self._roomHeight - newItemHeight)
                    #print("chosen value {0} from 0 to {1}".format(x, self._roomWidth - newItemWidth))
                    if x > self._roomWidth or y > self._roomHeight or x == 0 or y == 0:
                        collision = True
                        break
                    dir = random.randint(0, 180)
                    newItem = grasp.Grasp("GRASP" + str(grasp_num), x, y, 0, dir, newItemWidth, newItemHeight,zLength)
                    # newItem.setX(x)
                    # newItem.setY(y)

                else:
                    # select a storage item from items

                    item_location = random.choice(storage.Storage.locations)
                    myStorage = storage.Storage.getEmptyStorage(self._items, item_location)
                    if myStorage == None:
                        break

                    x = random.randint(0, myStorage.getWidth() - newItemWidth)
                    y = random.randint(0, myStorage.getHeight() - newItemHeight)
                    newItem = grasp.Grasp("GRASP" + str(grasp_num), x, y, 0, 0, newItemWidth, newItemHeight, zLength)

                    # e.g. x = 200
                    #     y = 100
                    #     s_width & s_height of storage  e.g. (60 x 30)
                    #     g_width & g_height of grasp item e.g. (10, 12)
                    #     g_x = x + (s_width - g_width) // 2    e.g. 200 + (60-10) // 2 === 225
                    #     g_y = y + (s_height - g_height) // 2

                    # x = myStorage.getX() + (myStorage.getWidth() - newItemWidth) // 2
                    # y = myStorage.getY() + (myStorage.getHeight() - newItemHeight) // 2
                    dir = random.randint(0, 180)
                    newItem.setStorage(myStorage)
                    if newItem.getX() > self._roomWidth or newItem.getY() > self._roomHeight or newItem.getX() <= 0 or newItem.getY() <= 0:
                        collision = True
                        break

                newItem.setRotation(dir)
                # newItem.setStorage(myStorage)

                collision = False
                for c in self._characters:
                    if (newItem.testOverlap(c.getPolygon())):
                        collision = True
                        #print("collision between grasp and character")

                for i in self._items:
                    if (newItem.testOverlap(i.getPolygon()) and not isinstance(i, storage.Storage)):
                        collision = True
                        #print("collision between grasp and non-storage item")

            if newItem != None and not newItem.testOfScreen(self._roomWidth, self._roomHeight, self.getFloorPolygon()):


                if position == "storage":
                    newItem.confirmStorage(item_location)
                self._items.append(newItem)


    def getCharactersMatching(self, naming_substring):
        # get length of the string filter
        substr_len = len(naming_substring)
        results = []
        for c in self._characters:
            if c.getName()[0:substr_len] == naming_substring:
                results.append(c)
        return results


    def _get_walls_JSON_list(self):
        JSON_Walls = []
        wall = {}
        wall["center"] = [self._roomWidth * Room.MULTIPLIER / 2.0, Room.UNITY_WALL_HEIGHT / 2.0, Room.UNITY_WALL_THICKNESS / -2.0]
        wall["size"] = [self._roomWidth * Room.MULTIPLIER + 2 * Room.UNITY_WALL_THICKNESS, Room.UNITY_WALL_HEIGHT,
                        Room.UNITY_WALL_THICKNESS]

        JSON_Walls.append(wall)

        wall2 = {}
        wall2["center"] = [self._roomWidth * Room.MULTIPLIER + Room.UNITY_WALL_THICKNESS / 2.0, Room.UNITY_WALL_HEIGHT / 2.0,
                           self._roomHeight * Room.MULTIPLIER / 2.0]
        wall2["size"] = [Room.UNITY_WALL_THICKNESS, Room.UNITY_WALL_HEIGHT, self._roomHeight * Room.MULTIPLIER]

        JSON_Walls.append(wall2)

        wall3 = {}
        wall3["center"] = [self._roomWidth * Room.MULTIPLIER / 2.0, Room.UNITY_WALL_HEIGHT / 2.0,
                           self._roomHeight * Room.MULTIPLIER + Room.UNITY_WALL_THICKNESS / 2.0]
        wall3["size"] = [self._roomWidth * Room.MULTIPLIER + 2 * Room.UNITY_WALL_THICKNESS, Room.UNITY_WALL_HEIGHT,
                         Room.UNITY_WALL_THICKNESS]

        JSON_Walls.append(wall3)

        wall4 = {}
        wall4["center"] = [Room.UNITY_WALL_THICKNESS / -2.0, Room.UNITY_WALL_HEIGHT / 2.0,
                           self._roomHeight * Room.MULTIPLIER / 2.0]
        wall4["size"] = [Room.UNITY_WALL_THICKNESS, Room.UNITY_WALL_HEIGHT-Room.UNITY_FLOOR_THICKNESS, self._roomHeight * Room.MULTIPLIER]

        JSON_Walls.append(wall4)

        return JSON_Walls

    def generate_JSON_string(self, num_trials=4):
        scenario = {}


        scenario["var1"] = 24
        scenario["array1"] = []

        scenario["trials"] = []


        for trial_num in range(num_trials):

            t = self.generate_JSON_trial(trial_num)

            scenario["trials"].append(t)

            self.performActions();



        return json.dumps(scenario, indent=4)


    def performActions(self):
        print("perform some actions before next JSON trial view is generated")

        self.generateNewGoals()
        self.moveCharacters()




    def generate_JSON_trial(self,  delay_ms = 5000, step=-1):

        trial = {}
        rs = self.getCharactersMatching("ROBOT")
        r = rs[0]
        trial["delay_ms"] = delay_ms
        trial["robot"] = r.toJSONStyle_dict(step)
        trial["humans"] = []
        trial["objects"] = []

        for h in self.getCharactersMatching("h00"):
            trial["humans"].append(h.toJSONStyle_dict(step))
        for i in self._items:
            if not isinstance(i, grasp.Grasp):
                trial["objects"].append(i.toJSONStyle_dict())
        trial["floor"] = {}
        trial["floor"]["size"] = [self._roomWidth*Room.MULTIPLIER, Room.UNITY_FLOOR_THICKNESS, self._roomHeight*Room.MULTIPLIER]
        trial["floor"]["center"] = [self._roomWidth//2 * Room.MULTIPLIER, Room.UNITY_FLOOR_THICKNESS/-2.0, self._roomHeight//2 * Room.MULTIPLIER]
        trial["ceiling"] = {}
        trial["ceiling"]["size"] = [self._roomWidth * Room.MULTIPLIER, Room.UNITY_FLOOR_THICKNESS,
                                  self._roomHeight * Room.MULTIPLIER]
        trial["ceiling"]["center"] = [self._roomWidth // 2 * Room.MULTIPLIER, Room.UNITY_WALL_HEIGHT,
                                    self._roomHeight // 2 * Room.MULTIPLIER]

        trial["walls"] = self._get_walls_JSON_list()


        return trial


    def addHumans(self, no_humans: int):
        current_no_humans = 0
        h_width = 50
        h_height = 50

        while current_no_humans < no_humans:
            newHuman = character.Character("h00" + str(current_no_humans), 'C:\\Users\\180123614\\Documents\\SocialRobotVRPritesh\\Assets\\Sprites\\person.png',
                                           random.randint(0, self._roomWidth - h_width - 10),
                                           random.randint(0, self._roomHeight - h_height - 10), 0, random.randint(0, Room.MAX_ANGLE),
                                           50, 50, self)
            collision = False
            for c in self._characters:
                if (newHuman.testOverlap(c.getPolygon())):
                    collision = True
                    #print(newHuman.getName(), "is overlapping", str(c.getName()))

            if not collision and not newHuman.testOfScreen(self._roomWidth++Room.MARGIN, self._roomHeight++Room.MARGIN, self.getFloorPolygon()):
                self._characters.append(newHuman)
                current_no_humans += 1
            #else:
                #print("Overlap occurred! ")



