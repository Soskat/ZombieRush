#!/usr/bin/python
#-*- coding: utf-8 -*-

import math
import random
from Vector2D import Vector2D
from Matrix2D import Matrix2D



################################################################################
# MATHEMATICAL CONSTANTS
################################################################################
pi = math.pi
two_pi = 2 * math.pi
half_pi = math.pi / 2.0
################################################################################
# MATH WRAPPERS
################################################################################
""" Gets random int value from range <min, max) """
def get_randint(minimum, maximum):
    return random.randint(minimum, maximum - 1)


""" Gets random float value from range <0.0, 1.0) """
def get_randfloat():
    return random.random()


""" Gets random float value from range (-1.0, 1.0) """
def get_randclamped():
    return random.random() - random.random()


""" Gets cosinus of theta angle """
def get_cos(theta):
    return math.cos(theta)


""" Gets sinus of theta angle """
def get_sin(theta):
    return math.sin(theta)


""" Gets sqrt of given value """
def get_sqrt(val):
    return math.sqrt(val)
################################################################################
# FUNCTIONS
################################################################################
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


""" Calculate vector rotation """
def rotate_vector(vec, angle):
    cos_h = math.cos(angle)
    sin_h = math.sin(angle)
    x = vec.x * cos_h - vec.y * sin_h
    y = vec.x * sin_h + vec.y * cos_h
    return Vector2D(x,y)


#####################################################################################################################
### REFACTOR NEEDED BELOW ----> add this method to Vector2D class
#####################################################################################################################
""" Scales vector magnitude by given number """
def scale_vector(v, a):
    magn = v.magn()
    return Vector2D(v.x * a/magn, v.y * a/magn)


""" Projects vector W on vector V """
def proj_vector(w, v):
    dot_prod = v.dot(w)
    vmagn = v.magn()
    proj_lenght = dot_prod / vmagn
    return v.mult_copy(proj_lenght / vmagn)


""" Rotates a vector around the origin by given angle in rads"""
def rotate_vector_around_origin(vec, angle):
    mat = Matrix2D()
    mat.rotate_by_angle(angle)
    return mat.transform_vector2D(vec)


""" Transforms a point from the agent's local space into world space """
def point_to_world_space(point, a_heading, a_side, a_pos):
    mat = Matrix2D()
    # rotate:
    mat.rotate(a_heading, a_side)
    # translate:
    mat.translate(a_pos.x, a_pos.y)
    # transform the vertices:
    return mat.transform_vector2D(point)


""" Transforms a vector from the agent's local space into world space """
def vector_to_world_space(vec, a_heading, a_side):
    mat = Matrix2D()
    # rotate:
    mat.rotate(a_heading, a_side)
    # transform the vertices:
    return mat.transform_vector2D(vec)


""" Transforms a point from world space into the agent's local space """
def point_to_local_space(point, a_heading, a_side, a_pos):
    mat = Matrix2D()
    t_x = -a_pos.dot(a_heading)
    t_y = -a_pos.dot(a_side)
    # create the transformation matrix:
    mat.matrix[0][0] = a_heading.x
    mat.matrix[0][1] = a_side.x
    mat.matrix[1][0] = a_heading.y
    mat.matrix[1][1] = a_side.y
    mat.matrix[2][0] = t_x
    mat.matrix[2][1] = t_y
    # transform the vertices:
    return mat.transform_vector2D(point)
