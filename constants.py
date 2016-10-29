#!/usr/bin/python
#-*- coding: utf-8 -*-

##########################
### colors
##########################
YELLOW = (255, 255, 0)  # player color
BLACK = (0, 0, 0)       # background color
GREY = (120, 120, 120)  # obstacle color
GREEN = (0, 255, 0)     # zombie color
# debug colors:
BLUE = (0, 0, 255)
RED = (255, 0, 0)
ORANGE = (255, 149, 0)

##########################
### game constants
##########################
# player related constants
player_step = 3
player_angle = 0.2
# zombie related constants
zombie_amount = 100
current_zombie_amount = 10
# other constants
obstacles_amount = 10
panic_distance = 100
time_elapsed = 0.5
