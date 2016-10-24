#!/usr/bin/python
#-*- coding: utf-8 -*-

import random
from Zombie import Zombie

import math



""" Class that coordinate zombie bots in game """
class ZombiePool:
    """ Constructor """
    def __init__(self, gameDisplay, displaySize,
                 zombieAmount, currZombieAmout, levelObstacles, zombieColor):
        self.__screen = gameDisplay
        self.__lvlObst = levelObstacles
        self.__zombieAmount = zombieAmount  # finite bots amount
        self.__currZombieAm = currZombieAmout
        self.__color = zombieColor          # zombies' color
        self.__zombies = []
        # make some zombies:
        flag = canAdd = True
        radius = 5
        x = y = keyX = keyY = 0
        cX = displaySize[0] / 2
        cY = displaySize[1] / 2
        cR = 20
        while len(self.__zombies) < self.__currZombieAm:
            print("loading...")
            flag = canAdd = True
            x = random.randint(0, displaySize[0])
            y = random.randint(0, displaySize[1])
            # check, if position is outside game display or in player's start area:
            if (x + radius >= displaySize[0] or x - radius <= 0 or
                y + radius >= displaySize[1] or y - radius <= 0 or
                self.__if_collide_with_player_area((cX,cY,cR), (x,y,radius))):
                continue # random all values again

            keyX = int(x / 100)
            keyY = int(y / 100)
            # check if new zombie may intersect with obstacle:
            for kx in range(keyX - 1, keyX + 2):
                if kx in self.__lvlObst:
                    for ky in range (keyY - 1, keyY + 2):
                        if ky in self.__lvlObst[kx]:
                            for ob in self.__lvlObst[kx][ky]:
                                if ob.if_collide((x,y,radius)):
                                    canAdd = flag = False
                                    break
                        if not flag: break
                if not flag: break

            if flag:
                for z in self.__zombies:
                    if self.__if_collide_with_player_area((x,y,radius), (z.posX, z.posY, z.radius)):
                        canAdd = False
                        break
            if canAdd:
                self.__zombies.append(Zombie(self.__screen, levelObstacles,
                    len(self.__zombies), (x,y), 2, 2.5, 5.0, 5.0, self.__color))

    """ Adds new zombie bot to the zombie pool """
    def __add_new_zombies(self):
        pass

    """ Draws all zombie bots """
    def draw(self):
        for z in self.__zombies:
            z.draw()


    """ Checks if zombie intersects with Player's start area """
    def __if_collide_with_player_area(self, zombie, ob):
        s1 = math.pow(zombie[0] - ob[0], 2)
        s2 = math.pow(zombie[1] - ob[1], 2)
        if math.sqrt(s1 + s2) < zombie[2] + ob[2]:
            return True
        else:
            return False
