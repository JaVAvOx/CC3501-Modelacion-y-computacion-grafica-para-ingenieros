from constants import *
from centered_figure import *
import pygame
import copy

class PowerUp:

    def __init__(self,center,surface,tipo,font):
        self.center = copy.copy(center)
        if tipo == 0: #horizontal laser
            self.figure = CenteredFigure([(-10,0),(0,10),(10,0),(0,-10)],
            center = self.center,color = laser_color, pygame_surface = surface)
            self.letter = 'H'
        elif tipo == 1: #vertical laser
            self.figure = CenteredFigure(
                [(-10, 0), (0, 10), (10, 0), (0, -10)],
                center=self.center, color=laser_color, pygame_surface=surface)
            self.letter = 'V'
        elif tipo == 2: #Bounce
            self.figure = CenteredFigure(
                [(-10, 0), (0, 10), (10, 0), (0, -10)],
                center=self.center, color=bounce_color, pygame_surface=surface)
            self.letter = 'B'
        elif tipo == 3: #Extra ball
            self.figure = CenteredFigure(
                [(-10, 0), (0, 10), (10, 0), (0, -10)],
                center=self.center, color=extraball_color, pygame_surface=surface)
            self.letter = 'E'
        self.surface = surface
        self.tipo = tipo
        self.active = False
        self.font = font

    def get_type(self):
        return self.tipo

    def get_center_pup(self):
        return self.center

    def draw(self):
        self.figure.draw()
        letter = self.font.render(self.letter,1,COLOR_black)
        self.surface.blit(letter,(self.center[0]-4,self.center[1]-7))

    def activate(self):
        if not self.active:
            self.active = True

    def status(self):
        return self.active
