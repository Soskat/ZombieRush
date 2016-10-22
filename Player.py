#!/usr/bin/python
#-*- coding: utf-8 -*-

import pygame
import math

""" Class that represents Player """
class Player:
	""" Constructor """
	def __init__(self, gameDisplay, displaySize, color, levelObst):
		self.__screen = gameDisplay				# game display
		self.__color = color					# Player's color
		self.__lvlObst = levelObst				# level obstacles info
		self.__vOr = [(-8,10), (0,-10), (8,10)]	# origin vertices
		self.__vertices = [[0,0], [0,0], [0,0]]	# current vertices
		self.__posX = 400	# X position
		self.__posY = 300	# Y position
		self.__heading = 0	# heading in degrees from UP direction to right
		self.__radius = 10	# Player's radius used in collision detection
		self.__maxX = displaySize[0] - self.__radius	# game world border
		self.__maxY = displaySize[1] - self.__radius	# game world border
		self.__minX = self.__minY = self.__radius		# game world borders


	""" Draws Player """
	def draw(self):
		x = y = 0
		for i in range(0,len(self.__vOr)):
			x = self.__vOr[i][0] * math.cos(self.__heading) - self.__vOr[i][1] * math.sin(self.__heading)
			y = self.__vOr[i][0] * math.sin(self.__heading) + self.__vOr[i][1] * math.cos(self.__heading)
			self.__vertices[i][0] = x + self.__posX
			self.__vertices[i][1] = y + self.__posY
		pygame.draw.polygon(self.__screen, self.__color, self.__vertices, 1)


	""" Turns Player around - changes Player's heading """
	def turn(self, angle):
		self.__heading += angle


	""" Move Player in his heading direction """
	def move(self, step):
		x = self.__posX - step * math.sin(self.__heading)
		y = self.__posY + step * math.cos(self.__heading)
		# check collisions with math borders:
		if x < self.__minX:	x = self.__minX
		elif x > self.__maxX: x = self.__maxX
		if y < self.__minY:	y = self.__minY
		elif y > self.__maxY: y = self.__maxY
		# check collisions with obstacles:
		keyX = int(x / 100)
		keyY = int(y / 100)
		for kx in range(keyX - 1, keyX + 2):
			if kx in self.__lvlObst:
				for ky in range (keyY - 1, keyY + 2):
					if ky in self.__lvlObst[kx]:
						for obst in self.__lvlObst[kx][ky]:
							condition, info = obst.if_collide((x, y, self.__radius))
							# in case of collision adjust Player's position to avoid it:
							if condition:
								x, y = self.__adjust_position((x,y), info)
		# move Player:
		self.__posX, self.__posY = x, y


	""" Adjusts position to avoid collision """
	def __adjust_position(self, newPos, collInfo):
		dx, dy, d, D = collInfo
		x = dx * (D - d) / d
		y = dy * (D - d) / d
		return newPos[0] - x, newPos[1] - y
