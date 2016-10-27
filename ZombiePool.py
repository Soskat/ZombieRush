#!/usr/bin/python
#-*- coding: utf-8 -*-

import random
import zrcommon as zrc
from Zombie import Zombie



""" Class that coordinate zombie bots in game """
class ZombiePool:
    """ Constructor """
    def __init__(self, game_display, display_size, player, time_elapsed,
                 zombie_amount, current_zombie_amout, level, zombie_color):
        self.__screen = game_display                    # game display handler
        self.__display_size = display_size              # game display size
        self.__level = level                            # Level handler
        self.__player = player                          # Player handler
        self.__time_elapsed = time_elapsed              # time elapsed
        self.__zombie_amount = zombie_amount            # finite bots amount
        self.__curr_zombie_am = current_zombie_amout    # current active bots amount
        self.__color = zombie_color                     # zombies' color
        self.__zombies = []                             # list of zombie bots
        # make some zombies:
        while len(self.__zombies) < self.__curr_zombie_am:
            self.__add_new_zombie()


    """ Adds new zombie bot to the zombie pool """
    def __add_new_zombie(self):
        can_add = True
        radius = 8
        x = y = 0
        c_x, c_y, c_r = self.__player.get_player_info()
        while True:
            can_add = True
            x = zrc.get_randint(0, self.__display_size[0])
            y = zrc.get_randint(0, self.__display_size[1])
            # check if (x,y) is outside game display or in player's start area:
            if (x + radius >= self.__display_size[0] or x - radius <= 0 or
                y + radius >= self.__display_size[1] or y - radius <= 0 or
                zrc.check_collision((c_x,c_y,c_r), (x,y,radius))):
                continue # random all values again
            # check if new zombie may intersect with any obstacles:
            if not self.__level.is_not_collided_with_obstacles(int(x/100), int(y/100), (x,y,radius)):
                continue
            # check if new zombie may intersect with other zombies:
            for z in self.__zombies:
                if zrc.check_collision((z.pos.x, z.pos.y, z.radius), (x,y,radius)):
                    can_add = False
                    break
            # add new zombie to list:
            if can_add:
                self.__zombies.append(Zombie(screen = self.__screen,
                                             level = self.__level,
                                             player = self.__player,
                                             time_elapsed = self.__time_elapsed,
                                             ID = len(self.__zombies),
                                             pos = (x,y),
                                             radius = radius,
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


    """ Moves all zombie bots """
    def move(self):
        for z in self.__zombies:
            z.move()
