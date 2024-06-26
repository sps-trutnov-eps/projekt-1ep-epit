import sys
import random
import pygame
import minigames.minigame_base as mini

def mini_kolecko():
    rozliseni_okna = mini.mini_surface.get_size()

    misto_x=0
    misto_y=0
    body=0
    timer=0
    while True:
        for udalost in pygame.event.get():
            if udalost.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        stisknute_klavesy = pygame.key.get_pressed()
        if misto_x==0 and misto_y==0:
            misto_x=random.randint(0,1180)
            misto_y=random.randint(0,860)
        if pygame.mouse.get_pressed()[0] and timer==0:
            mys=pygame.mouse.get_pos()
            if (((mys[1]-misto_y-50)**2+(mys[0]-misto_x-50)**2)*(1/2))<1250:
                body+=1
                misto_x=0
                misto_y=0
            else:
                body-=1
            if body==10:
                return mini.win_minigame()
        if pygame.mouse.get_pressed()[0]:
            timer=2
        if timer>0:
            timer-=1
        mini.mini_surface.fill((255,255,255))
        mini.mini_frame()
        pygame.draw.ellipse(mini.mini_surface,(0,0,0),(misto_x,misto_y,100,100))
        pygame.display.update()