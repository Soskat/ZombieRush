#!/usr/bin/python
#-*- coding: utf-8 -*-

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


    """ Seek """
    def seek(self, target):
        desired_velocity = zrc.sub_vectors(self.__veh.get_target(), self.__veh.pos)
        desired_velocity.norm().mult(self.__veh.max_velocity)
        return zrc.sub_vectors(desired_velocity, self.__veh.velocity)


    """ Caculate all steeering forces that worked on vehicle """
    def calculate(self):
        """ The most basic system is used - change this later! """              #< ========================= BUKA
        steering_force = Vector2D()
        # sum all steering forces together:
        if self.seek_on:
            steering_force.add(self.seek(self.__veh.get_target()))
        steering_force.trunc(self.__max_force)
        return steering_force
