#!/usr/bin/python
#-*- coding: utf-8 -*-

import pygame


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
