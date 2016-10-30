#!/usr/bin/python
#-*- coding: utf-8 -*-

import random
import zrcommon as zrc
import constants as c
from Zombie import Zombie



""" Class that coordinate zombie bots in game """
class ZombiePool:
    """ Constructor """
    def __init__(self, game_display, display_size, player, level):
        self.__screen = game_display                    # game display handler
        self.__level = level                            # Level handler
        self.__player = player                          # Player handler
        self.__time_elapsed = c.time_elapsed            # time elapsed
        self.__zombie_amount = c.zombie_amount          # finite bots amount
        self.__curr_zombie_am = c.current_zombie_amount # current active bots amount
        self.__color = c.zombie_color                   # zombies' color
        self.__radius = c.zombie_radius                 # zombies' radius
        # calculate game world borders:
        max_x = display_size[0] - self.__radius
        max_y = display_size[1] - self.__radius
        min_x = min_y = self.__radius
        self.__borders = (min_x, max_x, min_y, max_y)   # game world borders
        self.__zombies = []                             # list of zombie bots
        # make some zombies:
        while len(self.__zombies) < self.__curr_zombie_am:
            self.__add_new_zombie()


    """ Adds new zombie bot to the zombie pool """
    def __add_new_zombie(self):
        can_add = True
        x = y = 0
        c_x, c_y, c_r = self.__player.get_player_info()
        while True:
            can_add = True
            x = zrc.get_randint(self.__borders[0], self.__borders[1])
            y = zrc.get_randint(self.__borders[2], self.__borders[3])
            # check if (x,y) is in player's start area:
            if (zrc.check_collision((c_x,c_y,c_r), (x,y,self.__radius))):
                continue # random all values again
            # check if new zombie may intersect with any obstacles:
            if not self.__level.is_not_collided_with_obstacles(int(x/100),
                                                               int(y/100),
                                                               (x,y,self.__radius)):
                continue
            # check if new zombie may intersect with other zombies:
            for z in self.__zombies:
                if zrc.check_collision((z.pos.x, z.pos.y, z.radius), (x,y,self.__radius)):
                    can_add = False
                    break
            # add new zombie to list:
            if can_add:
                self.__zombies.append(Zombie(screen = self.__screen,
                                             level = self.__level,
                                             level_borders = self.__borders,
                                             player = self.__player,
                                             time_elapsed = self.__time_elapsed,
                                             ID = len(self.__zombies),
                                             pos = (x,y),
                                             radius = self.__radius,
                                             mass = 2,
                                             max_velocity = 2.0,
                                             max_force = 5.0,
                                             max_turn_rate = 5.0,
                                             color = self.__color))
                return


    """ Draws all zombie bots """
    def draw(self):
        for z in self.__zombies:
            z.draw()

    """ DEBUG DRAW MODE """
    def draw_debug(self):
        for z in self.__zombies:
            z.draw_debug()


    """ Moves all zombie bots """
    def move(self):
        for z in self.__zombies:
            z.move()
