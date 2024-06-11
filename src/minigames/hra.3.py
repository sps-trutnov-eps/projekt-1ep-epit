import sys 
import pygame 
import random 
 
# Velikost okna 
rozliseni_okna = (1000, 800) 
okno = pygame.display.set_mode(rozliseni_okna) 
 
rychlost_hrace = 5

x1 = 30 
y1 = 30 

 
while True: 
    for udalost in pygame.event.get(): 
     #ovladani
        okno.fill((0, 0, 0)) 
         
        stisknute_klavesy = pygame.key.get_pressed() 
         
        if udalost.type == pygame.QUIT: 
            pygame.quit() 
            sys.exit() 
    #logika    
    if stisknute_klavesy[pygame.K_RIGHT]:  
        x1 += rychlost_hrace 
    if stisknute_klavesy[pygame.K_LEFT]:  
        x1 -= rychlost_hrace  
    if stisknute_klavesy[pygame.K_UP]:  
        y1 -= rychlost_hrace  
    if stisknute_klavesy[pygame.K_DOWN]:  
        y1 += rychlost_hrace 
 
    #vykreslovani
    hrac = pygame.draw.rect(okno, (255, 0, 255), (x1, y1, 20, 20))
    
    zed1 = pygame.draw.rect(okno, (0, 255, 255), (0, 0, 550, 30))
    zed2 = pygame.draw.rect(okno, (0, 255, 255), (0, 50, 500, 30))
    zed3 = pygame.draw.rect(okno, (0, 255, 255), (520, 20, 30, 150))
    zed4 = pygame.draw.rect(okno, (0, 255, 255), (0, 0, 30, 50))
    zed5 = pygame.draw.rect(okno, (0, 255, 255), (470, 50, 30, 100))
    zed6 = pygame.draw.rect(okno, (0, 255, 255), (300, 120, 200, 30))
    zed7 = pygame.draw.rect(okno, (0, 255, 255), (320, 170, 230, 30))
    zed8 = pygame.draw.rect(okno, (0, 255, 255), (270, 120, 30, 150))
    zed9 = pygame.draw.rect(okno, (0, 255, 255), (320, 200, 30, 50))
    zed10 = pygame.draw.rect(okno, (0, 255, 255), (270, 270, 400, 30))
    zed11 = pygame.draw.rect(okno, (0, 255, 255), (320, 220, 330, 30))
    zed12 = pygame.draw.rect(okno, (0, 255, 255), (620, 80, 30, 170))
    zed13 = pygame.draw.rect(okno, (0, 255, 255), (620, 80, 250, 30))
    zed14 = pygame.draw.rect(okno, (0, 255, 255), (670, 130, 30, 170))
    zed15 = pygame.draw.rect(okno, (0, 255, 255), (670, 130, 150, 30))
    zed16 = pygame.draw.rect(okno, (0, 255, 255), (840, 110, 30, 400))
    zed17 = pygame.draw.rect(okno, (0, 255, 255), (790, 130, 30, 360))
     
    #kolize
    
    pygame.display.update() 
     
