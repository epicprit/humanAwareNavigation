import json
import math
import random

import pygame
import shapely.affinity
from shapely.geometry import Polygon, Point
from shapely.affinity import *

import node
import room


class Character:



    def __init__(self, char_name, imageFilename, xPos, yPos, zPos, rotation, width, height, room):

        self._char_name = char_name
        self._x = xPos
        self._y = yPos
        self._z = zPos
        self._direction = rotation
        self._width = width
        self._height = height
        self._goal = None
        self._speed = 60
        self._room = room
        self._route = None


        self._image = pygame.image.load(imageFilename)
        self._image = pygame.transform.scale(self._image, (width, height))
        self._image = pygame.transform.rotate(self._image, self._direction)

        self._nodeGrid = None

    def getNode(self, col:int, row:int):

        result = None
        if (self._nodeGrid == None):
            rows = (self._room._roomHeight // node.Node.DEFAULT_GRID_SIZE) + 1
            cols = (self._room._roomWidth // node.Node.DEFAULT_GRID_SIZE) + 1

            self._nodeGrid = []
            for col in range(cols):
                self._nodeGrid.append([None] * rows)

        try:
            if self._nodeGrid[col][row] == None:
                self._nodeGrid[col][row] = node.Node(int((col+0.5)*node.Node.DEFAULT_GRID_SIZE), int((row+0.5)*node.Node.DEFAULT_GRID_SIZE))
            result = self._nodeGrid[col][row]
        except:
                print("node offgrid, None returned")


        return result


    def testOfScreen(self, screenWidth, screenHeight):
        for (x, y) in list(self.getPolygon().exterior.coords):
            if (x > screenWidth) | (x < 0) | (y > screenHeight) | (y < 0):
                return True
        return False


    def turnRandom(self):
        turnRange = 60
        turnDegrees = random.randint(1, 2*turnRange) - turnRange
        self._turn(turnDegrees)

    def _turn(self, degrees):
        self._direction = (self._direction + degrees) % 360


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

    def getPolygon(self):
        return Polygon([(self._x, self._y), (self._x + self._width+20, self._y), (self._x, self._y + self._height+20),
                          (self._x + self._width+20, self._y + self._height+20)])


    def testOverlap(self, otherPolygon):
        return  self.getPolygon().overlaps(otherPolygon)

    def getRotation(self):
        return self._direction

    def getImage(self):
        return self._image

    def getX(self):
        return self._x
    def getY(self):
        return self._y

    def getName(self):
        return self._char_name

    def getGoal(self):
        if self._goal == None:
            return Point(self._x, self._y, self._z)
        return self._goal

    def generateNewGoal(self, room, prob=1.0):

        score = random.randint(1,100)
        if score <= int(prob*100):
            MARGIN = 20

            self._goal = Point(random.randint(MARGIN, room._roomWidth - MARGIN),
                               random.randint(MARGIN, room._roomHeight - MARGIN))
            circle = self._goal.buffer(1.0)
            bubble = shapely.affinity.scale(circle, MARGIN, MARGIN)

            while room.hasObjectsIn(bubble, [self]):
                self._goal = Point(random.randint(MARGIN, room._roomWidth - MARGIN),
                                   random.randint(MARGIN, room._roomHeight - MARGIN))
                circle = self._goal.buffer(1.0)
                bubble = shapely.affinity.scale(circle, MARGIN, MARGIN)


        return self._goal


    def moveCharacter(self, room):

        # vx and vy are linear speeds
        # va is angular speed
        TURN_ATTEMPTS_LIMIT = 5
        newPosition = self._calculateNextPosition(self._speed)

        attempts = 0

        inside_room = self._testNewGoalPosition(newPosition, room)

        while not self._testNewGoalPosition(newPosition, room) and attempts < TURN_ATTEMPTS_LIMIT:
            attempts += 1
            self.turnRandom()
            newPosition = self._calculateNextPosition(self._speed)

        if self._testNewGoalPosition(newPosition, room):
            self._x = newPosition.x
            self._y = newPosition.y
        else:
            print(self._char_name + ":  couldn't move this character due to collisions.")






    def _calculateLinearVelocities(self, stepDistance):
        vx = math.sin(math.radians(self._direction)) * stepDistance
        vy = math.cos(math.radians(self._direction)) * stepDistance
        """
        if self._direction < 90:
            vy *= -1


        elif self._direction == 90:
            vy *= -1



        elif self._direction < 180:
            vx *= -1
            vy *= -1


        elif self._direction == 180:
            vx *= -1


        elif self._direction < 270:
            vx *= -1
        elif self._direction == 270:
            pass
        else:
            pass  """
        return vx, vy


    def _calculateNextPosition(self, stepDistance):

        vx, vy = self._calculateLinearVelocities(stepDistance)

        return Point(self._x + vx, self._y + vy)

    def _testNewGoalPosition(self, newPosition, room, margin=20):

        circle = newPosition.buffer(margin)
        bubble = shapely.affinity.scale(circle, 1, 1)

        collisions = room.hasObjectsIn(circle, [self])

        return not room.hasObjectsIn(circle, [self]) and room.getFloorPolygon().contains(Point(newPosition))


    def getMyPositionAtStep(self, step):

        if step >= len(self._route):
            step = -1

        return self._route[step]

    def getRoute(self):
        if self._route == None:
            self._route = [node.Node(self._x, self._y)]
        return self._route

    def planRoute(self, destination:Point, room:room.Room):
        openList = []
        closeList = []

        myPositionNode = self.getNode(int(self._x // node.Node.DEFAULT_GRID_SIZE), int(self._y // node.Node.DEFAULT_GRID_SIZE))
        destNode = self.getNode(int(destination.x // node.Node.DEFAULT_GRID_SIZE) , int(destination.y // node.Node.DEFAULT_GRID_SIZE))

        if myPositionNode == destNode:
            print("Character ", self._char_name, "has no route because already at dest")
            return


        dest_col, dest_row = destNode.calculateGridPos()

        currentNode = myPositionNode

        print("starting position: ", destination.x, ", ", destination.y)
        print("starting node: ", myPositionNode.calculateGridPos())

        openList.append(currentNode)

        cheapestNode = None
        bestCost = math.inf
        foundDestination = False

        parents = {openList[0]:None}

        count = 0
        while len(set(openList)) > 0 and not foundDestination:


            cheapestNode = openList[0]
            bestCost = cheapestNode.calculateFCost(Point(self._x, self._y), destination)


            for n in openList:


                n_x, n_y =  n.calculateGridPos()
                d_x, d_y =  destNode.calculateGridPos()
                if n == destNode:
                    print("got to destination location!!", destNode.calculateGridPos())
                    foundDestination = True
                    print("now print out the route")

                    route = []




                    parentNode = destNode
                    while parentNode != None:


                        parentNode = parents[parentNode]

                        if parentNode != None:
                            route.append(parentNode)

                    route.reverse()

                    route.append(destNode)

                    self._route = route

                    for step in route:
                        print(step.calculateGridPos())
                    return

                if (n.calculateFCost(Point(self._x, self._y), destination) < bestCost) and n not in closeList:
                    cheapestNode =n
                    bestCost = cheapestNode.calculateFCost(Point(self._x, self._y), destination)

            try:
                openList.remove(cheapestNode)
                closeList.append(cheapestNode)

            except:
                pass

            #print(" >>  cheapest Node = ", cheapestNode.calculateGridPos(), " << ")

            newNeighbours = cheapestNode.findNeighhbours(self)

            for n in newNeighbours:
                if not self._testNewGoalPosition(Point(n.getX(), n.getY()), room, 200):
                    newNeighbours.remove(n)

            for n in set(newNeighbours):
                if n not in parents:
                    parents[n] = cheapestNode
                #print(" >>  >>  neighbour pos: ", n.calculateGridPos() )

                if n not in closeList and n not in openList:
                    openList.append(n)
                    pass
            cheapestNode = None
            sorted(openList, key = lambda node : node.getFCost())







    def setDirection(self, Angle):
        self._direction = Angle

    def toJSONStyle_dict(self, step=-1):
        MULTIPLIER = 0.01
        my_data = {}
        my_data["id"] = self._char_name
        if step >= 0:
            my_data["position"] = [self._route[step].getX() * MULTIPLIER, self._z * MULTIPLIER, self._route[step].getY() * MULTIPLIER]
        else:
            my_data["position"] = [self._x*MULTIPLIER, self._z*MULTIPLIER, self._y*MULTIPLIER]
        my_data["rotation"] = [0, self._direction, 0]
        my_data["va"] = self._speed*MULTIPLIER
        vx, vy = self._calculateLinearVelocities(self._speed)
        my_data["vx"] = vx * MULTIPLIER
        my_data["vy"] = vy * MULTIPLIER
        my_data["vz"] = 0.0



        my_data["goal"] = [self.getGoal().x*MULTIPLIER, self._z*MULTIPLIER, self.getGoal().y*MULTIPLIER]

        return my_data



