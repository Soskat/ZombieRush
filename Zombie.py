#!/usr/bin/python
#-*- coding: utf-8 -*-

import pygame
import constants as c
import zrcommon as zrc
from Vector2D import Vector2D
from MovingEntity import MovingEntity
from SteeringBehaviours import SteeringBehaviours



""" Class that represents a Zombie bot """
class Zombie:
    """ Constructor """
    def __init__(self, screen, level, level_borders, walls, player, zombie_list, ID, pos):
        self.__screen = screen                  # game display handler
        self.__level = level                    # Level handler
        self.__borders = level_borders          # space where zombies can wandern
        self.walls = walls                      # game world walls
        self.__player = player                  # Player handler
        self.__zombies = zombie_list            # list of all zombies
        self.__time_elapsed = c.time_elapsed    # time elapsed
        self.ID = ID                            # ID number
        self.__state = c.state_IDLE             # current zombie FSM state
        #self.RAGE = False                       # is_rage_mode_on flag
        self.__risk_timer = 0                   # determines how long zombie will be hiding
        self.me = MovingEntity( position = pos,
                                heading = pos,
                                max_speed = c.zombie_max_speed,
                                max_force = c.zombie_max_force,
                                max_turn_rate = c.zombie_max_turn_rate,
                                radius = c.zombie_radius,
                                mass = c.zombie_mass,
                                color = c.zombie_color
                               )
        self.__steering = SteeringBehaviours(self, self.me.max_force()) # steering behaviours handler
        """ DEBUG """
        self.debug_color = c.BLUE
        self.__steering_force = Vector2D()      # steering force

        """ DEBUG AGAIN """
        self.proj = Vector2D()


    """ Get player """
    def get_player(self):
        return self.__player


    """ Get obstacles """
    def get_obstacles(self):
        return self.__level.obstacles


    """ Get game world borders info """
    def get_borders(self):
        return self.__borders


    """ Checks if Zombie collides with given object.
        If yes, recalculate position of given object to avoid collision """
    def avoid_collision(self, obj):
        return zrc.avoid_collision((self.me.pos.x, self.me.pos.y, self.me.radius()), obj)


    #===========================================================================
    # FSM transition functions: ================================================
    """ Transition function A - can attack? """
    def can_attack(self):
        pass

    """ Transition function B - is safe? """
    def is_safe(self):
        if self.me.pos.dist_to_vector(self.get_player().me.pos) < c.panic_distance:
            self.debug_color = c.RED
            return False
        else:
            self.debug_color = c.BLUE
            return True

    """ Transition function B* - is away enaugh? """
    def is_away_enough(self):
        if self.me.pos.dist_to_vector(self.get_player().me.pos) < c.safe_distane:
            self.debug_color = c.RED
            return False
        else:
            self.debug_color = c.BLUE
            return True

    """ Transition function C - is hidden? """
    def is_hidden(self):
        if zrc.check_collision(
                                (self.me.pos.x, self.me.pos.y, self.me.radius()),
                                (self.__steering.bhs.x, self.__steering.bhs.y, 20.0)
                              ):
            return True
        else:
            return False
    #===========================================================================


    """ Move zombie bot """
    def move(self):
        # reset all steering behaviours flags:
        self.__steering.reset_flags()

        # check conditions in Finite State Mashine: ============================


        # state IDLE:
        if self.__state == c.state_IDLE:
            self.me.set_color(c.zombie_color)#----------------------------------
            self.__steering.wandern_w = c.w_wandern
            # is inside player's range - run away:
            if not self.is_safe():
                self.__steering.hide_on = True
                self.__state = c.state_RUN
            # is safe - wandern:
            else:
                self.__steering.wandern_on = True


        # state RUN:
        elif self.__state == c.state_RUN:
            self.me.set_color(c.Z_RUN)# ---------------------------------------
            self.__steering.hide_w = c.w_hide
            # reach best hiding spot:
            if self.is_hidden():
                self.__state = c.state_HIDDEN
                self.__risk_timer = zrc.get_randint(150, 300)
            # is away enough to be safe:
            elif self.is_away_enough():
                self.__steering.wandern_on = True
                self.__state = c.state_IDLE
            # is not safe - seek best hiding spot:
            else:
                self.__steering.hide_on = True


        # state HIDDEN:
        elif self.__state == c.state_HIDDEN:
            self.me.set_color(c.Z_HIDDEN)#--------------------------------------
            # is inside player's range - run away:
            if not self.is_safe():
                self.__steering.hide_on = True
                self.__state = c.state_RUN
            # is safe - stay where you are and wait for an ocassion to move:
            else:
                # take risk:
                if self.__risk_timer <= 0:
                    self.__steering.wandern_on = True
                    self.__state = c.state_IDLE
                # keep calm and stay hidden:
                self.__steering.obstacle_avoidance_on = False
                self.__steering.wall_avoidance_on = False
                self.me.velocity.reset()
                self.__risk_timer -= 1


        # state ATTACK:
        elif self.__state == c.state_ATTACK:
            self.me.set_color(c.Z_ATTACK)#--------------------------------------
            pass


        # calculate vehicle position based on steering forces: =================
        self.__steering_force = self.__steering.calculate()
        # Acceleration = Force / Mass:
        acceleration = self.__steering_force.mult(self.me.mass_inv())
        # update velocity:
        self.me.velocity.add(acceleration.mult(self.__time_elapsed))
        self.me.velocity.trunc(self.me.max_speed())
        # update position:
        self.me.pos.add(zrc.mult_vector(self.me.velocity, self.__time_elapsed))
        # check collisions: ====================================================
        # check collisions with game world borders: #-----------------------------------------------------------
        if self.me.pos.x < self.__borders[0]: self.me.pos.x = self.__borders[0]
        elif self.me.pos.x > self.__borders[1]: self.me.pos.x = self.__borders[1]
        if self.me.pos.y < self.__borders[2]: self.me.pos.y = self.__borders[2]
        elif self.me.pos.y > self.__borders[3]: self.me.pos.y = self.__borders[3]
        # check collisions with player:
        self.me.pos.x, self.me.pos.y = zrc.avoid_collision(
                                                            (self.__player.me.pos.x,
                                                             self.__player.me.pos.y,
                                                             self.__player.me.radius()),
                                                            (self.me.pos.x,
                                                             self.me.pos.y,
                                                             self.me.radius())
                                                          )
        # check collisions with other zombies:
        for z in self.__zombies:
            if z.ID == self.ID:
                continue
            self.me.pos.x, self.me.pos.y = z.avoid_collision((
                                                                self.me.pos.x,
                                                                self.me.pos.y,
                                                                self.me.radius()
                                                            ))

        # check collision with Closest Intersecting Obstacle:
        self.proj = None

        if (self.__steering.CIO != None and
            self.__steering.CIO.is_collided(self.me.get_collision_info())):
            # get distance vector from zombie to intersecting obstacle:
            to_obst = zrc.sub_vectors(self.__steering.CIO.center, self.me.pos)
            # to_obst.print_v("to_obst")
            # project zombie velocity to to_obst vector:
            self.proj = zrc.proj_vector(self.me.velocity, to_obst)

            self.proj = self.proj.mult(2)

            # self.me.velocity.print_v("velocity")
            # self.proj.print_v("proj")
            # substract proj from zombie velocity:
            self.me.velocity.sub(self.proj)
            # self.me.velocity.print_v("velocity after")
            # --------------------------------------------------- DEBUG ------------
            self.__steering.CIO.set_color(c.DARKYELLOW)
            # --------------------------------------------------- DEBUG ------------


        # update heading if zombie has a velocity greater than a very small value:
        if self.me.velocity.magn() > 0.0000001:
            self.me.heading = self.me.velocity.norm()
            self.me.side = self.me.heading.perp()


    #===========================================================================
    # All draw methods: ========================================================
    """ Draws zombie bot """
    def draw(self):
        pygame.draw.circle( self.__screen,
                            self.me.color(),
                            self.me.get_position(),
                            self.me.radius(),
                            2)


    """ DEBUG - draws debug info """
    def draw_debug(self):
        # draw distance line to player:
        self.draw_line(self.debug_color, self.me.pos, self.get_player().me.pos)
        # # draw target point for wandern behaviour:
        # pygame.draw.circle(self.__screen,
        #                    c.RED,
        #                    (
        #                         int(self.__steering.target_world.x),
        #                         int(self.__steering.target_world.y)
        #                    ),
        #                    3, 1)
        # draw best hiding spot:
        if self.__state == c.state_RUN:
            pygame.draw.circle(self.__screen,
                               c.DARKYELLOW,
                               (
                                    int(self.__steering.bhs.x),
                                    int(self.__steering.bhs.y)
                               ),
                               5, 3)


    """ DEBUG - draws vectors """
    def draw_vectors(self):
        # # draw heading vector:
        # self.draw_line(c.ORANGE,
        #                self.me.pos,
        #                zrc.add_vectors(self.me.pos, zrc.mult_vector(self.me.heading, 30)))
        # # draw side vector:
        # self.draw_line(c.DARKYELLOW,
        #                self.me.pos,
        #                zrc.add_vectors(self.me.pos, zrc.mult_vector(self.me.side, 10)))

        # draw steering force:
        # self.draw_line(c.CYAN,
        #                self.me.pos,
        #                zrc.add_vectors(self.me.pos, zrc.mult_vector(self.__steering_force, 10)))

        # draw ALL steering forces:
        self.draw_line(c.CYAN,
                       self.me.pos,
                       zrc.add_vectors(self.me.pos,
                                       self.__steering.obstacle_avoidance_force))
        self.draw_line(c.ORANGE,
                       self.me.pos,
                       zrc.add_vectors(self.me.pos,
                                       self.__steering.wandern_force))
        self.draw_line(c.DARKYELLOW,
                       self.me.pos,
                       zrc.add_vectors(self.me.pos,
                                       self.__steering.hide_force))

        # self.draw_line(c.CYAN,
        #                self.me.pos,
        #                zrc.add_vectors(self.me.pos,
        #                                zrc.mult_vector(self.__steering.obstacle_avoidance_force, 10)))
        # self.draw_line(c.ORANGE,
        #                self.me.pos,
        #                zrc.add_vectors(self.me.pos,
        #                                zrc.mult_vector(self.__steering.wandern_force, 10)))
        # self.draw_line(c.DARKYELLOW,
        #                self.me.pos,
        #                zrc.add_vectors(self.me.pos,
        #                                zrc.mult_vector(self.__steering.hide_force, 10)))



        # draw to_obst and proj vectors:
        # if self.__steering.CIO != None and self.proj != None:
        #     self.draw_line(c.LIGHTGREY,
        #                    self.me.pos,
        #                    self.__steering.CIO.center)
        #     self.draw_line(c.RED,
        #                    self.me.pos,
        #                    zrc.add_vectors(self.me.pos, zrc.mult_vector(self.proj, 10)))




    """ Draws single line """
    def draw_line(self, color, a, b):
        pygame.draw.line(self.__screen, color, (a.x, a.y), (b.x, b.y))
    #===========================================================================
