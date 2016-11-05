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
# FSM zombie colors
Z_ATTACK = (166, 0, 0)
Z_FLEE = (0, 255, 238)
Z_HIDDEN = (0, 130, 0)
Z_TAKE_RISK = (0, 180, 238)
##########################
### game constants
##########################
# player related constants
player_color = YELLOW
player_radius = 10
player_mass = 2
player_max_speed = 5.0
player_max_force = 5.0
player_max_turn_rate = 0.2
# zombie related constants
zombie_amount = 100
current_zombie_amount = 1
zombie_color = GREEN
zombie_radius = 8
zombie_mass = 2
zombie_max_speed = 5.0
zombie_max_force = 5.0
zombie_max_turn_rate = 0.2
# steering behaviours constants:
time_elapsed = 0.5
panic_distance = 100
deceleration_tweaker = 0.3
decelerate_SLOW = 3.0
decelerate_NORMAL = 2.0
decelerate_FAST = 1.0
wandern_radius = 50
wandern_distance = 50
wandern_jitter = 80.0
# finite state mashine states:
state_IDLE = 0
state_FLEE = 1
state_HIDDEN = 2
state_TAKE_RISK = 3
state_ATTACK = 4
# other constants
obstacle_color = GREY
obstacles_amount = 0#10
