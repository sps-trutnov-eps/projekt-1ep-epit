import sys
import random
import pygame
import minigames.minigame_base as mini

def mini_multi():
    rozliseni_okna = mini.mini_surface.get_size()

    timer=1960
    napsano=""
    body=0
    cislo=""
    vysledek=0
    cisla=0
    hrac=265
    mic_x=300
    mic_y=200
    rychlost_x=0.45
    rychlost_y=-0.7
    font=pygame.font.Font(None, 100)
    while True:
        stisknute_klavesy = pygame.key.get_pressed()
        for udalost in pygame.event.get():
            if udalost.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if udalost.type==pygame.KEYUP:
                if stisknute_klavesy[pygame.K_BACKSPACE]:
                    napsano=napsano[:-1]
                else :
                    napsano=napsano+str(udalost.unicode)
        mys=pygame.mouse.get_pos()
        if 600<mic_x or mic_x<0:
            rychlost_x=rychlost_x*-1
        if mic_y<0:
            rychlost_y*=-1
        if 770<mic_y<790 and hrac-30<mic_x<hrac+100 and rychlost_y>0:
            rychlost_y*=-1
            rychlost_x=-(hrac-mic_x+35)/100
            body+=1
            timer+=50
        mic_x=mic_x+rychlost_x
        mic_y=mic_y+rychlost_y
        if 49<mys[0]<581:
            hrac=mys[0]-50
        if cislo=="":
            cisla=random.randint(0,200)
            cislo=cislo+str(cisla)
            vysledek=cisla
            if body%3==0:
                cislo=cislo+"-"
            else :
                cislo=cislo+"+"
            cisla=random.randint(0,200)
            cislo=cislo+str(cisla)
            if body%3==0:
                cisla=cisla*-1
            vysledek+=cisla
        if napsano==str(vysledek):
            body+=1
            cislo=""
            napsano=""
            timer=1960
        if timer>0:
            timer-=0.3
        else :
            return mini.fail_minigame()
        if mic_y>960:
            return mini.fail_minigame()
        if body>20 and cislo=="":
            return mini.win_minigame()
        mini.mini_surface.fill((255,255,255))
        pygame.draw.rect(mini.mini_surface,(0,0,0),(890,700,200,100))
        pygame.draw.rect(mini.mini_surface,(255,255,255),(895,705,190,90))
        text=font.render(napsano, True, (0, 0, 0))
        mini.mini_surface.blit(text,(910,710))
        text=font.render(cislo, True, (0, 0, 0))
        mini.mini_surface.blit(text,(900,200))
        mini.mini_frame()
        pygame.draw.ellipse(mini.mini_surface,(0,0,0),(mic_x,mic_y,30,30))
        pygame.draw.rect(mini.mini_surface,(0,0,0),(hrac,800,100,20))
        pygame.draw.rect(mini.mini_surface,(0,0,0),(630,0,20,970))
        pygame.draw.rect(mini.mini_surface,(100,100,100),(1260,960-timer/2,20,1050))
        pygame.display.update()