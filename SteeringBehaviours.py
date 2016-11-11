#!/usr/bin/python
#-*- coding: utf-8 -*-

import constants as c
import zrcommon as zrc
from Vector2D import Vector2D



""" Class that define various steering behaviours """
class SteeringBehaviours:
    """ Constructor """
    def __init__(self, vehicle, max_force):
        self.__veh = vehicle                        # vehicle handler
        self.__max_force = max_force                # max steering force value
        # stuff for the wandern behaviour:
        theta = zrc.get_randfloat() * zrc.two_pi
        self.__wandern_target = Vector2D(c.wandern_radius * zrc.get_cos(theta),
                                         c.wandern_radius * zrc.get_sin(theta))
        self.target_world = Vector2D()      # wandern target projected into world space [DEBUG]
        # flags that control use of steering behaviours:
        self.reset_flags()
        # weights of steering behaviours:
        self.obstacle_avoidance_w = c.w_obstacle_avoidance
        self.wall_avoidance_w = c.w_wall_avoidance
        self.wandern_w = c.w_wandern
        # self.seek_w = c.w_zero
        # self.flee_w = c.w_zero
        self.hide_w = c.w_zero
        # self.evade_w = c.w_zero

        self.bhs = Vector2D()


    """ Switch off all flags """
    def reset_flags(self):
        self.obstacle_avoidance_on = True
        self.wall_avoidance_on = True
        self.wandern_on = False
        # self.seek_on = False
        # self.flee_on = False
        self.hide_on = False
        # self.evade_on = False
        #self.arrive_on = False
        #self.pursuit_on = False


	#===========================================================================
	# Steering behaviours: =====================================================
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
            return Vector2D()
        desired_velocity = zrc.sub_vectors(self.__veh.me.pos, target_pos)
        desired_velocity.norm().mult(self.__veh.me.max_speed())
        return zrc.sub_vectors(desired_velocity, self.__veh.me.velocity)


    """ Wandern """
    def wandern(self):
        # first, add a small random vector to the target's position
        # RandomClamped returns a value between -1 and 1:
        self.__wandern_target.add(Vector2D(zrc.get_randclamped() * c.wandern_jitter,
                                           zrc.get_randclamped() * c.wandern_jitter))
        # reproject this new vector back onto a unit circle:
        self.__wandern_target = self.__wandern_target.norm()
        # increase the length of the vector to the same as the radius
        # of the wander circle:
        self.__wandern_target = self.__wandern_target.mult(c.wandern_radius)
        # move the target into a position wandern_distance in front of the agent:
        target_local = zrc.add_vectors(self.__wandern_target, Vector2D(c.wandern_distance, 0))
        # project the target into world space:
        self.target_world = zrc.point_to_world_space(target_local,
                                                     self.__veh.me.heading,
                                                     self.__veh.me.side,
                                                     self.__veh.me.pos)
        # and steer towards it:
        return zrc.sub_vectors(self.target_world, self.__veh.me.pos)


    """ Obstacle avoidance """
    def obstacle_avoidance(self):
        # detection box lenght is proportional to the agent's velocity
        box_length = (c.min_detection_box_length +
                     (self.__veh.me.speed() / self.__veh.me.max_speed()) *
                     c.min_detection_box_length)

        obstacles = self.__veh.get_obstacles()  # obstacles list
        CIB = None                              # Closest Intersecting Obstacle
        dist_to_closest_ip = c.max_ip_dist      # used to track the distance to the CIB
        local_pos_CIB = Vector2D()              # used to record the transformed local coords of the CIB
        # search obstacles in agent's neighbourhood:
        key_x = int(self.__veh.me.pos.x / 100)
        key_y = int(self.__veh.me.pos.y / 100)
        for kx in range(key_x - 1, key_x + 2):
            if kx in obstacles:
                for ky in range (key_y - 1, key_y + 2):
                    if ky in obstacles[kx]:
                        for obst in obstacles[kx][ky]:
                            # calculate this obstacle's position in local space:
                            local_pos = zrc.point_to_local_space(obst.center,
                                                                 self.__veh.me.heading,
                                                                 self.__veh.me.side,
                                                                 self.__veh.me.pos)
                            # if the local position has a negative x value then
                            # it must lay behind the agent (in which case it can
                            # be ignored):
                            if local_pos.x >= 0:
                                # if the distance from the x axis to the object's position
                                # is less than its radius + half the width of the detection
                                # box then there is a potential intersection:
                                expanded_radius = obst.radius + self.__veh.me.radius()
                                if abs(local_pos.y) < expanded_radius:
                                    # now to do a line/circle intersection test.
                                    # The center of the circle is represented by (c_x, c_y).
                                    # The intersection points are given by the formula
                                    # x = c_x +/-sqrt(r^2 - c_y^2) for y = 0. We only need
                                    # to look at the smallest positive value of x because
                                    # that will be the closest point of intersection:
                                    c_x = local_pos.x
                                    c_y = local_pos.y
                                    # we only need to calculate the sqrt part of the
                                    # above equation once:
                                    sqrt_part = zrc.get_sqrt(expanded_radius*expanded_radius - c_y*c_y)
                                    ip = c_x - sqrt_part
                                    if ip <= 0.0:
                                        ip = c_x + sqrt_part

                                    # test to see if this is the closest so far.
                                    # If it is keep a record of the obstacle and
                                    # its local coordinates:
                                    if ip < dist_to_closest_ip:
                                        dist_to_closest_ip = ip
                                        CIB = obst
                                        local_pos_CIB = local_pos
        # if we have found an intersecting obstacle, calculate a steering force
        # away from it:
        steering = Vector2D()
        if CIB != None:
            # the closer the agent is to an object, the stronger steering force must be:
            multiplier = 1.0 + (box_length - local_pos_CIB.x) / box_length
            # calculate the lateral force:
            steering.y = (CIB.radius - local_pos_CIB.y) * multiplier
            # apply a braking force proportional to the obstacle's distance from
            # the vehicle
            braking_weight = 0.2
            steering.x = (CIB.radius - local_pos_CIB.x) * braking_weight

        return zrc.vector_to_world_space(steering,
                                         self.__veh.me.heading,
                                         self.__veh.me.side)


    """ Wall avoidance """
    def wall_avoidance(self):
        steering = Vector2D()
        vec = zrc.add_vectors(self.__veh.me.pos,
                              zrc.mult_vector(self.__veh.me.heading,
                                              c.wall_detection_feeler_length)
                              )
        # collision from left:
        if vec.x < 0:
            steering.x = -vec.x
        # collision from right:
        elif vec.x > self.__veh.get_borders()[1]:
            steering.x = -(vec.x - self.__veh.get_borders()[1])
        # collision from top:
        if vec.y < 0:
            steering.y = -vec.y
        # collision from bottom:
        elif vec.y > self.__veh.get_borders()[3]:
            steering.y = -(vec.y - self.__veh.get_borders()[1])
        return steering.mult(5.0)


    """ Hide """
    def hide(self, hunter):
        obstacles = self.__veh.get_obstacles()  # obstacles
        dist_to_closest = c.max_ip_dist         # distance to closest obstacle
        best_hiding_spot = Vector2D()           # best hiding spot
        # search whitin nearest obstacles:
        key_x = int(self.__veh.me.pos.x / 100)
        key_y = int(self.__veh.me.pos.y / 100)
        for kx in range(key_x - 1, key_x + 2):
            if kx in obstacles:
                for ky in range (key_y - 1, key_y + 2):
                    if ky in obstacles[kx]:
                        for obst in obstacles[kx][ky]:
                            # calculate the position of the hiding spot for this obstacle:
                            hiding_spot = zrc.get_hiding_position(obst, hunter)
                            # work in distance-squared space to find the closest
                            # hiding spot to the agent:
                            dist = hiding_spot.dist_to_vector(hunter)
                            if dist < dist_to_closest:
                                dist_to_closest = dist
                                best_hiding_spot = hiding_spot
        # if no suitable obstacles found then flee the hunter:
        if dist_to_closest == c.max_ip_dist:
            self.bhs = Vector2D()
            return self.flee(hunter)
        # else use seek on the hiding spot:
        self.bhs = best_hiding_spot
        return self.seek(best_hiding_spot)


    #===========================================================================
    """ Caculate all steeering forces that worked on vehicle """
    def calculate(self):
        """ The most basic system is used - change this later! """    #< ========================= BUKA
        steering_force = Vector2D()
        # sum all steering forces together:
        if self.obstacle_avoidance_on:
            steering_force.add(self.obstacle_avoidance().mult(self.obstacle_avoidance_w))
        if self.wall_avoidance_on:
            steering_force.add(self.wall_avoidance().mult(self.wall_avoidance_w))
        if self.wandern_on:
            steering_force.add(self.wandern().mult(self.wandern_w))
        if self.hide_on:
            steering_force.add(self.hide(self.__veh.get_target().me.pos).mult(self.hide_w))
        # if self.evade_on:
        #     steering_force.add(self.evade(self.__veh.get_target().me).mult(self.evade_w))
        # if self.seek_on:
        #     steering_force.add(self.seek(self.__veh.get_target().me.pos).mult(self.seek_w))
        # if self.flee_on:
        #     steering_force.add(self.flee(self.__veh.get_target().me.pos).mult(self.flee_w))
        ##if self.arrive_on: steering_force.add(self.arrive(self.__veh.get_target()))
        #if self.pursuit_on: steering_force.add(self.pursuit(self.__veh.get_target()))

        steering_force.trunc(self.__max_force)
        return steering_force





    #-----------------   WASTELAND   -------------------------------

        # """ Arrive """#<-------------------------   FIX IT  ----------------------------------------------
        # def arrive(self, target_pos):
        #     to_target = zrc.sub_vectors(target_pos, self.__veh.me.pos)
        #     # calculate the distance to the target position:
        #     dist = to_target.magn()
        #     #print("dist:", dist)
        #     if dist > 5:
        #         # calculate deceleration:
        #         if dist <= 100:
        #             deceleration = c.decelerate_SLOW
        #             self.__veh.me.set_color(c.RED) #<===============================--------- DEBUG --------------
        #         elif dist <= 250:
        #             deceleration = c.decelerate_NORMAL
        #             self.__veh.me.set_color(c.YELLOW) #<============================--------- DEBUG --------------
        #         else:
        #             deceleration = c.decelerate_FAST
        #             self.__veh.me.set_color(c.GREEN) #<=============================--------- DEBUG --------------
        #         #print(deceleration)
        #         # calculate the speed recquired to reach the target given the desired deceleration
        #         speed = dist / (deceleration * c.deceleration_tweaker)
        #         #print("speed:", speed)
        #         # make sure the velocity does not exceed the max:
        #         speed = min(speed, self.__veh.me.max_speed())
        #         print("speed after:", speed)
        #         # now proceed almost like in seek:
        #         to_target.mult(speed/dist)
        #         #print("to_target:", to_target.magn())
        #         #a = zrc.sub_vectors(to_target, self.__veh.me.velocity)
        #         #print("arrive_vec_magn:", a.magn())
        #         return zrc.sub_vectors(to_target, self.__veh.me.velocity)
        #
        #     return Vector2D()


        # """ Pursuit """#<-------------------------   FIX IT  ----------------------------------------------
        # def pursuit(self, evader):
        #     # if the evader is ahead and facing the agent then we can just seek evader's current position:
        #     to_evader = zrc.sub_vectors(evader.me.pos, self.__veh.me.pos)
        #     relative_heading = self.__veh.me.heading.dot(evader.me.heading)
        #     # acos(0.95) = 18 degs:
        #     if (to_evader.dot(self.__veh.me.heading) > 0 and relative_heading < -0.95):
        #         return self.seek(evader.me.pos)
        #
        #     # not considered ahead so we predict where the evader will be:
        #     # the look_ahead_time is proportional to the distance between the evader
        #     # and the pursuer; and is inversely proportional to the sum of the
        #     # agents' velocities:
        #     look_ahead_time = to_evader.magn() / (self.__veh.me.max_speed() + evader.me.speed())
        #     #look_ahead_time += self.turn_around_time(evader.me.pos)
        #     # seek to the predicted future position of the evader:
        #     return zrc.add_vectors(evader.me.pos, evader.me.velocity.mult(look_ahead_time))


        # """ Evade """
        # def evade(self, pursuer):
        #     to_pursuer = zrc.sub_vectors(pursuer.pos, self.__veh.me.pos)
        #     # evade only when inside panic distance:
        #     #if to_pursuer.magn() > c.panic_distance: return Vector2D()
        #     # the look_ahead_time is proportional to the distance between the
        #     # pursuer and the evader; and is inversely proportional to the sum
        #     # of the agents' velocities:
        #     look_ahead_time = to_pursuer.magn() / (self.__veh.me.max_speed() + pursuer.speed())
        #     # now flee away from predicted future position of the pursuer:
        #     a = self.flee(zrc.add_vectors(pursuer.pos,
        #                                      pursuer.velocity.mult(look_ahead_time)))
        #     a.print_v("evade force")
        #     return self.flee(zrc.add_vectors(pursuer.pos,
        #                                      pursuer.velocity.mult(look_ahead_time)))


    # """ Calculates turn around time for Pursuit """
    # def turn_around_time(self, target_pos):
    #     # determine the normalized vector to the target:
    #     to_target = zrc.sub_vectors(target_pos, self.__veh.me.pos).norm()
    #     dot = self.__veh.me.heading.dot(to_target)
    #
    #     # the higher the max turn rate of the vehicle, the higher this value
    #     # should be. If the vehicle is heading in the opposite direction to its
    #     # target position then a value of 0.5 means that this function will
    #     # return a time of 1 second for the vehicle to turn around:
    #     coefficient = 0.5
    #
    #     # the dot product gives a value of 1 if the target is directly ahead
    #     # and -1 if it is directly behind. Substracting 1 and multiplying by
    #     # the negative of the coefficient gives a positive value proportional
    #     # to the rotational displacement of the vehicle abd target:
    #     return (dot - 1.0) * -coefficient
