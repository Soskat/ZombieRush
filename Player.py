#!/usr/bin/python
#-*- coding: utf-8 -*-

import pygame
import constants as c
import zrcommon as zrc
from Vector2D import Vector2D
from MovingEntity import MovingEntity



class Player:
	"""Class that represents Player."""
	def __init__(self, game_display, display_size, level):
		"""Constructor.

		Args:
            param1 (pygame.Surface): game display handler
            param2 ((int, int)): game display size in form of a touple (x, y)
			param3 (Level): Level handler
		"""
		self.__screen = game_display		# game display handler
		self.__color = c.player_color		# Player's color
		self.__level = level				# level handler
		self.__zombies = None				# List of active zombies - initialized in ZombiePool
		self.__y_size = 10					# half of player's height
		self.__x_size = 8					# half of player's width
		self.health = c.player_max_health	# player's health
		self.score = 0						# player's score
		# MovingEntity object:
		self.me = MovingEntity( position = (int(display_size[1]/2), int(display_size[3]/2)),
                                heading = (0,-1),
                                max_speed = c.player_max_speed,
                                max_force = c.player_max_force,
                                max_turn_rate = c.player_max_turn_rate,
                                radius = c.player_radius,
                                mass = c.player_mass,
                                color = c.player_color
                               )
		# calculate game world borders:
		self.__min_x = display_size[0] + self.me.radius()
		self.__max_x = display_size[1] - self.me.radius()
		self.__min_y = display_size[2] + self.me.radius()
		self.__max_y = display_size[3] - self.me.radius()
		# death ray related variables:
		self.__death_ray = Vector2D()						# death ray vector
		self.__world_max_x = int(display_size[1]/100)		# used for researching game world
		self.__world_max_y = int(display_size[3]/100)		# used for researching game world


	def set_zombie_list(self, list_handler):
		"""Sets zombie list handler.

		Args:
			param (list): sets player's zombies list
		"""
		self.__zombies = list_handler


	def avoid_collision_with_zombies(self, obj):
		"""Detects possible collisions of object with all active zombies.
		If collision occurs, recalculates object's position to avoid collision.

		Args:
		    param ((int, int, int)): object info used in collision detection in form of a touple (x, y, radius)
		"""
		x, y, radius = obj
		if self.__zombies == None:
			return x, y
		for z in self.__zombies:
			x, y = z.avoid_collision((x, y, radius))
		return x, y


	def rotate_player(self):
		"""Rotates player representation (triangle).

		Returns:
			A list of recalculated points of Player representation - a triangle.
		"""
		a = zrc.scale_vector(self.me.heading, self.__y_size)
		b = zrc.scale_vector(self.me.side, self.__x_size)
		newV = [
			[a.x, a.y],
			[b.x - a.x, b.y - a.y],
			[-b.x - a.x, -b.y - a.y]
		]
		for nv in newV:
			nv[0] += self.me.pos.x
			nv[1] += self.me.pos.y
		return newV


	def turn(self, turn_right):
		"""Turns Player around - changes Player's heading.

		Args:
			param (bool): True if player turns right; False if he turns left
		"""
		if turn_right:
			angle = self.me.max_turn_rate()
		else:
			angle = -1 * self.me.max_turn_rate()
		self.me.heading = zrc.rotate_vector(self.me.heading, angle).norm()
		self.me.side = self.me.heading.perp()



	def shoot(self):
		"""Calculates death ray path."""
		# check if death ray vector collides with any obstacle: ================
		# is player faced to the East more than to the West?
		if self.me.heading.x < 0: side_dir = False
		else: side_dir = True
		# is player faced to the South more than to the North?
		if self.me.heading.y < 0: up_dir = False
		else: up_dir = True
		# generate research area keys:
		key_x = int(self.me.pos.x / 100)
		key_y = int(self.me.pos.y / 100)
		range_x = []	# x coords in level grid
		range_y = []	# y coords in level grid
		if side_dir: range_x = list(range(key_x, self.__world_max_x))
		else: range_x = list(range(0, key_x + 1))
		if up_dir: range_y = list(range(key_y, self.__world_max_y))
		else: range_y = list(range(0, key_y + 1))

		# search for obstacles:
		cip_dist = c.ray_length		# actual Closest Intersection Point distance
		for kx in range_x:
			if kx in self.__level.obstacles:
				for ky in range_y:
					if ky in self.__level.obstacles[kx]:
						# check if death ray collides with obstacles:
						for obst in self.__level.obstacles[kx][ky]:
							# calculate this obstacle's position in player local space:
							local_pos = zrc.point_to_local_space(obst.center,
																 self.me.heading,
																 self.me.side,
																 self.me.pos)
							# if the local position has a negative x value then it must lay
							# behind the player (in which case it can be ignored):
							if local_pos.x >= 0:
								# project vector of distance from player to obstacle
								# to the death ray:
								to_obst = obst.center.sub_copy(self.me.pos)
								to_obst_proj = zrc.proj_vector(to_obst, self.me.heading)
								# calculate distance from to_obst_proj to obstacle centre:
								to_obst_magn = to_obst.magn()
								to_obst_proj_magn = to_obst_proj.magn()
								dist_perp = zrc.get_sqrt(to_obst_magn*to_obst_magn -
														 to_obst_proj_magn*to_obst_proj_magn)
								# if dist_perp <= obstacle radius then this obstacle
								# collides with death ray:
								if dist_perp <= obst.radius:
									# now we must calulate intersection  point in order
									# to block death ray from Intersecting obstacle:
									diff = zrc.get_sqrt(obst.radius*obst.radius -
														dist_perp*dist_perp)
									ratio = to_obst_proj.magn()
									cip_scale = ratio - diff
									# rescale vector length so as it was no longer
									# than distance from player to intersection point
									# of death ray and the obstacle:
									to_obst_proj.norm().mult(cip_scale)
									# if to_obst_proj is the closest intersection point
									# record it:
									if cip_scale < cip_dist:
										cip_dist = cip_scale
		# update death ray vector:
		self.__death_ray = self.me.pos.add_copy(self.me.heading.mult_copy(cip_dist))

		# check if death ray vector collides with any zombies: =================
		for z in self.__zombies:
			# calculate this zombie's position in player local space:
			local_pos = zrc.point_to_local_space(z.me.pos,
												 self.me.heading,
												 self.me.side,
												 self.me.pos)
			# if the local position has a negative x value then it must lay
			# behind the player (in which case it can be ignored):
			if local_pos.x >= 0:
				# project vector of distance from player to zombie to the death ray:
				to_zombie = z.me.pos.sub_copy(self.me.pos)
				to_zombie_proj = zrc.proj_vector(to_zombie, self.me.heading)
				# if zombie is in range of death ray:
				if to_zombie_proj.magn() < cip_dist:
					# calculate distance from to_zombie_proj to zombie center:
					to_zombie_magn = to_zombie.magn()
					to_zombie_proj_magn = to_zombie_proj.magn()
					dist_perp = zrc.get_sqrt(to_zombie_magn*to_zombie_magn -
											 to_zombie_proj_magn*to_zombie_proj_magn)
					# if dist_perp < zombie's radius, zombie is dead:
					if dist_perp < z.me.radius():
						z.is_dead = True
						self.score += c.ppz


	def move(self, move_forward):
		"""Moves Player in his heading direction.

		Args:
			param (bool): True if player moves forward; False if he moves backward
		"""
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
	def draw(self):
		"""Draws Player."""
		pygame.draw.polygon(self.__screen,
							self.me.color(),
							self.rotate_player(),
							1
							)


	def draw_death_ray(self):
		"""Draws death ray."""
		self.draw_line(c.RED, self.me.pos, self.__death_ray, 3)


	def draw_debug(self):
		"""Draws debug mode."""
		# draw heading vector:
		self.draw_line(c.ORANGE,
					   self.me.pos,
					   self.me.pos.add_copy(self.me.heading.mult_copy(50)))
		# draw side vector:
		self.draw_line(c.DARKYELLOW,
					   self.me.pos,
					   self.me.pos.add_copy(self.me.side.mult_copy(20)))
		# draw panic distance circle around player:
		pygame.draw.circle(self.__screen,
						   c.CYAN,
						   self.me.get_position(),
						   c.panic_distance,
						   1
						   )
		# draw player's FOV cone:
		angle = c.fov_multiplier * zrc.pi	# angle = multiplier*90degr * 2*PI / 180degr
		fov_vec = [
					zrc.rotate_vector_around_origin(self.me.heading, angle),
					zrc.rotate_vector_around_origin(self.me.heading, -angle),
					zrc.rotate_vector_around_origin(self.me.heading, angle + zrc.pi),
					zrc.rotate_vector_around_origin(self.me.heading, -(angle + zrc.pi))
				  ]
		for fov in fov_vec:
			a = self.me.pos.add_copy(fov.mult(100))
			self.draw_line(c.LIGHTGREY, self.me.pos, a)


	def draw_line(self, color, a, b, width=1):
		"""Draws single line.

		Args:
			param1 ((int, int, int)): color of line in form of a touple (r, g, b)
			param2 (Vector2D): start point of the line
			param3 (Vector2D): end point of the line

		Keyword args:
			param4 (int): width of the line (default 1)
		"""
		pygame.draw.line(self.__screen, color, (a.x, a.y), (b.x, b.y), width)
