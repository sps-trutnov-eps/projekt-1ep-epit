import pygame as pg
from pygame import K_ESCAPE, KEYDOWN, QUIT
import random
from typing import List

SCREEN_WIDTH = 1360
SCREEN_HEIGHT = 756
TILE_SIZE = 256
MAP_SIZE = 15

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class player():

    def _collisions(self, layout, direction):
        for y, row in enumerate(layout):
            for x, tile in enumerate(row):
                if tile == '#':
                    tile_rect = pg.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    if self.rect.colliderect(tile_rect):
                        self._handle_collision(tile_rect, direction)
        if direction == 1:
            self.vel.y += self.gravity


def handle_events() -> bool:
    """Events handling function."""
    for event in pg.event.get():
        if (event.type == QUIT or
            (event.type == KEYDOWN and event.key == K_ESCAPE)):
            return False
    return True

def _handle_collision(self, tile_rect, direction):
        if direction == 0:
            if self.rect.right - tile_rect.left < TILE_SIZE // 2:
                self.rect.right = tile_rect.left
                self.vel.x = 0
            elif self.rect.left - tile_rect.right > -TILE_SIZE // 2:
                self.rect.left = tile_rect.right
                self.vel.x = 0
        elif direction == 1:
            if self.rect.bottom - tile_rect.top < TILE_SIZE // 2:
                self.rect.bottom = tile_rect.top
                self.vel.y = 0
            elif self.rect.top - tile_rect.bottom > -TILE_SIZE // 2:
                self.rect.top = tile_rect.bottom
                self.vel.y = 0

def mapa():
    global layout ,player
    layout = [['#', "#", '#', '#', '#', '#', '#', '#', '#' '#', '#', "#", ],
                ['#', " ", "#", ' ', '#', ' ', ' ', ' ', ' ', '#' ' ', '#',],
                ['#', " ", "#", ' ', '#', ' ', ' ', ' ', ' ', '#' ' ', '#',],
                ['#', " ", "#", ' ', '#', '#', '#', ' ', '#', '#' ' ', ' ', '#', '#',],
                ['#', " ", " ", ' ', ' ', ' ', ' ', ' ', ' ', ' ' ' ', ' ', ' ', '#',],
                ['#', "#", "#", ' ', '#', '#', '#', ' ', '#', '#' '#', '#', ' ', '#',],
                ['#', " ", " ", ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#' ' ', ' ', '#',],
                ["#", " ", "#", " ", "#", " ", "#", " ", "#", " ", ' ', '#' ' ', ' ', '#',],
                ["#", " ", "#", " ", "#", " ", "#", " ", "#", " ", ' ', '#' ' ', ' ', '#',],
                ["#", "#", "#", "#", "#", "#", "#", " ", "#", "#", '#', '#', '#', '#', '#',]]
    player = player(TILE_SIZE + TILE_SIZE // 2, 4*TILE_SIZE)
def draw(screen: pg.Surface, layout: List[List[str]],
            player, camera_x, camera_y, iterate: bool) -> None:
    """Draw function."""
    screen.fill(BLACK)
    for y, row in enumerate(layout):
        if y*TILE_SIZE - camera_y >= 0 or y*TILE_SIZE - camera_y <= SCREEN_WIDTH:
            for x, tile in enumerate(row):
                if (tile in ['#', 'E'] and (x*TILE_SIZE - camera_x >= 0 or \
                    x*TILE_SIZE - camera_x <= SCREEN_HEIGHT)):
                    tile_rect = pg.Rect((x*TILE_SIZE - camera_x),
                                            (y*TILE_SIZE - camera_y), TILE_SIZE, TILE_SIZE)
                    pg.draw.rect(screen, WHITE if tile == '#' else YELLOW, tile_rect)
    player.draw(screen)

def update_camera(player, layout: List[List[str]], screen: pg.Surface):
    """Camera update function."""
    camera_x = min(max(player.rect.centerx - screen.get_width() // 2, 0),
                    len(layout[0])*TILE_SIZE - screen.get_width())
    camera_y = min(max(player.rect.centery - screen.get_height() // 2, 0),
                    len(layout)*TILE_SIZE - screen.get_height())

    return camera_x, camera_y

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
    level(screen)
    camera_x, camera_y = update_camera(player, layout, screen)
    draw(screen, layout, player, camera_x, camera_y, False)

if __name__ == '__main__':
    main()
    pg.quit()
    