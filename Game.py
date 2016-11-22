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
display_size = (0, c.game_width,                            # min_x, max_x
                c.text_margin + c.font_size, c.game_height) # min_y, max_y
game_display = pygame.display.set_mode((c.game_width, c.game_height))
pygame.display.set_caption('Zombie Rush')

#initialize font:
font_family = None
game_font = pygame.font.Font(font_family, c.font_size)
menu_font = pygame.font.Font(font_family, c.big_font_size)

# set game clock:
clock = pygame.time.Clock()
fps = c.FPS
ray_cooldown = fps

################################################################################
move_FORWARD = move_BACKWARD = move_LEFT = move_RIGHT = False
play_again = False
play_game = True
################################################################################

# """ Calculates game world walls """ #-------------------------------------------------- is this used for real?
# def calculate_walls():
#     a = Vector2D(display_size[0], display_size[2])
#     b = Vector2D(display_size[1], display_size[2])
#     c = Vector2D(display_size[0], display_size[3])
#     d = Vector2D(display_size[1], display_size[3])
#     walls = [
#                 Wall(a, b),
#                 Wall(a, c),
#                 Wall(b, c),
#                 Wall(c, d)
#             ]
#     return walls
#

""" Draws GUI """
def draw_gui(player_hp, score, wave):
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
    # SCORE ====================================================================
    sc_label = game_font.render(str(score), True, c.WHITE)
    sc_label_pos = sc_label.get_rect()
    sc_label_pos.topright = (display_size[1] - c.text_margin, c.text_margin)
    game_display.blit(sc_label, sc_label_pos)


""" Shows game menu """
def show_menu():
    global play_again, play_game
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
                if event.key == pygame.K_ESCAPE:
                    return
        # print menu info: =======================================
        # resume game:
        resume_label = game_font.render("Resume game: [ESC]", True, c.WHITE)
        resume_label_pos = resume_label.get_rect()
        resume_label_pos.centerx = game_display.get_rect().centerx
        resume_label_pos.centery = game_display.get_rect().centery - 50
        game_display.blit(resume_label, resume_label_pos)
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


""" Main game loop """
def game_loop():
    global move_FORWARD, move_BACKWARD, move_LEFT, move_RIGHT, play_again, play_game

    # draw death ray flags and timer:
    can_use_ray = c.ray_READY
    ray_timer = 0
    # debug mode flags:
    debug_flag = True
    debug_mode = False

    level = Level(game_display, display_size, c.world_margin)
    player = Player(game_display, display_size, level)
    zombie_pool = ZombiePool(game_display, display_size, player, level, menu_font)

    print("================ Start Zombie Rush ================")
    print(play_game)
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
        draw_gui(player.health, player.score, zombie_pool.wave)

        # update game window: =============================
        pygame.display.update()
        clock.tick(fps)


        print("================================================")


""" Game manager """
def game_manager():
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
