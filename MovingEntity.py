#!/usr/bin/python
#-*- coding: utf-8 -*-

from zrcommon import Vector2D


""" Class that represents a moving entity """
class MovingEntity:
    """ Constructor """
    def __init__(self, position, heading, max_speed, max_force, max_turn_rate,
                       radius, mass, color):
        self.__radius = radius                          # radius
        self.__mass = mass                              # mass
        self.__color = color                            # color
        self.__max_speed = max_speed                    # max speed
        self.__max_force = max_force                    # max force
        self.__max_turn_rate = max_turn_rate            # max turn rate
        self.pos = Vector2D(position[0], position[1])   # position vector
        self.heading = Vector2D(heading[0], heading[1]) # heading vector
        self.v_side = self.heading.perp()               # vector perpendicular to heading
        self.velocity = Vector2D()                      # velocity vector

    """ Speed """
    def speed(self):
        return self.velocity.magn()

    """ Max speed """
    def max_speed(self):
        return self.__max_speed

    """ Max force """
    def max_force(self):
        return self.__max_force

    """ Max turn rate """
    def max_turn_rate(self):
        return self.__max_turn_rate

    """ Radius """
    def radius(self):
        return self.__radius

    """ Mass """
    def mass(self):
        return self.__mass

    """ Color """
    def color(self):
        return self.__color
