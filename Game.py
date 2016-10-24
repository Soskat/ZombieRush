#!/usr/bin/python
#-*- coding: utf-8 -*-

import pygame
from Player import Player
from Level import Level
from ZombiePool import ZombiePool


YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
GREY = (120, 120, 120)
GREEN = (0, 255, 0)

step = 3
angle = 0.2
zombie_amount = 100
current_zombie_amount = 10

################################################################################

pygame.init()

# initialize game window:
display_size = (800, 600)
margin = 20
game_display = pygame.display.set_mode(display_size)
pygame.display.set_caption('Zombie Rush')

# set game clock:
clock = pygame.time.Clock()
fps = 30

################################################################################
move_FORWARD, move_BACKWARD, move_LEFT, move_RIGHT = False, False, False, False
################################################################################

""" Main game loop """
def game_loop():
    global move_FORWARD, move_BACKWARD, move_LEFT, move_RIGHT

    play_game = True

    level = Level(game_display, display_size, margin, GREY, 10)
    player = Player(game_display, display_size, YELLOW, level)
    zombie_pool = ZombiePool(game_display, display_size, player,
                            zombie_amount, current_zombie_amount, level, GREEN)

    while play_game:
        # check game input:
        for event in pygame.event.get():
            # quit game window:
            if event.type == pygame.QUIT:
                play_game = False

            if event.type == pygame.KEYDOWN:
                # turn left:
                if event.key in [pygame.K_LEFT, pygame.K_a]:
                    move_LEFT = True
                # turn right:
                if event.key in [pygame.K_RIGHT, pygame.K_d]:
                    move_RIGHT = True
                # move forward:
                if event.key in [pygame.K_UP, pygame.K_w]:
                    move_FORWARD = True
                # move backward:
                if event.key in [pygame.K_DOWN, pygame.K_s]:
                    move_BACKWARD = True
                """ QUICK QUIT """
                if event.key == pygame.K_SPACE:
                    play_game = False

            # on key up:
            if event.type == pygame.KEYUP:
                # stop going left:
                if event.key in [pygame.K_LEFT, pygame.K_a]:
                    move_LEFT = False
                # stop going right:
                if event.key in [pygame.K_RIGHT, pygame.K_d]:
                    move_RIGHT = False
                # stop going up:
                if event.key in [pygame.K_UP, pygame.K_w]:
                    move_FORWARD = False
                # stop going back:
                if event.key in [pygame.K_DOWN, pygame.K_s]:
                    move_BACKWARD = False

        if move_FORWARD: player.move(-step)
        if move_BACKWARD: player.move(step)
        if move_RIGHT: player.turn(angle)
        if move_LEFT: player.turn(-angle)

        game_display.fill(BLACK)
        level.draw()
        player.draw()
        zombie_pool.draw()

        # update game window: =============================
        pygame.display.update()
        clock.tick(fps)

################################################################################
game_loop()

pygame.quit()

quit()
