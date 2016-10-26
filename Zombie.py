#!/usr/bin/python
#-*- coding: utf-8 -*-

import pygame
from zrcommon import Vector2D
from SteeringBehaviours import SteeringBehaviours


""" Class that represents a Zombie bot """
class Zombie:
    """ Constructor """
    def __init__(self, screen, level, player,
                       ID, pos, radius, mass, max_velocity, max_force, max_turn_rate,
                       color):
        self.__screen = screen              # game display handler
        self.__level = level                # Level handler
        self.__player = player              # Player handler
        self.__color = color                # zombie's color
        self.ID = ID                        # ID number
        self.pos = Vector2D(pos[0], pos[1]) # position
        self.radius = radius                # radius
        """ steering behaviours """
        self.velocity = Vector2D()              # velocity vector
        self.__heading = Vector2D()             # heading vector
        self.__v_side = self.__heading.perp()   # vector perpendicular to heading vector
        self.__mass = 1 / mass                  # mass used in calculations
        self.max_velocity = max_velocity        # maximum velocity at which bot can travel
        self.__max_force = max_force            # maximum force that bot can produce to power itself
        self.__max_turn_rate = max_turn_rate    # maximum rate at which bot can rotate
        self.__steering = SteeringBehaviours(self, self.__max_force)


    """ Move zombie bot """
    def move(self):
        TIME_ELAPSED = 0.3      #<====================================================================================== ??
        # calculate vehicle position based on steering forces:
        steering_force = self.__steering.calculate()
        print("steering_force after truncate")
        steering_force.print_v()
        # Acceleration = Force / Mass
        acceleration = steering_force.mult(self.__mass)
        print("acceleration")
        acceleration.print_v()
        # update velocity:
        self.velocity = self.velocity.add(acceleration.mult(TIME_ELAPSED)).trunc(self.max_velocity)
        # update position:
        self.pos = self.pos.add(self.velocity.mult(TIME_ELAPSED))
        # update heading if zombie has a velocity greater than a very small value:
        if self.velocity.magn() > 0.0000001:
            self.__heading = self.velocity.norm()
            self.__v_side = self.__heading.perp()


    """ Draws zombie bot """
    def draw(self):
        pygame.draw.circle(self.__screen, self.__color,
                           (int(self.pos.x), int(self.pos.y)),
                           self.radius,
                           2)


    """ Get player position """
    def get_target(self):
        return self.__player.get_pos()
