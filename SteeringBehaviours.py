#!/usr/bin/python
#-*- coding: utf-8 -*-

import constants as c
import zrcommon as zrc
from zrcommon import Vector2D



""" Class that define various steering behaviours """
class SteeringBehaviours:
    """ Constructor """
    def __init__(self, vehicle, max_force):
        self.__veh = vehicle            # vehicle handler
        self.__max_force = max_force    # max steering force value
        """ flags that control use of steering behaviours """
        self.seek_on = True
        self.flee_on = True


    """ Seek """
    def seek(self, target):
        desired_velocity = zrc.sub_vectors(self.__veh.get_target(), self.__veh.pos)
        desired_velocity.norm().mult(self.__veh.max_velocity)
        return zrc.sub_vectors(desired_velocity, self.__veh.velocity)


    """ Flee """
    def flee(self, target):
        # flee only when the target is inside panic_distance:
        if not zrc.check_collision(
                (self.__veh.pos.x, self.__veh.pos.y, self.__veh.radius),
                (self.__veh.get_target().x, self.__veh.get_target().y, c.panic_distance)
                ):
            self.__veh.debug_color = c.BLUE#<=================================== ------------- DEBUG
            return Vector2D()
        self.__veh.debug_color = c.RED#<======================================== ------------- DEBUG
        desired_velocity = zrc.sub_vectors(self.__veh.pos, self.__veh.get_target())
        desired_velocity.norm().mult(self.__veh.max_velocity)
        return zrc.sub_vectors(desired_velocity, self.__veh.velocity)


    """ Caculate all steeering forces that worked on vehicle """
    def calculate(self):
        """ The most basic system is used - change this later! """              #< ========================= BUKA
        steering_force = Vector2D()
        # sum all steering forces together:
        #if self.seek_on: steering_force.add(self.seek(self.__veh.get_target()))
        if self.flee_on:
            steering_force.add(self.flee(self.__veh.get_target()))
        steering_force.trunc(self.__max_force)
        return steering_force
