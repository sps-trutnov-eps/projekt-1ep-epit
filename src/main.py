from minig import switch_to_minigame
import netcode
import threading
import pygame
from pygame import K_ESCAPE, KEYDOWN, QUIT

SCREEN_RESOLUTION = (1280, 960)
BLACK = (0, 0, 0)

def handle_events() -> None:
    """Event function."""
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            exit(0)

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

    while True:
        netcode.client_sync()
        switch_to_minigame("test", screen)
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
    netcode.setup_netcode(("127.0.0.1", 15533), "player #1")
    map_level(screen)

if __name__ == '__main__':
    thread = threading.Thread(target=handle_events)
    thread.start()
    main()
