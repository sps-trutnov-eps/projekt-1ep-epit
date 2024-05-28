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
x4 = 2674
x5 = 2490
x6 = 0
y6 = 2880
x7 = 628
y7 = 1074
x8 = 628
y8 = 1574
x9 = 1374
y9 = 1760
x10 = 1000
y10 = 1760
x11 = 1374
y11 = 1760
x12 = 1930
y12 = 1760
x13 = 3232
y13 = 1760
x14 = 3232
y14 = 1020
x15 = 3420
y15 = 1100
x16 = 3420
y16 = 1575
x17 = 2750
y17 = 2880
x18 = 2675
y18 = 1830
x19 = 1450
y19 = 3250

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
    global x, y, x1, y1, x2, x3 ,y2, y3, x4, x5, x6, y6, x7, y7, x8, y8, x9, y9, x10, y10, x11, y11, x12, y12, x13, y13, x14, y14, x15, y15, x16, y16, x17, y17, x18, y18, x19, y19
    keys = pg.key.get_pressed()
    if keys[pg.K_w]:
        y += 20
        y1 += 20
        y2 += 20
        y3 += 20
        y6 += 20
        y7 += 20
        y8 += 20
        y9 += 20
        y10 += 20
        y11 += 20
        y12 += 20
        y13 += 20
        y14 += 20
        y15 += 20
        y16 += 20
        y17 += 20
        y18 += 20
        y19 += 20

    if keys[pg.K_s]:
        y -= 20
        y1 -= 20
        y2 -= 20
        y3 -= 20
        y6 -= 20
        y7 -= 20
        y8 -= 20
        y9 -= 20
        y10 -= 20
        y11 -= 20
        y12 -= 20
        y13 -= 20
        y14 -= 20
        y15 -= 20
        y16 -= 20
        y17 -= 20
        y18 -= 20
        y19 -= 20

    if keys[pg.K_a]:
        x += 20
        x1 += 20
        x2 += 20
        x3 += 20
        x4 += 20
        x5 += 20
        x6 += 20
        x7 += 20
        x8 += 20
        x9 += 20
        x10 += 20
        x11 += 20
        x12 += 20
        x13 += 20
        x14 += 20
        x15 += 20
        x16 += 20
        x17 += 20
        x18 += 20
        x19 += 20

    if keys[pg.K_d]:
        x -= 20
        x1 -= 20
        x2 -= 20
        x3 -= 20
        x4 -= 20
        x5 -= 20
        x6 -= 20
        x7 -= 20
        x8 -= 20
        x9 -= 20
        x10 -= 20
        x11 -= 20
        x12 -= 20
        x13 -= 20
        x14 -= 20
        x15 -= 20
        x16 -= 20
        x17 -= 20
        x18 -= 20
        x19 -= 20
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
    pg.draw.rect(screen, (255, 255, 255), (x1, y1, 95, 3000))
    pg.draw.rect(screen, (255, 255, 255), (x2, y2, 95, 1114))
    pg.draw.rect(screen, (255, 255, 255), (x, y3, 910, 95))
    pg.draw.rect(screen, (255, 255, 255), (x3, y3, 1025, 95))
    pg.draw.rect(screen, (255, 255, 255), (x4, y2, 95, 1114))
    pg.draw.rect(screen, (255, 255, 255), (x5, y3, 469, 95))
    pg.draw.rect(screen, (255, 255, 255), (x6, y6, 1470, 95))
    pg.draw.rect(screen, (255, 255, 255), (x7, y7, 95, 250))
    pg.draw.rect(screen, (255, 255, 255), (x8, y8, 95, 1310))
    pg.draw.rect(screen, (255, 255, 255), (x9, y9, 95, 1610))
    pg.draw.rect(screen, (255, 255, 255), (x10, y10, 95, 1310))
    pg.draw.rect(screen, (255, 255, 255), (x11, y11, 280, 98))
    pg.draw.rect(screen, (255, 255, 255), (x12, y12, 1040, 98))
    pg.draw.rect(screen, (255, 255, 255), (x13, y13, 280, 98))
    pg.draw.rect(screen, (255, 255, 255), (x14, y14, 850, 95))
    pg.draw.rect(screen, (255, 255, 255), (x15, y15, 95, 200))
    pg.draw.rect(screen, (255, 255, 255), (x16, y16, 95, 1310))
    pg.draw.rect(screen, (255, 255, 255), (x17, y17, 1500, 95))
    pg.draw.rect(screen, (255, 255, 255), (x18, y18, 95, 1500))
    pg.draw.rect(screen, (255, 255, 255), (x19, y19, 1400, 95))

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