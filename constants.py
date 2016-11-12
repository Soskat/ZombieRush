#!/usr/bin/python
#-*- coding: utf-8 -*-

##########################
### colors
##########################
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
GREY = (120, 120, 120)
LIGHTGREY = (212, 212, 212)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
ORANGE = (255, 149, 0)
DARKYELLOW = (232, 178, 0)
CYAN = (0, 255, 255)
# FSM zombie colors
Z_ATTACK = (166, 0, 0)
Z_RUN = (0, 255, 238)
Z_HIDDEN = (0, 100, 0)
##########################
### game constants
##########################
game_width = 800
game_height = 600
max_ip_dist = max(game_width, game_height) * 2.0
# player related constants
player_color = YELLOW
player_radius = 10
player_mass = 2
player_max_speed = 5.0
player_max_force = 5.0
player_max_turn_rate = 0.2
# zombie stats related constants
zombie_amount = 100
current_zombie_amount = 10
zombie_color = GREEN
zombie_radius = 8
zombie_mass = 2
zombie_max_speed = 5.0
zombie_max_force = 5.0
zombie_max_turn_rate = 0.2
# steering behaviours constants:
time_elapsed = 0.5
panic_distance = 100
safe_distane = panic_distance * 2.5
min_detection_box_length = 40.0
wall_detection_feeler_length = 40.0
# deceleration:
deceleration_tweaker = 0.3
decelerate_SLOW = 3.0
decelerate_NORMAL = 2.0
decelerate_FAST = 1.0
# wandern:
wandern_radius = 60
wandern_distance = 70
wandern_jitter = 90.0
# finite state mashine states:
state_IDLE = 0
state_RUN = 1
state_HIDDEN = 2
state_ATTACK = 3
# steering behaviours base weights:
w_obstacle_avoidance = 1.2
w_wall_avoidance = 1.2
w_wandern = 0.5
w_hide = 0.5
w_zero = 0.0
# other constants
obstacle_color = GREY
obstacles_amount = 10
