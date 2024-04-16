import math
import queue
from threading import Thread
import pygame
from pygame import K_ESCAPE, KEYDOWN, QUIT

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def handle_events() -> bool:
    """Events handling function."""
    for event in pygame.event.get():
        if (event.type == QUIT or
            (event.type == KEYDOWN and event.key == K_ESCAPE)):
            return False
    return True

def add_score(clock, score: int, seized_land: int, q: queue.Queue) -> None:
    dt = clock.get_time() / 1000
    score += seized_land * dt
    q.put(math.floor(score))

def map_level(screen: pygame.Surface, seized_land: int) -> int:
    """Level function."""
    clock = pygame.time.Clock()
    sprites = pygame.sprite.Group()

    while handle_events():
        sprites.update()
        screen.fill(BLACK)
        sprites.draw(screen)
        pygame.display.update()
        clock.tick(60)
        print(score)

    return math.floor(seized_land)

def init_game() -> pygame.Surface:
    """Pygame init function."""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Game')
    return screen

def main() -> None:
    """Main function."""
    screen = init_game()
    start_time = pygame.time.get_ticks()
    clock = pygame.time.Clock()
    score = 0
    seized_land = 1
    q = queue.Queue()

    t = Thread(target=add_score, args=(clock, score, seized_land, q))
    t.start()
    score = q.get()

    seized_land = map_level(screen, seized_land)

if __name__ == '__main__':
    main()
    pygame.quit()
