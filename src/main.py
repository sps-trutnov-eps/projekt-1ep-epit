from minig import switch_to_minigame
import netcode
import common
import pygame
from pygame import K_ESCAPE, KEYDOWN, QUIT, MOUSEBUTTONDOWN

SCREEN_RESOLUTION = (1280, 960)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

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

# == level ==

def level(screen: pygame.Surface, team: int, score: int = 0) -> None:
    """Level function."""
    clock = pygame.time.Clock()
    sprites = pygame.sprite.Group()
    land = ["T10"] if team == 0 else ["T7"]

    while True:
        # switch_to_minigame("piano", "ep" if "T10" in land else "it", room, score, land, screen)
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                return None
        update_sprites(sprites, screen, team)
        sprites.update(team)
        screen.fill(BLACK)
        sprites.draw(screen)
        pygame.display.update()
        clock.tick(60)
    
    return 0 # return to lobby

# == lobby ==

def lobby(screen: pygame.Surface, team: int = 0) -> int:
    while True:
        netcode.client_sync()
        
        if netcode.client_state.game_state == 1: # did the game start?
            return 1

        #if lobby_info == None: # lobby info not yet received
        #    continue

        host_start_button = (150, 600, 200, 50)
        team_button = (300, 150, 200, 50)

        for event in pygame.event.get():
            if (event.type == QUIT or
                (event.type == KEYDOWN and event.key == K_ESCAPE)):
                exit(0)
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if common.is_click_on_ui(host_start_button, event):
                    netcode.start_game()
                    return team
                if common.is_click_on_ui(team_button, event):
                    team = 0 if team == 1 else 1

        screen.fill(BLACK)

        if not result_info == None:
            # TODO: show game results

            continue

        # TODO: draw lobby info

        pygame.draw.rect(screen, (127, 127, 127), host_start_button)
        pygame.draw.rect(screen, (127, 127, 127), team_button)
        common.game_font.render_to(screen, common.center_in_rect(host_start_button, common.game_font.get_rect("Start game")), "Start game", (255, 255, 255))

        pygame.display.update()

def init_game() -> pygame.Surface:
    """Pygame init function."""
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_RESOLUTION)
    pygame.display.set_caption('EPIT')
    return screen

def main() -> None:
    """Main function."""
    screen = init_game()

    netcode.setup_netcode(("127.0.0.1", 15533), "player 1", True, (set_lobby_info, set_result_info))

    # simple scene switcher, lobby or level return the index of the next scene (None = exit)

    team = lobby(screen)
    level(screen, 0)

if __name__ == '__main__':
    main()
    exit(0)