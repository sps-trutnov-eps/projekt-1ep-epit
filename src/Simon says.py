import sys
import pygame
import random

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
ctverec_na_kliknuti = None
odpočet = 3
odpočet_start = False
čas_startu_odpočtu = 0
sekvence = []
pocet_sekvenci = 0
max_sekvenci = 5

# Funkce pro zobrazení akce
def zobraz_akci(index):
    barvy[index] = BLUE
    pygame.draw.rect(okno, (200, 200, 200), (pozice_hlavni_x, pozice_hlavni_y, 450, 450))
    for i, ctverec in enumerate(ctverce):
        pygame.draw.rect(okno, barvy[i], ctverec)
    pygame.display.update()
    pygame.time.delay(500)  # Zobraz akci po dobu 0.5 sekundy
    barvy[index] = GRAY
    pygame.draw.rect(okno, (200, 200, 200), (pozice_hlavni_x, pozice_hlavni_y, 450, 450))
    for i, ctverec in enumerate(ctverce):
        pygame.draw.rect(okno, barvy[i], ctverec)
    pygame.display.update()

# Funkce pro generování nové sekvence
def nova_sekvence():
    index = random.randint(0, 8)
    sekvence.append(index)
    for i in sekvence:
        zobraz_akci(i)
        pygame.time.delay(500)

# Funkce pro zobrazení chyby
def zobraz_chybu():
    for _ in range(3):  # Problikne třikrát
        for i in range(len(ctverce)):
            barvy[i] = BLUE
        pygame.draw.rect(okno, (200, 200, 200), (pozice_hlavni_x, pozice_hlavni_y, 450, 450))
        for i, ctverec in enumerate(ctverce):
            pygame.draw.rect(okno, barvy[i], ctverec)
        pygame.display.update()
        pygame.time.delay(200)
        for i in range(len(ctverce)):
            barvy[i] = GRAY
        pygame.draw.rect(okno, (200, 200, 200), (pozice_hlavni_x, pozice_hlavni_y, 450, 450))
        for i, ctverec in enumerate(ctverce):
            pygame.draw.rect(okno, barvy[i], ctverec)
        pygame.display.update()
        pygame.time.delay(200)

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
                    if text == "Pro začátek hry stisni klávesu enter":
                        # Spustit hru
                        hrajeme_hru = True
        elif not hrajeme_hru and udalost.type == pygame.KEYDOWN:
            if udalost.key == pygame.K_RETURN:
                odpočet_start = True
                čas_startu_odpočtu = pygame.time.get_ticks()

    if odpočet_start:
        aktuální_čas = pygame.time.get_ticks()
        sekundy_od_startu = (aktuální_čas - čas_startu_odpočtu) // 1000

        if sekundy_od_startu < odpočet:
            okno.fill(WHITE)
            font = pygame.font.Font(None, 74)
            text = font.render(str(odpočet - sekundy_od_startu), True, BLACK)
            okno.blit(text, (rozliseni_okna[0] // 2 - text.get_width() // 2, rozliseni_okna[1] // 2 - text.get_height() // 2))
            pygame.display.update()
        else:
            odpočet_start = False
            okno.fill(WHITE)
            pygame.draw.rect(okno, (200, 200, 200), (pozice_hlavni_x, pozice_hlavni_y, 450, 450))
            for ctverec, barva in zip(ctverce, barvy):
                pygame.draw.rect(okno, barva, ctverec)
            pygame.display.update()
            pygame.time.delay(2000)
            hrajeme_hru = True
            sekvence = []
            nova_sekvence()
            ctverec_na_kliknuti = 0
            pocet_sekvenci = 1

    # Vykreslení obrazu
    if not hrajeme_hru and not odpočet_start:
        okno.fill(WHITE)
        pygame.draw.rect(okno, WHITE, (0, 0, rozliseni_okna[0], 600))
        for i, text in enumerate(texty_menu):
            text_surface = fonty_menu[i].render(text, True, BLACK)
            text_rect = text_surface.get_rect(center=(rozliseni_okna[0] // 2, pozice_textu_y[i]))
            okno.blit(text_surface, text_rect)
    elif hrajeme_hru:
        okno.fill(WHITE)
        pygame.draw.rect(okno, (200, 200, 200), (pozice_hlavni_x, pozice_hlavni_y, 450, 450))
        for ctverec, barva in zip(ctverce, barvy):
            pygame.draw.rect(okno, barva, ctverec)
        if ctverec_na_kliknuti is not None:
            if udalost.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if ctverce[sekvence[ctverec_na_kliknuti]].collidepoint(mouse_pos):
                    zobraz_akci(sekvence[ctverec_na_kliknuti])
                    ctverec_na_kliknuti += 1
                    if ctverec_na_kliknuti >= len(sekvence):
                        if pocet_sekvenci < max_sekvenci:
                            pygame.time.delay(1000)
                            nova_sekvence()
                            ctverec_na_kliknuti = 0
                            pocet_sekvenci += 1
                        else:
                            hrajeme_hru = False
                            ctverec_na_kliknuti = None
                            # Zobrazení konce hry
                            okno.fill(WHITE)
                            font = pygame.font.Font(None, 74)
                            text = font.render("Konec hry!", True, BLACK)
                            okno.blit(text, (rozliseni_okna[0] // 2 - text.get_width() // 2, rozliseni_okna[1] // 2 - text.get_height() // 2))
                            pygame.display.update()
                            pygame.time.delay(3000)
                            hrajeme_hru = False
                            sekvence = []
                            nova_sekvence()
                            ctverec_na_kliknuti = 0
                            pocet_sekvenci = 1
                else:
                    zobraz_chybu()
                    pygame.time.delay(1000)
                    ctverec_na_kliknuti = 0  # Znovu začne aktuální sekvence
                    for i in sekvence:
                        zobraz_akci(i)
                        pygame.time.delay(500)

    pygame.display.update()
