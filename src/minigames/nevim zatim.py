import sys
import pygame

rozliseni_okna = (1250, 800)
okno = pygame.display.set_mode(rozliseni_okna)

zivoty = 5
rychlost_hrace = 0.5
x1 = 615
y1 = 50

nep1_x = 30
nep2_x = 1070
nep3_x = 30
nep4_x = 970
nep5_x = 430
nep6_x = 30

speed1 = 1
speed2 = 1.5
speed3 = 2
speed4 = 2
speed5 = 1.5
speed6 = 1

while True:
    for udalost in pygame.event.get():  
        if udalost.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
    stisknute_klavesy = pygame.key.get_pressed()
    
    nep1_x += speed1
    nep2_x += speed2
    nep3_x += speed3
    nep4_x += speed4
    nep5_x += speed5
    nep6_x += speed6
    
    if nep1_x > 1150:
        speed1 *= -1
    if nep1_x < 0:
        speed1 *= -1
        
    if nep2_x > 1100:
        speed2 *= -1
    if nep2_x < 0:
        speed2 *= -1
        
    if nep3_x > 1050:
        speed3 *= -1
    if nep3_x < 0:
        speed3 *= -1
    
    if nep4_x > 1000:
        speed4 *= -1
    if nep4_x < 0:
        speed4 *= -1
        
    if nep5_x > 850:
        speed5 *= -1
    if nep5_x < 0:
        speed5 *= -1
        
    if nep6_x > 950:
        speed6 *= -1
    if nep6_x < 0:
        speed6 *= -1
        
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
    
    
    nep1 = pygame.draw.rect(okno, (0, 0, 0), (nep1_x, 150, 100, 50))
    nep2 = pygame.draw.rect(okno, (0, 0, 0), (nep2_x, 250, 150, 50))
    nep3 = pygame.draw.rect(okno, (0, 0, 0), (nep3_x, 350, 200, 50))
    nep4 = pygame.draw.rect(okno, (0, 0, 0), (nep4_x, 450, 250, 50))
    nep5 = pygame.draw.rect(okno, (0, 0, 0), (nep5_x, 700, 400, 20))
    nep6 = pygame.draw.rect(okno, (0, 0, 0), (nep6_x, 570, 300, 50))
    
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
    
#______________________________________
        
    if hrac.colliderect(nep1):
        x1 = 615
        y1 = 50
        zivoty -= 1
    
    if hrac.colliderect(nep2):
        x1 = 615
        y1 = 50
        zivoty -= 1
    
    if hrac.colliderect(nep3):
        x1 = 615
        y1 = 50
        zivoty -= 1
        
    if hrac.colliderect(nep4):
        x1 = 615
        y1 = 50
        zivoty -= 1
    
    if hrac.colliderect(nep5):
        x1 = 615
        y1 = 50
        zivoty -= 1
        
    if hrac.colliderect(nep6):
        x1 = 615
        y1 = 50
        zivoty -= 1
        
    pygame.display.update()
            
        