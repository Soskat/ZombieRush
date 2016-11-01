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
DARKYELLOW = (232, 178, 0)
##########################
### game constants
##########################
# player related constants
player_step = 4
player_angle = 0.2
player_color = YELLOW
player_radius = 10
player_mass = 2
player_max_speed = 4.0
player_max_force = 5.0
player_max_turn_rate = 0.2
# zombie related constants
zombie_amount = 100
current_zombie_amount = 1
zombie_color = GREEN
zombie_radius = 8
zombie_mass = 2
zombie_max_speed = 3.0
zombie_max_force = 5.0
zombie_max_turn_rate = 0.2
# steering behaviours constants:
time_elapsed = 0.5
panic_distance = 100
deceleration_tweaker = 0.3
# other constants
obstacle_color = GREY
obstacles_amount = 0#10
