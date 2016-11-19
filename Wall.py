#!/usr/bin/python
#-*- coding: utf-8 -*-

import zrcommon as zrc
from Vector2D import Vector2D



""" Class that represents 2D wall in game world """
class Wall:
    """ Constructor """
    def __init__(self, a, b):
        self.__a = a
        self.__b = b
        self.__n = self.calculate_normal()


    """ Calculates normal vector """
    def calculate_normal(self):
        temp = self.__a.sub_copy(self.__b).norm()
        return Vector2D(-temp.y, temp.x)


    """ Returns the start point of the wall """
    def start_point(self):
        return self.__a


    """ Returns the end point of the wall """
    def end_point(self):
        return self.__b


    """ Returns the normal vector of the wall """
    def normal_v(self):
        return self.__n
