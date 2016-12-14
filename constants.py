#!/usr/bin/python
#-*- coding: utf-8 -*-

from math import sqrt
##########################
### colors
##########################
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (120, 120, 120)
LIGHTGREY = (212, 212, 212)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
RAGERED = (190, 0, 0)
ORANGE = (255, 149, 0)
DARKYELLOW = (232, 178, 0)
CYAN = (0, 255, 255)
# FSM zombie colors
color_ratio = int(255 / 50)
##########################
### game constants
##########################
game_width = 800
game_height = 600
world_margin = 20
text_margin = 10
FPS = 30
font_size = 36
big_font_size = 42
font_path = "fonts/coders_crux/coders_crux.ttf"
max_ip_dist = max(game_width, game_height) * 2.0
# player related constants
player_color = YELLOW
player_radius = 10
player_mass = 2
player_max_speed = 5.0
player_max_force = 5.0
player_max_turn_rate = 0.1
player_max_health = 100
player_half_health = player_max_health / 2
# death ray related constants:
ray_length = sqrt(game_width*game_width + game_height*game_height)
ray_time = int(FPS / 3)
ray_READY = 0
ray_SHOOT = 1
ray_COOLDOWN = 2
# distances related constants:
panic_distance = 100
safe_distane = panic_distance * 2.5
rage_neighbour_distance = 50
contact_distance = 20
# zombie stats related constants
max_zombie_amount = 100
zombie_amount = 10
zombie_color = GREEN
zombie_radius = 8
zombie_radius_obst_avoid = 3 * zombie_radius
zombie_mass = 2
zombie_max_speed = 5.0
zombie_max_force = 5.0
zombie_max_turn_rate = 0.2
ppz = 10                    # Points Per Zombie
zombie_damage = 5           # damage causet by zombie
# steering behaviours constants:
time_elapsed = 0.5
fov_multiplier = 0.3
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
# steering behaviours base weights (normalized):
w_obstacle_avoidance = 1.0
w_wall_avoidance = 1.0
w_separation = 1.0
w_wandern = 0.2
w_hide = 0.2
w_seek = 0.2
# other constants
obstacle_color = GREY
obstacles_amount = 10
obstacle_min_radius = 35
obstacle_max_radius = 45
