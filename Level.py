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
        x = y = radius = obst = 0
        flag = canAdd = True
        cX = displaySize[0] / 2
        cY = displaySize[1] / 2
        cR = 20

        while obst < obstaclesAmount:
            flag = canAdd = True
            radius = random.randint(35, 50)
            x = random.randint(0, displaySize[0])
            y = random.randint(0, displaySize[1])
            # check if obstacle is outside game display or in player's start area:
            if (x + radius >= displaySize[0] or x - radius <= 0 or
                y + radius >= displaySize[1] or y - radius <= 0 or
                self.__if_collide_with_player((cX,cY,cR), (x,y,radius))):
                continue # random all values again

            keyX = int(x / 100)
            keyY = int(y / 100)
            # check if new obstacle may intersect with others:
            for kx in range(keyX - 1, keyX + 2):
                if kx in self.obstacles:
                    for ky in range (keyY - 1, keyY + 2):
                        if ky in self.obstacles[kx]:
                            for ob in self.obstacles[kx][ky]:
                                if self.__if_obstacles_collide((x,y,radius), ob):
                                    canAdd = flag = False
                                    break
                        if not flag: break
                if not flag: break

            # new obstacle can be added:
            if canAdd:
                if not keyX in self.obstacles:
                    self.obstacles[keyX] = {}
                self.obstacles[keyX][keyY] = [Obstacle(self.__screen, (x,y), radius, self.__color)]
                obst += 1


    """ Draws level """
    def draw(self):
        for keyX in self.obstacles:
            for keyY in self.obstacles[keyX]:
                for obst in self.obstacles[keyX][keyY]:
                    obst.draw()


    """ Checks intersection between given obstacles.
        ob1 is a touple, ob2 is an Obstacle instance. """
    def __if_obstacles_collide(self, ob1, ob2):
        s1 = math.pow(ob1[0] - ob2.center[0], 2)
        s2 = math.pow(ob1[1] - ob2.center[1], 2)
        if math.sqrt(s1 + s2) < ob1[2] + ob2.radius:
            return True
        else:
            return False


    """ Checks if obstacle intersects with Player's start area. """
    def __if_collide_with_player(self, player, ob):
        s1 = math.pow(player[0] - ob[0], 2)
        s2 = math.pow(player[1] - ob[1], 2)
        if math.sqrt(s1 + s2) < player[2] + ob[2]:
            return True
        else:
            return False
