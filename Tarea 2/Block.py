from constants import *
from centered_figure import *
import copy
import pygame
import random
class Block:

    def __init__(self,center,surface,color,hp,fuente):
        self.center = copy.copy(center)
        if color == (0, 0, 255):
            self.color = COLOR_blue
        else:
            self.color = random.choice([COLOR_orange, COLOR_purple, COLOR_red])
        self.figure = CenteredFigure(
            [(-34, 34), (34, 34), (34, -34), (-34, -34)], center=self.center,
            color=self.color, pygame_surface=surface)
        self.hp = hp
        self.fuente = fuente
        self.surface = surface

    def draw(self):
        Verts = self.figure.get_vertices()
        self.figure.draw()
        pygame.draw.rect(self.surface, COLOR_black,(Verts[3][0]+2,Verts[3][1]+2,65,65))
        text = self.fuente.render(str(self.hp), 1, COLOR_white)
        self.surface.blit(text,(self.center[0]-10,self.center[1]-10))

    def decrease_hp(self):
        self.hp -= 1
    def get_hp(self):
        return self.hp
