#!/usr/bin/python
#-*- coding: utf-8 -*-


""" Class that coordinate zombie bots in game """
class ZombiePool:
    """ Constructor """
    def __init__(self, zombieAmount):
        self.__zombieAmount = zombieAmount  # finite bots amount
