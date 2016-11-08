#!/usr/bin/python
#-*- coding: utf-8 -*-


import math



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


    #####################################################################################################################
    ### REFACTOR NEEDED BELOW
    #####################################################################################################################
    """ Multiply vector by given number """
    def mult(self, a):
        return Vector2D(self.x * a, self.y * a)


    """ Get vector magnitude (length) """
    def magn(self):
        return math.sqrt(math.pow(self.x, 2) + math.pow(self.y, 2))


    #####################################################################################################################
    ### REFACTOR NEEDED BELOW
    #####################################################################################################################
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


    """ Returns dot product with given vector """
    def dot(self, v):
        return self.x * v.x + self.y * v.y


    """ Returns distance to vector """
    def dist_to_vector(self, v):
        return math.sqrt(math.pow(self.x - v.x, 2) + math.pow(self.y - v.y, 2))


    """ Reverses vector """
    def reverse(self):
        self.x *= -1
        self.y *= -1




    """ --- TEST --- """
    def print_v(self, name):
        print("%s: (%f, %f)" % (name, self.x, self.y))
