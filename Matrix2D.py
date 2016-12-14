#!/usr/bin/python
#-*- coding: utf-8 -*-


import zrcommon as zrc
from Vector2D import Vector2D



class Matrix2D(object):
    """Class that represents 2D matrix."""
    def __init__(self):
        """Constructor."""
        self.matrix = [[0 for i in range(3)] for j in range(3)] # matrix values
        self.matrix[0][0] = self.matrix[1][1] = self.matrix[2][2] = 1


    def identity(self):
        """Create an identity matrix."""
        for x in range(len(self.matrix)):
            for y in range(len(self.matrix[x])):
                self.matrix[x][y] = 0
        self.matrix[0][0] = self.matrix[1][1] = self.matrix[2][2] = 1


    def zero(self):
        """Create an empty matrix."""
        for x in range(len(self.matrix)):
            for y in range(len(self.matrix[x])):
                self.matrix[x][y] = 0


    def mult_matrix(self, mat):
        """Multiply two matrices."""
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


    def translate(self, x, y):
        """Create a transformation matrix."""
        mat = Matrix2D()
        mat.matrix[2][0] = x
        mat.matrix[2][1] = y
        self.mult_matrix(mat)


    def rotate(self, heading, side):
        """Create a rotation matrix from a 2D vector."""
        mat = Matrix2D()
        mat.matrix[0][0] = heading.x
        mat.matrix[0][1] = heading.y
        mat.matrix[1][0] = side.x
        mat.matrix[1][1] = side.y
        self.mult_matrix(mat)


    def rotate_by_angle(self, angle):
        """Creates a rotation matrix from an angle."""
        mat = Matrix2D()
        cos_a = zrc.get_cos(angle)
        sin_a = zrc.get_sin(angle)
        mat.matrix[0][0] = cos_a
        mat.matrix[0][1] = sin_a
        mat.matrix[1][0] = -sin_a
        mat.matrix[1][1] = cos_a
        self.mult_matrix(mat)


    def transform_vector2D(self, point):
        """Applies a 2D transformation matrix to a single Vector2D.

        Returns:
            Vector2D with applied 2D matrix transformation.
        """
        x = self.matrix[0][0]*point.x + self.matrix[1][0]*point.y + self.matrix[2][0]
        y = self.matrix[0][1]*point.x + self.matrix[1][1]*point.y + self.matrix[2][1]
        return Vector2D(x, y)
