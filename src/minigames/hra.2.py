import sys
import pygame
import random
import time
pygame.init()

x_hrac = 85
y_hrac = 20

rychlost_hrace = 0.085

x_zed_1 = 0
y_zed_1 = 0

x_zed_2 = 120
y_zed_2 = 0

x_zed_3 = 60
y_zed_3 = 180

x_zed_4 = 0
y_zed_4 = 400

x_zed_5 = 220
y_zed_5 = 0

x_zed_6 = 330
y_zed_6 = 0

x_zed_7 = 215
y_zed_7 = 600

x_zed_8 = 0
y_zed_8 = 770

x_zed_9 = 830
y_zed_9 = 250

x_zed_10 = 543
y_zed_10 = 383

x_zed_11 = 823
y_zed_11 = 150

x_zed_12 = 0
y_zed_12 = 0

zivoty = 3

# Velikost okna
rozliseni_okna = (1000, 800)
okno = pygame.display.set_mode(rozliseni_okna)

while True:
    # ovladani
    for udalost in pygame.event.get():
        if udalost.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    # logika
    
    if zivoty <= 0:
        pygame.quit()
        sys.exit()
        
    stisknute_klavesy = pygame.key.get_pressed()
    
    if stisknute_klavesy[pygame.K_RIGHT]: 
        x_hrac += rychlost_hrace
    if stisknute_klavesy[pygame.K_LEFT]: 
        x_hrac -= rychlost_hrace
    if stisknute_klavesy[pygame.K_UP]: 
        y_hrac -= rychlost_hrace
    if stisknute_klavesy[pygame.K_DOWN]: 
        y_hrac += rychlost_hrace
        
    # vykreslovani
    okno.fill((255, 255, 255))
    
    hrac = pygame.draw.rect(okno, (0, 0, 0), (x_hrac, y_hrac, 9.8, 9.8))
    
    zed_1 = pygame.draw.rect(okno, (255, 0, 0), (x_zed_1, y_zed_1, 60, 800))
    zed_2 = pygame.draw.rect(okno, (255, 0, 0), (x_zed_2, y_zed_2, 1000, 140))
    zed_3 = pygame.draw.rect(okno, (255, 0, 0), (x_zed_3, y_zed_3, 120, 800))
    zed_4 = pygame.draw.rect(okno, (255, 0, 0), (x_zed_4, y_zed_4, 300, 160))
    zed_5 = pygame.draw.rect(okno, (255, 0, 0), (x_zed_5, y_zed_5, 592.5, 370))
    zed_6 = pygame.draw.rect(okno, (255, 0, 0), (x_zed_6, y_zed_6, 200, 700))
    zed_7 = pygame.draw.rect(okno, (255, 0, 0), (x_zed_7, y_zed_7, 600, 150))
    zed_8 = pygame.draw.rect(okno, (255, 0, 0), (x_zed_8, y_zed_8, 850, 50))
    zed_9 = pygame.draw.rect(okno, (255, 0, 0), (x_zed_9, y_zed_9, 500, 550))
    zed_10 = pygame.draw.rect(okno, (255, 0, 0), (x_zed_10, y_zed_10, 600, 200))
    zed_11 = pygame.draw.rect(okno, (255, 0, 0), (x_zed_11, y_zed_11, 500, 150))
    zed_12 = pygame.draw.rect(okno, (255, 0, 0), (x_zed_12, y_zed_12, 500, 10))
    
    cil = pygame.draw.rect(okno, (0, 255, 0), (990, 140, 90, 10))
    
    #kolize
    if hrac.colliderect(zed_1):
        zivoty -= 1
        x_hrac = 85
        y_hrac = 20
        
    if hrac.colliderect(zed_2):
        zivoty -= 1
        x_hrac = 85
        y_hrac = 20
        
    if hrac.colliderect(zed_3):
        zivoty -= 1
        x_hrac = 85
        y_hrac = 20
        
    if hrac.colliderect(zed_4):
        zivoty -= 1
        x_hrac = 85
        y_hrac = 20
        
    if hrac.colliderect(zed_5):
        zivoty -= 1
        x_hrac = 85
        y_hrac = 20
        
    if hrac.colliderect(zed_6):
        zivoty -= 1
        x_hrac = 85
        y_hrac = 20
        
    if hrac.colliderect(zed_7):
        zivoty -= 1
        x_hrac = 85
        y_hrac = 20
        
    if hrac.colliderect(zed_8):
        zivoty -= 1
        x_hrac = 85
        y_hrac = 20
        
    if hrac.colliderect(zed_9):
        zivoty -= 1
        x_hrac = 85
        y_hrac = 20
        
    if hrac.colliderect(zed_10):
        zivoty -= 1
        x_hrac = 85
        y_hrac = 20
        
    if hrac.colliderect(zed_11):
        zivoty -= 1
        x_hrac = 85
        y_hrac = 20
        
    if hrac.colliderect(zed_12):
        zivoty -= 1
        x_hrac = 85
        y_hrac = 20
        
    if hrac.colliderect(cil):
        pygame.quit()
        sys.exit()
        
    pygame.display.update()