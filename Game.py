#!/usr/bin/python
#-*- coding: utf-8 -*-

import pygame
import constants as c
from Player import Player
from Level import Level
from ZombiePool import ZombiePool
from Vector2D import Vector2D



################################################################################
pygame.init()

# initialize game window:
display_size = (0, c.game_width,                            # min_x, max_x
                c.text_margin + c.font_size, c.game_height) # min_y, max_y
game_display = pygame.display.set_mode((c.game_width, c.game_height))
pygame.display.set_caption('Zombie Rush')

#initialize font:
font_family = c.font_path
game_font = pygame.font.Font(font_family, c.font_size)
menu_font = pygame.font.Font(font_family, c.big_font_size)

# set game clock:
clock = pygame.time.Clock()
fps = c.FPS
ray_cooldown = fps

################################################################################
play_again = False
play_game = True
player_dead = False
################################################################################


def draw_gui(player_hp, score, wave, ray_timer):
    """Draws GUI.

    Args:
        param1 (int): player's health points
        param2 (int): player's score
        param3 (int): current wave ID
        param4 (int): death ray cooldown status (seconds to next shot)
    """
    # PLAYER HEALTH ============================================================
    # draw player HP counter:
    hp_label = game_font.render("HP:", True, c.WHITE)
    hp_label_pos = hp_label.get_rect()
    hp_label_pos.topleft = (c.text_margin, c.text_margin)
    game_display.blit(hp_label, hp_label_pos)
    # draw player's health bar:
    hp_bar = pygame.Rect((hp_label_pos.width + c.text_margin * 2, c.text_margin),
                         (player_hp, hp_label_pos.height))
    # calculate color of health bar:
    if player_hp < 0:
        hp_bar.width = 0
        hp_bar_color = (255, 0, 0)
    elif player_hp <= c.player_half_health:
        hp_bar_color = (255, player_hp * c.color_ratio, 0)
    else:
        hp_bar_color = (255 - (player_hp - 50) * c.color_ratio, 255, 0)
    pygame.draw.rect(game_display, hp_bar_color, hp_bar)
    # WAVE ====================================================================
    # draw wave counter info:
    wave_text = "Wave " + str(wave)
    wv_label = game_font.render(wave_text, True, c.WHITE)
    wv_label_pos = wv_label.get_rect()
    wv_label_pos.centerx = game_display.get_rect().centerx
    wv_label_pos.top = c.text_margin
    game_display.blit(wv_label, wv_label_pos)
    # DEATH RAY TIMER: =========================================================
    rd_bar = pygame.Rect((0, 0), (0, 10))
    rd_bar.top = wv_label_pos.bottom + 5
    rd_bar.width = (ray_cooldown - ray_timer) * 5
    rd_bar.centerx = game_display.get_rect().centerx
    if ray_timer <= 0:
        rd_bar_color = c.ORANGE
    else:
        rd_bar_color = c.RAGERED
    pygame.draw.rect(game_display, rd_bar_color, rd_bar)
    # SCORE ====================================================================
    sc_label = game_font.render(str(score), True, c.WHITE)
    sc_label_pos = sc_label.get_rect()
    sc_label_pos.topright = (display_size[1] - c.text_margin, c.text_margin)
    game_display.blit(sc_label, sc_label_pos)


def show_menu():
    """ Shows game menu. """
    global play_again, play_game, player_dead
    while True:
        # check game input: ======================================
        for event in pygame.event.get():
            # quit game window:
            if event.type == pygame.QUIT:
                play_game = False
                return
            # manage keyboard input:
            if event.type == pygame.KEYDOWN:
                # quit game:
                if event.key == pygame.K_q:
                    play_game = False
                    return
                # restart game:
                if event.key == pygame.K_r:
                    play_game = False
                    play_again = True
                    return
                # resume game:
                if event.key == pygame.K_ESCAPE and not player_dead:
                    return
        # print menu info: =======================================
        if not player_dead:
            # resume game:
            resume_label = game_font.render("Resume game: [ESC]", True, c.WHITE)
            resume_label_pos = resume_label.get_rect()
            resume_label_pos.centerx = game_display.get_rect().centerx
            resume_label_pos.centery = game_display.get_rect().centery - 50
            game_display.blit(resume_label, resume_label_pos)
        else:
            # show dead info:
            dead_label = game_font.render("You're dead", True, c.RED)
            dead_label_pos = dead_label.get_rect()
            dead_label_pos.centerx = game_display.get_rect().centerx
            dead_label_pos.centery = game_display.get_rect().centery - 60
            game_display.blit(dead_label, dead_label_pos)
        # restart game:
        restart_label = game_font.render("Restart game: [R]", True, c.WHITE)
        restart_label_pos = restart_label.get_rect()
        restart_label_pos.centerx = game_display.get_rect().centerx
        restart_label_pos.centery = game_display.get_rect().centery
        game_display.blit(restart_label, restart_label_pos)
        # quit game:
        quit_label = game_font.render("Quit game: [Q]", True, c.WHITE)
        quit_label_pos = quit_label.get_rect()
        quit_label_pos.centerx = game_display.get_rect().centerx
        quit_label_pos.centery = game_display.get_rect().centery + 50
        game_display.blit(quit_label, quit_label_pos)
        # update game window: =============================
        pygame.display.update()
        clock.tick(fps)


def game_loop():
    """ Main game loop. """
    global play_again, play_game, player_dead

    move_FORWARD = move_BACKWARD = move_LEFT = move_RIGHT = False
    # draw death ray flags and timer:
    can_use_ray = c.ray_READY
    ray_timer = 0
    # debug mode flags:
    debug_flag = True
    debug_mode = False

    level = Level(game_display, display_size, c.world_margin)
    player = Player(game_display, display_size, level)
    zombie_pool = ZombiePool(game_display, display_size, player, level, menu_font)

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
                # show game menu:
                if event.key == pygame.K_ESCAPE:
                    show_menu()
                """ SWITCH DEBUG MODE """
                if event.key == pygame.K_v:
                    if debug_flag:
                        if debug_mode: debug_mode = False
                        else: debug_mode = True
                        debug_flag = False

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
                if event.key == pygame.K_v:
                    debug_flag = True

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
        # draw game GUI:
        if player.health <= 0:
            player_dead = True
            show_menu()
        if can_use_ray == c.ray_SHOOT: dr_timer = 0
        else: dr_timer = ray_timer
        draw_gui(player.health, player.score, zombie_pool.wave, dr_timer)

        # update game window: =============================
        pygame.display.update()
        clock.tick(fps)


def game_manager():
    """ Game manager. """
    global play_again, play_game
    while True:
        game_loop()
        if not play_again: return
        else:
            play_again = False
            play_game = True
################################################################################
game_manager()

pygame.quit()

quit()
