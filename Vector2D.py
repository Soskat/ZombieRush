#!/usr/bin/python
#-*- coding: utf-8 -*-


import math



class Vector2D:
    """Class that represents 2D vector."""
    def __init__(self, x=0, y=0):
        """Constructor.

        Keyword args:
            param1 (float): X coordinate (default 0)
            param2 (float): Y coordinate (default 0)
        """
        self.x = x      # x vector component
        self.y = y      # y vector component


    def add(self, v):
        """Adds vector v to yourself."""
        self.x += v.x
        self.y += v.y


    def add_copy(self, v):
        """Returns a sum of copy of self and given vector."""
        return Vector2D(self.x + v.x, self.y + v.y)


    def sub(self, v):
        """Substracts vector v from yourself and returns that vector."""
        self.x -= v.x
        self.y -= v.y
        return self


    def sub_copy(self, v):
        """Returns a difference of copy of self and given vector."""
        return Vector2D(self.x - v.x, self.y - v.y)


    def mult(self, a):
        """Multiplies vector by given number and returns self handler."""
        self.x *= a
        self.y *= a
        return self


    def mult_copy(self, a):
        """Returns a copy of self multiplied by a."""
        return Vector2D(self.x * a, self.y * a)


    def magn(self):
        """Gets vector magnitude (length)."""
        return math.sqrt(math.pow(self.x, 2) + math.pow(self.y, 2))


    def norm(self):
        """Returns normalized vector."""
        vmag = self.magn()
        return Vector2D(self.x / vmag, self.y / vmag)


    def perp(self):
        """Gets vector perpendicular to yourself."""
        return Vector2D(self.y, -self.x)


    def trunc(self, max_length):
        """Truncates vector length."""
        vmag = self.magn()
        if vmag > max_length:
            ratio = max_length/vmag
            self.x *= ratio
            self.y *= ratio


    def dot(self, v):
        """Returns dot product with given vector."""
        return self.x * v.x + self.y * v.y


    def dist_to_vector(self, v):
        """Returns distance to vector."""
        return math.sqrt(math.pow(self.x - v.x, 2) + math.pow(self.y - v.y, 2))


    def reverse(self):
        """Reverses vector."""
        self.x *= -1
        self.y *= -1


    def reset(self):
        """Resets vector values to zero."""
        self.x = 0
        self.y = 0
