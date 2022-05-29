import json
import random

import pygame
from shapely.geometry import Polygon
from shapely.affinity import *
import item
import plant

class Storage(item.Item):


    INSIDE = 1
    ON_TOP = 2
    UNDERNEATH = 4



    locations = [INSIDE, ON_TOP, UNDERNEATH]



    meaning = {INSIDE: "inside", ON_TOP: "on_top", UNDERNEATH: "underneath"}

    @staticmethod
    def getEmptyStorage(items,storageCode):
        storage_items = []
        for i in items:
            if isinstance(i, Storage):
                #s = (storage.Storage) (i)
                if i.checkStorage(storageCode):
                    if len(i.getStoredItems(storageCode)) ==0 :
                        storage_items.append(i)
                    elif storageCode == Storage.INSIDE and len(i.getStoredItems(storageCode)) < len(i._inside_locations):
                        storage_items.append(i)
        if len(storage_items) == 0:
            return None
        return random.choice(storage_items)

    def __init__(self, item_name, xPos, yPos, zPos, rotation, objectWidth, objectHeight,zLength,storageCode):
        super().__init__(item_name, xPos, yPos, zPos, rotation, objectWidth, objectHeight,zLength)
        self.stored_items = {Storage.INSIDE:[], Storage.ON_TOP:[], Storage.UNDERNEATH:[]}
        self._colour = (200, 0, 200)
        self._model = random.choice(['Shelf', 'Desk', 'Bookcase'])

        if self._model == 'Shelf':
            self._objectWidth = 60
            self._objectHeight = 40
            self._zLength = 150
            self._storageCode = Storage.INSIDE #+ Storage.ON_TOP
            self._inside_locations = []
            self._inside_locations.append([0, 8, 4])
            self._inside_locations.append([0, 55, 4])
            self._inside_locations.append([0, 104, 4])

        elif self._model == 'Desk':
            self._objectWidth = 100
            self._objectHeight = 60
            self._zLength = 81
            self._storageCode = Storage.UNDERNEATH + Storage.ON_TOP

        elif self._model == 'Bookcase':
            self._objectWidth = 200
            self._objectHeight = 50
            self._zLength = 120
            self._storageCode = Storage.INSIDE #+ Storage.ON_TOP
            self._inside_locations = []
            self._inside_locations.append([47, 77, -4])
            self._inside_locations.append([47, 34, -4])
            self._inside_locations.append([-54, 34, -4])
            self._inside_locations.append([-54, 77, -4])


        #self._storageCode = storageCode


    def addItem(self, item_to_add:item.Item, location=ON_TOP):



        #set the relative position of the object stored compared to the storage object
        # if underneath, x = 10, y = 0, z = 10
        # if on top, x = 10, y = storage object height (zlength), z = 10
        # if inside, this will vary depending on the item, ...

        if location == Storage.UNDERNEATH:
            item_to_add.setX(10)
            item_to_add.setY(10)
            item_to_add.setZ(0)

        elif location == Storage.ON_TOP:
            item_to_add.setX(10)
            item_to_add.setY(10)
            item_to_add.setZ(self._zLength)

        elif location == Storage.INSIDE:
            items_inside_already = len(self.stored_items[location])
            item_to_add.setX(self._inside_locations[items_inside_already][0])
            item_to_add.setY(self._inside_locations[items_inside_already][2])
            item_to_add.setZ(self._inside_locations[items_inside_already][1])

            if isinstance(item_to_add, plant.Plant):
                item_to_add.scale(0.2)

        (self.stored_items[location]).append(item_to_add)

    def getStoredItems(self, location):
        return self.stored_items[location]

    def checkStorage(self, storage_code):
        return (self._storageCode & storage_code) != 0

    def getSuggestedLocation(self, roomWidth, roomHeight):

        NORTH = 0
        SOUTH = 180
        EAST = 90
        WEST = 270
        walls = [NORTH, SOUTH, WEST, EAST]

        MARGIN = 20
        CORNER_MARGIN = 30

        x = -1
        y = -1
        chosen_wall = random.choice(walls)
        direction_facing = (chosen_wall + 180) % 360
        if chosen_wall == NORTH:
            # case 1 = NORTH WALL
            x = random.randint(CORNER_MARGIN, roomWidth - CORNER_MARGIN - self._objectWidth)
            y = MARGIN

        # case 2 = EAST WALL
        elif chosen_wall == EAST:
            x = roomWidth - self._objectHeight - MARGIN
            y = random.randint(CORNER_MARGIN, roomHeight - CORNER_MARGIN - self._objectWidth)


        elif chosen_wall == SOUTH:
            # case 3 = SOUTH WALL
            x = random.randint(CORNER_MARGIN, roomWidth - CORNER_MARGIN - self._objectWidth)
            y = roomHeight - self._objectHeight - MARGIN


        elif chosen_wall == WEST:
            # case 4 = WEST WALL
            x = MARGIN
            y = random.randint(CORNER_MARGIN, roomHeight - CORNER_MARGIN - self._objectWidth)

        return x, y, direction_facing

    def getPolygon(self):

        if self.getRotation() %180 == 0:
            return Polygon([(self._x, self._y), (self._x + self._objectWidth, self._y), (self._x, self._y + self._objectHeight),
                        (self._x + self._objectWidth, self._y + self._objectHeight)])
        else:
            return Polygon(
                [(self._x, self._y), (self._x + self._objectHeight, self._y), (self._x, self._y + self._objectWidth),
                 (self._x + self._objectHeight, self._y + self._objectWidth)])


    def toJSONStyle_dict(self):

        # update the relative position x, y and z
        # for on top items y = self._zlength, x and z should be 10cm

        my_data = item.Item.toJSONStyle_dict(self)
        my_data["contents"] = {}

        for location in ["inside", "on_top", "underneath"]:
            my_data["contents"][location] = []

        for stored_item in self.getStoredItems(Storage.INSIDE):
            my_data["contents"]["inside"].append(stored_item.toJSONStyle_dict())


        for stored_item in self.getStoredItems(Storage.UNDERNEATH):
            my_data["contents"]["underneath"].append(stored_item.toJSONStyle_dict())


        for stored_item in self.getStoredItems(Storage.ON_TOP):


            my_data["contents"]["on_top"].append(stored_item.toJSONStyle_dict())


        return my_data



