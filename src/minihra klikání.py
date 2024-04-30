import sys

import pygame
pygame.init()

rozliseni_okna = (800, 600)

okno = pygame.display.set_mode(rozliseni_okna)





antidrzeni = 0
nahoru = 0
postup = rozliseni_okna[0]/2
IT = 100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
tutorial = 1


text_font = pygame.font.SysFont('Arial black', 40)

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    okno.blit(img, (x, y))


while True:
    for udalost in pygame.event.get():
        if udalost.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    if tutorial == 1:
        
        stisknute_klavesy = pygame.key.get_pressed()
        okno.fill((255, 255, 255))
        draw_text('Klikáním na přeskáčku ', text_font, (255,0,0), 10, 50)
        draw_text('na šipku nahoru a dolu vyhraj', text_font, (255,0,0), 10, 150)
        draw_text('Dostaň čáru na konec obrazovky', text_font, (255,0,0), 10, 250)
        draw_text('Hru zapneš stisknutím šipky nahoru nebo dolu ', text_font, (255,0,0), 10, 350)
        draw_text('Šipky nahoru nebo dolu ', text_font, (255,0,0), 10, 450)
        pygame.display.flip()
    
        pygame.display.update()
        if stisknute_klavesy[pygame.K_UP] or stisknute_klavesy[pygame.K_DOWN]:
            tutorial = 0
    else:
        
        stisknute_klavesy = pygame.key.get_pressed()
          
        
        
        if stisknute_klavesy[pygame.K_UP]:
            nahoru = 1
            
        if nahoru > 0 and stisknute_klavesy[pygame.K_DOWN]:
            nahoru = 0
            postup += 10
        
        if stisknute_klavesy[pygame.K_DOWN] and stisknute_klavesy[pygame.K_UP]:
            postup -= 10
        
        if IT > 0 :
            postup -= 0.01
            
     
            
        
        
       
        
        okno.fill((255, 255, 255))
        draw_text('Klikáním na přeskáčku ', text_font, (255,0,0), 10, 50)
        draw_text('na šipku nahoru a dolu vyhraj', text_font, (255,0,0), 10, 150)
        draw_text('Dostaň se na konec obrazovky', text_font, (255,0,0), 10, 250)
        
        
        pygame.draw.rect(okno, (0, 0, 0), (rozliseni_okna[1] - rozliseni_okna[1] +1 , 20, postup, 20))
        
        pygame.display.flip()
        
        pygame.display.update()
       
