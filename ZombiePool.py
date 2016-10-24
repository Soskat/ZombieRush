#!/usr/bin/python
#-*- coding: utf-8 -*-

import random
from Zombie import Zombie

import zrcommon



""" Class that coordinate zombie bots in game """
class ZombiePool:
    """ Constructor """
    def __init__(self, gameDisplay, displaySize, player,
                 zombieAmount, currZombieAmout, level, zombieColor):
        self.__screen = gameDisplay             # game display handler
        self.__level = level                    # Level handler
        self.__player = player                  # Player handler
        self.__zombieAmount = zombieAmount      # finite bots amount
        self.__currZombieAm = currZombieAmout   # current active bots amount
        self.__color = zombieColor              # zombies' color
        self.__zombies = []                     # list of zombie bots
        # make some zombies:
        canAdd = True
        radius = 8
        x = y = 0
        cX, cY, cR = self.__player.get_position_info()
        while len(self.__zombies) < self.__currZombieAm:
            counter += 1
            canAdd = True
            x = zrcommon.get_randint(0, displaySize[0])
            y = zrcommon.get_randint(0, displaySize[1])
            # check if (x,y) is outside game display or in player's start area:
            if (x + radius >= displaySize[0] or x - radius <= 0 or
                y + radius >= displaySize[1] or y - radius <= 0 or
                zrcommon.check_collision((cX,cY,cR), (x,y,radius))):
                continue # random all values again
            # check if new zombie may intersect with obstacles:
            x, y = self.__level.avoid_collision_with_obstacles((x,y,radius))
            # check if new zombie may intersect with other zombies:
            for z in self.__zombies:
                if zrcommon.check_collision((z.posX, z.posY, z.radius), (x,y,radius)):
                    canAdd = False
                    break
            # add new zombie to list:
            if canAdd:
                self.__zombies.append(Zombie(gameDisplay = self.__screen,
                                             level = level,
                                             player = player,
                                             ID = len(self.__zombies),
                                             position = (x,y),
                                             radius = radius,
                                             mass = 2,
                                             maxVeloc = 2.5,
                                             maxForce = 5.0,
                                             maxTurnRate = 5.0,
                                             color = self.__color))


    """ Adds new zombie bot to the zombie pool """
    def __add_new_zombie(self):
        pass


    """ Draws all zombie bots """
    def draw(self):
        for z in self.__zombies:
            z.draw()
