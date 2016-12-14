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
    def __init__(self, screen, level, level_borders, rage_manager, player, zombie_list, ID, pos):
        self.__screen = screen                  # game display handler
        self.__level = level                    # Level handler
        self.__borders = level_borders          # space where zombies can wandern
        self.__rm = rage_manager                # RageManager object
        self.__player = player                  # Player handler
        self.__zombies = zombie_list            # list of all zombies
        self.__time_elapsed = c.time_elapsed    # time elapsed
        self.ID = ID                            # ID number
        self.is_dead = False                    # is zombie dead?
        self.rage_on = False                    # is rage mode on?
        self.zombie_mates = []                  # list of ombies in neighbourhood
        self.__attack_cooldown = c.FPS          # attack cooldown timer
        self.__state = c.state_IDLE             # current zombie FSM state
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
        self.__key_x = int(self.me.pos.x / 100)                         # x coordinate key
        self.__key_y = int(self.me.pos.y / 100)                         # y coordinate key
        # add self to gw_space dictionary:
        self.__rm.gw_space[self.__key_x][self.__key_y].append(self)


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


    """ Removes self from list related to current position area in game world """
    def remove_from_game_world(self):
        self.__rm.gw_space[self.__key_x][self.__key_y].remove(self)


    """ Creates list of zombie's neighbours """
    def tag_neighbours(self):
        self.zombie_mates = []
        # tag zombies from your neighbourhood:
        for kx in range(self.__key_x - 1, self.__key_x + 2):
            if kx in self.__rm.gw_space:
                for ky in range(self.__key_y - 1, self.__key_y + 2):
                    if ky in self.__rm.gw_space[kx]:
                        for z in self.__rm.gw_space[kx][ky]:
                            if z.ID != self.ID:
                                dist = self.me.pos.dist_to_vector(z.me.pos)
                                if dist <= self.__rm.rage_circle:
                                    self.zombie_mates.append(z)


    """ Adjust position of zombies so as they don't intersect with each other """
    def enforce_non_penetration_constraint(self):
        # go through all zombies from your neighbourhood:
        for z in self.zombie_mates:
            # calculate the distance between self and zombie agent:
            to_agent = z.me.pos.sub_copy(self.me.pos)
            dist_to_agent = to_agent.magn()
            # if dist_to_agent is smaller than the sum of their radii then this
            # zombie must be moved away in the direction parallel to the
            # to_agent vector:
            overlap = self.me.radius() + z.me.radius() - dist_to_agent
            if overlap >= 0:
                # move the entity a distance away equivalent to the amount of overlap:
                z.me.pos.add(to_agent.mult(overlap / dist_to_agent))


    #===========================================================================
    # FSM transition functions: ================================================
    """ Transition function A - can attack? """
    def can_attack(self):
        # there're enough zombies to go wild rage mode:
        if len(self.zombie_mates) + 1 >= self.__rm.rage_team:
            self.rage_on = True
            for z in self.zombie_mates:
                z.rage_on = True


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
        # tag all current neighbours:
        self.tag_neighbours()
        # check conditions for rage mode:
        if not self.rage_on:
            self.can_attack()
        # rage mode is on:
        if self.rage_on:
            self.me.set_color(c.RAGERED)
            self.__state = c.state_ATTACK

        # check conditions in Finite State Mashine: ============================
        # state IDLE: - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        if self.__state == c.state_IDLE:
            self.__steering.wandern_w = c.w_wandern
            # is inside player's range - run away:
            if not self.is_safe():
                self.__steering.hide_on = True
                self.__state = c.state_RUN
            # is safe - wandern:
            else:
                self.__steering.wandern_on = True
        # state RUN: - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        elif self.__state == c.state_RUN:
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
        # state HIDDEN: - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        elif self.__state == c.state_HIDDEN:
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
        # state ATTACK: - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        elif self.__state == c.state_ATTACK:
            self.__steering.seek_on = True
            self.__attack_cooldown -= 1
            # hurt player if he's whiting your range:
            if (self.me.pos.dist_to_vector(self.__player.me.pos) < c.contact_distance
                and self.__attack_cooldown <= 0):
                self.__player.health -= c.zombie_damage
                self.__attack_cooldown = c.FPS
            # if player is dead your job is done - do some other stuff:
            if self.__player.health <= 0:
                self.__state = c.state_IDLE

        # calculate vehicle position based on steering forces: =================
        self.__steering_force = self.__steering.calculate()
        # Acceleration = Force / Mass:
        acceleration = self.__steering_force.mult(self.me.mass_inv())
        # update velocity:
        self.me.velocity.add(acceleration.mult(self.__time_elapsed))

        # check collision with Closest Intersecting Obstacle:
        self.proj = None
        if (self.__steering.CIO != None and
            self.__steering.CIO.is_collided(self.me.get_collision_info())):
            # get distance vector from zombie to intersecting obstacle:
            to_obst = self.__steering.CIO.center.sub_copy(self.me.pos)
            # project zombie velocity to to_obst vector:
            self.proj = zrc.proj_vector(to_obst, self.me.velocity)
            # substract proj from zombie velocity:
            self.me.velocity.sub(self.proj)

        self.me.velocity.trunc(self.me.max_speed())
        # update position:
        self.me.pos.add(self.me.velocity.mult_copy(self.__time_elapsed))

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
        self.enforce_non_penetration_constraint()

        # update heading if zombie has a velocity greater than a very small value:
        if self.me.velocity.magn() > 0.0000001:
            self.me.heading = self.me.velocity.norm()
            self.me.side = self.me.heading.perp()

        # update gw_space dictionary if needed:
        kx = int(self.me.pos.x / 100)
        ky = int(self.me.pos.y / 100)
        if kx != self.__key_x or ky != self.__key_y:
            self.__rm.gw_space[self.__key_x][self.__key_y].remove(self)
            self.__key_x, self.__key_y = kx, ky
            self.__rm.gw_space[self.__key_x][self.__key_y].append(self)


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
        # draw rage neighbour distance circle:
        pygame.draw.circle( self.__screen,
                            c.ORANGE,
                            self.me.get_position(),
                            c.rage_neighbour_distance,
                            1)
        # draw best hiding spot:
        if self.__state == c.state_RUN:
            pygame.draw.circle(self.__screen,
                               c.DARKYELLOW,
                               (
                                    int(self.__steering.bhs.x),
                                    int(self.__steering.bhs.y)
                               ),
                               5, 3)
        """ DRAW VECTORS """
        # draw heading vector:
        self.draw_line(c.ORANGE,
                       self.me.pos,
                       self.me.pos.add_copy(self.me.heading.mult_copy(20)))
        # draw side vector:
        self.draw_line(c.DARKYELLOW,
                       self.me.pos,
                       self.me.pos.add_copy(self.me.side.mult_copy(20)))
        # draw velocity:
        self.draw_line(c.GREEN,
                       self.me.pos,
                       self.me.pos.add_copy(self.me.velocity.mult_copy(10)))
        # draw steering force:
        self.draw_line(c.CYAN,
                       self.me.pos,
                       self.me.pos.add_copy(self.__steering_force))
        # draw ALL steering forces:
        self.draw_line(c.BLUE,
                       self.me.pos,
                       self.me.pos.add_copy(self.__steering.obstacle_avoidance_force))


    """ Draws single line """
    def draw_line(self, color, a, b):
        pygame.draw.line(self.__screen, color, (a.x, a.y), (b.x, b.y))
    #===========================================================================
