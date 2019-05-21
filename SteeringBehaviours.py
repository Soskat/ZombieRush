#!/usr/bin/python
#-*- coding: utf-8 -*-

import constants as c
import zrcommon as zrc
from Vector2D import Vector2D




class SteeringBehaviours:
    """Class that define various steering behaviours."""
    def __init__(self, vehicle, max_force):
        """Constructor.

        Args:
            param1 (Zombie): agent handler
            param2 (float): max force vector magnitude
        """
        self.__veh = vehicle                # vehicle handler
        self.__max_force = max_force        # max steering force value
        self.CIO = None                     # Closest Intersecting Obstacle
        # stuff for the wandern behaviour:
        theta = zrc.get_randfloat() * zrc.two_pi
        self.__wandern_target = Vector2D(c.wandern_radius * zrc.get_cos(theta),
                                         c.wandern_radius * zrc.get_sin(theta))
        # flags that control use of steering behaviours:
        self.reset_flags()
        # weights of steering behaviours:
        self.obstacle_avoidance_w = c.w_obstacle_avoidance
        self.wall_avoidance_w = c.w_wall_avoidance
        self.separation_w = c.w_separation
        self.wandern_w = c.w_wandern
        self.hide_w = c.w_hide
        self.seek_w = c.w_seek
        # public vectors:
        self.bhs = Vector2D()
        self.obstacle_avoidance_force = Vector2D()
        self.wall_avoidance_force = Vector2D()
        self.separation_force = Vector2D()
        self.wandern_force = Vector2D()
        self.hide_force = Vector2D()
        self.seek_force = Vector2D()


    def reset_flags(self):
        """Switch off all flags."""
        self.obstacle_avoidance_on = True
        self.wall_avoidance_on = True
        self.separation_on = True
        self.wandern_on = False
        self.hide_on = False
        self.seek_on = False

	#===========================================================================
	# Steering behaviours: =====================================================
    def seek(self, target_pos):
        """Seek behaviour.

        Args:
            param (Vector2D): target's position vector

        Returns:
            Vector2D of seek force
        """
        desired_velocity = target_pos.sub_copy(self.__veh.me.pos)
        desired_velocity.norm().mult(self.__veh.me.max_speed())
        return desired_velocity.sub(self.__veh.me.velocity)


    def flee(self, target_pos):
        """Flee behaviour.

        Args:
            param (Vector2D): target's position vector

        Returns:
            Vector2D of flee force
        """
        # flee only when the target is inside panic_distance:
        if not zrc.check_collision(
                (self.__veh.me.pos.x, self.__veh.me.pos.y, self.__veh.me.radius()),
                (target_pos.x, target_pos.y, c.panic_distance)
                ):
            return Vector2D()
        desired_velocity = self.__veh.me.pos.sub_copy(target_pos)
        desired_velocity.norm().mult(self.__veh.me.max_speed())
        return desired_velocity.sub(self.__veh.me.velocity)


    def wandern(self):
        """Wandern behaviour.

        Returns:
            Vector2D of wandern force
        """
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
        target_local = self.__wandern_target.add_copy(Vector2D(c.wandern_distance, 0))
        # project the target into world space:
        target_world = zrc.point_to_world_space(target_local,
                                                     self.__veh.me.heading,
                                                     self.__veh.me.side,
                                                     self.__veh.me.pos)
        # and steer towards it:
        return target_world.sub_copy(self.__veh.me.pos)


    def obstacle_avoidance(self):
        """Obstacle avoidance behaviour.

        Returns:
            Vector2D of obstacle avoidance force
        """
        if self.CIO != None:
            self.CIO = None
        # detection box lenght is proportional to the agent's velocity
        box_length = (c.min_detection_box_length +
                     (self.__veh.me.speed() / self.__veh.me.max_speed()) *
                     c.min_detection_box_length)

        obstacles = self.__veh.get_obstacles()  # obstacles list
        CIO_loc = None                          # Closest Intersecting Obstacle
        dist_to_closest_ip = c.max_ip_dist      # used to track the distance to the CIO_loc
        local_pos_CIO_loc = Vector2D()          # used to record the transformed local coords of the CIO_loc
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
                                expanded_radius = obst.radius + c.zombie_radius_obst_avoid
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
                                    # If yes, keep a record of the obstacle and
                                    # its local coordinates:
                                    if ip < dist_to_closest_ip:
                                        dist_to_closest_ip = ip
                                        CIO_loc = obst
                                        local_pos_CIO_loc = local_pos
        # if we have found an intersecting obstacle, calculate a steering force
        # away from it:
        steering = Vector2D()
        if CIO_loc != None:
            # the closer the agent is to an object, the stronger steering force must be:
            multiplier = 1.0 + (box_length - local_pos_CIO_loc.x) / box_length
            # calculate the lateral force:
            steering.y = (CIO_loc.radius - local_pos_CIO_loc.y) * multiplier
            # apply a braking force proportional to the obstacle's distance from
            # the vehicle
            braking_weight = 0.2
            steering.x = (CIO_loc.radius - local_pos_CIO_loc.x) * braking_weight

            self.CIO = CIO_loc

        return zrc.vector_to_world_space(steering,
                                         self.__veh.me.heading,
                                         self.__veh.me.side)


    def wall_avoidance(self):
        """Wall avoidance behaviour.

        Returns:
            Vector2D of wall avoidance force
        """
        steering = Vector2D()
        vec = self.__veh.me.pos.add_copy(
                                self.__veh.me.heading.mult_copy(
                                                      c.wall_detection_feeler_length)
                                        )
        # collision from left:
        if vec.x < self.__veh.get_borders()[0]:
            steering.x = -vec.x
        # collision from right:
        elif vec.x > self.__veh.get_borders()[1]:
            steering.x = -(vec.x - self.__veh.get_borders()[1])
        # collision from top:
        if vec.y < self.__veh.get_borders()[2]:
            steering.y = self.__veh.get_borders()[2] - vec.y
        # collision from bottom:
        elif vec.y > self.__veh.get_borders()[3]:
            steering.y = -(vec.y - self.__veh.get_borders()[3])
        return steering.mult(5.0)


    def hide(self, hunter):
        """Hide behaviour.

        Args:
            param (Vector2D): hunter handler

        Returns:
            Vector2D of hide force
        """
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
                            hiding_spot = self.get_hiding_position(obst, hunter.pos)
                            # work in distance-squared space to find the closest
                            # hiding spot to the agent:
                            dist = hiding_spot.dist_to_vector(hunter.pos)
                            # if zombie is in FOV of player and hiding_spot is behind player
                            # reject this hiding spot:
                            zombie_dot_hunter = hunter.heading.dot(self.__veh.me.heading)
                            hiding_spot_dot_hunter = hunter.heading.dot(hunter.heading.sub_copy(hiding_spot))
                            if (zombie_dot_hunter > c.fov_multiplier and
                                hiding_spot_dot_hunter < -c.fov_multiplier):
                                continue
                            # if nearer hiding spot was found:
                            if dist < dist_to_closest:
                                dist_to_closest = dist
                                best_hiding_spot = hiding_spot
        # if no suitable obstacles found then flee the hunter:
        if dist_to_closest == c.max_ip_dist:
            self.bhs = Vector2D()
            return self.flee(hunter.pos)
        # else use seek on the hiding spot:
        self.bhs = best_hiding_spot
        return self.seek(best_hiding_spot)


    def separation(self):
        """Separation avoidance behaviour.

        Returns:
            Vector2D of separation avoidance force
        """
        steering_force = Vector2D()
        for z in self.__veh.zombie_mates:
            to_agent = self.__veh.me.pos.sub_copy(z.me.pos)
            # scale the force inversely proportional to the zombie's distance
            # from it's neighbour:
            steering_force.add(to_agent.norm().mult(1 / to_agent.magn()))
        return steering_force


    #===========================================================================
    def get_hiding_position(self, obstacle, hunter):
        """Gets most appealing hiding spot for given obstacle and hunter position.

        Args:
            param1 (Obstacle): obstacle for which we try to find best hiding spot
            param2 (Vector2D): hunter's position vector

        Returns:
            Vector2D of hiding position
        """
        # calculate how far away the agent is to be from the choosen obstacle's
        # bounding radius:
        dist_from_boundary = 30.0
        dist_away = obstacle.radius + dist_from_boundary
        # calculate the heading toward the object from the hunter:
        to_obj = obstacle.center.sub_copy(hunter).norm()
        # scale it to size and add to the obstacle position to get the hiding spot:
        # return zrc.add_vectors(obstacle.center, to_obj.mult(dist_away))
        return obstacle.center.add_copy(to_obj.mult(dist_away))


    def calculate(self):
        """Caculate all steeering forces that worked on vehicle."""
        steering_force = Vector2D()
        # sum all steering forces together: ====================================
        # obstacle avoidance:
        if self.obstacle_avoidance_on:
            self.obstacle_avoidance_force = self.obstacle_avoidance().mult(self.obstacle_avoidance_w)
            steering_force.add(self.obstacle_avoidance_force)
        # wall avoidance:
        if self.wall_avoidance_on:
            self.wall_avoidance_force = self.wall_avoidance().mult(self.wall_avoidance_w)
            steering_force.add(self.wall_avoidance_force)
        # separation:
        if self.separation_on:
            self.separation_force = self.separation().mult(self.separation_w)
            steering_force.add(self.separation_force)
        # wander:
        if self.wandern_on:
            self.wandern_force = self.wandern().mult(self.wandern_w)
            steering_force.add(self.wandern_force)
        # hide:
        if self.hide_on:
            self.hide_force = self.hide(self.__veh.get_player().me).mult(self.hide_w)
            steering_force.add(self.hide_force)
        # seek:
        if self.seek_on:
            self.seek_force = self.seek(self.__veh.get_player().me.pos).mult(self.seek_w)
            steering_force.add(self.seek_force)

        # truncate steering_force to the maximum force value: ==================
        steering_force.trunc(self.__max_force)
        return steering_force
