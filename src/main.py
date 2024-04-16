import pygame as pg
from pygame import K_ESCAPE, KEYDOWN, QUIT

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def handle_events() -> bool:
    """Events handling function."""
    for event in pg.event.get():
        if (event.type == QUIT or
            (event.type == KEYDOWN and event.key == K_ESCAPE)):
            return False
    return True

def map_level(screen: pg.Surface, score: int) -> None:
    """Level function."""
    clock = pg.time.Clock()
    sprites = pg.sprite.Group()

    while handle_events():
        dt = clock.get_time() / 1000
        score += seized_land * dt
        sprites.update()
        screen.fill(BLACK)
        sprites.draw(screen)
        pg.display.update()
        clock.tick(60)
    
    return score

def init_game() -> pg.Surface:
    """Pygame init function."""
    pg.init()
    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pg.display.set_caption('Game')
    return screen

def main() -> None:
    """Main function."""
    screen = init_game()
    start_time = pg.time.get_ticks()
    score = 0

    score = map_level(screen)

if __name__ == '__main__':
    main()
    pg.quit()
