#!/usr/bin/python
#-*- coding: utf-8 -*-

import pygame
from SteeringBehaviours import SteeringBehaviours


""" Class that represents a Zombie bot """
class Zombie:
    """ Constructor """
    def __init__(self, screen, level, player,
                       ID, position, radius, mass, max_velocity, max_force, max_turn_rate,
                       color):
        self.__screen = screen      # game display handler
        self.__level = level        # Level handler
        self.__player = player      # Player handler
        self.__color = color        # zombie's color
        self.ID = ID                # ID number
        self.posX = position[0]     # x posotion
        self.posY = position[1]     # y position
        self.radius = radius        # radius
        #self.__heading = [0.0, 0.0]             # heading vector
        #self.__v_side = [0.0, 0.0]              # vector perpendicular to heading vector    <-------------------------------------------------- DO IT RIGHT
        #self.__velocity = 0.0                   # current velocity
        self.__mass = mass                      # mass
        self.__max_velocity = max_velocity      # maximum velocity at which bot can travel
        self.__max_force = max_force            # maximum force that bot can produce to power itself
        self.__max_turn_rate = max_turn_rate    # maximum rate at which bot can rotate
        """ steering behaviours """
        self.__steering = SteeringBehaviours(self)
        self.__heading = [0.0, 0.0]             # heading vector
        self.__v_side = [0.0, 0.0]              # vector perpendicular to heading vector    <-------------------------------------------------- DO IT RIGHT
        self.__velocity = 0.0                   # current velocity
        self.__st_force = [0.0, 0.0]


    """ Move zombie bot """
    def move(self):
        self.__st_force = self.__steering.seek(self.__player.get_position())
        acceleration = [self.__st_force[i] / self.__mass for i in range(len(self.__st_force)) ]

    """ Draws zombie bot """
    def draw(self):
        pygame.draw.circle(self.__screen, self.__color,
                           (self.posX, self.posY),
                           self.radius,
                           2)


    """ Get zombie bot position """
    def get_position(self):
        return [self.posX, self.posY]
