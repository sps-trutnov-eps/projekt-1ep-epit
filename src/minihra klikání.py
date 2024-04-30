import sys

import pygame
pygame.init()

rozliseni_okna = (800, 600)

okno = pygame.display.set_mode(rozliseni_okna)





antidrzeni = 0
nahoru = 0
postup = 10


while True:
    for udalost in pygame.event.get():
        if udalost.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    stisknute_klavesy = pygame.key.get_pressed()
    

    
    
    if stisknute_klavesy[pygame.K_UP]:
        nahoru = 1
        
    if nahoru > 0 and stisknute_klavesy[pygame.K_DOWN]:
        nahoru = 0
        postup += 1
    
    if stisknute_klavesy[pygame.K_DOWN] and stisknute_klavesy[pygame.K_UP]:
        postup -= 1
    
    
        
        
    
    print(nahoru)
    print(postup)
    
    
   
    
    okno.fill((255, 255, 255))
    
    pygame.draw.rect(okno, (0, 0, 0), (rozliseni_okna[1] - rozliseni_okna[1] + rozliseni_okna[1]/4 , 20, postup, 20))
    
    
    pygame.display.update()

