#!/usr/bin/python
#-*- coding: utf-8 -*-

import pygame
import constants as c
from Player import Player
from Level import Level
from ZombiePool import ZombiePool
from Vector2D import Vector2D
from Wall import Wall



################################################################################
pygame.init()

# initialize game window:
display_size = (c.game_width, c.game_height)
margin = c.world_margin
game_display = pygame.display.set_mode(display_size)
pygame.display.set_caption('Zombie Rush')

# set game clock:
clock = pygame.time.Clock()
fps = c.FPS
ray_cooldown = fps

################################################################################
move_FORWARD = move_BACKWARD = move_LEFT = move_RIGHT = False
play_again = False
################################################################################

""" Calculates game world walls """
def calculate_walls():
    a = Vector2D(0, 0)
    b = Vector2D(display_size[0], 0)
    c = Vector2D(0, display_size[1])
    d = Vector2D(display_size[0], display_size[1])
    walls = [
                Wall(a, b),
                Wall(a, c),
                Wall(b, c),
                Wall(c, d)
            ]
    return walls


""" Game manager """
def game_manager():
    global play_again
    while True:
        game_loop()
        if not play_again: return
        else: play_again = False


""" Main game loop """
def game_loop():
    global move_FORWARD, move_BACKWARD, move_LEFT, move_RIGHT, play_again

    play_game = True
    # draw death ray flags and timer:
    can_use_ray = c.ray_READY
    ray_timer = 0
    # debug mode flags:
    debug_flag = True
    debug_mode = False
    draw_v_flag = True
    draw_v_mode = False

    level = Level(game_display, display_size, margin)
    player = Player(game_display, display_size, level)
    zombie_pool = ZombiePool(game_display, display_size, player, level, calculate_walls())

    print("================ Start Zombie Rush ================")
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
                """ PLAY AGAIN """
                if event.key == pygame.K_r:
                    play_game = False
                    play_again = True
                """ SWITCH DEBUG MODE """
                if event.key == pygame.K_u:
                    if debug_flag:
                        if debug_mode: debug_mode = False
                        else: debug_mode = True
                        debug_flag = False
                """ SWITCH DRAW VECTORS MODE """
                if event.key == pygame.K_v:
                    # if draw_v_flag:
                        if draw_v_mode: draw_v_mode = False
                        else: draw_v_mode = True
                        draw_v_flag = False


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
                """ SWITCH DEBUG MODE """
                if event.key == pygame.K_u:
                    debug_flag = True
                """ SWITCH DRAW VECTORS MODE """
                if event.key == pygame.K_v:
                    draw_v_flag = True

        # check for mouse input:
        if pygame.mouse.get_pressed()[0] and can_use_ray == c.ray_READY:
            can_use_ray = c.ray_SHOOT
            ray_timer = c.ray_time


        # do all calculations: =================================================
        # move player:
        if move_FORWARD: player.move(True)
        if move_BACKWARD: player.move(False)
        if move_RIGHT: player.turn(True)
        if move_LEFT: player.turn(False)
        # move zombies:
        zombie_pool.move()
        # manage player's death ray cooldown:
        if can_use_ray == c.ray_COOLDOWN:
            ray_timer -= 1
            if ray_timer <= 0:
                can_use_ray = c.ray_READY

        # draw everything: =====================================================
        # draw background:
        game_display.fill(c.BLACK)
        # draw DEBUG stuff:
        if debug_mode:
            player.draw_debug()
            zombie_pool.draw_debug()
        if draw_v_mode:
            player.draw_vectors()
            zombie_pool.draw_vectors()
        # draw death ray:
        if can_use_ray == c.ray_SHOOT:
            player.shoot()
            player.draw_death_ray()
            ray_timer -= 1
            if ray_timer <= 0:
                can_use_ray = c.ray_COOLDOWN
                ray_timer = ray_cooldown
        # draw obstacles, player and zombies:
        level.draw()
        player.draw()
        zombie_pool.draw()

        # update game window: =============================
        pygame.display.update()
        clock.tick(fps)

        print("================================================")
################################################################################
game_manager()

pygame.quit()

quit()
