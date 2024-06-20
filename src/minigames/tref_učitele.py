import sys
import random
import pygame
import minigame_base as mini

rozliseni_okna = mini.mini_surface.get_size()

def mini_terf():
    mys=(-10,-10)
    hlava_x=250
    timer=0
    smer=0
    while True:
        for udalost in pygame.event.get():
            if udalost.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        nahodny=random.randint(1,200)
        if nahodny==1:
            smer=random.randint(-1,1)
        #dodělat vzhled
        
        
        
        
        if timer==0 and pygame.mouse.get_pressed()[0]:
            mys=pygame.mouse.get_pos()
            timer=200
        if timer==1:

            if (((mys[1]-530)**2+(mys[0]-hlava_x-50)**2)*(1/2))<1250:
                print("trefa")
            else:
                print("netrefa")
        
        if timer!=0:
            timer-=1
        if 200<hlava_x+smer<1000:
            hlava_x+=smer/2
        mini.mini_surface.fill((255,255,255)) 
        pygame.draw.ellipse(mini.mini_surface,(0,0,0),(hlava_x,rozliseni_okna[1]/2,100,100))
        pygame.draw.ellipse(mini.mini_surface,(100,100,100),(mys[0]-timer/2,mys[1]-timer/2,timer,timer))
        pygame.display.update()

