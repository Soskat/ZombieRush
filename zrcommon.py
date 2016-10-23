#!/usr/bin/python
#-*- coding: utf-8 -*-

import math
import random


""" Gets random int value from range <min, max) """
def get_randint(minimum, maximum):
    return random.randint(minimum, maximum)


""" Checks if given object collide with each other. If yes, returns detailed collision info.
    Arguments ob1 and ob2 are touples of (x,y,radius) """
def check_collision_detailed(ob1, ob2):
    dx = ob1[0] - ob2[0]
    dy = ob1[1] - ob2[1]
    d = math.sqrt(math.pow(dx, 2) + math.pow(dy, 2))
    D = ob1[2] + ob2[2]
    if d < D:
        return True, (dx, dy, d, D)
    else:
        return False, None
