#!/usr/bin/python
#-*- coding: utf-8 -*-

import pygame



""" Class that represents a Zombie bot """
class Zombie:
    """ Constructor """
    def __init__(self, gameDisplay, level, player,
                       ID, position, mass, maxVeloc, maxForce, maxTurnRate,
                       color):
        self.__screen = gameDisplay         # game display handler
        self.__level = level                # Level handler
        self.__player = player              # Player handler
        self.__color = color                # zombie's color
        self.ID = ID                        # ID number
        self.posX = position[0]             # x posotion
        self.posY = position[1]             # y position
        self.radius = 8                     # radius
        self.__heading = [0.0, 0.0]         # heading vector
        self.__vSide = [0.0, 0.0]           # vector perpendicular to heading vector    <-------------------------------------------------- DO IT RIGHT
        self.__velocity = 0.0               # current velocity
        self.__mass = mass                  # mass
        self.__maxVeloc = maxVeloc          # maximum velocity at which bot can travel
        self.__maxForce = maxForce          # maximum force that bot can produce to power itself
        self.__maxTurnRate = maxTurnRate    # maximum rate at which bot can rotate


    """ Draws zombie bot """
    def draw(self):
        pygame.draw.circle(self.__screen, self.__color, (self.posX, self.posY),
                            self.radius, 2)
