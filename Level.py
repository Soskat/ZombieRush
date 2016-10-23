#!/usr/bin/python
#-*- coding: utf-8 -*-

import pygame
import zrcommon
from Obstacle import Obstacle

"""" Class that represents a level """
class Level:
    """ Constructor """
    def __init__(self, gameDisplay, displaySize, margin, color, obstaclesAmount):
        self.__screen = gameDisplay
        self.__color = color
        self.obstacles = {}

        # generate obstacles:
        x = y = radius = obst = keyX = keyY = 0
        cX = displaySize[0] / 2
        cY = displaySize[1] / 2
        cR = 20
        while obst < obstaclesAmount:
            radius = zrcommon.get_randint(35, 50)
            x = zrcommon.get_randint(0, displaySize[0])
            y = zrcommon.get_randint(0, displaySize[1])
            # check if obstacle is outside game display or in player's start area:
            if (x + radius >= displaySize[0] or x - radius <= 0 or
                y + radius >= displaySize[1] or y - radius <= 0 or
                zrcommon.check_collision((cX,cY,cR), (x,y,radius))):
                continue # random all values again

            keyX = int(x / 100)
            keyY = int(y / 100)
            # check if new obstacle not intersect others - if no, add it to dict:
            if self.if_not_collide_with_obstacles(keyX, keyY, (x,y,radius)):
                if not keyX in self.obstacles:
                    self.obstacles[keyX] = {}
                if not keyY in self.obstacles[keyX]:
                    self.obstacles[keyX][keyY] = []
                self.obstacles[keyX][keyY].append(Obstacle(self.__screen, (x,y), radius, self.__color))
                obst += 1


    """ Draws level """
    def draw(self):
        for keyX in self.obstacles:
            for keyY in self.obstacles[keyX]:
                for obst in self.obstacles[keyX][keyY]:
                    obst.draw()


    """ Checks if object collides with any obstacles """
    def if_not_collide_with_obstacles(self, keyX, keyY, obj):
        for kx in range(keyX - 1, keyX + 2):
            if kx in self.obstacles:
                for ky in range (keyY - 1, keyY + 2):
                    if ky in self.obstacles[kx]:
                        for ob in self.obstacles[kx][ky]:
                            if ob.if_collide(obj):
                                return False
        return True
