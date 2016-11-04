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
    def seek(self, target_pos):
        desired_velocity = zrc.sub_vectors(target_pos, self.__veh.me.pos)
        desired_velocity.norm().mult(self.__veh.me.max_speed())
        return zrc.sub_vectors(desired_velocity, self.__veh.me.velocity)


    """ Flee """
    def flee(self, target_pos):
        # flee only when the target is inside panic_distance:
        if not zrc.check_collision(
                (self.__veh.me.pos.x, self.__veh.me.pos.y, self.__veh.me.radius()),
                (target_pos.x, target_pos.y, c.panic_distance)
                ):
            self.__veh.debug_color = c.BLUE#<=================================== ------------- DEBUG
            return Vector2D()
        self.__veh.debug_color = c.RED#<======================================== ------------- DEBUG
        desired_velocity = zrc.sub_vectors(self.__veh.me.pos, target_pos)
        desired_velocity.norm().mult(self.__veh.me.max_speed())
        return zrc.sub_vectors(desired_velocity, self.__veh.me.velocity)


    """ Arrive """#<-------------------------   FIX IT  ----------------------------------------------
    def arrive(self, target_pos):
        to_target = zrc.sub_vectors(target_pos, self.__veh.me.pos)
        # calculate the distance to the target position:
        dist = to_target.magn()
        #print("dist:", dist)
        if dist > 5:
            # calculate deceleration:
            if dist <= 100:
                deceleration = c.decelerate_SLOW
                self.__veh.me.set_color(c.RED) #<===============================--------- DEBUG --------------
            elif dist <= 250:
                deceleration = c.decelerate_NORMAL
                self.__veh.me.set_color(c.YELLOW) #<============================--------- DEBUG --------------
            else:
                deceleration = c.decelerate_FAST
                self.__veh.me.set_color(c.GREEN) #<=============================--------- DEBUG --------------
            #print(deceleration)
            # calculate the speed recquired to reach the target given the desired deceleration
            speed = dist / (deceleration * c.deceleration_tweaker)
            #print("speed:", speed)
            # make sure the velocity does not exceed the max:
            speed = min(speed, self.__veh.me.max_speed())
            print("speed after:", speed)
            # now proceed almost like in seek:
            to_target.mult(speed/dist)
            #print("to_target:", to_target.magn())
            #a = zrc.sub_vectors(to_target, self.__veh.me.velocity)
            #print("arrive_vec_magn:", a.magn())
            return zrc.sub_vectors(to_target, self.__veh.me.velocity)

        return Vector2D()


    """ Pursuit """#<-------------------------   FIX IT  ----------------------------------------------
    def pursuit(self, evader):
        # if the evader is ahead and facing the agent then we can just seek evader's current position:
        to_evader = zrc.sub_vectors(evader.me.pos, self.__veh.me.pos)
        relative_heading = self.__veh.me.heading.dot(evader.me.heading)
        # acos(0.95) = 18 degs:
        if (to_evader.dot(self.__veh.me.heading) > 0 and relative_heading < -0.95):
            return self.seek(evader.me.pos)

        # not considered ahead so we predict where the evader will be:
        # the look_ahead_time is proportional to the distance between the evader
        # and the pursuer; and is inversely proportional to the sum of the
        # agents' velocities:
        look_ahead_time = to_evader.magn() / (self.__veh.me.max_speed() + evader.me.speed())
        #look_ahead_time += self.turn_around_time(evader.me.pos)
        # seek to the predicted future position of the evader:
        return zrc.add_vectors(evader.me.pos, evader.me.velocity.mult(look_ahead_time))


    """ Calculates turn around time for Pursuit """
    def turn_around_time(self, target_pos):
        # determine the normalized vector to the target:
        to_target = zrc.sub_vectors(target_pos, self.__veh.me.pos).norm()
        dot = self.__veh.me.heading.dot(to_target)

        # the higher the max turn rate of the vehicle, the higher this value
        # should be. If the vehicle is heading in the opposite direction to its
        # target position then a value of 0.5 means that this function will
        # return a time of 1 second for the vehicle to turn around:
        coefficient = 0.5

        # the dot product gives a value of 1 if the target is directly ahead
        # and -1 if it is directly behind. Substracting 1 and multiplying by
        # the negative of the coefficient gives a positive value proportional
        # to the rotational displacement of the vehicle abd target:
        return (dot - 1.0) * -coefficient

    """ Caculate all steeering forces that worked on vehicle """
    def calculate(self):
        """ The most basic system is used - change this later! """              #< ========================= BUKA
        steering_force = Vector2D()
        # sum all steering forces together:
        if self.seek_on: steering_force.add(self.seek(self.__veh.get_target().me.pos))
        #if self.flee_on: steering_force.add(self.flee(self.__veh.get_target().me.pos))
        #if self.arrive_on: steering_force.add(self.arrive(self.__veh.get_target()))
        #if self.pursuit_on: steering_force.add(self.pursuit(self.__veh.get_target()))
        steering_force.trunc(self.__max_force)
        return steering_force
