#!/usr/bin/python
#-*- coding: utf-8 -*-


import math
from Vector2D import Vector2D



""" Class that represents 2D matrix """
class Matrix2D(object):
    """ Constructor """
    def __init__(self):
        self.matrix = [[0 for i in range(3)] for j in range(3)] # matrix values
        self.matrix[0][0] = self.matrix[1][1] = self.matrix[2][2] = 1


    """ Create an identity matrix """
    def identity(self):
        for x in range(len(self.matrix)):
            for y in range(len(self.matrix[x])):
                self.matrix[x][y] = 0
        self.matrix[0][0] = self.matrix[1][1] = self.matrix[2][2] = 1


    """ Create an empty matrix """
    def zero(self):
        for x in range(len(self.matrix)):
            for y in range(len(self.matrix[x])):
                self.matrix[x][y] = 0


    """ Multiply two matrices """
    def mult_matrix(self, mat):
        temp_mat = [[0 for i in range(3)] for j in range(3)]
        # first row:
        temp_mat[0][0] = self.matrix[0][0]*mat.matrix[0][0] + self.matrix[0][1]*mat.matrix[1][0] + self.matrix[0][2]*mat.matrix[2][0]
        temp_mat[0][1] = self.matrix[0][0]*mat.matrix[0][1] + self.matrix[0][1]*mat.matrix[1][1] + self.matrix[0][2]*mat.matrix[2][1]
        temp_mat[0][2] = self.matrix[0][0]*mat.matrix[0][2] + self.matrix[0][1]*mat.matrix[1][2] + self.matrix[0][2]*mat.matrix[2][2]
        # second row:
        temp_mat[1][0] = self.matrix[1][0]*mat.matrix[0][0] + self.matrix[1][1]*mat.matrix[1][0] + self.matrix[1][2]*mat.matrix[2][0]
        temp_mat[1][1] = self.matrix[1][0]*mat.matrix[0][1] + self.matrix[1][1]*mat.matrix[1][1] + self.matrix[1][2]*mat.matrix[2][1]
        temp_mat[1][2] = self.matrix[1][0]*mat.matrix[0][2] + self.matrix[1][1]*mat.matrix[1][2] + self.matrix[1][2]*mat.matrix[2][2]
        # third row:
        temp_mat[2][0] = self.matrix[2][0]*mat.matrix[0][0] + self.matrix[2][1]*mat.matrix[1][0] + self.matrix[2][2]*mat.matrix[2][0]
        temp_mat[2][1] = self.matrix[2][0]*mat.matrix[0][1] + self.matrix[2][1]*mat.matrix[1][1] + self.matrix[2][2]*mat.matrix[2][1]
        temp_mat[2][2] = self.matrix[2][0]*mat.matrix[0][2] + self.matrix[2][1]*mat.matrix[1][2] + self.matrix[2][2]*mat.matrix[2][2]
        self.matrix = temp_mat


    """ Create a transformation matrix """
    def translate(self, x, y):
        mat = Matrix2D()
        mat.matrix[2][0] = x
        mat.matrix[2][1] = y
        self.mult_matrix(mat)


    """ Create a rotation matrix from a 2D vector"""
    def rotate(self, heading, v_side):
        mat = Matrix2D()
        mat.matrix[0][0] = heading.x
        mat.matrix[0][1] = heading.y
        mat.matrix[1][0] = v_side.x
        mat.matrix[1][1] = v_side.y
        self.mult_matrix(mat)


    """ Applies a 2D transformation matrix to a single Vector2D """
    def transform_vector2D(self, point):
        x = self.matrix[0][0]*point.x + self.matrix[1][0]*point.y + self.matrix[2][0]
        y = self.matrix[0][1]*point.x + self.matrix[1][1]*point.y + self.matrix[2][1]
        return Vector2D(x, y)
