import sys
import random
import pygame
import minigames.minigame_base as mini

rozliseni_okna = mini.mini_surface.get_size()

def mini_simon():
    vybrano=0
    mys=(0,0)
    rada=[1]
    x=0
    timer=0
    barva=255
    y=0
    z=0
    pygame.draw.rect(mini.mini_surface,(0, barva,0),(0,0,rozliseni_okna[0]/2,rozliseni_okna[1]/2))
    pygame.draw.rect(mini.mini_surface,(barva,0,0),(rozliseni_okna[0]/2,0,rozliseni_okna[0]/2,rozliseni_okna[1]/2))
    pygame.draw.rect(mini.mini_surface,(barva,barva,0),(0,rozliseni_okna[1]/2,rozliseni_okna[0]/2,rozliseni_okna[1]/2))
    pygame.draw.rect(mini.mini_surface,(0,0,barva),(rozliseni_okna[0]/2,rozliseni_okna[1]/2,rozliseni_okna[0]/2,rozliseni_okna[1]/2))
    while True:
        for udalost in pygame.event.get():
            if udalost.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        nahodny=random.randint(1,4)
        if y==-1:
            if pygame.mouse.get_pressed()[0]:
                mys=pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]
                if 0<mys[0]<640 and 0<mys[1]<480:
                    vybrano=1
                if 640<mys[0]<1280 and 0<mys[1]<480:
                    vybrano=2
                if 0<mys[0]<640 and 480<mys[1]<960:
                    vybrano=3
                if 640<mys[0]<1280 and 480<mys[1]<960:
                    vybrano=4
                if timer==0:
                    if vybrano==rada[x]:
                        x+=1
                    if x==len(rada):
                        y=0
                        rada.append(nahodny)
                        x=0
                    if vybrano!=rada[x] and vybrano!=rada[x-1] and x!=0:
                        x=0
                        y=0
                        print("chyba")
                
                timer=2
        if timer>0:
            timer-=1
            
        if y!=-1:
            if z==0:
                barva-=1
                if barva==0:
                    z=1
            if z==1 and barva<255:
                barva+=1
                if barva==255:
                    y+=1
                    z=0
                    if y==len(rada):
                        y=-1
        if rada[y]==1:
            pygame.draw.rect(mini.mini_surface,(0, barva,0),(0,0,rozliseni_okna[0]/2,rozliseni_okna[1]/2))
        elif rada[y]==2:
            pygame.draw.rect(mini.mini_surface,(barva,0,0),(rozliseni_okna[0]/2,0,rozliseni_okna[0]/2,rozliseni_okna[1]/2))
        elif rada[y]==3:
            pygame.draw.rect(mini.mini_surface,(barva,barva,0),(0,rozliseni_okna[1]/2,rozliseni_okna[0]/2,rozliseni_okna[1]/2))
        elif rada[y]==4:
            pygame.draw.rect(mini.mini_surface,(0,0,barva),(rozliseni_okna[0]/2,rozliseni_okna[1]/2,rozliseni_okna[0]/2,rozliseni_okna[1]/2))
        pygame.display.update()

