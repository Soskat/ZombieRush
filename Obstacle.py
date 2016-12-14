#!/usr/bin/python
#-*- coding: utf-8 -*-

import pygame
import zrcommon
from Vector2D import Vector2D



class Obstacle:
    """Class that represents an obstacle."""
    def __init__(self, game_display, center, radius, color):
        """Constructor.

        Args:
            param1 (pygame.Surface): game display handler
            param2 ((int, int)): center of game world coordinates in form of a touple (x, y)
            param3 (int): obstacle's radius
            param4 ((int, int, int)): obstacle's color in form of a touple (r, g, b)
        """
        self.__screen = game_display
        self.center = Vector2D(center[0], center[1])
        self.radius = radius
        self.__color = color


    def draw(self):
        """Draws Obstacle."""
        pygame.draw.circle(self.__screen,
                           self.__color,
                           (self.center.x, self.center.y),
                           self.radius,
                           1
                          )


    def is_collided(self, ob):
        """Checks if Obstacle collides with given object.

        Args:
            param ((int, int, int)): object info used in collision detection in form of a touple (x, y, radius)

        Returns:
            True if collision occured. False otherwise.
        """
        return zrcommon.check_collision((self.center.x, self.center.y, self.radius), ob)


    def avoid_collision(self, ob):
        """Checks if Obstacle collides with given object.
        If yes, recalculate position of given object to avoid collision.

        Args:
            param ((int, int, int)): object info used in collision detection in form of a touple (x, y, radius)

        Returns:
            True if collision occured. False otherwise.
        """
        return zrcommon.avoid_collision((self.center.x, self.center.y, self.radius), ob)
