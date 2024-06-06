import pygame as pg
import sys
import math
import random

pg.init()
okno = pg.display.set_mode([800, 600])


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


pozice = (1,1)
bod_x = 300
bod_y = 300
velikost_kruhu = 50
stred_x = bod_x + velikost_kruhu/2
stred_y = bod_y + velikost_kruhu/2
stred = (stred_x, stred_y)
dotyk = math.sqrt((pozice[0]-stred_x)**2+(pozice[1]+stred_y)**2)
fake_stred = bod_x + bod_y + velikost_kruhu
body = 0




while True:
    for udalost in pg.event.get():
        if udalost.type == pg.QUIT :
            pg.quit()
            sys.exit()
    
    stisknute_klavesy = pg.key.get_pressed()
    if stisknute_klavesy[pg.K_ESCAPE]:
        pg.quit()
        sys.exit()
    
    pozice = pg.mouse.get_pos()
    dotyk = math.sqrt((pozice[0]-stred_x)**(2)+(pozice[1]-stred_y)**(2))
    
    
    
    if dotyk <= 26 and udalost.type == pg.MOUSEBUTTONDOWN :
       body + 1
       bod_x = random.randrange(0, 800 - velikost_kruhu)
       bod_y = random.randrange(0, 600 - velikost_kruhu)
       stred_x = bod_x + velikost_kruhu/2
       stred_y = bod_y + velikost_kruhu/2
       fake_stred = bod_x + bod_y + velikost_kruhu
       
       
   
    
    print(dotyk)
    
    
    okno.fill((100,200,36))
    
    pg.draw.ellipse(okno, (100,28,0), (bod_x,bod_y,velikost_kruhu,velikost_kruhu) )
        
    pg.display.update()
