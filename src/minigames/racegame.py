import pygame
import sys
import math
pygame.init()
    
okno = pygame.display.set_mode((1200, 800))

pozicey1 = 500
pozicex1 = 500

clock = pygame.time.Clock()


while True:
 
    
    for udalost in pygame.event.get():
        if udalost.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    okno.fill((79, 121, 66))
    
    pygame.draw.rect(okno, (128, 128, 128), (200, 500, 500, 100))
    pygame.draw.rect(okno, (128, 128, 128), (600, 500, 100, 200))
    pygame.draw.rect(okno, (128, 128, 128), (600, 600, 400, 100))
    pygame.draw.rect(okno, (128, 128, 128), (900, 200, 100, 400))
    pygame.draw.rect(okno, (128, 128, 128), (900, 200, 200, 100))
    pygame.draw.rect(okno, (128, 128, 128), (1000, 0, 100, 300))
    pygame.draw.rect(okno, (128, 128, 128), (800, 0, 300, 100))
    pygame.draw.rect(okno, (128, 128, 128), (800, 0, 100, 200))
    pygame.draw.rect(okno, (128, 128, 128), (200, 100, 700, 100))
    pygame.draw.rect(okno, (128, 128, 128), (200, 200, 100, 400))
    
    hrac = pygame.draw.rect(okno, (255, 255, 255), (pozicex1, pozicey1, 20, 20))
    
    time = 600
    
    stisknute_klavesy = pygame.key.get_pressed()
    
    if stisknute_klavesy[pygame.K_w]:
        pozicey1 -= 0.3
    if stisknute_klavesy[pygame.K_s]:
        pozicey1 += 0.3
    if stisknute_klavesy[pygame.K_a]:
        pozicex1 -= 0.3
    if stisknute_klavesy[pygame.K_d]:
        pozicex1 += 0.3
        
    if 300 < pozicex1 < 700 and 500 > pozicey1 > 300:
        pozicey1 = 500
    if 190 < pozicex1 < 599 and pozicey1 > 580:
        pozicey1 = 580
    if 100 < pozicey1 < 600 and pozicex1 < 200:
        pozicex1 = 200
    if 200 < pozicex1 < 799 and pozicey1 < 100:
       pozicey1 = 100
    if 0 < pozicey1 < 100 and 800 > pozicex1:
        pozicex1 = 800
    if pozicey1 < 0:
        pozicey1 = 0
    if 600 < pozicey1 < 700 and 600 > pozicex1:
        pozicex1 = 600
    if 580 < pozicex1 < 1000 and pozicey1 > 680:
        pozicey1 = 680
    if 200 < pozicey1 < 500 and 280 < pozicex1 < 400:
        pozicex1 = 280
    
    
    
    
    
    
        
    pygame.display.update()
    