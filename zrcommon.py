#!/usr/bin/python
#-*- coding: utf-8 -*-

import math
import random


""" Gets random int value from range <min, max) """
def get_randint(minimum, maximum):
    return random.randint(minimum, maximum - 1)


""" Checks if given object collide with each other.
    Arguments ob1 and ob2 are touples of (x,y,radius) """
def check_collision(ob1, ob2):
    s1 = math.pow(ob1[0] - ob2[0], 2)
    s2 = math.pow(ob1[1] - ob2[1], 2)
    if math.sqrt(s1 + s2) < ob1[2] + ob2[2]:
        return True
    else:
        return False


""" Checks if given object collide with each other.
    If yes, recalculate given position to avoid collision.
    Arguments ob1 and ob2 are touples of (x,y,radius) """
def avoid_collision(ob1, ob2):
    dx = ob1[0] - ob2[0]
    dy = ob1[1] - ob2[1]
    d = math.sqrt(math.pow(dx, 2) + math.pow(dy, 2))
    D = ob1[2] + ob2[2]
    if d < D:
        # ob1 and ob2 collide - move ob2 to avoid callision:
        x = dx * (D - d) / d
        y = dy * (D - d) / d
        return ob2[0] - x, ob2[1] - y
    else:
        return ob2[0], ob2[1]


""" Calculates player's triangle rotation based on his heading in current position """
def calculate_player_rotation(origin_vertices, position, heading):
    x = y = 0
    cos_h = math.cos(heading)
    sin_h = math.sin(heading)
    newV = [[0 for y in range(2)] for x in range(len(origin_vertices))]
    for i in range(0, len(origin_vertices)):
        x = origin_vertices[i][0] * cos_h - origin_vertices[i][1] * sin_h
        y = origin_vertices[i][0] * sin_h + origin_vertices[i][1] * cos_h
        newV[i][0] = x + position[0]
        newV[i][1] = y + position[1]
    return newV


""" Calculate player's new position in his heading direction """
def calculate_player_position(position, heading, step):
    x = position[0] - step * math.sin(heading)
    y = position[1] + step * math.cos(heading)
    return x, y



""" ===== Vector operations ===== """

""" Substract vector v from vector u """
def sub_v(u, v):
    return [ u[i]-v[i] for i in range(len(u)) ]

""" Calculate vector magnitude """
def v_magn(v):
    return math.sqrt( sum(v[i]*v[i] for i in range(len(v))) )

""" Normalize vector """
def norm_v(v):
    vmag = v_magn(v)
    return [ v[i]/vmag  for i in range(len(v)) ]

""" Truncate vector length """
def truncate_v(v, max_lenght):
    if v_magn(v) > max_lenght:
        
