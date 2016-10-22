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
        s1 = math.pow(self.center[0] - ob[0], 2)
        s2 = math.pow(self.center[1] - ob[1], 2)
        if math.sqrt(s1 + s2) < self.radius + ob[2]:
            return True
        else:
            return False
