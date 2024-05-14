import pygame as pg
from pygame import K_ESCAPE, KEYDOWN, QUIT

import netcode
import common

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def handle_events() -> bool:
    """Events handling function."""
    for event in pg.event.get():
        if (event.type == QUIT or
            (event.type == KEYDOWN and event.key == K_ESCAPE)):
            exit(0)
    return True

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

def lobby(screen: pg.Surface) -> int:
    while True:
        netcode.client_sync()
        
        if netcode.client_state.game_state == 1: # did the game start?
            return 1

        #if lobby_info == None: # lobby info not yet received
        #    continue

        host_start_button = (150, 600, 200, 50)

        for event in pg.event.get():
            if (event.type == QUIT or
                (event.type == KEYDOWN and event.key == K_ESCAPE)):
                exit(0)
            
            elif event.type == pg.MOUSEBUTTONDOWN:
                if common.is_click_on_ui(host_start_button, event):
                    netcode.start_game()

        screen.fill(BLACK)

        if not result_info == None:
            # TODO: show game results

            continue

        # TODO: draw lobby info

        pg.draw.rect(screen, (127, 127, 127), host_start_button)
        common.game_font.render_to(screen, common.center_in_rect(host_start_button, common.game_font.get_rect("Start game")), "Start game", (255, 255, 255))

        pg.display.update()

# == level ==

def level(screen: pg.Surface) -> int:
    """Level function."""
    clock = pg.time.Clock()
    sprites = pg.sprite.Group()

    while handle_events():
        netcode.client_sync()

        sprites.update()

        screen.fill(BLACK)
        sprites.draw(screen)
        pg.display.update()
        clock.tick(60)
    
    return 0 # return to lobby

def init_game() -> pg.Surface:
    """Pygame init function."""
    pg.init()
    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pg.display.set_caption('Game')
    return screen

def main(scene_id: int = 0) -> None:
    """Main function."""
    screen = init_game()

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

    exit(0) # use atexit for cleaning up
