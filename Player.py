#!/usr/bin/python
#-*- coding: utf-8 -*-

import pygame
import constants as c
import zrcommon as zrc
from Vector2D import Vector2D
from MovingEntity import MovingEntity



""" Class that represents Player """
class Player:
	""" Constructor """
	def __init__(self, game_display, display_size, level):
		self.__screen = game_display		# game display handler
		self.__color = c.player_color		# Player's color
		self.__level = level				# level handler
		self.__zombies = None				# List of active zombies - initialized in ZombiePool
		self.__y_size = 10					# half of player's height
		self.__x_size = 8					# half of player's width
		self.me = MovingEntity( position = (int(display_size[0]/2), int(display_size[0]/ 2)),
                                heading = (0,-1),
                                max_speed = c.player_max_speed,
                                max_force = c.player_max_force,
                                max_turn_rate = c.player_max_turn_rate,
                                radius = c.player_radius,
                                mass = c.player_mass,
                                color = c.player_color
                               )
		self.__max_x = display_size[0] - self.me.radius()	# game world border
		self.__max_y = display_size[1] - self.me.radius()	# game world border
		self.__min_x = self.__min_y = self.me.radius()		# game world borders


	""" Sets zombie list handler """
	def set_zombie_list(self, list_handler):
		self.__zombies = list_handler


	""" Detects possible collisions of object with all active zombies.
		If collision occurs, recalculates object's position to avoid collision """
	def avoid_collision_with_zombies(self, obj):
		x, y, radius = obj
		if self.__zombies == None:
			return x, y
		for z in self.__zombies:
			x, y = z.avoid_collision((x, y, radius))
		return x, y


	""" Rotates player representation (triangle) """
	def rotate_player(self):
		a = zrc.scale_vector(self.me.heading, self.__y_size)
		b = zrc.scale_vector(self.me.v_side, self.__x_size)
		newV = [
			[a.x, a.y],
			[b.x - a.x, b.y - a.y],
			[-b.x - a.x, -b.y - a.y]
		]
		for nv in newV:
			nv[0] += self.me.pos.x
			nv[1] += self.me.pos.y
		return newV


	""" Turns Player around - changes Player's heading """
	def turn(self, turn_right):
		if turn_right:
			angle = self.me.max_turn_rate()
		else:
			angle = -1 * self.me.max_turn_rate()
		self.me.heading = zrc.rotate_vector(self.me.heading, angle).norm()
		self.me.v_side = self.me.heading.perp()


	""" Move Player in his heading direction """
	def move(self, move_forward):
		a = zrc.scale_vector(self.me.heading, self.me.max_speed())
		if move_forward:
			x = self.me.pos.x + a.x
			y = self.me.pos.y + a.y
		else:
			x = self.me.pos.x - a.x
			y = self.me.pos.y - a.y
		# check collisions with game world borders:
		if x < self.__min_x:	x = self.__min_x
		elif x > self.__max_x: 	x = self.__max_x
		if y < self.__min_y:	y = self.__min_y
		elif y > self.__max_y: 	y = self.__max_y
		# check collisions with obstacles:
		x, y = self.__level.avoid_collision_with_obstacles((x,y,self.me.radius()))
		# check collisions with zombies:
		x, y = self.avoid_collision_with_zombies((x,y,self.me.radius()))
		# move Player:
		self.me.pos.x, self.me.pos.y = x, y


	#===========================================================================
	# All draw methods: ========================================================
	""" Draws Player """
	def draw(self):
		pygame.draw.polygon(self.__screen,
							self.me.color(),
							self.rotate_player(),
							1
							)


	""" DEBUG DRAW MODE """
	def draw_debug(self):
		pygame.draw.circle(self.__screen,
						   c.ORANGE,
						   self.me.get_position(),
						   c.panic_distance,
						   1
						   )


	""" Debug - draw vectors """
	def draw_vectors(self):
		# draw heading vector:
		a = zrc.add_vectors(self.me.pos, zrc.mult_vector(self.me.heading, 50))
		pygame.draw.line(self.__screen,
						 c.ORANGE,
						 (self.me.pos.x, self.me.pos.y),
						 (a.x, a.y)
						 )
		# draw v_side vector:
		b = zrc.add_vectors(self.me.pos, zrc.mult_vector(self.me.v_side, 20))
		pygame.draw.line(self.__screen,
						 c.DARKYELLOW,
						 (self.me.pos.x, self.me.pos.y),
						 (b.x, b.y)
						 )
	#===========================================================================
