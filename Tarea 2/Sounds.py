# coding=utf-8
import pygame
from constants import *
class Sounds:

    def __init__(self):
        self.collide = pygame.mixer.Sound(sound_collide)
        self._sound_laser = pygame.mixer.Sound(laser_sound)

    def block_collide(self):
        self.collide.play(0)

    def wall(self):
        self.collide.play(0)

    def laser(self):
        self._sound_laser.play(0)
