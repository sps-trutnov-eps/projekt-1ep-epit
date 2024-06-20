import sys
import random
import pygame
import minigames.minigame_base as mini

def mini_prepis():
    rozliseni_okna = mini.mini_surface.get_size()

    slova=("slovo a další a ještě jedno", "nic","něco jsem napsal")
    vybrane=random.randint(0,len(slova)-1)
    napsano=""
    font=pygame.font.Font(None, 128)
    text=font.render(slova[vybrane], True, (0, 0, 0))
    while True:
        mini.mini_surface.fill((255,255,255)) 
        stisknute_klavesy = pygame.key.get_pressed()
        for udalost in pygame.event.get():
            if udalost.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if udalost.type==pygame.KEYUP:
                if stisknute_klavesy[pygame.K_BACKSPACE]:
                    napsano=napsano[:-1]
                else :
                    napsano=napsano+str(udalost.unicode)

        mini.mini_frame()

        text2=font.render(napsano, True, (0, 0, 0))
        mini.mini_surface.blit(text,(100,200))
        mini.mini_surface.blit(text2,(100,300))
        if napsano==slova[vybrane]:
            return mini.win_minigame()
        pygame.display.update()

