import sys
import pygame
import random

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

WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

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

barvy = [GRAY] * len(ctverce)

fonty_menu = [
    pygame.font.Font(None, 36),
    pygame.font.Font(None, 36),
    pygame.font.Font(None, 26)
]
texty_menu = ["Pro začátek hry stisni klávesu enter", "Vítej v minihře Simon says", "Budou blikat čtverečky, ty si musíš zapamatovat jejich pořadí a potom ho zkopírovat"]
pozice_textu_y = [220, 100, 120]

hrajeme_hru = False
ctverec_na_kliknuti = None
odpočet = 3
odpočet_start = False
čas_startu_odpočtu = 0
sekvence = []
pocet_sekvenci = 0
max_sekvenci = 5
def zobraz_akci(index):
    barvy[index] = BLUE
    pygame.draw.rect(okno, (200, 200, 200), (pozice_hlavni_x, pozice_hlavni_y, 450, 450))
    for i, ctverec in enumerate(ctverce):
        pygame.draw.rect(okno, barvy[i], ctverec)
    pygame.display.update()
    pygame.time.delay(500)  
    barvy[index] = GRAY
    pygame.draw.rect(okno, (200, 200, 200), (pozice_hlavni_x, pozice_hlavni_y, 450, 450))
    for i, ctverec in enumerate(ctverce):
        pygame.draw.rect(okno, barvy[i], ctverec)
    pygame.display.update()
def nova_sekvence():
    index = random.randint(0, 8)
    sekvence.append(index)
    for i in sekvence:
        zobraz_akci(i)
        pygame.time.delay(500)
def zobraz_chybu():
    for _ in range(3):  
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
def simon_minigame():
    global hrajeme_hru, ctverec_na_kliknuti, odpočet_start, čas_startu_odpočtu, sekvence, pocet_sekvenci
    while True:
        for udalost in pygame.event.get():
            if udalost.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif not hrajeme_hru and udalost.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for i, text in enumerate(texty_menu):
                    text_rect = fonty_menu[i].render(text, True, BLACK).get_rect(center=(rozliseni_okna[0] // 2, pozice_textu_y[i]))
                    if text_rect.collidepoint(mouse_pos):
                        if text == "Pro začátek hry stisni klávesu enter":
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
                                return True  
                    else:
                        zobraz_chybu()
                        return False  
            for i, ctverec in enumerate(ctverce):
                pygame.draw.rect(okno, barvy[i], ctverec)
        pygame.display.update()
def switch_to_minigame(name):
    if name == "simon":
        return simon_minigame()
    else:
        raise ValueError(f"Minigame {name} not found")
if __name__ == "__main__":
    pygame.init()
    display_surface = pygame.display.set_mode((800, 600))
    result = switch_to_minigame("simon")
    if result:
        print("Vyhrál jsi!")
    else:
        print("Prohrál jsi!")


