#!/usr/bin/python
#-*- coding: utf-8 -*-

import pygame
import constants as c
import zrcommon as zrc
from zrcommon import Vector2D
from MovingEntity import MovingEntity


""" Class that represents Player """
class Player:
	""" Constructor """
	def __init__(self, game_display, display_size, level):
		self.__screen = game_display						# game display handler
		self.__color = c.player_color						# Player's color
		self.__level = level								# level handler
		#self.__origV = [(-8,10), (0,-10), (8,10)]			# origin vertices
		self.__origV = [Vector2D(-8,10),	# origin vertices
						Vector2D(0,-10),
						Vector2D(8,10)]
		#x, y = int(display_size[0] / 2), int(display_size[1] / 2)
		#self.__pos = zrc.Vector2D(x,y)		# position
		#self.__heading_angle = 0			# heading in degrees from UP direction to right
		#self.__heading = zrc.Vector2D(0, 1)	# heading vector
		#self.__radius = c.player_radius		# Player's radius used in collision detection
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




	# """ Gets Player's current position and radius """
	# def get_player_info(self):
	# 	return (self.__pos.x, self.__pos.y, self.__radius)
	#
	#
	# """ Get Player's current position """
	# def position(self):
	# 	return self.__pos
	#
	#
	# """ Get Player's current heading """
	# def heading(self):
	# 	return self.__heading
	#
	# """ Get PLayer's velocity vector """
	# def velocity(self):
	# 	velocity = self.__heading
	# 	velocity.norm().mult(c.player_step)
	# 	return velocity


	""" Draws Player """
	def draw(self):
		newV = []
		for v in [(-8,10), (0,-10), (8,10)]:
			newV.append((self.me.pos.x + v[0], self.me.pos.y + v[1]))
		pygame.draw.polygon(self.__screen,
							self.me.color(),
							newV,
							1)

	def rotate_player(self):
		# newV.append((self.__origV[0][0] + self.me.heading.x + self.me.pos.x,
		# 			 self.__origV[0][1] + self.me.heading.y + self.me.pos.y))
		# newV.append((self.__origV[1][0] + self.me.heading.x + self.me.pos.x,
		# 			 self.__origV[1][1] + self.me.heading.y + self.me.pos.y))
		# newV.append((self.__origV[2][0] + self.me.heading.x + self.me.pos.x,
		# 			 self.__origV[2][1] + self.me.heading.y + self.me.pos.y))
		p1 = zrc.proj_vector(self.__origV[0], self.me.v_side)
		p2 = zrc.proj_vector(self.__origV[1], self.me.heading)
		p3 = zrc.proj_vector(self.__origV[2], self.me.v_side)
		newV = [[int(p1.x), int(p1.y)], [int(p2.x), int(p2.y)], [int(p3.x), int(p3.y)]]
		for nv in newV:
			nv[0] += self.me.pos.x
			nv[1] += self.me.pos.y
		return newV


	""" DEBUG DRAW MODE """
	def draw_debug(self):
		pygame.draw.circle(self.__screen,
						   c.ORANGE,
						   (self.me.pos.x, self.me.pos.y),
						   c.panic_distance,
						   1)

	""" Debug - draw vectors """
	def draw_vectors(self):
		# draw heading vector:
		a = zrc.add_vectors(self.me.pos, zrc.mult_vector(self.me.heading, 50))
		pygame.draw.line(self.__screen,
						 c.ORANGE,
						 (self.me.pos.x, self.me.pos.y),
						 (a.x, a.y))
		# draw v_side vector:
		b = zrc.add_vectors(self.me.pos, zrc.mult_vector(self.me.v_side, 20))
		pygame.draw.line(self.__screen,
						 c.DARKYELLOW,
						 (self.me.pos.x, self.me.pos.y),
						 (b.x, b.y))


	""" Turns Player around - changes Player's heading """
	def turn(self, turn_right):
		if turn_right:
			angle = self.me.max_turn_rate()
		else:
			angle = -1 * self.me.max_turn_rate()
		self.me.heading = zrc.rotate_vector(self.me.heading, angle).norm()
		self.me.v_side = self.me.heading.perp()


	""" Move Player in his heading direction """
	def move_OLD(self, step):
		x, y = zrc.calculate_player_position((self.__pos.x, self.__pos.y),
											  self.__heading_angle,
											  step)
		# check collisions with game world borders:
		if x < self.__min_x:	x = self.__min_x
		elif x > self.__max_x: 	x = self.__max_x
		if y < self.__min_y:	y = self.__min_y
		elif y > self.__max_y: 	y = self.__max_y
		# check collisions with obstacles:
		x, y = self.__level.avoid_collision_with_obstacles((x,y,self.__radius))
		# move Player:
		self.__pos.x, self.__pos.y = int(x), int(y)


	""" Move Player in his heading direction """
	def move(self, move_forward):
		a = zrc.mult_vector(self.me.heading, self.me.max_speed())
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
		# move Player:
		self.me.pos.x, self.me.pos.y = int(x), int(y)
