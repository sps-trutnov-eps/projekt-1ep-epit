import sys
import random
import pygame

def piano(screen: pygame.Surface):
    barva=(255,0,0)
    timer=0
    score=0
    vyhra=0
    rozliseni_okna = (1280, 960)
    ctverec_x=400
    ctverec_y=200
    rychlost=0.5
    pozice_padu=0
    font=pygame.font.Font(None, 128)
    text1=font.render("H", True, (0, 0, 0))
    text2=font.render("J", True, (0, 0, 0))
    text3=font.render("K", True, (0, 0, 0))
    text4=font.render("L", True, (0, 0, 0))
    while True:
        stisknute_klavesy = pygame.key.get_pressed()
        text5=font.render(str(score), True, (0,0,0,))
        
        pozice_padu=random.randint(0,3)
        for udalost in pygame.event.get():
            if udalost.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        if timer==0:
            if ctverec_y+100>rozliseni_okna[1] or (stisknute_klavesy[pygame.K_h] and (ctverec_x!=400 or 0<ctverec_y<600)) or (stisknute_klavesy[pygame.K_j] and (ctverec_x!=500 or 0<ctverec_y<600)) or (stisknute_klavesy[pygame.K_k] and (ctverec_x!=600 or 0<ctverec_y<600)) or (stisknute_klavesy[pygame.K_l] and (ctverec_x!=700 or 0<ctverec_y<600)):
                ctverec_y=-100
                score=0
                rychlost=0.5
                timer=200
                ctverec_x=400+100*pozice_padu
                #prohra
        ctverec_y+=rychlost
        if rozliseni_okna[1]>ctverec_y>rozliseni_okna[1]-100 or rozliseni_okna[1]>ctverec_y+100>rozliseni_okna[1]-100:
            if (stisknute_klavesy[pygame.K_h] and ctverec_x==400)or (stisknute_klavesy[pygame.K_j] and ctverec_x==500) or (stisknute_klavesy[pygame.K_k] and ctverec_x==600) or (stisknute_klavesy[pygame.K_l] and ctverec_x==700):
                ctverec_x=400+100*pozice_padu
                ctverec_y=-100
                score+=1
                if rychlost<2:
                    rychlost+=0.2
                timer=200
                barva=(0,255,0)
                
        if timer!=0:
            timer-=1
        screen.fill((255, 255, 255))
        if timer==0:
            barva=(255,0,0)
        if score>10 and vyhra==0:
            return mini.win_minigame()
        pygame.draw.rect(screen,barva, (0, rozliseni_okna[1]-100, rozliseni_okna[0],100))
        pygame.draw.rect(screen, (0, 0, 0), (ctverec_x, ctverec_y, 100, 100))
        screen.blit(text1, (415, rozliseni_okna[1]-100))
        screen.blit(text2, (515, rozliseni_okna[1]-100))
        screen.blit(text3, (615, rozliseni_okna[1]-100))
        screen.blit(text4, (715, rozliseni_okna[1]-100))
        screen.blit(text5, (rozliseni_okna[0]/2-40, 100))
        pygame.display.update()
