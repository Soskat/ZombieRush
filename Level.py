#!/usr/bin/python
#-*- coding: utf-8 -*-

import pygame
import random
import math
from Obstacle import Obstacle

"""" Class that represents a level """
class Level:
    """ Constructor """
    def __init__(self, gameDisplay, displaySize, margin, color, obstaclesAmount):
        self.__screen = gameDisplay
        self.__color = color
        # generate obstacles:
        self.obstacles = {}
        obst = 0
        radius = 0
        x = y = 0
        while obst < obstaclesAmount:
            canAdd = False
            radius = random.randint(35, 50)
            x = random.randint(0, displaySize[0])
            y = random.randint(0, displaySize[1])
            # check if obstacle is fully inside game display:
            if (x + radius >= displaySize[0] or x - radius <= 0 or
                y + radius >= displaySize[1] or y - radius <= 0):
                continue # random all values again

            tempColor = self.__color                                            #""" <============================ """

            keyX = int(x / 100)
            keyY = int(y / 100)
            if keyX in self.obstacles:
                print("-- there's %i in obstacles" % keyX)
                if keyY in self.obstacles[keyX]:
                    print("-- there's %i in obstacles[%i]" % (keyY, keyX))
                    # check if new obstacle intersects with others:
                    for i in range(keyX - 1, keyX + 1):
                        print("X key:", i)                                      #""" <============================ """
                        if i in self.obstacles:
                            for j in range (keyY - 1, keyY + 1):
                                print("\tY key:", j)                            #""" <============================ """
                                if j in self.obstacles[i]:
                                    for ob in self.obstacles[i][j]:
                                        if not self.__obstacles_collide((x,y,radius), ob):
                                            canAdd = False
                                            tempColor = (200,0,0)
                                            print("NOPE !")                     #""" <============================ """
                                            break
                else: # add keyY to dictionary obstacles[keyX]
                    canAdd = True
                    tempColor = self.__color
            else: # add keyX to dictionary obstacles
                self.obstacles[keyX] = {}
                canAdd = True
                tempColor = self.__color

            if canAdd:
                self.obstacles[keyX][keyY] = [Obstacle(self.__screen, (x,y), radius, tempColor)]
                print("Obstacle %i, keyX: %i, keyY: %i" % (obst, keyX, keyY))      #""" <============================ """
                obst += 1

    """ Draws level """
    def draw(self):
        self.__draw_grid()
        for keyX in self.obstacles:
            for keyY in self.obstacles[keyX]:
                for obst in self.obstacles[keyX][keyY]:
                    obst.draw()

    """ Checks intersection between given obstacles.
        ob1 is a touple, ob2 is an Obstacle instance. """
    def __obstacles_collide(self, ob1, ob2):
        s1 = math.pow(ob1[0] - ob2.center[0], 2)
        s2 = math.pow(ob1[1] - ob2.center[1], 2)
        if math.sqrt(s1 + s2) < ob1[2] + ob2.radius:
            return True
        else:
            return False

    def __draw_grid(self):
        # vertical lines:
        for x in range(0, 800, 100):
            pygame.draw.line(self.__screen, (0,50,200), (x,0), (x,600))
        # horizontal lines:
        for y in range(0, 600, 100):
            pygame.draw.line(self.__screen, (0,50,200), (0,y), (800,y))
