#!/usr/bin/python
#-*- coding: utf-8 -*-

import zrcommon as zrc



""" Class that represents 2D wall in game world """
class Wall:
    """ Constructor """
    def __init__(self, a, b):
        self.__a = a
        self.__b = b
        self.__n = self.calculate_normal()

    """ Calculates normal vector """
    def calculate_normal(self):
        temp = zrc.sub_vectors(a, b).norm()
        return Vector2D(-temp.y, temp.x)
