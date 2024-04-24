import pygame as pg
from pygame import K_ESCAPE, KEYDOWN, QUIT

import netcode
import common

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def handle_events() -> bool:
    """Events handling function."""
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
        netcode.client_sync()

        sprites.update()

        screen.fill(BLACK)
        sprites.draw(screen)
        pg.display.update()
        clock.tick(60)

def init_game() -> pg.Surface:
    """Pygame init function."""
    pg.init()
    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pg.display.set_caption('Game')
    return screen

def main(scene_id: int = 0) -> None:
    """Main function."""
    screen = init_game()

    netcode.setup_netcode(False)
    level(screen)

if __name__ == '__main__':
    main()

    exit(0)
