import sys
import pygame
import random
import time
pygame.init()
 
# Velikost okna
rozliseni_okna = (1000, 1000)
okno = pygame.display.set_mode(rozliseni_okna)
 
x_hrac = 740
y_hrac = 930
rychlost_hrace = 1.5

 
x_zem = 0
y_zem = 950
 
nep_y1 = 0
nep_y2 = 0
nep_y3 = 0
nep_y4 = 0
nep_y5 = 0
 
gravitace_1 = 0.01
gravitace_2 = 0.0035
gravitace_3 = 0.02
gravitace_4 = 0.0075
gravitace_5 = 0.02
 
nep_rychlost1 = 0
nep_rychlost2 = 0
nep_rychlost3 = 0
nep_rychlost4 = 0
nep_rychlost5 = 0
 
pozice_nep_x_1 = random.choice([50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800, 850, 900, 950])
pozice_nep_x_2 = random.choice([50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800, 850, 900, 950])
pozice_nep_x_3 = random.choice([50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800, 850, 900, 950])
pozice_nep_x_4 = random.choice([50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800, 850, 900, 950])
pozice_nep_x_5 = random.choice([50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800, 850, 900, 950])

x_zed = 0
y_zed = 0

x_zed2 = 980
y_zed2 = 0
 
# Časovač na 10 sekund
start_time = time.time()
timer_duration = 10
 
while True:
    # Ukončení hry po 10 sekundách
    current_time = time.time()
    elapsed_time = current_time - start_time
    if elapsed_time > timer_duration:
        pygame.quit()
        sys.exit()
 
    # Ovládání
    for udalost in pygame.event.get():
        if udalost.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
 
    # Logika
        
    stisknute_klavesy = pygame.key.get_pressed()
    if stisknute_klavesy[pygame.K_RIGHT]: 
        x_hrac += rychlost_hrace
    if stisknute_klavesy[pygame.K_LEFT]: 
        x_hrac -= rychlost_hrace
    nep_rychlost1 += gravitace_1
    nep_y1 += nep_rychlost1
    nep_rychlost2 += gravitace_2
    nep_y2 += nep_rychlost2
    nep_rychlost3 += gravitace_3
    nep_y3 += nep_rychlost3
    nep_rychlost4 += gravitace_4
    nep_y4 += nep_rychlost4
    nep_rychlost5 += gravitace_5
    nep_y5 += nep_rychlost5
 
    # Vykreslování
    okno.fill((255, 255, 255))
    hrac = pygame.draw.rect(okno, (255, 0, 255), (x_hrac, y_hrac, 20, 20))
    zem = pygame.draw.rect(okno, (0, 255, 0), (x_zem, y_zem, 1500, 50))
    strp = pygame.draw.rect(okno, (0, 0, 0), (0, 0, 1000, 50))
    nep_1 = pygame.draw.rect(okno, (0, 0, 0), (pozice_nep_x_1, nep_y1, 50, 50))
    nep_2 = pygame.draw.rect(okno, (0, 0, 0), (pozice_nep_x_2, nep_y2, 50, 50))
    nep_3 = pygame.draw.rect(okno, (0, 0, 0), (pozice_nep_x_3, nep_y3, 50, 50))
    nep_4 = pygame.draw.rect(okno, (0, 0, 0), (pozice_nep_x_4, nep_y4, 50, 50))
    nep_5 = pygame.draw.rect(okno, (0, 0, 0), (pozice_nep_x_5, nep_y5, 50, 50))
    zed1 = pygame.draw.rect(okno, (0, 0, 0), (x_zed, y_zed, 20, 1000))
    zed2 = pygame.draw.rect(okno, (0, 0, 0), (x_zed2, y_zed2, 20 , 1000))
 
    # Kolize
    if hrac.colliderect(zed1):
        x_hrac = 21
        y_hrac = 930
    
    if hrac.colliderect(zed2):
        x_hrac = 959
        y_hrac = 930


    if nep_1.colliderect(zem):
        pozice_nep_x_1 = random.choice([50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800, 850, 900, 950])
        nep_y1 = 0
        nep_rychlost1 = 0
    if nep_1.colliderect(hrac):
        pygame.quit()
        sys.exit()
 
    if nep_2.colliderect(zem):
        pozice_nep_x_2 = random.choice([50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800, 850, 900, 950])
        nep_y2 = 0
        nep_rychlost2 = 0
    if nep_2.colliderect(hrac):
        pygame.quit()
        sys.exit()
 
    if nep_3.colliderect(zem):
        pozice_nep_x_3 = random.choice([50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800, 850, 900, 950])
        nep_y3 = 0
        nep_rychlost3 = 0
    if nep_3.colliderect(hrac):
        pygame.quit()
        sys.exit()
 
    if nep_4.colliderect(zem):
        pozice_nep_x_4 = random.choice([50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800, 850, 900, 950])
        nep_y4 = 0
        nep_rychlost4 = 0
    if nep_4.colliderect(hrac):
       pygame.quit()
       sys.exit()
        
    if nep_5.colliderect(zem):
        pozice_nep_x_5 = random.choice([50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800, 850, 900, 950])
        nep_y5 = 0
        nep_rychlost5 = 0
    if nep_5.colliderect(hrac):
        pygame.quit()
        sys.exit()
 
    pygame.display.update()

