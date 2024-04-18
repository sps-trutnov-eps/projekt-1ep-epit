import pygame
from pygame import K_ESCAPE, KEYDOWN, QUIT

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 960
BLACK = (0, 0, 0)

def handle_events(score: int, seized_land: int) -> int:
    """Event function."""
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            return None
        if event.type == pygame.USEREVENT:
            score += seized_land
    return score

def update_sprites(sprites: pygame.sprite.Group, screen: pygame.Surface) -> None:
    """Sprite update function."""
    sprites.update()
    screen.fill(BLACK)
    sprites.draw(screen)
    pygame.display.update()

def map_level(screen: pygame.Surface, seized_land: int = 0, score: int = 0) -> None:
    """Level function."""
    clock = pygame.time.Clock()
    sprites = pygame.sprite.Group()

    while score is not None:
        score = handle_events(score, seized_land)
        update_sprites(sprites, screen)
        clock.tick(60)

def init_game() -> pygame.Surface:
    """Pygame init function."""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('EPIT')
    return screen

def main() -> None:
    """Main function."""
    screen = init_game()
    pygame.time.set_timer(pygame.USEREVENT, 1000)
    map_level(screen)

if __name__ == '__main__':
    main()
    pygame.quit()
