import pygame
import sys
import math
pygame.init()
    
okno = pygame.display.set_mode((1200, 800))

pozicey1 = 500
pozicex1 = 500

while True:
 
    
    for udalost in pygame.event.get():
        if udalost.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    okno.fill((0, 0, 0))
    
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
    
    stisknute_klavesy = pygame.key.get_pressed()
    
    if stisknute_klavesy[pygame.K_w]:
        pozicey1 -= 0.3
    if stisknute_klavesy[pygame.K_s]:
        pygame.transform.rotate(hrac, 10)
    if stisknute_klavesy[pygame.K_a]:
        pozicex1 -= 0.3
    if stisknute_klavesy[pygame.K_d]:
        pozicex1 += 0.3
        
    if 300 < pozicex1 < 700 and 500 > pozicey1 > 300:
        pozicey1 = 500
        
    
    
    
    
    
        
    pygame.display.update()