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
def get_randint(minimum, maximum):
    """Gets random int value from range <min, max)."""
    return random.randint(minimum, maximum - 1)


def get_randfloat():
    """Gets random float value from range <0.0, 1.0)."""
    return random.random()


def get_randclamped():
    """Gets random float value from range (-1.0, 1.0)."""
    return random.random() - random.random()


def get_cos(theta):
    """Gets cosinus of theta angle.

    Args:
        param (float): angle
    """
    return math.cos(theta)


def get_sin(theta):
    """Gets sinus of theta angle.

    Args:
        param (float): angle
    """
    return math.sin(theta)


def get_sqrt(val):
    """Gets sqrt of given value.

    Args:
        param (float): given value
    """
    return math.sqrt(val)
################################################################################
# FUNCTIONS
################################################################################
def check_collision(ob1, ob2):
    """Checks if given object collide with each other.

    Args:
        param1 ((int, int, int)): object #1 to check collision in form of a toulple (x,y,radius)
        param2 ((int, int, int)): object #2 to check collision in form of a toulple (x,y,radius)

    Returns:
        True if collision occurs; False otherwise
    """
    s1 = math.pow(ob1[0] - ob2[0], 2)
    s2 = math.pow(ob1[1] - ob2[1], 2)
    # if d < R + r
    if math.sqrt(s1 + s2) < ob1[2] + ob2[2]:
        return True
    else:
        return False


def avoid_collision(ob1, ob2):
    """Checks if given object collide with each other.
    If yes, recalculate given position to avoid collision.

    Args:
        param1 ((int, int, int)): object #1 to check collision in form of a toulple (x,y,radius)
        param2 ((int, int, int)): object #2 to check collision in form of a toulple (x,y,radius)

    Returns:
        A touple (int, int) of new X, Y coordinates
    """
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


def rotate_vector(vec, angle):
    """Calculates vector rotation.

    Args:
        param1 (Vector2D): vector to rotate
        param2 (float): rotation angle

    Returns:
        New Vector2D of given transformation
    """
    cos_h = math.cos(angle)
    sin_h = math.sin(angle)
    x = vec.x * cos_h - vec.y * sin_h
    y = vec.x * sin_h + vec.y * cos_h
    return Vector2D(x,y)


def scale_vector(v, a):
    """Scales vector magnitude by given number.

    Args:
        param1 (Vector2D): vector to scale
        param2 (float): scale value

    Returns:
        New Vector2D of given transformation
    """
    magn = v.magn()
    return Vector2D(v.x * a/magn, v.y * a/magn)


def proj_vector(w, v):
    """Projects vector W on vector V.

    Args:
        param1 (Vector2D): vector which is projected on another vector
        param2 (Vector2D): vector which is base for projection of another vector

    Returns:
        Vector2D of projection W on V
    """
    dot_prod = v.dot(w)
    vmagn = v.magn()
    proj_lenght = dot_prod / vmagn
    return v.mult_copy(proj_lenght / vmagn)


def rotate_vector_around_origin(vec, angle):
    """ Rotates a vector around the origin by given angle in rads.

    Args:
        param1 (Vector2D): vector to rotate
        param2 (float): angle in radians

    Returns:
        New Vector2D of given transformation
    """
    mat = Matrix2D()
    mat.rotate_by_angle(angle)
    return mat.transform_vector2D(vec)


def point_to_world_space(point, a_heading, a_side, a_pos):
    """ Transforms a point from the agent's local space into world space.

    Args:
        param1 (Vector2D): vector of transform point
        param2 (Vector2D): agent's heading vector
        param3 (Vector2D): agent's side vector
        param4 (Vector2D): agent's position vector

    Returns:
        New Vector2D of given transformation
    """
    mat = Matrix2D()
    # rotate:
    mat.rotate(a_heading, a_side)
    # translate:
    mat.translate(a_pos.x, a_pos.y)
    # transform the vertices:
    return mat.transform_vector2D(point)


def vector_to_world_space(vec, a_heading, a_side):
    """ Transforms a vector from the agent's local space into world space.

    Args:
        param1 (Vector2D): transform vector
        param2 (Vector2D): agent's heading vector
        param3 (Vector2D): agent's side vector

    Returns:
        New Vector2D of given transformation
    """
    mat = Matrix2D()
    # rotate:
    mat.rotate(a_heading, a_side)
    # transform the vertices:
    return mat.transform_vector2D(vec)


def point_to_local_space(point, a_heading, a_side, a_pos):
    """ Transforms a point from world space into the agent's local space.

    Args:
        param1 (Vector2D): vector of transform point
        param2 (Vector2D): agent's heading vector
        param3 (Vector2D): agent's side vector
        param4 (Vector2D): agent's position vector

    Returns:
        New Vector2D of given transformation
    """
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
