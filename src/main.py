import math
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
        if event.type == pygame.USEREVENT:
            score += seized_land
    return True

def map_level(screen: pygame.Surface, seized_land: int, score: int) -> None:
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
    pygame.time.set_timer(pygame.USEREVENT, 1000)
    score = 0
    seized_land = 1

    map_level(screen, seized_land, score)

if __name__ == '__main__':
    main()
    pygame.quit()
