#!/usr/bin/python
#-*- coding: utf-8 -*-

import math
import random


################################################################################
# FUNCTIONS
################################################################################

""" Gets random int value from range <min, max) """
def get_randint(minimum, maximum):
    return random.randint(minimum, maximum - 1)


""" Checks if given object collide with each other.
    Arguments ob1 and ob2 are touples of (x,y,radius) """
def check_collision(ob1, ob2):
    s1 = math.pow(ob1[0] - ob2[0], 2)
    s2 = math.pow(ob1[1] - ob2[1], 2)
    # is d < R + r
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


""" Substracts given vectors """
def sub_vectors(v, u):
    return Vector2D(v.x - u.x, v.y - u.y)


""" Multiplies vector by number """
def mult_vector(v, a):
    v.mult(a)
    return v


################################################################################
# CLASS VECTOR2D
################################################################################
""" Class that represents 2D vector """
class Vector2D:
    """ Constructor """
    def __init__(self, x=0, y=0):
        self.x = x      # x vector component
        self.y = y      # y vector component

    """ Add vector v to yourself """
    def add(self, v):
        self.x += v.x
        self.y += v.y

    """ Substract vector v from yourself """
    def sub(self, v):
        self.x -= v.x
        self.y -= v.y

    """ Multiply vector by given number """
    def mult(self, a):
        return Vector2D(self.x * a, self.y * a)

    """ Get vector magnitude """
    def magn(self):
        return math.sqrt(math.pow(self.x, 2) + math.pow(self.y, 2))

    """ Normalize vector """
    def norm(self):
        vmag = self.magn()
        return Vector2D(self.x / vmag, self.y / vmag)

    """ Get vector perpendicular to yourself """
    def perp(self):
        return Vector2D(self.y, -self.x)

    """ Truncate vector length """
    def trunc(self, max_length):
        vmag = self.magn()
        if vmag > max_length:
            ratio = max_length/vmag
            self.x *= ratio
            self.y *= ratio

    """ --- TEST --- """
    def print_v(self, name):
        print("%s: (%f, %f)" % (name, self.x, self.y))
