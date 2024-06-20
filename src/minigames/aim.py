import pygame as pg
import sys
import math
import random
import minigames.minigame_base as mini

#pg.init()
#okno = pg.display.set_mode([800, 600])


# create a system cursor
system = pg.cursors.Cursor(pg.SYSTEM_CURSOR_NO)

# create bitmap cursors
bitmap_1 = pg.cursors.Cursor(*pg.cursors.arrow)
bitmap_2 = pg.cursors.Cursor(
    (24, 24), (0, 0), *pg.cursors.compile(pg.cursors.thickarrow_strings)
)

# create a color cursor
surf = pg.Surface((40, 40)) # you could also load an image 
surf.fill((120, 50, 50))        # and use that as your surface
color = pg.cursors.Cursor((20, 20), surf)

cursors = [system, bitmap_1, bitmap_2, color]
cursor_index = 1

pg.mouse.set_cursor(cursors[cursor_index])

text_font = pg.font.SysFont('Arial', 50)
text_font2 = pg.font.SysFont('Arial', 70)

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    mini.mini_surface.blit(img, (x, y))

def mini_aim():
    bg_image = pg.image.load('../assets/aim_klik/Pozadí Aim minigame.png')

    pozice = (1,1)
    bod_x = 359
    bod_y = 339
    velikost_kruhu = 50
    stred_x = bod_x + velikost_kruhu/2
    stred_y = bod_y + velikost_kruhu/2
    stred = (stred_x, stred_y)
    dotyk = math.sqrt((pozice[0]-stred_x)**2+(pozice[1]+stred_y)**2)
    fake_stred = bod_x + bod_y + velikost_kruhu
    body = 0
    cas = 0
    tutorial = 1
    barva_kruhu1 = 0
    barva_kruhu2 = 0
    barva_kruhu3 = 0
    barva_kruhu = (barva_kruhu1, barva_kruhu2, barva_kruhu3)


    while True:
        for udalost in pg.event.get():
            if udalost.type == pg.QUIT:
                pg.quit()
                sys.exit()
        
        


            if tutorial == 1:
                if udalost.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                    
                mini.mini_surface.fill((100,200,100))
                draw_text(("AIM test"), text_font2, (155,0,100), 300, 0)
                draw_text(("klikni na co nejvíc kruhů"), text_font2, (255,0,100), 0, 75)
                draw_text(("naklikej 25 bodů"), text_font2, (255,0,100), 0, 150)
                draw_text(("než dá timer 25sekund"), text_font2, (255,0,100), 0, 225)
                draw_text(("hru zapneš kliknutím myši kamkoli"), text_font, (255,0,100), 0, 550)
                
                if udalost.type == pg.MOUSEBUTTONDOWN:
                    tutorial = 0
                    
                
                mini.mini_frame()
                
                pg.display.update()
                
            else:
            
                pozice = pg.mouse.get_pos()
                dotyk = math.sqrt((pozice[0]-stred_x)**(2)+(pozice[1]-stred_y)**(2))
                


                if dotyk <= 27 and udalost.type == pg.MOUSEBUTTONDOWN :
                    body += 1
                    bod_x = random.randrange(0, 800 - velikost_kruhu)
                    bod_y = random.randrange(0, 600 - velikost_kruhu)
                    stred_x = bod_x + velikost_kruhu/2
                    stred_y = bod_y + velikost_kruhu/2
                    fake_stred = bod_x + bod_y + velikost_kruhu
                    barva_kruhu1 = random.randrange(0, 255)
                    if barva_kruhu1 >= 190 and barva_kruhu1 <= 200:
                        barva_kruhu1 += 10
                    barva_kruhu2 = random.randrange(0, 255)
                    if barva_kruhu2 >= 190 and barva_kruhu2 <= 200:
                        barva_kruhu2 += 10
                    barva_kruhu3 = random.randrange(0, 255)
                    if barva_kruhu3 >= 190 and barva_kruhu3 <= 200:
                            barva_kruhu3 += 10
                    barva_kruhu = (barva_kruhu1, barva_kruhu2, barva_kruhu3)
                    
                
                
                
            
                
                cas += 0.00076      
                rncas = round(cas, 1)
                
                
                if body == 25:
                    return mini.win_minigame()
                    
                if rncas >= 25:
                    return mini.fail_minigame()
                
                
                mini.mini_surface.fill((100,200,100))
                mini.mini_surface.blit(bg_image, (0, 0))
                
                draw_text(str(body), text_font, (0,0,255), 355, 75)
                draw_text(str(rncas), text_font, (255,0,0), 340, 125)
                
                
                pg.draw.ellipse(mini.mini_surface, barva_kruhu, (bod_x,bod_y,velikost_kruhu,velikost_kruhu) )
                
                mini.mini_frame()
                    
                pg.display.update()
