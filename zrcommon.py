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
def calculate_player_rotation(originV, position, heading):
    x = y = 0
    cosH = math.cos(heading)
    sinH = math.sin(heading)
    newV = [[0 for y in range(2)] for x in range(len(originV))]
    for i in range(0, len(originV)):
        x = originV[i][0] * cosH - originV[i][1] * sinH
        y = originV[i][0] * sinH + originV[i][1] * cosH
        newV[i][0] = x + position[0]
        newV[i][1] = y + position[1]
    return newV


""" Calculate player's new position in his heading direction """
def calculate_player_position(position, heading, step):
    x = position[0] - step * math.sin(heading)
    y = position[1] + step * math.cos(heading)
    return x, y
