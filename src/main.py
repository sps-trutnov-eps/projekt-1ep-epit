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

def handle_events() -> bool:
    """Events handling function."""
    for event in pygame.event.get():
        if (event.type == QUIT or
            (event.type == KEYDOWN and event.key == K_ESCAPE)):
            exit(0)
    return True

# == main menu ==

session_info: tuple

# emulates a pretty normal feeling text input with pygame events
# graphics are VERY WIP, anyone feel free to improve them
def main_menu_text_prompt(screen: pygame.Surface, tooltip_text: str, default_input: str = "") -> str:
    clock = pygame.time.Clock()
    delta_time = 0

    text_input = default_input
    
    is_typing = True
    is_backspace = False
    backspace_cooldown = 0

    pygame.key.start_text_input()

    while is_typing:
        for event in pygame.event.get():
            if (event.type == QUIT or
                (event.type == KEYDOWN and event.key == K_ESCAPE)):
                exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    is_backspace = True
                    backspace_cooldown = .5

                    if len(text_input) != 0:
                        text_input = text_input[:-1]

                elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    if len(text_input) != 0:
                        is_typing = False
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_BACKSPACE:
                    is_backspace = False
            elif event.type == pygame.TEXTINPUT:
                text_input += event.text

        backspace_cooldown -= delta_time
        if is_backspace and backspace_cooldown <= 0 and len(text_input) != 0:
            text_input = text_input[:-1]
            backspace_cooldown = .025

        screen.fill(BLACK)
        
        common.game_font.render_to(screen, common.center_in_rect((SCREEN_RESOLUTION[0] // 2, SCREEN_RESOLUTION[1] // 2 - 25, 0, 0), common.game_font.get_rect(tooltip_text)), tooltip_text, WHITE)
        common.game_font.render_to(screen, common.center_in_rect((SCREEN_RESOLUTION[0] // 2, SCREEN_RESOLUTION[1] // 2, 0, 0), common.game_font.get_rect(text_input)), text_input, WHITE)

        # hehe
        if len(text_input) > 620:
            common.game_font.render_to(screen, common.center_in_rect((SCREEN_RESOLUTION[0] // 2, SCREEN_RESOLUTION[1] // 2 + 50, 0, 0), common.game_font.get_rect("i'm just gonna wait")), "i'm just gonna wait", WHITE)
        elif len(text_input) > 420:
            pass
        elif len(text_input) > 380:
            common.game_font.render_to(screen, common.center_in_rect((SCREEN_RESOLUTION[0] // 2, SCREEN_RESOLUTION[1] // 2 + 50, 0, 0), common.game_font.get_rect("WHY ARE YOU DO DETERMINED")), "WHY ARE YOU DO DETERMINED", WHITE)
        elif len(text_input) > 200:
            pass
        elif len(text_input) > 150:
            common.game_font.render_to(screen, common.center_in_rect((SCREEN_RESOLUTION[0] // 2, SCREEN_RESOLUTION[1] // 2 + 50, 0, 0), common.game_font.get_rect("you know this... won't do anything, right?")), "you know this... won't do anything, right?", WHITE)
        elif len(text_input) > 85:
            common.game_font.render_to(screen, common.center_in_rect((SCREEN_RESOLUTION[0] // 2, SCREEN_RESOLUTION[1] // 2 + 50, 0, 0), common.game_font.get_rect("why...")), "why...", WHITE)
        elif len(text_input) > 35:
            common.game_font.render_to(screen, common.center_in_rect((SCREEN_RESOLUTION[0] // 2, SCREEN_RESOLUTION[1] // 2 + 50, 0, 0), common.game_font.get_rect("what are you doing?")), "what are you doing?", WHITE)

        pygame.display.update()
        delta_time = clock.tick(60) * 0.001

    pygame.key.stop_text_input()

    return text_input

# just allows you to select your name and server ip or host a new game, runs at startup
# graphics are VERY WIP, anyone feel free to improve them
def main_menu(screen: pygame.Surface) -> int:
    global session_info

    # client mode select (join game or host game)

    game_mode = 0

    join_render_area = (SCREEN_RESOLUTION[0] // 2 - 100, SCREEN_RESOLUTION[1] // 2 + 150, 200, 50)
    host_render_area = (SCREEN_RESOLUTION[0] // 2 - 100, SCREEN_RESOLUTION[1] // 2 + 225, 200, 50)

    while game_mode == 0:
        for event in pygame.event.get():
            if (event.type == QUIT or
                (event.type == KEYDOWN and event.key == K_ESCAPE)):
                exit(0)
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if common.is_click_on_ui(join_render_area, event):
                    game_mode = 1
                    break
                elif common.is_click_on_ui(host_render_area, event):
                    game_mode = 2
                    break

        screen.fill(BLACK)

        pygame.draw.rect(screen, (255, 255, 255), join_render_area)
        common.game_font.render_to(screen, common.center_in_rect(join_render_area, common.game_font.get_rect("Join Game")), "Join Game", BLACK)

        pygame.draw.rect(screen, (255, 255, 255), host_render_area)
        common.game_font.render_to(screen, common.center_in_rect(host_render_area, common.game_font.get_rect("Host Game")), "Host Game", BLACK)

        pygame.display.update()

    # selected player name

    player_name = main_menu_text_prompt(screen, "Username:")

    if game_mode == 1:
        # TODO: server list (lan server detection? aaaahhh the netcode nightmares)
        server_ip = main_menu_text_prompt(screen, "Server IP:", "127.0.0.1")
    else:
        server_ip = "127.0.0.1" # auto connect to locally hosted game

    # draw loading screen while connecting to server

    screen.fill(BLACK)
    common.game_font.render_to(screen, common.center_in_rect((SCREEN_RESOLUTION[0] // 2, SCREEN_RESOLUTION[1] // 2 - 25, 0, 0), common.game_font.get_rect("Connecting...")), "Connecting...", WHITE)

    pygame.display.update()

    session_info = (server_ip, player_name, game_mode)

    # connect to server

    netcode.setup_netcode((session_info[0], 15533), session_info[1], True if session_info[2] == 2 else False, (set_lobby_info, set_result_info, set_player_info, set_game_score))

    return 1 # switch scene to lobby

# == dc screen ==

# only used to inform the player of a network error
def dc_screen(screen: pygame.Surface, message: str):
    while handle_events():
        screen.fill(BLACK)
        
        common.game_font.render_to(screen, common.center_in_rect((SCREEN_RESOLUTION[0] // 2, SCREEN_RESOLUTION[1] // 2 - 25, 0, 0), common.game_font.get_rect("Disconnected from server:")), "Disconnected from server:", WHITE)
        common.game_font.render_to(screen, common.center_in_rect((SCREEN_RESOLUTION[0] // 2, SCREEN_RESOLUTION[1] // 2, 0, 0), common.game_font.get_rect(message)), message, WHITE)

        pygame.display.update()

# == lobby ==

# lobby data (dict indexed by player_name containing [team_index])
lobby_info: dict[str, list[int]] = None

# can change team by `netcode.change_team(index)` (only when in lobby)

# game result data (TODO)
result_info = None

def set_lobby_info(lobby: dict):
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
            return 2

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

# == level ==

player_info: dict[str, list] | None = None
game_score: None = None # TODO: set type

def set_player_info(players: dict):
    global player_info
    player_info = players

def set_game_score(score: list):
    global game_score
    game_score = score

def level(screen: pygame.Surface) -> int:
    """Level function."""
    clock = pygame.time.Clock()
    sprites = pygame.sprite.Group()

    while handle_events():
        netcode.client_sync()

        sprites.update()

        screen.fill(BLACK)
        sprites.draw(screen)
        pygame.display.update()
        clock.tick(60)
    
    return 1 # return to lobby

def init_game() -> pygame.Surface:
    """Pygame init function."""
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_RESOLUTION)
    pygame.display.set_caption('EPIT')
    return screen

def main(scene_id:int = 0) -> None:
    """Main function."""
    screen = init_game()

    try:
        # simple scene switcher, lobby or level return the index of the next scene (None = exit)

        loop_list = [
            main_menu,
            lobby,
            level
        ]

        while True:
            scene_id = loop_list[scene_id](screen)
    
    except netcode.GameDisconnect as e:
        dc_screen(screen, e.what)

    while True:
        scene_id = loop_list[scene_id](screen)

if __name__ == '__main__':
    main()
    exit(0)