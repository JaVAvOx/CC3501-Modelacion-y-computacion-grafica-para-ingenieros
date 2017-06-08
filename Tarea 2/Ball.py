# coding=utf-8
import pygame
import random
import copy
import math
from centered_figure import *
from constants import *


class Ball:

    def __init__(self,center,surface,blocks, power_ups, sounds,variables,tipo):

        self.tipo = tipo
        self.center = copy.copy(center)
        self.blocks = blocks
        self.pups = power_ups
        self.sounds = sounds
        if tipo == 1:
            color = COLOR_white
        elif tipo == 2:
            color = COLOR_magenta
        elif tipo == 3:
            color = COLOR_blue
        if tipo == 1:
            self.figure = CenteredFigure(
                [(-2, 2), (2, 2), (2, -2), (-2, -2)], center=self.center,
                color=color, pygame_surface=surface)
        elif tipo == 2:
            self.figure = CenteredFigure(
                [(0, 2), (2, -2), (-2, -2)], center=self.center,
                color=color, pygame_surface=surface)
        elif tipo == 3:
            self.figure = CenteredFigure(
                [(0, -2), (2, 2), (-2, 2)], center=self.center,
                color=color, pygame_surface=surface)
        self.figure.scale(3)
        self.floor = True
        self.variables = variables
        self.surface = surface
        self.vel = [0,0]
        self.acc = False

    def draw(self):
        self.figure.draw()

    def setVel(self,tupla):
        Y = self.center[1] - tupla[1]
        X = tupla[0] - self.center[0]
        B = math.atan2(Y,X)
        self.vel[0] = math.cos(B)*5
        self.vel[1] = -math.sin(B)*5

    def getSuelo(self):
        return self.center[1] == altura_piso-3

    def move(self):
        self.center[0] = self.center[0] + self.vel[0]
        self.center[1] = self.center[1] + self.vel[1]


        if self.center[1] < altura_techo:
            self.center[1] = altura_techo
            self.vel[1] *= -1

        if self.center[1] > altura_piso-3:
            self.center[1] = altura_piso-3
            self.vel[0] = 0
            self.vel[1] = 0

            if not self.variables.position_s:
                self.variables.pointer_init = self.center[0]
                self.variables.position_s = True
        if self.center[0] < 0:
            self.center[0] = 0
            self.vel[0] *= -1

        if self.center[0] > WS - 3:
            self.center[0] = WS -3
            self.vel[0] *= -1



        for block in self.blocks:
            if self.figure.collide(block.figure):
                V = block.figure.get_vertices()
                if self.center[1]<V[1][1] and self.center[1]>V[2][1]:
                    self.vel[0] *= -1
                    self.sounds.block_collide()
                    if self.center[0] > V[1][0]:
                        self.center[0] = V[1][0] + 6
                    elif self.center[0] < V[0][0]:
                        self.center[0] = V[0][0] - 6
                    if block.get_hp() > 1:
                        block.decrease_hp()
                        block.draw()
                        break
                    else:
                        self.blocks.remove(block)
                        break

                elif self.center[0]>V[0][0] and self.center[0]<V[1][0]:
                    self.vel[1] *= -1
                    self.sounds.block_collide()
                    if self.center[1] <= V[2][1]:
                        self.center[1] = V[2][1] - 7
                    elif self.center[1] >= V[0][1]:
                        self.center[1] = V[0][1] + 7

                    if block.get_hp() > 1:
                        block.decrease_hp()
                        block.draw()
                        break
                    else:
                        self.blocks.remove(block)
                        break

        for pup in self.pups:
            if self.figure.collide(pup.figure):
                pup.activate()
                if pup.get_type() == 0:
                    pup_center = pup.figure.get_center()
                    pygame.draw.line(self.surface, laser_color, [0,pup_center[1]],
                                     [WS, pup_center[1]], 3)
                    self.sounds.laser()

                    for block in self.blocks:
                        if block.center[1] == pup_center[1]:
                            if block.get_hp() > 1:
                                block.decrease_hp()
                            else:
                                self.blocks.remove(block)
                elif pup.get_type() == 1:
                    pup_center = pup.figure.get_center()
                    pygame.draw.line(self.surface, laser_color,
                        [pup_center[0],altura_techo],[pup_center[0], altura_piso],3)
                    self.sounds.laser()

                    for block in self.blocks:
                        if block.center[0] == pup_center[0]:
                            if block.get_hp() > 1:
                                block.decrease_hp()
                            else:
                                self.blocks.remove(block)


                elif pup.get_type() == 2:
                    theta = math.radians(random.randint(0,359))
                    self.center[1]-=20
                    self.vel[0] = math.cos(theta)*5
                    self.vel[1] = math.sin(theta)*5

                elif pup.get_type() == 3:
                    self.pups.remove(pup)
                    self.variables.extra_ball_c += 1
