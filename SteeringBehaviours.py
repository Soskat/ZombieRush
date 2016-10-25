#!/usr/bin/python
#-*- coding: utf-8 -*-


import zrcommon as zrc

""" Class that define various steering behaviours """
class SteeringBehaviours:
    def __init__(self, vehicle):
        self.__vehicle = vehicle

    """ Seek """
    def seek(self, target):
        desired_velocity = zrc.norm_v(zrc.subv(target, self.__vehicle.get_position())) * self.__vehicle.max_velocity
        return zrc.sub_v(desired_velocity, self.__vehicle.velocity)
