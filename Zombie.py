#!/usr/bin/python
#-*- coding: utf-8 -*-

import pygame
import constants as c
import zrcommon as zrc
from zrcommon import Vector2D
from SteeringBehaviours import SteeringBehaviours



""" Class that represents a Zombie bot """
class Zombie:
    """ Constructor """
    def __init__(self, screen, level, level_borders, player,
                       ID, pos):
        self.__screen = screen                  # game display handler
        self.__level = level                    # Level handler
        self.__borders = level_borders          # space where zombies can wandern
        self.__player = player                  # Player handler
        self.__time_elapsed = c.time_elapsed    # time elapsed
        self.__color = c.zombie_color           # zombie's color
        self.ID = ID                            # ID number
        self.__pos = Vector2D(pos[0], pos[1])   # position
        self.radius = c.zombie_radius           # radius
        """ steering behaviours """
        self.velocity = Vector2D()                          # velocity vector
        self.__heading = Vector2D(pos[0], pos[1]).norm()    # heading vector
        self.__v_side = self.__heading.perp()               # vector perpendicular to heading vector
        self.__mass = 1 / c.zombie_mass                     # mass used in calculations
        self.max_velocity = c.zombie_max_velocity           # maximum velocity at which bot can travel
        self.__max_force = c.zombie_max_force               # maximum force that bot can produce to power itself
        self.__max_turn_rate = c.zombie_max_turn_rate       # maximum rate at which bot can rotate
        self.__steering = SteeringBehaviours(self, self.__max_force)
        """ DEBUG """
        self.debug_color = c.BLUE


    """ Move zombie bot """
    def move(self):
        # calculate vehicle position based on steering forces:
        steering_force = self.__steering.calculate()
        # Acceleration = Force / Mass:
        acceleration = steering_force.mult(self.__mass)
        # update velocity:
        """ debug - res velocity """
        #self.velocity = Vector2D(0,0)
        """ end debug """
        self.velocity.add(acceleration.mult(self.__time_elapsed))
        self.velocity.trunc(self.max_velocity)

        #print("velocity.magn:", self.velocity.magn())

        # update position:
        self.__pos.add(zrc.mult_vector(self.velocity, self.__time_elapsed))
        # check collisions:
        # check collisions with game world borders:
        if self.__pos.x < self.__borders[0]: self.__pos.x = self.__borders[0]
        elif self.__pos.x > self.__borders[1]: self.__pos.x = self.__borders[1]
        if self.__pos.y < self.__borders[2]: self.__pos.y = self.__borders[2]
        elif self.__pos.y > self.__borders[3]: self.__pos.y = self.__borders[3]

        # update heading if zombie has a velocity greater than a very small value:
        if self.velocity.magn() > 0.0000001:
            self.__heading = self.velocity.norm()
            self.__v_side = self.__heading.perp()


    """ Draws zombie bot """
    def draw(self):
        pygame.draw.circle(self.__screen, self.__color,
                           (int(self.__pos.x), int(self.__pos.y)),
                           self.radius,
                           2)

    """ DEBUG DRAW MODE """
    def draw_debug(self):
        target = self.get_target().position()
        pygame.draw.line(self.__screen,
                         self.debug_color,
                         (self.__pos.x, self.__pos.y),
                         (target.x, target.y))


    """ Get player """
    def get_target(self):
        return self.__player


    """ Get yourself position """
    def position(self):
        return self.__pos


    """ Get yourself heading """
    def heading(self):
        return self.__heading
