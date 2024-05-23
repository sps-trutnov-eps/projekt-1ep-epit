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
# == lobby ==

# lobby data (dict indexed by player_name containing [team_index])
lobby_info: dict[str, list[int]] = None

# can change team by `netcode.change_team(index)` (only when in lobby)

# game result data (TODO)
result_info = None

def set_lobby_info(lobby: list):
    global lobby_info
    lobby_info = lobby

def set_result_info(result: list):
    global result_info
    result_info = result

def lobby(screen: pygame.Surface) -> int:
    while True:
        netcode.client_sync()
        
        if netcode.client_state.game_state == 1: # did the game start?
            return 1

        #if lobby_info == None: # lobby info not yet received
        #    continue

        host_start_button = (150, 600, 200, 50)

        for event in pygame.event.get():
            if (event.type == QUIT or
                (event.type == KEYDOWN and event.key == K_ESCAPE)):
                exit(0)
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if common.is_click_on_ui(host_start_button, event):
                    netcode.start_game()

        screen.fill(BLACK)

        if not result_info == None:
            # TODO: show game results

            continue

        # TODO: draw lobby info

        pygame.draw.rect(screen, (127, 127, 127), host_start_button)
        common.game_font.render_to(screen, common.center_in_rect(host_start_button, common.game_font.get_rect("Start game")), "Start game", (255, 255, 255))

        pygame.display.update()

# == level ==

def level(screen: pygame.Surface) -> int:
    """Level function."""
    clock = pygame.time.Clock()
    sprites = pygame.sprite.Group()

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

def map_level(screen: pygame.Surface, team: int, score: int = 0) -> None:
    """Level function."""
    clock = pygame.time.Clock()
    sprites = pygame.sprite.Group()
    land = ["T10"] if team == 0 else ["T7"]

    while True:
        # switch_to_minigame("piano", screen)
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                return None
        netcode.send_packet(client_state.server_conn, ("land_ep" if "T10" in land else "land_it", land, player_name, protocol_version))
        update_sprites(sprites, screen, team)
        clock.tick(60)
    
    return 0 # return to lobby

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
                map_level(screen, team)
        update_sprites(sprites, screen, team)

def init_game() -> pygame.Surface:
    """Pygame init function."""
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_RESOLUTION)
    pygame.display.set_caption('EPIT')
    return screen

def main(scene_id: int = 0) -> None:
    """Main function."""
    screen = init_game()
    lobby(screen)

    netcode.setup_netcode(("127.0.0.1", 15533), "player #1", True, (set_lobby_info, set_result_info))

    # simple scene switcher, lobby or level return the index of the next scene (None = exit)
    
    loop_list = [
        lobby,
        level
    ]

    while True:
        scene_id = loop_list[scene_id](screen)

if __name__ == '__main__':
    main()
    exit(0)