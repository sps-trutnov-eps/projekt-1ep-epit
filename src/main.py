import pygame as pg
from pygame import K_ESCAPE, KEYDOWN, QUIT

import minig
import netcode

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

    if False: # if is host
        # start server thread
        server_thread = netcode.threading.Thread(target=netcode.start_server())
        server_thread.start()

    minig.switch_to_minigame("test", screen)
    level(screen)

if __name__ == '__main__':
    main()
    pg.quit()
