import sys
import pygame

pygame.init()

# Nastavení rozlišení okna
rozliseni_okna = (800, 600)
okno = pygame.display.set_mode(rozliseni_okna)

# Definice pozic čtverců
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

# Barvy
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)  

# Vytvoření seznamu čtverců
ctverce = [
    pygame.Rect(pozice_prvni_x, pozice_prvni_y, 100, 100),
    pygame.Rect(pozice_druhy_x, pozice_druhy_y, 100, 100),
    pygame.Rect(pozice_treti_x, pozice_treti_y, 100, 100),
    pygame.Rect(pozice_ctvrty_x, pozice_ctvrty_y, 100, 100),
    pygame.Rect(pozice_paty_x, pozice_paty_y, 100, 100),
    pygame.Rect(pozice_sesty_x, pozice_sesty_y, 100, 100),
    pygame.Rect(pozice_sedmy_x, pozice_sedmy_y, 100, 100),
    pygame.Rect(pozice_osmy_x, pozice_osmy_y, 100, 100),
    pygame.Rect(pozice_devaty_x, pozice_devaty_y, 100, 100)
]

# Barvy čtverců
barvy = [GRAY] * len(ctverce)

# Časovač pro automatickou změnu barvy
AUTO_COLOR_CHANGE_INTERVAL = 250  
last_color_change_time = pygame.time.get_ticks()

# Fonty pro menu
fonty_menu = [
    pygame.font.Font(None, 36),
    pygame.font.Font(None, 36),
    pygame.font.Font(None, 26)
]

# Texty možností menu
texty_menu = ["Pro začátek hry stisni klávesu enter", "Vítej v minihře Simon says", "Budou blikat čtverečky, ty si musíš zapamatovat jejich pořadí a potom ho zkopírovat"]
pozice_textu_y = [220, 100, 120]

# Stav hry
hrajeme_hru = False

# Hlavní smyčka
while True:
    for udalost in pygame.event.get():
        if udalost.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif not hrajeme_hru and udalost.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            # Kontrola, jestli bylo kliknuto na tlačítka v hlavním menu
            for i, text in enumerate(texty_menu):
                text_rect = fonty_menu[i].render(text, True, BLACK).get_rect(center=(rozliseni_okna[0] // 2, pozice_textu_y[i]))
                if text_rect.collidepoint(mouse_pos):
                    if text == "Start":
                        # Spustit hru
                        hrajeme_hru = True
        elif not hrajeme_hru and udalost.type == pygame.KEYDOWN:
            if udalost.key == pygame.K_RETURN:
                hrajeme_hru = True
                    
    # Pokud hrajeme hru, reagujeme na stisk myši
    if hrajeme_hru:
        tlacitka_mysi = pygame.mouse.get_pressed()
        
        # Pokud je stisknuto levé tlačítko myši
        if tlacitka_mysi[0]:
            mouse_pos = pygame.mouse.get_pos()
            
            for i, ctverec in enumerate(ctverce):
                if ctverec.collidepoint(mouse_pos):
                    
                    barvy[i] = BLUE
                    
                    last_color_change_time = pygame.time.get_ticks()
        
        # Automatická změna barvy po uplynutí časovače
        if pygame.time.get_ticks() - last_color_change_time >= AUTO_COLOR_CHANGE_INTERVAL:
            for i in range(len(ctverce)):
                
                if barvy[i] == BLUE:
                    barvy[i] = GRAY
            
            last_color_change_time = pygame.time.get_ticks()

    # Vykreslení obrazu
    okno.fill(WHITE)
    
    # Pokud nehráme hru, vykreslíme hlavní menu
    if not hrajeme_hru:
        pygame.draw.rect(okno, WHITE, (0, 0, rozliseni_okna[0], 600))
        for i, text in enumerate(texty_menu):
            text_surface = fonty_menu[i].render(text, True, BLACK)
            text_rect = text_surface.get_rect(center=(rozliseni_okna[0] // 2, pozice_textu_y[i]))
            okno.blit(text_surface, text_rect)
    else:
        # Pokud hrajeme hru, vykreslíme čtverce
        pygame.draw.rect(okno, (200, 200, 200), (pozice_hlavni_x, pozice_hlavni_y, 450, 450))
        for ctverec, barva in zip(ctverce, barvy):
            pygame.draw.rect(okno, barva, ctverec)
        
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