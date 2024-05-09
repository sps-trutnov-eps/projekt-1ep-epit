from minig import switch_to_minigame
import netcode
import pygame
from pygame import K_ESCAPE, KEYDOWN, QUIT, MOUSEBUTTONDOWN

SCREEN_RESOLUTION = (1280, 960)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        super().__init__()
        self.image = pygame.Surface((w, h))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect(topleft=(x, y))
    
    def update(self, color):
        self.image.fill(color)

def update_sprites(sprites: pygame.sprite.Group, screen: pygame.Surface, team: str) -> None:
    """Sprite update function."""
    sprites.update(BLUE if team == "1.EP" else RED)
    screen.fill(BLACK)
    sprites.draw(screen)
    pygame.display.update()

def map_level(screen: pygame.Surface, score: int = 0, land: list = ["T10"]) -> None:
    """Level function."""
    clock = pygame.time.Clock()
    sprites = pygame.sprite.Group()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                return None
        update_sprites(sprites, screen)
        clock.tick(60)

    switch_to_minigame("piano", screen)
    netcode.client_sync()

def lobby(screen: pygame.Surface):
    sprites = pygame.sprite.Group()
    button = Button(1000 , 100, 200, 50)
    sprites.add(button)
    team = "1.EP"

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                return None
            if button.rect.collidepoint(pygame.mouse.get_pos()) and event.type == MOUSEBUTTONDOWN:
                if team == "1.EP":
                    team = "1.IT"
                else:
                    team = "1.EP"
        print(team)
        update_sprites(sprites, screen, team)

def init_game() -> pygame.Surface:
    """Pygame init function."""
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_RESOLUTION)
    pygame.display.set_caption('EPIT')
    return screen

def main() -> None:
    """Main function."""
    screen = init_game()
    lobby(screen)
    netcode.setup_netcode(("127.0.0.1", 15533), "player #1")

if __name__ == '__main__':
    main()
