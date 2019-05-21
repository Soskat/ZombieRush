#!/usr/bin/python
#-*- coding: utf-8 -*-

from Vector2D import Vector2D




class MovingEntity:
    """Class that represents a moving entity."""
    def __init__(self, position, heading, max_speed, max_force, max_turn_rate,
                       radius, mass, color):
        """Constructor.

        Args:
            param1 ((int, int)): position vector coordinates in form of a touple of (x, y)
            param2 ((int, int)): heading vector coordinates in form of a touple of (x, y)
            param3 (float): max speed
            param4 (float): max force vector magnitude
            param5 (float): max turn rate
            param6 (int): radius
            param7 (float): mass
            param8 ((int, int, int)): color in form of a touple of (r, g, b)
        """
        self.__radius = radius                                  # radius
        self.__mass = mass                                      # mass
        self.__color = color                                    # color
        self.__max_speed = max_speed                            # max speed
        self.__max_force = max_force                            # max force
        self.__max_turn_rate = max_turn_rate                    # max turn rate
        self.pos = Vector2D(position[0], position[1])           # position vector
        self.velocity = Vector2D()                              # velocity vector
        self.heading = Vector2D(heading[0], heading[1]).norm()  # heading vector
        self.side = self.heading.perp()                         # vector perpendicular to heading

    def speed(self):
        """Gets speed."""
        return self.velocity.magn()

    def max_speed(self):
        """Gets max speed."""
        return self.__max_speed

    def max_force(self):
        """Gets max force."""
        return self.__max_force

    def max_turn_rate(self):
        """Gets max turn rate."""
        return self.__max_turn_rate

    def radius(self):
        """Gets radius."""
        return self.__radius

    def mass_inv(self):
        """Gets mass used in calculations."""
        return 1.0 / self.__mass

    def color(self):
        """Gets color."""
        return self.__color

    def set_color(self, color):
        """Sets color."""
        self.__color = color

    def get_position(self):
        """Gets position coords casted to int in form of touple."""
        return (int(self.pos.x), int(self.pos.y))

    def get_collision_info(self):
        """Get collision info touple (pos.x, pos.y, radius)."""
        return (self.pos.x, self.pos.y, self.radius())
