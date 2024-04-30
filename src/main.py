from minig import switch_to_minigame
import pygame
from pygame import K_ESCAPE, KEYDOWN, QUIT

SCREEN_RESOLUTION = (1280, 960)
BLACK = (0, 0, 0)

def handle_events() -> bool:
    """Event function."""
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            return False
    return True

def update_sprites(sprites: pygame.sprite.Group, screen: pygame.Surface) -> None:
    """Sprite update function."""
    sprites.update()
    screen.fill(BLACK)
    sprites.draw(screen)
    pygame.display.update()

def map_level(screen: pygame.Surface, score: int = 0, land: int = 1) -> None:
    """Level function."""
    clock = pygame.time.Clock()
    sprites = pygame.sprite.Group()

    while handle_events():
        switch_to_minigame("piano", screen)
        update_sprites(sprites, screen)
        clock.tick(60)

def init_game() -> pygame.Surface:
    """Pygame init function."""
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_RESOLUTION)
    pygame.display.set_caption('EPIT')
    return screen

def main() -> None:
    """Main function."""
    screen = init_game()
    map_level(screen)

if __name__ == '__main__':
    main()
    pygame.quit()
