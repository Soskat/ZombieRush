#!/usr/bin/python
#-*- coding: utf-8 -*-

import pygame
import constants as c
import zrcommon as zrc
from zrcommon import Vector2D
from MovingEntity import MovingEntity
from SteeringBehaviours import SteeringBehaviours



""" Class that represents a Zombie bot """
class Zombie:
    """ Constructor """
    def __init__(self, screen, level, level_borders, player, ID, pos):
        self.__screen = screen                  # game display handler
        self.__level = level                    # Level handler
        self.__borders = level_borders          # space where zombies can wandern
        self.__player = player                  # Player handler
        self.__time_elapsed = c.time_elapsed    # time elapsed
        self.ID = ID                            # ID number
        self.me = MovingEntity( position = pos,
                                heading = pos,
                                max_speed = c.zombie_max_speed,
                                max_force = c.zombie_max_force,
                                max_turn_rate = c.zombie_max_turn_rate,
                                radius = c.zombie_radius,
                                mass = c.zombie_mass,
                                color = c.zombie_color
                               )
        self.__steering = SteeringBehaviours(self, self.me.max_force()) # steering behaviours handler
        """ DEBUG """
        self.debug_color = c.BLUE


    """ Move zombie bot """
    def move(self):
        # calculate vehicle position based on steering forces:
        steering_force = self.__steering.calculate()
        # Acceleration = Force / Mass:
        acceleration = steering_force.mult(self.me.mass_inv())
        # update velocity:
        """ debug - res velocity """
        #self.velocity = Vector2D(0,0)
        """ end debug """
        self.me.velocity.add(acceleration.mult(self.__time_elapsed))
        self.me.velocity.trunc(self.me.max_speed())

        #print("velocity.magn:", self.velocity.magn())

        # update position:
        self.me.pos.add(zrc.mult_vector(self.me.velocity, self.__time_elapsed))
        # check collisions:
        # check collisions with game world borders:
        if self.me.pos.x < self.__borders[0]: self.me.pos.x = self.__borders[0]
        elif self.me.pos.x > self.__borders[1]: self.me.pos.x = self.__borders[1]
        if self.me.pos.y < self.__borders[2]: self.me.pos.y = self.__borders[2]
        elif self.me.pos.y > self.__borders[3]: self.me.pos.y = self.__borders[3]

        # update heading if zombie has a velocity greater than a very small value:
        if self.me.velocity.magn() > 0.0000001:
            self.me.heading = self.me.velocity.norm()
            self.me.v_side = self.me.heading.perp()


    """ Draws zombie bot """
    def draw(self):
        pygame.draw.circle( self.__screen,
                            self.me.color(),
                            self.me.get_position(),
                            self.me.radius(),
                            2
                           )

    """ DEBUG DRAW MODE """
    def draw_debug(self):
        target = self.get_target().me.pos
        pygame.draw.line(self.__screen,
                         self.debug_color,
                         (self.me.pos.x, self.me.pos.y),
                         (target.x, target.y))


    """ Debug - draw vectors """
    def draw_vectors(self):
        # draw heading vector:
        a = zrc.add_vectors(self.me.pos, zrc.mult_vector(self.me.heading, 30))
        pygame.draw.line(self.__screen,
                         c.ORANGE,
                         (self.me.pos.x, self.me.pos.y),
                         (a.x, a.y))
        # draw v_side vector:
        b = zrc.add_vectors(self.me.pos, zrc.mult_vector(self.me.v_side, 10))
        pygame.draw.line(self.__screen,
                         c.DARKYELLOW,
                         (self.me.pos.x, self.me.pos.y),
                         (b.x, b.y))


    """ Get player """
    def get_target(self):
        return self.__player
