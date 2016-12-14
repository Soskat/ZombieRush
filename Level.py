#!/usr/bin/python
#-*- coding: utf-8 -*-

import pygame
import zrcommon as zrc
import constants as c
from Obstacle import Obstacle



class Level:
    """"Class that represents a level."""
    def __init__(self, game_display, display_size, margin):
        """ Constructor.

        Args:
            param1 (pygame.Surface): game display handler
            param2 ((int, int)): game display size in form of a touple (x, y)
            param3 (int): game world margin
        """
        self.__screen = game_display                                    # game display handler
        self.__color = c.obstacle_color                                 # obstacles' color
        self.obstacles = {}                                             # dictionary of all obstacles (for SP)
        self.__top_border_left = (0, display_size[2])                   # top left border
        self.__top_border_right = (display_size[1], display_size[2])    # top right border

        # generate obstacles:
        x = y = radius = obst = key_x = key_y = 0
        left = display_size[0] + margin
        right = display_size[1] - margin
        top = display_size[2] + margin
        bottom = display_size[3] - margin
        double_margin = 2 * margin
        c_x = display_size[1] / 2
        c_y = display_size[3] / 2
        c_r = c.player_radius
        while obst < c.obstacles_amount:
            radius = zrc.get_randint(c.obstacle_min_radius, c.obstacle_max_radius)
            x = zrc.get_randint(display_size[0], display_size[1])
            y = zrc.get_randint(display_size[2], display_size[3])
            # check if obstacle is outside game display or in player's start area:
            if (x + radius >= right or x - radius <= left or
                y + radius >= bottom or y - radius <= top or
                zrc.check_collision((c_x,c_y,c_r), (x,y,radius))):
                continue # random all values again

            key_x = int(x / 100)
            key_y = int(y / 100)
            # check if new obstacle doesn't intersect others or player area - if yes, add it to dict:
            if self.is_not_collided_with_obstacles(key_x, key_y, (x,y,radius + double_margin)):
                if not key_x in self.obstacles:
                    self.obstacles[key_x] = {}
                if not key_y in self.obstacles[key_x]:
                    self.obstacles[key_x][key_y] = []
                self.obstacles[key_x][key_y].append(Obstacle(self.__screen, (x,y), radius, self.__color))
                obst += 1


    def draw(self):
        """ Draws level. """
        # draw top border line:
        pygame.draw.line(self.__screen, self.__color, self.__top_border_left, self.__top_border_right)
        # draw obstacles:
        for key_x in self.obstacles:
            for key_y in self.obstacles[key_x]:
                for obst in self.obstacles[key_x][key_y]:
                    obst.draw()


    def is_not_collided_with_obstacles(self, key_x, key_y, obj):
        """ Checks if object collides with any obstacles.

        Args:
            param1 (int): X coordinate transformed into SP dictionary key
            param2 (int): Y coordinate transformed into SP dictionary key
            param3 ((int, int, int)): object info used in collision detection in form of a touple (x, y, radius)

        Returns:
            True if given object does not collide with other obstacles. False otherwise.
        """
        for kx in range(key_x - 1, key_x + 2):
            if kx in self.obstacles:
                for ky in range (key_y - 1, key_y + 2):
                    if ky in self.obstacles[kx]:
                        for ob in self.obstacles[kx][ky]:
                            if ob.is_collided(obj):
                                return False
        return True


    def avoid_collision_with_obstacles(self, obj):
        """Calculates new object's position so as to avoid collision with obstacles.

        Args:
            param ((int, int, int)): object info used in collision detection in form of a touple (x, y, radius)

        Returns:
            Recalculated (x, y) coordinates.
        """
        x, y, radius = obj
        key_x = int(x / 100)
        key_y = int(y / 100)
        for kx in range(key_x - 1, key_x + 2):
            if kx in self.obstacles:
                for ky in range (key_y - 1, key_y + 2):
                    if ky in self.obstacles[kx]:
                        for obst in self.obstacles[kx][ky]:
                            # recalculate position if collision occured:
                            x, y = obst.avoid_collision((x,y,radius))
        return x, y
