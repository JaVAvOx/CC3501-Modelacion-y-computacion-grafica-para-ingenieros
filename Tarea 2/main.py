# coding=utf-8
import os
import random
from centered_figure import CenteredFigure
from constants import *
import pygame
from pygame.locals import *
import sys
from Ball import *
from Sounds import *
from Block import *
from Auxiliar import *
from PowerUp import *
import math




pygame.init()
os.environ['SDL_VIDEO_CENTERED'] = '1'
surface = pygame.display.set_mode((WS,HS))
pygame.display.set_caption("PPBlock")
state = 0
menu_state = 0
selected_ball = 1
clock = pygame.time.Clock()
sound = Sounds()
aux = Aux()
font1 = pygame.font.Font(FONT1, 45)  # Title
font2 = pygame.font.Font(FONT2, 35)  # Body
font3 = pygame.font.Font(FONT2, 35)  # Header in game
font = pygame.font.Font(FONT2, 15)  # Header in game
Blocks = list()
centroX = 35
centroY = altura_techo + 35
powerups = list()
balls = list()
position = tuple()
timer = 0
yc = 0
ball_selected = 1
lado_selected = 15
title = font1.render("PP-BLOCK", 1, COLOR_white)
img = pygame.image.load('credits.png')
obama = pygame.image.load('obama.png')




