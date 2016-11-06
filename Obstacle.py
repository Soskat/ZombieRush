#!/usr/bin/python
#-*- coding: utf-8 -*-

import pygame
import zrcommon
from Vector2D import Vector2D



""" Class that represents an obstacle """
class Obstacle:
    """ Constructor """
    def __init__(self, game_display, center, radius, color):
        self.__screen = game_display
        self.center = Vector2D(center[0], center[1])
        self.radius = radius
        self.__color = color


    """ Draws Obstacle """
    def draw(self):
        pygame.draw.circle(self.__screen,
                           self.__color,
                           (self.center.x, self.center.y),
                           self.radius,
                           1
                          )


    """ Checks if Obstacle collides with given object """
    def is_collided(self, ob):
        return zrcommon.check_collision((self.center.x, self.center.y, self.radius), ob)


    """ Checks if Obstacle collides with given object.
        If yes, recalculate position of given object to avoid collision """
    def avoid_collision(self, ob):
        return zrcommon.avoid_collision((self.center.x, self.center.y, self.radius), ob)
