import sys
import pygame
import minigames.minigame_base as mini

bg_image = pygame.image.load('../assets/aim_klik/Pozadí.v2 klikání.png')

text_font = pygame.font.SysFont('Arial black', 47)
text_font2 = pygame.font.SysFont('Arial black', 20)
text_font3 = pygame.font.SysFont('Arial black', 200)

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    mini.mini_surface.blit(img, (x, y))

def mini_klik():
    nahoru = 0
    postup = mini.mini_surface.get_width()/2
    clicks = 0
    cas = 0.1111111111
    cps = 1
    cps2 = 1
    IT = 100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
    tutorial = 1
    hra = 0
    konec = 0

    while True:
        for udalost in pygame.event.get():
            if udalost.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        if tutorial == 1:
            
            stisknute_klavesy = pygame.key.get_pressed()
            mini.mini_surface.fill((190, 190, 190))
            draw_text('Klikáním na přeskáčku na ', text_font, (255,0,100), 10, 50)
            draw_text('Šipky nahoru a dolu vyhraj', text_font, (255,0,100), 10, 100)
            draw_text('Dostaň čáru do prava', text_font, (255,0,100), 10, 150)
            draw_text('Nenech IT dostat čáru do leva', text_font, (255,0,100), 10, 200)
            draw_text('Hru zapneš stisknutím Šipky nahoru nebo dolu ', text_font2, (0,155,0), 10, 565)
            
            
            pygame.display.flip()
        
            pygame.display.update()
            if stisknute_klavesy[pygame.K_UP] or stisknute_klavesy[pygame.K_DOWN]:
                tutorial = 0
                hra = 1
                
            
            mini.mini_frame()
            
        elif hra == 1:
            cas += 0.001222222222222222222
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
                postup -= 0.01
                
                
            if postup > mini.mini_surface.get_width():
                hra = 0
            
                
            if postup < 0:
                return mini.fail_minigame()
            
        
            
        
            
            mini.mini_surface.fill((255, 255, 255))
            mini.mini_surface.blit(bg_image, (0, 0))
            
            draw_text("CPS:", text_font2, (255,0,0), 5, 225)
            draw_text(str(cps2), text_font, (0,255,0), 60, 200)

            
            
            pygame.draw.rect(mini.mini_surface, (0, 0, 0), (mini.mini_surface.get_height() - mini.mini_surface.get_height() +1 , 20, postup, 20))
            
            pygame.display.flip()
            
            mini.mini_frame()

        else:
            
            mini.mini_surface.fill((190, 190, 190))
            draw_text("tvoje CPS:", text_font2, (255,0,0), mini.mini_surface.get_width()/2- + 350, mini.mini_surface.get_height()/2 - 20)
            draw_text(str(cps2), text_font3, (0,255,0), mini.mini_surface.get_width()/2- + 250, mini.mini_surface.get_height()/2 - 200)
            
            konec += 0.1
            if konec > 100:
                return mini.win_minigame()
                
                
            
            pygame.display.flip()
            
            mini.mini_frame()
            
