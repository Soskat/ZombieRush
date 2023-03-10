#!/usr/bin/python
#-*- coding: utf-8 -*-

import random
import zrcommon as zrc
import constants as c
from Zombie import Zombie
from Vector2D import Vector2D
from RageManager import RageManager



class ZombiePool:
    """Class that coordinate zombie bots in game."""
    def __init__(self, game_display, display_size, player, level, font):
        """Constructor.

        Args:
            param1 (pygame.Surface): game display handler
            param2 (list): game display size
            param3 (Player): Player handler
            param4 (Level): Level handler
            param5 (pygame.forn.Font): font handler
        """
        self.__screen = game_display                    # game display handler
        self.__level = level                            # Level handler
        self.__player = player                          # Player handler
        self.__time_elapsed = c.time_elapsed            # time elapsed
        self.__zombie_amount = c.zombie_amount          # zombie amount
        self.__radius = c.zombie_radius                 # zombies' radius
        self.__zombies = []                             # list of zombie bots
        # stuff related to waves of zombies:
        self.wave = 1                                   # number of current wave of zombies
        self.__time_to_spawn = 3 * c.FPS                # time to spawn new zombies
        self.__spawn_timer = 0                          # spawn timer
        self.__font = font                              # font used for printing next wave info
        # calculate game world borders for later use:
        min_x = display_size[0] + self.__radius
        max_x = display_size[1] - self.__radius
        min_y = display_size[2] + self.__radius
        max_y = display_size[3] - self.__radius
        self.__borders = (min_x, max_x, min_y, max_y)   # game world borders
        # create RageManager object
        self.__rage_manager = RageManager((display_size[1], display_size[3]))
        # make some zombies:
        while len(self.__zombies) < self.__zombie_amount:
            self.__add_new_zombie()
        # give zombies' list handler to player:
        self.__player.set_zombie_list(self.__zombies)


    def __add_new_zombie(self):
        """Adds new zombie bot to the zombie pool."""
        can_add = True
        x = y = 0
        c_x, c_y = self.__player.me.get_position()
        c_r = self.__player.me.radius()
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
                if zrc.check_collision(
                                        (z.me.pos.x, z.me.pos.y, z.me.radius()),
                                        (x,y,self.__radius)
                                      ):
                    can_add = False
                    break
            # add new zombie to list:
            if can_add:
                self.__zombies.append(Zombie(screen = self.__screen,
                                             level = self.__level,
                                             level_borders = self.__borders,
                                             rage_manager = self.__rage_manager,
                                             player = self.__player,
                                             zombie_list = self.__zombies,
                                             ID = len(self.__zombies),
                                             pos = (x,y)
                                             ))
                return


    def move(self):
        """Moves all zombie bots."""
        # all zombies have been killed:
        if len(self.__zombies) == 0:
            # it is the time to spawn some zombies:
            if self.__spawn_timer == self.__time_to_spawn:
                # adjust zombie amount if needed:
                if self.__zombie_amount < c.max_zombie_amount:
                    self.__zombie_amount = int(self.__zombie_amount * 1.1)
                # adjust rage_team number if needed:
                if self.__zombie_amount == 15:
                    self.__rage_manager.rage_team = 5
                elif self.__zombie_amount == 30:
                    self.__rage_manager.rage_team = 7
                elif self.__zombie_amount == 75:
                    self.__rage_manager.rage_team = 10
                # add new zombies to game:
                while len(self.__zombies) < self.__zombie_amount:
                    self.__add_new_zombie()
                self.__spawn_timer = -1
            # update wave number:
            elif self.__spawn_timer == 0:
                self.wave += 1
            self.__spawn_timer += 1
        # there are zombies in games - mave them:
        else:
            for z in self.__zombies:
                if z.is_dead:
                    z.remove_from_game_world()
                    self.__zombies.remove(z)
                else:
                    z.move()


	#===========================================================================
	# All draw methods: ========================================================
    def draw(self):
        """Draws all zombie bots."""
        # show message about upcoming wave:
        if len(self.__zombies) == 0:
            info = "Get ready to wave %d!" % self.wave
            info_label = self.__font.render(info, True, c.LIGHTGREY)
            info_label_pos = info_label.get_rect()
            info_label_pos.center = self.__screen.get_rect().center
            self.__screen.blit(info_label, info_label_pos)
        # draw zombies:
        else:
            for z in self.__zombies:
                z.draw()


    def draw_debug(self):
        """Draws debug mode."""
        for z in self.__zombies:
            z.draw_debug()
