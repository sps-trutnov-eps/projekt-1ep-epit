import sys
import random
import pygame
pygame.init()

rozliseni_okna = (1280, 960)
okno = pygame.display.set_mode(rozliseni_okna)
hrac_x=5
hrac_y=5
timer=0
rychlost_x=0
rychlost_y=0
posledni=2
hrac=[-10]
y=0
jidlo=random.randint(0,191)
while True:
    for udalost in pygame.event.get():
        if udalost.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    stisknute_klavesy = pygame.key.get_pressed()
    if stisknute_klavesy[pygame.K_w]:
        posledni=1
    elif stisknute_klavesy[pygame.K_d]:
        posledni=2
    elif stisknute_klavesy[pygame.K_s]:
        posledni=3
    elif stisknute_klavesy[pygame.K_a]:
        posledni=4
    if timer==100:
        timer=0
        if posledni==1:
            hrac_y-=1
        elif posledni==2:
            hrac_x+=1
        elif posledni==3:
            hrac_y+=1
        else:
            hrac_x-=1
        for i in range(len(hrac)):
            if hrac_x+hrac_y*16==hrac[i-1] or not -1<hrac_x<17 or not -1<hrac_y<13:
                print("prohra")
        if len(hrac)>50:
            print("výhra")
        hrac.append(hrac_x+hrac_y*16)
        if jidlo==hrac_x+hrac_y*16:
            jidlo=random.randint(0,191)
            while y!=len(hrac):
                if jidlo==hrac[y]:
                    jidlo=random.randint(0,191)
                    y=0
                else:
                    y+=1
            y=0
        else:
            hrac.remove(hrac[0])
    timer+=1
    okno.fill((255,255,255))
    for i in range(len(hrac)):
        pygame.draw.rect(okno,(100,100,100),((hrac[i-1]%16)*80,(hrac[i-1]-hrac[i-1]%16)/16*80,80,80))
    pygame.draw.rect(okno,(255,0,0),((jidlo%16)*80,(jidlo-jidlo%16)/16*80,80,80))
    pygame.draw.rect(okno,(0,0,0),(hrac_x*80,hrac_y*80,80,80))
    pygame.display.update()

