#!/usr/bin/python
#-*- coding: utf-8 -*-

import pygame
from Player import Player
from Level import Level

yellow = (255, 255, 0)
black = (0, 0, 0)
grey = (120, 120, 120)
step = 3
angle = 0.2

################################################################################

pygame.init()

# initialize game window:
displaySize = (800, 600)
margin = 20
gameDisplay = pygame.display.set_mode(displaySize)
pygame.display.set_caption('Zombie Rush')

# set game clock:
clock = pygame.time.Clock()
framesPerSecond = 30

################################################################################
movFORWARD, movBACKWARD, movLEFT, movRIGHT = False, False, False, False
################################################################################

""" Main game loop """
def game_loop():
    global movFORWARD, movBACKWARD, movLEFT, movRIGHT

    playGame = True

    level = Level(gameDisplay, displaySize, margin, grey, 10)
    player = Player(gameDisplay, displaySize, yellow, level.obstacles)

    while playGame:
        # check game input:
        for event in pygame.event.get():
            # quit game window:
            if event.type == pygame.QUIT:
                playGame = False

            if event.type == pygame.KEYDOWN:
                # turn left:
                if event.key in [pygame.K_LEFT, pygame.K_a]:
                    movLEFT = True
                # turn right:
                if event.key in [pygame.K_RIGHT, pygame.K_d]:
                    movRIGHT = True
                # move forward:
                if event.key in [pygame.K_UP, pygame.K_w]:
                    movFORWARD = True
                # move backward:
                if event.key in [pygame.K_DOWN, pygame.K_s]:
                    movBACKWARD = True
                """ QUICK QUIT """
                if event.key == pygame.K_SPACE:
                    playGame = False

            # on key up:
            if event.type == pygame.KEYUP:
                # stop going left:
                if event.key in [pygame.K_LEFT, pygame.K_a]:
                    movLEFT = False
                # stop going right:
                if event.key in [pygame.K_RIGHT, pygame.K_d]:
                    movRIGHT = False
                # stop going up:
                if event.key in [pygame.K_UP, pygame.K_w]:
                    movFORWARD = False
                # stop going back:
                if event.key in [pygame.K_DOWN, pygame.K_s]:
                    movBACKWARD = False

        if movFORWARD: player.move(-step)
        if movBACKWARD: player.move(step)
        if movRIGHT: player.turn(angle)
        if movLEFT: player.turn(-angle)

        gameDisplay.fill(black)
        level.draw()
        player.draw()

        # update game window: =============================
        pygame.display.update()
        clock.tick(framesPerSecond)

################################################################################
game_loop()

pygame.quit()

quit()
