from minig import switch_to_minigame
import netcode
import pygame
from pygame import K_ESCAPE, KEYDOWN, QUIT, MOUSEBUTTONDOWN

SCREEN_RESOLUTION = (1280, 960)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

class ClassButton(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.font = pygame.font.Font(None, 64)
        self.text = self.font.render("1.EP", True, WHITE, None)
        self.rect = self.text.get_rect(topleft=(x, y))
        self.image = pygame.Surface((self.text.get_width(), self.text.get_height()))
        self.image.fill(BLUE)

    def update(self, team):
        self.image.fill(BLUE if team == 0 else RED)
        self.text = (self.font.render("1.EP", True, WHITE, None) if team == 0 else self.font.render("1.IT", True, WHITE, None))
        self.image.blit(self.text, (0, 0))

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class PlayButton(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.font = pygame.font.Font(None, 64)
        self.text = self.font.render("Play", True, WHITE, None)
        self.rect = self.text.get_rect(center=(x, y))
        self.image = pygame.Surface((self.text.get_width(), self.text.get_height()))
        self.image.fill(RED)
        self.image.blit(self.text, (0, 0))

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("player0.png")
        self.rect = self.image.get_rect(center=(x, y))
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)

def update_sprites(sprites: pygame.sprite.Group, screen: pygame.Surface, team: int) -> None:
    """Sprite update function."""
    sprites.update(team)
    screen.fill(BLACK)
    sprites.draw(screen)
    pygame.display.update()

def map_level(screen: pygame.Surface, score: int = 0, land: list = ["T10"]) -> None:
    """Level function."""
    clock = pygame.time.Clock()
    sprites = pygame.sprite.Group()

    while True:
        # switch_to_minigame("piano", screen)
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                return None
        update_sprites(sprites, screen)
        clock.tick(60)
        # netcode.client_sync()

def lobby(screen: pygame.Surface):
    sprites = pygame.sprite.Group()
    class_button = ClassButton(SCREEN_RESOLUTION[0]*(4 / 5) , SCREEN_RESOLUTION[1]*(1 / 5))
    sprites.add(class_button)
    play_button = PlayButton(SCREEN_RESOLUTION[0] // 2 , SCREEN_RESOLUTION[1]*(4 / 5))
    sprites.add(play_button)
    for i in range(6):
        player = Player(SCREEN_RESOLUTION[0]*((1 + i) / 7), SCREEN_RESOLUTION[1] // 2)
        sprites.add(player)
    team = 0

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                return None
            if class_button.rect.collidepoint(pygame.mouse.get_pos()) and event.type == MOUSEBUTTONDOWN:
                if team == 0:
                    team = 1
                else:
                    team = 0
            if play_button.rect.collidepoint(pygame.mouse.get_pos()) and event.type == MOUSEBUTTONDOWN:
                map_level(screen)
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
    # netcode.setup_netcode(("127.0.0.1", 15533), "player #1")

if __name__ == '__main__':
    main()
