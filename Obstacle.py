#!/usr/bin/python
#-*- coding: utf-8 -*-

import pygame
import zrcommon

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
        return zrcommon.check_collision_detailed((self.center[0], self.center[1], self.radius), ob)
