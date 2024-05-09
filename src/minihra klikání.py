import sys
import dataclasses
import pygame
import minigames.minigame_base as mini

pygame.init()

rozliseni_okna = (800, 600)

okno = pygame.display.set_mode(rozliseni_okna)

def test_minigame():
    vyhrál = False


@dataclasses.dataclass()
class MinigameEndState:
    did_win: bool
bg_image = pygame.image.load('pozadí.v2.png')
antidrzeni = 0
nahoru = 0
postup = rozliseni_okna[0]/2
IT = 100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
tutorial = 1


text_font = pygame.font.SysFont('Arial black', 47)
text_font2 = pygame.font.SysFont('Arial black', 20)

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
        okno.fill((220, 220, 220))
        draw_text('Klikáním na přeskáčku na ', text_font, (255,0,0), 10, 50)
        draw_text('Šipky nahoru a dolu vyhraj', text_font, (255,0,0), 10, 100)
        draw_text('Dostaň čáru do prava', text_font, (255,0,0), 10, 150)
        draw_text('Nenech IT dostat čáru do leva', text_font, (255,0,0), 10, 200)
        draw_text('Hru zapneš stisknutím Šipky nahoru nebo dolu ', text_font2, (0,155,0), 10, 565)
        
        pygame.display.flip()
    
        pygame.display.update()
        if stisknute_klavesy[pygame.K_UP] or stisknute_klavesy[pygame.K_DOWN]:
            tutorial = 0
            
        
        mini.mini_frame()
        
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
            
        if postup > rozliseni_okna[0]:
            print("vyhrálj´jsi")
            sys.exit()
           # return mini.fail_minigame()
            
        if postup < 0:
            print("prohrál jsi")
            sys.exit()
            #return mini.win_minigame()
        
        
       
        
        okno.fill((255, 255, 255))
        okno.blit(bg_image, (0, 0))

        
        
        pygame.draw.rect(okno, (0, 0, 0), (rozliseni_okna[1] - rozliseni_okna[1] +1 , 20, postup, 20))
        
        pygame.display.flip()
        
        mini.mini_frame()

       
