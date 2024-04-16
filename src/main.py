import math
import pygame as pg
from pygame import K_ESCAPE, KEYDOWN, QUIT

SCREEN_WIDTH = 800  # Adjusted screen width
SCREEN_HEIGHT = 600  # Adjusted screen height

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

CELL_SIZE = 50
ZOOM_FACTOR = 1.5  # Increase this value for more zoom

def handle_events() -> bool:
    """Events handling function."""
    for event in pg.event.get():
        if (event.type == QUIT or
            (event.type == KEYDOWN and event.key == K_ESCAPE)):
            return False
    return True

def draw_map(screen: pg.Surface, layout: list, view_x: int, view_y: int) -> None:
    """Draws the map."""
    for y, row in enumerate(layout):
        for x, cell in enumerate(row):
            if (x * CELL_SIZE >= view_x and x * CELL_SIZE < view_x + SCREEN_WIDTH // ZOOM_FACTOR and
                    y * CELL_SIZE >= view_y and y * CELL_SIZE < view_y + SCREEN_HEIGHT // ZOOM_FACTOR):
                if cell == '#':
                    color = WHITE
                else:
                    color = BLACK
                pg.draw.rect(screen, color, ((x * CELL_SIZE - view_x) * ZOOM_FACTOR, (y * CELL_SIZE - view_y) * ZOOM_FACTOR, CELL_SIZE * ZOOM_FACTOR, CELL_SIZE * ZOOM_FACTOR))

def map_level(screen: pg.Surface, layout: list, score: int, seized_land: int) -> int:
    """Level function."""
    clock = pg.time.Clock()
    sprites = pg.sprite.Group()

    view_x = 0
    view_y = 0

    while handle_events():
        dt = clock.get_time() / 1000
        score += seized_land * dt
        sprites.update()
        screen.fill(BLACK)
        draw_map(screen, layout, view_x, view_y)  # Draw the map
        sprites.draw(screen)
        pg.display.update()
        clock.tick(60)

    return score, math.floor(seized_land)

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
    seized_land = 0

    layout = [['#', "#", '#', '#', '#', '#', '#', '#', '#', '#', '#', "#", ],
              ['#', " ", "#", ' ', '#', ' ', ' ', ' ', ' ', '#', ' ', '#',],
              ['#', " ", "#", ' ', '#', ' ', ' ', ' ', ' ', '#', ' ', '#',],
              ['#', " ", "#", ' ', '#', '#', '#', ' ', '#', '#', ' ', ' ', '#', '#',],
              ['#', " ", " ", ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#',],
              ['#', "#", "#", ' ', '#', '#', '#', ' ', '#', '#', '#', '#', ' ', '#',],
              ['#', " ", " ", ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#', ' ', ' ', '#',],
              ["#", " ", "#", " ", "#", " ", "#", " ", "#", " ", ' ', '#', ' ', ' ', '#',],
              ["#", " ", "#", " ", "#", " ", "#", " ", "#", " ", ' ', '#', ' ', ' ', '#',],
              ["#", "#", "#", "#", "#", "#", "#", " ", "#", "#", '#', '#', '#', '#', '#',]]

    score, seized_land = map_level(screen, layout, score, seized_land)

if __name__ == '__main__':
    main()
    pg.quit()
