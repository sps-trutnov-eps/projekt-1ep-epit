import sys
import random
import pygame
pygame.init()
score=0
rozliseni_okna = (1280, 960)
kola=[]
x=0
y=0
for i in range(10):
    kola.append(random.randint(50,1230))
    kola.append(random.randint(50,910))
    kola.append(random.randint(50,100))
okno = pygame.display.set_mode(rozliseni_okna)


while True:
    for udalost in pygame.event.get():
        if udalost.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    stisknute_klavesy = pygame.key.get_pressed()
    if pygame.mouse.get_pressed()[0]:
        mys=pygame.mouse.get_pos()
        for i in range(10):
            if (((mys[1]-kola[i*3+1]-kola[i*3+2]/2)**2+(mys[0]-kola[i*3]-kola[i*3+2]/2)**2)*(1/2))<kola[i*3+2]**2/8 and x==0:
                kola[i*3]=random.randint(50,1230)
                kola[i*3+1]=random.randint(50,910)
                kola[i*3+2]=random.randint(50,100)
                score+=1
            else:
                y+=1
        if y==10:
            x=1
    else:
        x=0
    y=0
    for i in range(10):
        if kola[i*3+2]<0:
            if score>50:
                print("výhra")
            else:
                print("proha")
    kola[random.randint(0,9)*3+2]-=score**(2/3)/100
    okno.fill((255,255,255))
    for i in range(10):
        pygame.draw.ellipse(okno,(0,0,0),(kola[i*3],kola[i*3+1],kola[i*3+2],kola[i*3+2]))
    pygame.display.update()
    

y=7
x=9