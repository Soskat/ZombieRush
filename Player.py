#!/usr/bin/python
#-*- coding: utf-8 -*-

import pygame
import zrcommon



""" Class that represents Player """
class Player:
	""" Constructor """
	def __init__(self, game_display, display_size, color, level):
		self.__screen = game_display				# game display handler
		self.__color = color					# Player's color
		self.__level = level					# level handler
		self.__origin_vertices = [(-8,10), (0,-10), (8,10)]	# origin vertices
		self.__pos_x = 400		# X position
		self.__pos_y = 300		# Y position
		self.__heading = 0		# heading in degrees from UP direction to right
		self.__radius = 10		# Player's radius used in collision detection
		self.__max_x = display_size[0] - self.__radius	# game world border
		self.__max_y = display_size[1] - self.__radius	# game world border
		self.__min_x = self.__min_y = self.__radius		# game world borders


	""" Draws Player """
	def draw(self):
		pygame.draw.polygon(self.__screen, self.__color,
							zrcommon.calculate_player_rotation(self.__origin_vertices,
															   (self.__pos_x, self.__pos_y),
															   self.__heading),
							1)


	""" Turns Player around - changes Player's heading """
	def turn(self, angle):
		self.__heading += angle


	""" Move Player in his heading direction """
	def move(self, step):
		x, y = zrcommon.calculate_player_position((self.__pos_x, self.__pos_y),
												  self.__heading,
												  step)
		# check collisions with math borders:
		if x < self.__min_x:	x = self.__min_x
		elif x > self.__max_x: x = self.__max_x
		if y < self.__min_y:	y = self.__min_y
		elif y > self.__max_y: y = self.__max_y
		# check collisions with obstacles:
		x, y = self.__level.avoid_collision_with_obstacles((x,y,self.__radius))
		# move Player:
		self.__pos_x, self.__pos_y = x, y


	""" Gets Player's current position """
	def get_position_info(self):
		return (self.__pos_x, self.__pos_y, self.__radius)
