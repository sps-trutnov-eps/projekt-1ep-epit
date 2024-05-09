import pygame
import minigames.minigame_base as mini
import minigames.test as mini_test
import minigame.simon as mini_simon
import sys



import sys

import pygame
pygame.init()

rozliseni_okna = (800, 600)

okno = pygame.display.set_mode(rozliseni_okna)
    
    
    
pozice_hlavni_x = 175
pozice_hlavni_y = 75

pozice_prvni_x = 200
pozice_prvni_y = 100
pozice_druhy_x = 350
pozice_druhy_y = 100
pozice_treti_x = 500
pozice_treti_y = 100
pozice_ctvrty_x = 200
pozice_ctvrty_y = 250
pozice_paty_x = 350
pozice_paty_y = 250
pozice_sesty_x = 500
pozice_sesty_y = 250
pozice_sedmy_x = 200
pozice_sedmy_y = 400
pozice_osmy_x = 350
pozice_osmy_y = 400
pozice_devaty_x = 500
pozice_devaty_y = 400


while True:
    for udalost in pygame.event.get():
        if udalost.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    
    
    okno.fill((255, 255, 255))
    
    pygame.draw.rect(okno, (200, 200, 200), (pozice_hlavni_x, pozice_hlavni_y, 450, 450))
    pygame.draw.rect(okno, (128, 128, 128), (pozice_prvni_x, pozice_prvni_y, 100, 100))
    pygame.draw.rect(okno, (128, 128, 128), (pozice_druhy_x, pozice_druhy_y, 100, 100))
    pygame.draw.rect(okno, (128, 128, 128), (pozice_treti_x, pozice_treti_y, 100, 100))
    pygame.draw.rect(okno, (128, 128, 128), (pozice_ctvrty_x, pozice_ctvrty_y, 100, 100))
    pygame.draw.rect(okno, (128, 128, 128), (pozice_paty_x, pozice_paty_y, 100, 100))
    pygame.draw.rect(okno, (128, 128, 128), (pozice_sesty_x, pozice_sesty_y, 100, 100))
    pygame.draw.rect(okno, (128, 128, 128), (pozice_sedmy_x, pozice_sedmy_y, 100, 100))
    pygame.draw.rect(okno, (128, 128, 128), (pozice_osmy_x, pozice_osmy_y, 100, 100))
    pygame.draw.rect(okno, (128, 128, 128), (pozice_devaty_x, pozice_devaty_y, 100, 100))
    
    
    
    
    pygame.display.update()



# tady odkažte svoji minihru s jejím jménem (stejně jako test)
minigame_lib = {
    "test": mini_test.test_minigame,
    "simon": mini_simon
}

def switch_to_minigame(name, sur: pygame.Surface):
    # minigame setup

    mini.mini_surface = sur
    mini_loop = minigame_lib[name]

    # run minigame

    result = mini_loop()

    # check result

    if result == None:
        raise ValueError(f"minigame {name} nevrátil jestli vyhrál/prohrál (`return False` pokud nejde vyhrát ani prohrát, např. automat)")
    elif result == False:
        pass # minihra nemá wil/fail state (např. automat)

    elif result.did_win == False: # win
        pass # TODO: pro Pavla
    
    elif result.did_win == True: # fail
        pass # TODO: pro Pavla
    
    okno.fill((255,255,255))