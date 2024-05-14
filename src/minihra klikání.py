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
nahoru = 0
postup = rozliseni_okna[0]/2
clicks = 0
cas = 0.1111111111
cps = 1
cps2 = 1
IT = 100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
tutorial = 1
hra = 0
konec = 0


text_font = pygame.font.SysFont('Arial black', 47)
text_font2 = pygame.font.SysFont('Arial black', 20)
text_font3 = pygame.font.SysFont('Arial black', 200)

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
            hra = 1
            
        
        mini.mini_frame()
        
    elif hra == 1:
        cas += 0.008888888888888888888888888888888888
        cps = clicks/cas
        cps2 = round(cps, 2)
        
        stisknute_klavesy = pygame.key.get_pressed()
          
        
        
        if stisknute_klavesy[pygame.K_UP]:
            nahoru = 1
            
        if nahoru > 0 and stisknute_klavesy[pygame.K_DOWN]:
            nahoru = 0
            postup += 10
            clicks += 2
        
        if stisknute_klavesy[pygame.K_DOWN] and stisknute_klavesy[pygame.K_UP]:
            postup -= 10
            clicks -= 2
        
        if IT > 0 :
            postup -= 0.05
            
            
        if postup > rozliseni_okna[0]:
            hra = 0
           
            
        if postup < 0:
            print("prohrál jsi")
            #return mini.fail_minigame()
        
        
        
       
        
        okno.fill((255, 255, 255))
        okno.blit(bg_image, (0, 0))
        
        draw_text("CPS:", text_font2, (255,0,0), 5, 225)
        draw_text(str(cps2), text_font, (0,255,0), 60, 200)

        
        
        pygame.draw.rect(okno, (0, 0, 0), (rozliseni_okna[1] - rozliseni_okna[1] +1 , 20, postup, 20))
        
        pygame.display.flip()
        
        mini.mini_frame()

    else:
        
        okno.fill((255, 255, 255))
        draw_text("tvoje CPS:", text_font2, (255,0,0), rozliseni_okna[0]/2- + 350, rozliseni_okna[1]/2 - 20)
        draw_text(str(cps2), text_font3, (0,255,0), rozliseni_okna[0]/2- + 250, rozliseni_okna[1]/2 - 200)
        
        konec += 0.1
        if konec > 100:
            print("vyhrál jsi")
            sys.exit()
            # return mini.win_minigame()
            
            
        
        pygame.display.flip()
        
        mini.mini_frame()
        
