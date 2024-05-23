import pygame as pg
from pygame import K_ESCAPE, KEYDOWN, QUIT
import os

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
x = 0
y = 0
xp = 500
yp = 0
x1 = 4070
y1 = 0
x2 = 1374
y2 = 0
x3 = 1187
y3 = 1020

file_path = os.path.join(os.path.dirname(__file__), "pixil-frame-0 (3).png")
file_path2 = os.path.join(os.path.dirname(__file__), "pixil-frame-0 (5).png")
try:
    obrazek = pg.image.load(file_path)
    obrazekP = pg.image.load(file_path2)
except Exception as e:
    print(f"Error loading images: {e}")
    pg.quit()
    exit(1)

print("Images loaded successfully.")
def handle_events() -> bool:
    """Events handling function."""
    global x, y, x1, y1, x2, x3 ,y2, y3
    keys = pg.key.get_pressed()
    if keys[pg.K_w]:
        y += 20
        y1 += 20
        y2 += 20
        y3 += 20
    if keys[pg.K_s]:
        y -= 20
        y1 -= 20
        y2 -= 20
        y3 -= 20
    if keys[pg.K_a]:
        x += 20
        x1 += 20
        x2 += 20
        x3 += 20
    if keys[pg.K_d]:
        x -= 20
        x1 -= 20
        x2 -= 20
        x3 -= 20
    for event in pg.event.get():
        if (event.type == QUIT or
            (event.type == KEYDOWN and event.key == K_ESCAPE)):
            return False
    return True

def level(screen: pg.Surface) -> None:
    """Level function."""
    clock = pg.time.Clock()
    sprites = pg.sprite.Group()

    while handle_events():
        sprites.update()
        screen.fill(BLACK)
        sprites.draw(screen)
        screen.blit(obrazek, (x, y))
        screen.blit(obrazekP, (xp, yp))
        draw_walls()
        pg.display.update()
        clock.tick(100)
def draw_walls():
        pg.draw.rect(screen, (255, 255, 255), (x, y, 73, 3000))
        pg.draw.rect(screen, (255, 255, 255), (x, y, 4200, 90))
        pg.draw.rect(screen, (255, 255, 255), (x1, y1, 95, 2000))
        pg.draw.rect(screen, (255, 255, 255), (x2, y2, 95, 1114))
        pg.draw.rect(screen, (255, 255, 255), (x, y3, 910, 95))
        pg.draw.rect(screen, (255, 255, 255), (x3, y3, 1025, 95))

def init_game() -> pg.Surface:
    global screen
    """Pygame init function."""
    pg.init()
    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pg.display.set_caption('Game')
    
    return screen

def main(scene_id: int = 0) -> None:
    """Main function."""
    screen = init_game()

    
    level(screen)

if __name__ == '__main__':
    main()
    pg.quit()