import pygame as pg
from pygame import K_ESCAPE, KEYDOWN, QUIT

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
x = 0
y = 0
xp = 500
yp = 0

obrazek = pg.image.load("pixil-frame-0 (3).png")
obrazekP = pg.image.load("pixil-frame-0 (5).png")

def handle_events() -> bool:
    """Events handling function."""
    global x, y
    keys = pg.key.get_pressed()
    if keys[pg.K_w]:
        y += 20
    if keys[pg.K_s]:
        y -= 20
    if keys[pg.K_a]:
        x += 20
    if keys[pg.K_d]:
        x -= 20

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
        pg.display.update()
        clock.tick(100)

def init_game() -> pg.Surface:
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

