#!/usr/bin/python
#-*- coding: utf-8 -*-

##########################
### colors
##########################
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
GREY = (120, 120, 120)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
ORANGE = (255, 149, 0)
##########################
### game constants
##########################
# player related constants
player_step = 3
player_angle = 0.2
player_radius = 10
player_color = YELLOW
# zombie related constants
zombie_amount = 100
current_zombie_amount = 10
zombie_color = GREEN
zombie_radius = 8
zombie_mass = 2
zombie_max_velocity = 2.0
zobie_max_force = 5.0
zombie_max_turn_rate = 5.0
# other constants
obstacle_color = GREY
obstacles_amount = 10
time_elapsed = 0.5
panic_distance = 100
deceleration_tweaker = 0.3