while True:
    clock.tick(60)
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if aux.get_mouse_state():
                position = pygame.mouse.get_pos()
                aux.generate = False
                for ball in balls:
                    ball.floor = False
                    ball.center[1] -= 5
                    ball.acc = False

                balls_down = False
                aux.mouse_state = False
                aux.position_s = False



        if keys[K_q]:
            exit()



        if state == 0:
            if keys[K_UP]:
                menu_state -= 1
                menu_state = menu_state % 4

            if keys[K_DOWN]:
                menu_state += 1
                menu_state = menu_state % 4

            if keys[K_LEFT]:
                if menu_state == 1:
                    if selected_ball != 1:
                        selected_ball -= 1
                    else:
                        selected_ball = 3
            if keys[K_RIGHT]:
                if menu_state == 1:
                    if selected_ball != 3:
                        selected_ball += 1
                    else:
                        selected_ball = 1


        if keys[K_RETURN]:
            if state == 0:
                if menu_state == 2:
                    state = 3
                if menu_state == 3:
                    exit()
                if menu_state == 0:
                    state = 1
                    aux.can_play = True

                    balls.append(Ball([WS/2,altura_piso-3],surface,Blocks,powerups,sound,aux,selected_ball))
                    for iteration in range(7):
                        pp = random.randint(1,4)
                        if centroX > 490:
                            centroX = 35
                        cen = [centroX,centroY]
                        if pp == 1 or pp == 2:
                            Blocks.append(Block(cen,surface,COLOR_red,aux.get_points_ammount(),font))
                            centroX += 70
                        if pp == 3:
                            t = random.randint(0,3)
                            powerups.append(PowerUp(cen,surface,t,font))
                            centroX += 70
                        else:
                            centroX += 70
                    centroX = 35
                    aux.generate = False
                    balls_down = True


        if keys[K_ESCAPE]:
            if state == 3:
                state = 0
                yc = 0

    if state == 0: # current: menu
        if menu_state == 0: # play selected
            surface.fill(COLOR_black)
            surface.blit(title, (66, 145))
            pygame.draw.rect(surface, COLOR_white, (193, 295, 98, 35), 0)
            play_button = font2.render("PLAY", 1, COLOR_black)
            ball_button = font2.render("SELECT BALL", 1, COLOR_white)
            credits_button = font2.render("CREDITS", 1, COLOR_white)
            exit_button = font2.render("QUIT", 1, COLOR_white)
            surface.blit(play_button, (201, 295))
            surface.blit(ball_button, (137, 340))
            surface.blit(credits_button, (180, 385))
            surface.blit(exit_button, (214, 430))

        if menu_state == 1:  # select ball selected
            surface.fill(COLOR_black)
            surface.blit(title, (66, 145))
            pygame.draw.rect(surface, COLOR_white, (126, 340, 280, 35), 0)
            play_button = font2.render("PLAY", 1, COLOR_white)
            if (selected_ball == 1):
                ball_button = font2.render("SELECT BALL: 1", 1, COLOR_black)
            elif (selected_ball == 2):
                ball_button = font2.render("SELECT BALL: 2", 1, COLOR_black)
            else:
                ball_button = font2.render("SELECT BALL: 3", 1, COLOR_black)
            credits_button = font2.render("CREDITS", 1, COLOR_white)
            exit_button = font2.render("QUIT", 1, COLOR_white)
            surface.blit(play_button, (201, 295))
            surface.blit(ball_button, (137, 340))
            surface.blit(credits_button, (180, 385))
            surface.blit(exit_button, (214, 430))

        if menu_state == 2:
            surface.fill(COLOR_black)
            surface.blit(title, (66, 145))
            pygame.draw.rect(surface, COLOR_white, (170, 385, 154, 35), 0)
            play_button = font2.render("PLAY", 1, COLOR_white)
            ball_button = font2.render("SELECT BALL", 1, COLOR_white)
            credits_button = font2.render("CREDITS", 1, COLOR_black)
            exit_button = font2.render("QUIT", 1, COLOR_white)
            surface.blit(play_button, (201, 295))
            surface.blit(ball_button, (137, 340))
            surface.blit(credits_button, (180, 385))
            surface.blit(exit_button, (214, 430))

        if (menu_state == 3): # QUIT selected
            surface.fill(COLOR_black)
            surface.blit(title, (66, 145))
            pygame.draw.rect(surface, COLOR_white, (209, 430, 78, 35), 0)
            play_button = font2.render("PLAY", 1, COLOR_white)
            ball_button = font2.render("SELECT BALL", 1, COLOR_white)
            credits_button = font2.render("CREDITS", 1, COLOR_white)
            exit_button = font2.render("QUIT", 1, COLOR_black)
            surface.blit(play_button, (201, 295))
            surface.blit(ball_button, (137, 340))
            surface.blit(credits_button, (180, 385))
            surface.blit(exit_button, (214, 430))



        pygame.display.update()


    if (state == 3): # Credits
        surface.fill(COLOR_black)
        surface.blit(img, (0, yc))
        yc -= 1
        if (yc == -730):
            yc = 660
        pygame.display.update()


    if state == 1: # Game
        timer += 1
        if not balls_down:
            i = 0
            for ball in balls:
                if ball.getSuelo():
                    i += 1
                    ball.center[0] = aux.pointer_init
                if i == len(balls):
                    aux.mouse_change()

                    aux.generate = True
                    balls_down = True

        if aux.generate and aux.mouse_state:

            aux.increase_points()
            balls.append(Ball([aux.pointer_init,altura_piso-3],surface,Blocks,powerups,sound,aux,selected_ball))
            counter = 0
            while counter < aux.extra_ball_c:
                balls.append(Ball([aux.pointer_init,altura_piso-3],surface,Blocks,powerups,sound,aux,selected_ball))
                counter += 1
            aux.extra_ball_c = 0
            for block in Blocks:
                block.center[1] += 70
            for pup in powerups:
                pup.center[1] += 70
                if pup.status():
                    powerups.remove(pup)

            var = aux.get_points_ammount()
            if var % 10 == 0:
                var *= 2
                new_color_ball = COLOR_blue
            else: new_color_ball = COLOR_red

            for iteration in range(7):
                p = random.randint(1,4)
                if centroX > 490:
                    centroX = 35
                cen = [centroX,centroY]
                if p == 1 or p == 2:
                    Blocks.append(Block(cen,surface,new_color_ball,var,font))
                    centroX += 70
                elif p == 3:
                    t = random.randint(0,3)
                    powerups.append(PowerUp(cen,surface,t,font))
                    centroX += 70
                else:
                    centroX += 70
            centroX = 35
            aux.generate = False



        for block in Blocks:
            if block.center[1] >= 600:
                aux.can_play = False
        if not aux.can_play:
            surface.fill(COLOR_black)
            gameover = font3.render('GAME OVER',1, COLOR_white)
            press = font3.render('Press Q to exit',1,COLOR_white)
            surface.blit(gameover, (WS / 2 - 95, HS / 2 - 60))
            surface.blit(press, (WS / 2 - 130, HS / 2 ))
            pygame.display.update()
        else:
            surface.fill(COLOR_black)
            pygame.draw.line(surface,COLOR_white,[0,altura_techo],[WS,altura_techo],2)
            pygame.draw.line(surface, COLOR_white, [0, altura_piso],
                             [WS, altura_piso], 2)
            text = font2.render('POINTS: '+str(aux.get_points_ammount()), 1, COLOR_white)
            q_for_quit = font2.render('Q = QUIT', 1, COLOR_white)
            surface.blit(text,(0,10))
            surface.blit(q_for_quit, (365, 10))
            surface.blit(obama, (aux.get_pointer()-54, 695))

            if aux.get_mouse_state():
                X = aux.pointer_init
                Y = altura_piso
                mx = pygame.mouse.get_pos()[0]
                my = pygame.mouse.get_pos()[1]
                pygame.draw.line(surface,COLOR_white,[X,Y-3],[mx,my],2)
            if timer%6 == 0 and not aux.get_mouse_state():
                for ball in balls:
                    if not ball.acc:
                        ball.setVel(position)
                        timer = 0
                        ball.acc = True
                        break
            for ball in balls:
                ball.move()
                ball.draw()
            for block in Blocks:
                if block.get_hp() <= 0:
                    Blocks.remove(block)
                else:
                    block.draw()
            for pup in powerups:
                if pup.center[1] >= 600:
                    powerups.remove(pup)
                else:
                    pup.draw()

            pygame.display.update()




