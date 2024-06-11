import time
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

def lobby(screen: pygame.Surface) -> int:
    pygame.display.set_caption('lobby')

    black = (0, 0, 0)
    brown = (139, 69, 19)
    gray = (169, 169, 169)
    light_brown = (205, 133, 63)
    blue = (0, 0, 255)
    dark_gray = (50, 50, 50)

    center = (400, 300)
    square_size = 550
    
    def draw_table_and_chairs(surface, table_color, chair_color, table_rect, chair_size, gap):
        pygame.draw.rect(surface, table_color, table_rect)
    
        table_x, table_y, table_width, table_height = table_rect
        chair_width, chair_height = chair_size
    
        pygame.draw.rect(surface, chair_color, (table_x + (table_width - chair_width * 2 - gap) / 2, table_y - chair_height - 5, chair_width, chair_height))
        pygame.draw.rect(surface, chair_color, (table_x + (table_width + gap) / 2, table_y - chair_height - 5, chair_width, chair_height))
    
    def draw_square(surface, color, center, size):
        top_left = (center[0] - size // 2, center[1] - size // 2)
        pygame.draw.rect(surface, color, (*top_left, size, size))
        
    def draw_teacher_table_and_chair(surface, table_color, chair_color, table_rect, chair_rect):
        pygame.draw.rect(surface, table_color, table_rect)
        pygame.draw.rect(surface, chair_color, chair_rect)
    
    def draw_door(surface, color, position, size, knob_color, knob_radius):
        pygame.draw.rect(surface, color, pygame.Rect(position, size))
        knob_position = (position[0] + size[0] - knob_radius, position[1] + knob_radius)
        pygame.draw.circle(surface, knob_color, knob_position, 3)
        
    running = True

    player_state = ([400, 300], [0, 0])

    t = time.time()
    
    while running:
        netcode.client_sync()
        
        if netcode.client_state.game_state == 1: # did the game start?
            return 2

        #if lobby_info == None: # lobby info not yet received
        #    continue

        host_start_button = (150, 600, 200, 50)
        team_button = (300, 150, 200, 50)

        colliders = [
            (center[0] - square_size // 2 - 50, center[1] - square_size // 2 - 50, square_size + 100, 50),
            (center[0] - square_size // 2 - 50, center[1] - square_size // 2 - 50, 50, square_size + 100),
            (center[0] - square_size // 2 - 50, center[1] + square_size // 2, square_size + 100, 50),
            (center[0] + square_size // 2, center[1] - square_size // 2 - 50, 50, square_size + 100),
        ]

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

        screen.fill(black)
        
        draw_square(screen, dark_gray, center, square_size + 20)
        draw_square(screen, brown, center, square_size)
        
        table_width, table_height = 60, 30
        chair_width, chair_height = 25, 25
        rows = 4
        cols = 4
        spacing = 40
        gap = 5
        vertical_offset = -40
        horizontal_offset = -40 
        
        start_x = center[0] - (cols * (table_width + spacing) / 2) + (table_width / 2) + horizontal_offset
        start_y = center[1] - (cols * (table_height + chair_height + spacing) / 2) + chair_height + (table_height / 2) + vertical_offset
        
        for row in range(rows):
            for col in range(cols):
                table_x = start_x + col * (table_width + spacing)
                table_y = start_y + row * (table_height + chair_height + spacing)
                chair_x = start_x + col * (table_width + spacing)
                chair_y = start_y + row * (table_height + chair_height + spacing)
                table_rect = (table_x, table_y, table_width, table_height)
                chair_rect = (chair_x, chair_y, chair_width, chair_height)
                draw_table_and_chairs(screen, light_brown, light_brown, table_rect, (chair_width, chair_height), gap)
                
                colliders.append(table_rect)

        teacher_table_width, teacher_table_height = 35, 25 #je to naopak, table width, height zaznamenává velikost židle a chair width, height zaznamenává velikost stolu
        teacher_chair_width, teacher_chair_height = 100, 40
                
        teacher_table_x = center[0] - square_size // 2 + 10
        teacher_table_y = center[1] + square_size // 2 - teacher_table_height - 10
            
        teacher_chair_x = teacher_table_x + (teacher_table_width - teacher_table_width) // 2
        teacher_chair_y = teacher_table_y - teacher_chair_height - 5
            
        teacher_table_rect = (teacher_table_x, teacher_table_y, teacher_table_width, teacher_table_height)
        teacher_chair_rect = (teacher_chair_x, teacher_chair_y, teacher_chair_width, teacher_chair_height)
            
        door_width, door_height = 10, 70
        door_x = center[0] + square_size // 2 - door_width
        door_y = center[1] + square_size // 2 - door_height - 10
        draw_door(screen, gray, (door_x, door_y), (door_width, door_height), black, 10)
            
        draw_teacher_table_and_chair(screen, black, light_brown, teacher_table_rect, teacher_chair_rect)
        colliders.append(teacher_chair_rect)

        #pygame.draw.rect(screen, blue, (player_x, player_y, player_width, player_height))
        
        # updates the delta (frame) time and player movement

        delta_time = time.time() - t
        t = time.time()

        # temp color squares, would be replaced with skins if implemented

        player_state = common.player_move_update(pygame.key.get_pressed(), delta_time, player_state, colliders)
        draw_square(screen, (255, 0, 0), player_state[0], common.pm_player_size * 2)

        netcode.update_player_info(player_state[0], player_state[1])

        pred_time = (time.time() - player_info_age) * .9

        if not player_info == None:
            for name, p in player_info.items():
                if name == session_info[1]: # do not render the local player
                    continue
                
                # TODO: prediction can be improved

                # pred_p = common.player_move_update({}, pred_time, (p[0], p[1]), colliders)
                pred_p = (p[0][0] + p[1][0] * pred_time, p[0][1] + p[1][1] * pred_time) # simple velocity add

                draw_square(screen, (0, 255, 0), pred_p, common.pm_player_size * 2)

        pygame.display.update()

# == level ==

player_info: dict[str, list] | None = None
player_info_age: float = 0

game_score: None = None # TODO: set type

def set_player_info(players: dict):
    global player_info
    global player_info_age

    player_info = players
    player_info_age = time.time()

def set_game_score(score: list):
    global game_score
    game_score = score

def level(screen: pygame.Surface, land: str, score: int = 0) -> int:
    """Level function."""
    clock = pygame.time.Clock()
    sprites = pygame.sprite.Group()
    team = ("ep" if land[0] == "T10" else "it")

    while handle_events():
        netcode.client_sync()

        # minigame = {
        #     "classroom": "minigame"
        # }

        # minig.switch_to_minigame( minigame[room], team, room, land, score, screen)

        sprites.update()

        screen.fill(BLACK)
        sprites.draw(screen)
        pygame.display.update()
        clock.tick(60)
    
    return 1 # return to lobby

def init_game() -> pygame.Surface:
    """Pygame init function."""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_RESOLUTION[0], SCREEN_RESOLUTION[1]))
    pygame.display.set_caption('Game')
    return screen

def p_test(screen: pygame.Surface) -> int:
    p_state = ([0, 0], [0, 0])

    wall_rects = [
        (100, 100, 50, 50),
        (100, 200, 20, 50),
        (300, 200, 20, 20),
        (200, 200, 50, 50),
        (100, 510, 51, 50),
        (300, 100, 51, 20),
    ]
    
    import time

    t1 = time.time()

    while handle_events():
        screen.fill(BLACK)

        delta_time = time.time() - t1
        t1 = time.time()

        p_state = common.player_move_update(pygame.key.get_pressed(), delta_time, p_state, wall_rects)
        pygame.draw.rect(screen, (255, 0, 0), (p_state[0][0] - common.pm_player_size, p_state[0][1] - common.pm_player_size, common.pm_player_size * 2, common.pm_player_size * 2))
        
        for w in wall_rects:
            pygame.draw.rect(screen, (0, 255, 0), w)

        pygame.display.update()

def main(scene_id: int = 0) -> None:
    """Main function."""
    screen = init_game()
    
    # p_test(screen)

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