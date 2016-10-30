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
        self.arrive_on = True
        self.pursuit_on = True


    """ Seek """
    def seek(self, target):
        desired_velocity = zrc.sub_vectors(target, self.__veh.position())
        desired_velocity.norm().mult(self.__veh.max_velocity)
        return zrc.sub_vectors(desired_velocity, self.__veh.velocity)


    """ Flee """
    def flee(self, target):
        # flee only when the target is inside panic_distance:
        if not zrc.check_collision(
                (self.__veh.position().x, self.__veh.position().y, self.__veh.radius),
                (target.x, target.y, c.panic_distance)
                ):
            self.__veh.debug_color = c.BLUE#<=================================== ------------- DEBUG
            return Vector2D()
        self.__veh.debug_color = c.RED#<======================================== ------------- DEBUG
        desired_velocity = zrc.sub_vectors(self.__veh.position(), target)
        desired_velocity.norm().mult(self.__veh.max_velocity)
        return zrc.sub_vectors(desired_velocity, self.__veh.velocity)


    """ Arrive """#<-------------------------   FIX IT  ----------------------------------------------
    def arrive(self, target):
        to_target = zrc.sub_vectors(target, self.__veh.position())
        # calculate the distance to the target position:
        dist = to_target.magn()
        print("dist:", dist)
        if dist > 0:
            # calculate deceleration:
            if dist <= 100:
                deceleration = 3
            elif dist <= 200:
                deceleration = 2
            else:
                deceleration = 1
            print(deceleration)
            # calculate the speed recquired to reach the target given the desired deceleration
            speed = dist / (float(deceleration) * c.deceleration_tweaker)
            print("speed:", speed)
            # make sure the velocity does not exceed the max:
            speed = min(speed, self.__veh.max_velocity)
            print("speed after:", speed)
            # now proceed almost like in seek:
            to_target.mult(speed/dist)
            print("to_target:", to_target.magn())
            a = zrc.sub_vectors(to_target, self.__veh.velocity)
            print("arrive_vec_magn:", a.magn())
            return zrc.sub_vectors(to_target, self.__veh.velocity)
        return Vector2D()


    """ Pursuit """
    def pursuit(self, evader):
        # if the evader is ahead and facing the agent then we can just seek evader's current position:
        to_evader = zrc.sub_vectors(evader.position(), self.__veh.position())
        relative_heading = self.__veh.heading().dot(evader.heading())
        if (to_evader.dot(self.__veh.heading()) > 0 and relative_heading < -0.95): # acos(0.95) = 18 deg
            return self.seek(evader.position())
        # not considered ahead so we predict where the evader will be:
        
        return Vector2D()


    """ Caculate all steeering forces that worked on vehicle """
    def calculate(self):
        """ The most basic system is used - change this later! """              #< ========================= BUKA
        steering_force = Vector2D()
        # sum all steering forces together:
        #if self.seek_on: steering_force.add(self.seek(self.__veh.get_target().position()))
        #if self.flee_on: steering_force.add(self.flee(self.__veh.get_target().position()))
        #if self.arrive_on: steering_force.add(self.arrive(self.__veh.get_target().position()))
        if self.pursuit_on: steering_force.add(self.pursuit(self.__veh.get_target()))
        steering_force.trunc(self.__max_force)
        return steering_force
