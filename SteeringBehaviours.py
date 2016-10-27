#!/usr/bin/python
#-*- coding: utf-8 -*-


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
        print("seek: ----------------------------")
        desired_velocity = self.__veh.get_target().sub(self.__veh.pos).norm().mult(self.__veh.max_velocity)
        desired_velocity.print_v()
        a = desired_velocity.sub(self.__veh.velocity)
        a.print_v()
        return a


    """ Caculate all steeering forces that worked on vehicle """
    def calculate(self):
        """ The most basic system is used - change this later! """              #< ========================= BUKA
        steering_force = Vector2D()
        # sum all steering forces together:
        if self.seek_on:
            steering_force.add(self.seek(self.__veh.get_target()))
            steering_force.print_v()
            print("seek on")

        print("steering_force")
        steering_force.print_v()
        return steering_force.trunc(self.__max_force)
