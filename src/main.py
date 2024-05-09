from minig import switch_to_minigame
import netcode
import pygame
from pygame import K_ESCAPE, KEYDOWN, QUIT

SCREEN_RESOLUTION = (1280, 960)
BLACK = (0, 0, 0)

def update_sprites(sprites: pygame.sprite.Group, screen: pygame.Surface) -> None:
    """Sprite update function."""
    sprites.update()
    screen.fill(BLACK)
    sprites.draw(screen)
    pygame.display.update()

def map_level(screen: pygame.Surface, score: int = 0, land: list = []) -> None:
    """Level function."""
    clock = pygame.time.Clock()
    sprites = pygame.sprite.Group()

    while True:
        switch_to_minigame("piano", screen)
        update_sprites(sprites, screen)
        clock.tick(60)

    netcode.client_sync()

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
    netcode.setup_netcode(("127.0.0.1", 15533), "player #1")

if __name__ == '__main__':
    main()
