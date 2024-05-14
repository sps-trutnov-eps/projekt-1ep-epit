from minig import switch_to_minigame
import netcode
import pygame
from pygame import K_ESCAPE, KEYDOWN, QUIT, MOUSEBUTTONDOWN

SCREEN_RESOLUTION = (1280, 960)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

player0 = pygame.image.load("player0.png")
player1 = pygame.image.load("player1.png")
player2 = pygame.image.load("player2.png")
player3 = pygame.image.load("player3.png")
player4 = pygame.image.load("player4.png")
player5 = pygame.image.load("player5.png")

class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        super().__init__()
        self.image = pygame.Surface((w, h))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect(topleft=(x, y))
    
    def update(self, color):
        self.image.fill(color)

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.x = x
        self.y = y
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
    
    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

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
    button = Button(SCREEN_RESOLUTION[0]*(4 / 5) , SCREEN_RESOLUTION[1]*(1 / 5), 200, 50)
    for i in range(5):
        player = Player(SCREEN_RESOLUTION[0]*((1 + i) / 6), SCREEN_RESOLUTION // 2, player0)
    sprites.add(button)
    team = 0

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                return None
            if button.rect.collidepoint(pygame.mouse.get_pos()) and event.type == MOUSEBUTTONDOWN:
                if team == 0:
                    team = 1
                else:
                    team = 0
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
