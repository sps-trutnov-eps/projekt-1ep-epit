import sys
import pygame

rozliseni_okna = (1250, 800)
okno = pygame.display.set_mode(rozliseni_okna)

zivoty = 3
rychlost_hrace = 0.5
x1 = 615
y1 = 50

while True:
    for udalost in pygame.event.get():  
        if udalost.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
    stisknute_klavesy = pygame.key.get_pressed() 
 
    if stisknute_klavesy[pygame.K_RIGHT]: 
        x1 += rychlost_hrace
    if stisknute_klavesy[pygame.K_LEFT]: 
        x1 -= rychlost_hrace 
    if stisknute_klavesy[pygame.K_UP]: 
        y1 -= rychlost_hrace 
    if stisknute_klavesy[pygame.K_DOWN]: 
        y1 += rychlost_hrace
        
    okno.fill((0, 155, 255))
        
    hrac = pygame.draw.rect(okno, (255, 0, 255), (x1, y1, 30, 30))
    
    
        
    
        
    zed1 = pygame.draw.rect(okno, (255, 0, 0), (0, 0, 1250, 10))
    zed2 = pygame.draw.rect(okno, (255, 0, 0), (1240, 0, 10, 750))
    zed3 = pygame.draw.rect(okno, (255, 0, 0), (0, 0, 10, 750))
    zed4 = pygame.draw.rect(okno, (255, 0, 0), (0, 740, 550, 10))
    zed5 = pygame.draw.rect(okno, (255, 0, 0), (700, 740, 600, 10))
    cil = pygame.draw.rect(okno, (0, 255, 0), (0, 750, 1250, 50))
    
    
    if zivoty <= 0:
        pygame.quit()
        sys.exit()
    
    if hrac.colliderect(cil):
        pygame.quit()
        sys.exit()
        
    if hrac.colliderect(zed1):
        x1 = 615
        y1 = 50
        zivoty -= 1
        
    if hrac.colliderect(zed2):
        x1 = 615
        y1 = 50
        zivoty -= 1
        
    if hrac.colliderect(zed3):
        x1 = 615
        y1 = 50
        zivoty -= 1
        
    if hrac.colliderect(zed4):
        x1 = 615
        y1 = 50
        zivoty -= 1
        
    if hrac.colliderect(zed5):
        x1 = 615
        y1 = 50
        zivoty -= 1
        
    pygame.display.update()
            
        