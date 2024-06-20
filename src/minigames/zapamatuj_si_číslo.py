import sys
import random
import pygame
import minigames.minigame_base as mini

def mini_memory():
    rozliseni_okna = mini.mini_surface.get_size()

    napsano=""
    napsano2=""
    vybrane=random.randint(1,4)
    font=pygame.font.Font(None, 128)
    text1=font.render("π = 3,141", True, (0, 0, 0))
    text2=font.render("G = 6,674*10^-11", True, (0, 0, 0))
    text3=font.render("√2 = 1,414", True, (0, 0, 0))
    text4=font.render("1AU = 150*10^9 m", True, (0, 0, 0))
    timer=0
    while True:
        stisknute_klavesy = pygame.key.get_pressed()
        mini.mini_surface.fill((255,255,255)) 
        for udalost in pygame.event.get():
            if udalost.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if udalost.type==pygame.KEYUP:
                if stisknute_klavesy[pygame.K_BACKSPACE]:
                    if len(napsano2)==0:
                        napsano=napsano[:-1]
                    if len(napsano2)!=0:
                        napsano2=napsano2[:-1]
                else :
                    if vybrane!=4:
                        if len(napsano)>4 and vybrane==2:
                            napsano2=napsano2+str(udalost.unicode)
                        if len(napsano)<5:
                            napsano=napsano+str(udalost.unicode)
                    if vybrane==4:
                        if len(napsano)>2:
                            napsano2=napsano2+str(udalost.unicode)
                        if len(napsano)<3:
                            napsano=napsano+str(udalost.unicode)
        if timer==0:
            mini.mini_surface.blit(text1, (315,100))
            mini.mini_surface.blit(text2, (315,200))
            mini.mini_surface.blit(text3, (315,300))
            mini.mini_surface.blit(text4, (315,400))
        if timer==1:
            text4=font.render("1AU =    150*10^9    m", True, (0, 0, 0))
            if vybrane==1:
                mini.mini_surface.blit(text1, (315,500))
            if vybrane==2:
                mini.mini_surface.blit(text2, (315,500))
            if vybrane==3:
                mini.mini_surface.blit(text3, (280,500))
            if vybrane==4:
                mini.mini_surface.blit(text4, (200,500))
            pygame.draw.rect(mini.mini_surface,(0,0,0),(462,498,236,104))
            pygame.draw.rect(mini.mini_surface,(255,255,255),(465,500,230,100))
            if vybrane==2 or vybrane==4:
                pygame.draw.rect(mini.mini_surface,(0,0,0),(877,498,136,104))
                pygame.draw.rect(mini.mini_surface,(255,255,255),(880,500,130,100))
        text=font.render(napsano,True, (0,0,0))    
        mini.mini_surface.blit(text,(465,500))
        text=font.render(napsano2,True, (0,0,0))
        mini.mini_surface.blit(text,(880,500))
        if pygame.mouse.get_pressed()[0]:
            timer=1
        
        if vybrane==1:
            if napsano=="3,141":
                return mini.win_minigame()
        if vybrane==2:
            if napsano=="6,674" and napsano2=="-11":
                return mini.win_minigame()
        if vybrane==3:
            if napsano=="1,414":
                return mini.win_minigame()
        if vybrane==4:
            if napsano=="150" and napsano2=="9":
                return mini.win_minigame()

        mini.mini_frame()

        pygame.display.update()

