import pygame as pg
from pygame import K_ESCAPE, KEYDOWN, QUIT

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Načtení obrázků
try:
    obrazek = pg.image.load("pixil-frame-0 (3).png")
    obrazekP = pg.image.load("pixil-frame-0 (5).png")
except Exception as e:
    print(f"Error loading images: {e}")
    exit(1)

# Definice blokovaných oblastí (stěn mapy)
blocked_areas = [
    pg.Rect(100, 100, 200, 30),   # První zdí
    pg.Rect(400, 300, 150, 25),   # Druhá zdí
    # Další zdi můžete přidat podle potřeby
]

# Výpočet středu mapy
map_center_x = SCREEN_WIDTH // 2
map_center_y = SCREEN_HEIGHT // 2

# Výpočet středu hráče na začátku hry
player_width, player_height = obrazek.get_width(), obrazek.get_height()  # Rozměry hráče
player_x = map_center_x - player_width // 2
player_y = map_center_y - player_height // 2

# Výpočet pozice obrázku P
xp = SCREEN_WIDTH - player_width // 2

def handle_events() -> bool:
    global player_x, player_y
    keys = pg.key.get_pressed()
    x_change, y_change = 0, 0
    if keys[pg.K_w]:
        y_change = -20
    if keys[pg.K_s]:
        y_change = 20
    if keys[pg.K_a]:
        x_change = -20
    if keys[pg.K_d]:
        x_change = 20

    new_x = player_x + x_change
    new_y = player_y + y_change

    # Kolizní detekce s blokovanými oblastmi (stěnami)
    player_rect = pg.Rect(new_x, new_y, player_width, player_height)
    for wall in blocked_areas:
        if player_rect.colliderect(wall):
            return True

    # Kolizní detekce s okrajem okna
    if not (0 <= new_x <= SCREEN_WIDTH - player_width) or not (0 <= new_y <= SCREEN_HEIGHT - player_height):
        return True

    # Kolizní detekce pomocí pixelových hodnot
    for i in range(-2, 3):  # Prozkoumáme okolí hráče v rozsahu 5x5 pixelů
        for j in range(-2, 3):
            check_x = new_x + i
            check_y = new_y + j
            if obrazek.get_at((check_x, check_y)) == BLACK:
                return True  # Pokud narazíme na černou barvu, vrátíme True a zastavíme pohyb

    # Pouze změna souřadnic, pokud není kolize
    player_x = new_x
    player_y = new_y

    for event in pg.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            return False
    return True

def level(screen: pg.Surface) -> None:
    clock = pg.time.Clock()
    while handle_events():
        screen.fill(BLACK)
        # Vykreslení blokovaných oblastí (stěn mapy)
        for wall in blocked_areas:
            pg.draw.rect(screen, WHITE, wall)
        screen.blit(obrazek, (player_x, player_y))
        screen.blit(obrazekP, (xp, SCREEN_HEIGHT // 2))  # Pozice obrázku P
        pg.display.update()
        clock.tick(60)

def init_game() -> pg.Surface:
    pg.init()
    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pg.display.set_caption('Game')
    return screen

def main() -> None:
    screen = init_game()
    level(screen)

if __name__ == '__main__':
    main()
    pg.quit()
