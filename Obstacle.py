#!/usr/bin/python
#-*- coding: utf-8 -*-

import pygame
import math


""" Class that represents an obstacle """
class Obstacle:
    """ Constructor """
    def __init__(self, gameDisplay, center, radius, color):
        self.__screen = gameDisplay
        self.center = center
        self.radius = radius
        self.__color = color


    """ Draws Obstacle """
    def draw(self):
        pygame.draw.circle(self.__screen, self.__color, self.center, self.radius, 1)


    """ Checks if Obstacle collides with given object """
    def if_collide(self, ob):
        dx = self.center[0] - ob[0]
        dy = self.center[1] - ob[1]
        d = math.sqrt(math.pow(dx, 2) + math.pow(dy, 2))
        D = self.radius + ob[2]
        if d < self.radius + ob[2]:
            return True, (dx, dy, d, D)
        else:
            return False, None
