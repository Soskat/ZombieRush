#!/usr/bin/python
#-*- coding: utf-8 -*-


import constants as c



""" Class that manages variables and conditions relatedo to Zombie's rage mode """
class RageManager:
    """ Constructor """
    def __init__(self, display_size):
        self.rage_circle = c.rage_neighbour_distance    # rage area
        self.rage_team = 3                              # number of zombies that invoking their rage
        self.gw_space = {}                              # game world space partitioning dictionary
        for kx in range(0, int(display_size[0] / 100)):
            self.gw_space[kx] = {}
            for ky in range(0, int(display_size[1] / 100)):
                self.gw_space[kx][ky] = []
