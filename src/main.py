import time
import netcode
import common
import pygame
import json
import random
from pygame import K_ESCAPE, KEYDOWN, QUIT

pygame.init()

import minig

SCREEN_RESOLUTION = (1280, 960)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (127, 127, 127)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

TEAMS = {
    "ep": BLUE,
    "it": RED,
}

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

    join_render_area = (SCREEN_RESOLUTION[0] // 2 - 100 + 150, SCREEN_RESOLUTION[1] // 2 - 25 - 40, 200, 50)
    host_render_area = (SCREEN_RESOLUTION[0] // 2 - 100 + 150, SCREEN_RESOLUTION[1] // 2 - 25 + 40, 200, 50)

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

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                editor(screen)

        screen.fill(BLACK)

        common.game_font.render_to(screen, common.center_in_rect((SCREEN_RESOLUTION[0] // 2 - 150 - 48, SCREEN_RESOLUTION[1] // 2, 0, 0), common.game_font.get_rect("EP", size=100)), "EP", TEAMS["ep"], size=100)
        common.game_font.render_to(screen, common.center_in_rect((SCREEN_RESOLUTION[0] // 2 - 150 + 48, SCREEN_RESOLUTION[1] // 2, 0, 0), common.game_font.get_rect("it", size=100)), "it", TEAMS["it"], size=100)

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

# lobby data (dict indexed by player_name containing [team_name, skin_index])
lobby_info: dict[str, tuple[str, int]] | None = None

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
    green = (0, 255, 0)

    center = (640, 480)
    square_size = 550
    
    
    def is_click_on_ui(button_rect, event):
        return button_rect.collidepoint(event.pos)
    
    def start_game():
            netcode.start_game()

    
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
        
    player_state = ([400, 300], [0, 0])

    t = time.time()
    sel_team = "ep"
    
    while True:
        netcode.client_sync()
        
        if netcode.client_state.game_state == 1: # did the game start?
            return 2

        if not lobby_info == None:
            sel_team = lobby_info[session_info[1]][0]

        host_start_button = (250, 400, 100, 40)
        team_button = (150, 450, 200, 50)

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
                if common.is_click_on_ui(host_start_button, event) and netcode.client_state.is_host:
                    netcode.start_game()
                if common.is_click_on_ui(team_button, event):
                    sel_team = "ep" if sel_team == "it" else "it"
                    netcode.change_team(sel_team)

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
        
        if netcode.client_state.is_host:
            #host_start_button = (door_x + 25, door_y)
            pygame.draw.rect(screen, green, host_start_button)
            font = pygame.font.Font(None, 36)
            text = font.render("Start", True, black)
            text_rect = text.get_rect(center=pygame.Rect(host_start_button).center)
            screen.blit(text, text_rect)
        pygame.draw.rect(screen, blue, team_button)
        font = pygame.font.Font(None, 36)
        text = font.render("Change team", True, black)
        text_rect = text.get_rect(center=pygame.Rect(team_button).center)
        screen.blit(text, text_rect)

        #pygame.draw.rect(screen, blue, (player_x, player_y, player_width, player_height))
        
        # updates the delta (frame) time and player movement

        delta_time = time.time() - t
        t = time.time()

        # temp color squares, would be replaced with skins if implemented

        player_state = common.player_move_update(pygame.key.get_pressed(), delta_time, player_state, colliders)
        draw_square(screen, TEAMS[sel_team], player_state[0], common.pm_player_size * 2)

        netcode.update_player_info(player_state[0], player_state[1])

        pred_time = (time.time() - player_info_age) * .9

        if not player_info == None:
            for name, p in player_info.items():
                if name == session_info[1]: # do not render the local player
                    continue
                
                # TODO: prediction can be improved

                # pred_p = common.player_move_update({}, pred_time, (p[0], p[1]), colliders)
                pred_p = (p[0][0] + p[1][0] * pred_time, p[0][1] + p[1][1] * pred_time) # simple velocity add

                draw_square(screen, TEAMS[lobby_info[name][0] if not lobby_info == None else "ep"], pred_p, common.pm_player_size * 2)
                common.game_font.render_to(screen, (pred_p[0] - common.game_font.get_rect(name).centerx, pred_p[1] - 30), name, WHITE)

        pygame.display.update()

# == level ==

player_info: dict[str, list] | None = None
player_info_age: float = 0

game_score: None = None # TODO: set type

class Camera2D:
    __slots__ = ["x", "y"]

    x: int
    y: int

    def __init__(self) -> None:
        self.set_pos(0, 0)

    def set_pos(self, x, y) -> None:
        self.x = x
        self.y = y

    def get_pos(self) -> tuple[int, int]:
        return (self.x, self.y)

    def offset(self, x, y) -> None:
        self.x += x
        self.y += y
    
    def translate(self, rect: pygame.Rect) -> pygame.Rect:
        return pygame.Rect((rect[0] - self.x + (SCREEN_RESOLUTION[0] // 2), rect[1] - self.y + (SCREEN_RESOLUTION[1] // 2), rect[2], rect[3]))
    
    def translate_inverse(self, pos) -> tuple[int, int]:
        return (pos[0] + self.x - (SCREEN_RESOLUTION[0] // 2), pos[1] + self.y - (SCREEN_RESOLUTION[1] // 2))

def set_player_info(players: dict):
    global player_info
    global player_info_age

    player_info = players
    player_info_age = time.time()

def set_game_score(score: list):
    global game_score
    game_score = score

# map_path = "../assets/default_map.json"
map_path = "edit_map.json"

# map_path: str, land: str, score: int = 0
def level(screen: pygame.Surface) -> int:
    """Level function."""

    pygame.display.set_caption("In-Game")

    # load selected map file

    with open(map_path, "r") as f:
        map_data = json.load(f)

    bg_surface = pygame.transform.scale_by(pygame.image.load(map_data["map_background"][0]), map_data["map_background"][1]).convert() 
    bg_rect = bg_surface.get_rect()
    bg_rect = (bg_rect[0] - bg_rect.centerx, bg_rect[1] - bg_rect.centery, bg_rect[2], bg_rect[3])

    inter_surface = pygame.image.load("../assets/interact_notification.png")
    inter_rect = inter_surface.get_rect()
    inter_rect = (inter_rect[0] - inter_rect.centerx, inter_rect[1] - inter_rect.centery, inter_rect[2], inter_rect[3])

    map_colliders = map_data["map_colliders"]
    map_interactibles = map_data["map_interactibles"]

    prop_preload_surfs = {}
    for p in map_data["map_props"]:
        if p[0] in prop_preload_surfs:
            continue

        prop_preload_surfs[p[0]] = pygame.image.load(p[0]).convert_alpha() # unscaled, unconverted, only raw image data

    map_props = []
    for p in map_data["map_props"]:
        prop_surf = pygame.transform.scale_by(prop_preload_surfs[p[0]], p[1]).convert_alpha()
        map_props.append((prop_surf, p[2]))

    # game loop

    clock = pygame.time.Clock()
    team = lobby_info[session_info[1]][0]

    cam = Camera2D()
    player_state = [map_data["map_spawnpoints"][team], (0, 0)]

    while handle_events():
        netcode.client_sync()

        # game logic update
        delta_time = clock.get_time() / 1000 # milisec -> sec

        keys = pygame.key.get_pressed()
        player_state = common.player_move_update(keys, delta_time, player_state, map_colliders)
        netcode.update_player_info(player_state[0], player_state[1])

        cam_pos = cam.get_pos()
        cam_diff = (player_state[0][0] - cam_pos[0], player_state[0][1] - cam_pos[1])
        cam_pos = (cam_pos[0] + cam_diff[0] * .09, cam_pos[1] + cam_diff[1] * .09) # light camera interp
        cam.set_pos(*cam_pos)

        is_in_interact = False

        for inter in map_interactibles:
            dist_squared = (player_state[0][0] - inter[2][0]) ** 2 + (player_state[0][1] - inter[2][1]) ** 2
            if dist_squared < inter[1] ** 2:
                is_in_interact = True
                
                room = None # TODO
                if keys[pygame.K_e]:
                    minig.switch_to_minigame(random.choice(list(minig.minigame_lib.keys())), team, room, screen)

        screen.fill(BLACK)

        # map rendering
        screen.blit(bg_surface, cam.translate(bg_rect))
        for p in map_props:
            screen.blit(p[0], cam.translate((*p[1], 0, 0)))

        # player rendering
        pred_time = (time.time() - player_info_age) * .9

        if not player_info == None:
            for name, p in player_info.items():
                if name == session_info[1]: # do not render the local player
                    continue
                
                # TODO: prediction can be improved

                # pred_p = common.player_move_update({}, pred_time, (p[0], p[1]), colliders)
                pred_p = cam.translate((p[0][0] + p[1][0] * pred_time - common.pm_player_size, p[0][1] + p[1][1] * pred_time - common.pm_player_size, common.pm_player_size * 2, common.pm_player_size * 2)) # simple velocity add

                pygame.draw.rect(screen, TEAMS[lobby_info[name][0]], pred_p)
                common.game_font.render_to(screen, (pred_p[0] - common.game_font.get_rect(name).centerx + common.pm_player_size, pred_p[1] - 30, 0, 0), name, WHITE)
        
        pygame.draw.rect(screen, TEAMS[team], cam.translate((player_state[0][0] - common.pm_player_size, player_state[0][1] - common.pm_player_size, common.pm_player_size * 2, common.pm_player_size * 2)))

        if is_in_interact:
            screen.blit(inter_surface, cam.translate((inter_rect[0] + player_state[0][0], inter_rect[1] + player_state[0][1] - 45, *inter_rect[2:4])))

        pygame.display.update()
        clock.tick(60)
    
    return 1 # return to lobby

# == edit mode ==

def reload_prop(p) -> pygame.Surface:
    return pygame.transform.scale_by(pygame.image.load(p[0]), p[1]).convert_alpha()

# dev-only in editor playtest with a simple player
def playtest(screen: pygame.Surface, bg: pygame.Surface, colls: list, props: list, inters: list):
    cam = Camera2D()
    player_state = ([0, 0], [0, 0])

    prop_surfs = []
    for prop in props:
        prop_surfs.append(reload_prop(prop))

    inter_surface = pygame.image.load("../assets/interact_notification.png")
    inter_rect = inter_surface.get_rect()
    inter_rect = (inter_rect[0] - inter_rect.centerx, inter_rect[1] - inter_rect.centery, inter_rect[2], inter_rect[3])

    t = time.time()

    while True:
        for event in pygame.event.get():
            if (event.type == QUIT or
                (event.type == KEYDOWN and event.key == K_ESCAPE)):
                return
        
        delta_time = time.time() - t
        t = time.time()

        player_state = common.player_move_update(pygame.key.get_pressed(), delta_time, player_state, colls)
        cam.set_pos(*player_state[0])

        screen.fill(BLACK)

        bg_rect = bg.get_rect()
        bg_rect = (bg_rect[0] - bg_rect.centerx, bg_rect[1] - bg_rect.centery, bg_rect[2], bg_rect[3])

        screen.blit(bg, cam.translate(bg_rect))

        for i, prop in enumerate(props):
            prop_rect = cam.translate((*prop[2], *prop_surfs[i].get_size()))
            screen.blit(prop_surfs[i], prop_rect)

        for inter in inters:
            dist_squared = (player_state[0][0] - inter[2][0]) ** 2 + (player_state[0][1] - inter[2][1]) ** 2
            if dist_squared < inter[1] ** 2:
                screen.blit(inter_surface, cam.translate((inter_rect[0] + player_state[0][0], inter_rect[1] + player_state[0][1] - 45, *inter_rect[2:4])))

        pygame.draw.rect(screen, (255, 0, 0), cam.translate((player_state[0][0] - common.pm_player_size, player_state[0][1] - common.pm_player_size, common.pm_player_size * 2, common.pm_player_size * 2)))
        pygame.display.update()

# dev-only offline ui for creating map files (i love crunch time - alter)
def editor(screen: pygame.Surface):
    # import editor only modules only here
    import pygame.gfxdraw as gfx
    import os

    # init editor vars
    cam = Camera2D()
    ui_col = (200, 200, 200)

    edit_mode = 0

    selector = 0
    max_sel = [2, 0, 2, 1, 2]

    bg_assets = [os.path.join("../assets/backgs/", f) for f in os.listdir("../assets/backgs/") if os.path.isfile(os.path.join("../assets/backgs/", f))]
    prop_assets = [os.path.join("../assets/props/", f) for f in os.listdir("../assets/props/") if os.path.isfile(os.path.join("../assets/props/", f))]

    # load file if any

    try:
        with open("edit_map.json", "r") as f:
            map_data = json.load(f)
        
        map_background = bg_assets.index(map_data["map_background"][0])
        map_background_scale = map_data["map_background"][1]

        map_colliders = map_data["map_colliders"]
        map_props = map_data["map_props"]
        map_spawnpoints = map_data.get("map_spawnpoints", {})
        map_interactibles = map_data.get("map_interactibles", [])

        print("successfully loaded edit_map.json")

    except: # if load failed create new map
        map_background = 0
        map_background_scale = 1
        
        map_colliders = []
        map_props = []
        map_spawnpoints = {}
        map_interactibles = []

    # helper funcs

    def save_map():
        print("saving edit_map.json")

        with open("edit_map.json", "w") as f:
            json.dump({
                "map_background": [bg_assets[map_background], map_background_scale],
                "map_colliders": map_colliders,
                "map_props": map_props,
                "map_spawnpoints": map_spawnpoints,
                "map_interactibles": map_interactibles,
            }, f)

    def reload_backg() -> pygame.Surface:
        return pygame.transform.scale_by(pygame.image.load(bg_assets[map_background]), map_background_scale).convert()

    # load assets

    map_background_surf = reload_backg()

    map_prop_surfs = []
    for p in map_props:
        map_prop_surfs.append(reload_prop(p))

    is_prim_next = False
    is_prim_prev = False
    
    is_sec_next = False
    is_sec_prev = False

    left_hold = False
    right_hold = False

    selected_prop = 0
    selected_prop_scale = 1
    selected_prop_surf = reload_prop((prop_assets[selected_prop], 1))

    selected_team_index = 0

    selected_interactible_type = 0
    selected_interactible_dist = 50

    coll_start_drag = None
    is_coll_dragging = False

    t = time.time()

    while True:
        for event in pygame.event.get():
            if (event.type == QUIT or
                (event.type == KEYDOWN and event.key == K_ESCAPE)):
                save_map()
                exit(0)

        delta_time = time.time() - t
        t = time.time()

        # input update
        prim_next = False
        prim_prev = False

        sec_next = False
        sec_prev = False

        left_click = False
        right_click = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_t]:
            playtest(screen, map_background_surf, map_colliders, map_props, map_interactibles)

            t = time.time()
            continue

        cam_off = [0, 0]
        if keys[pygame.K_w]:
            cam_off[1] -= int(450 * delta_time)
        if keys[pygame.K_s]:
            cam_off[1] += int(450 * delta_time)
        if keys[pygame.K_a]:
            cam_off[0] -= int(450 * delta_time)
        if keys[pygame.K_d]:
            cam_off[0] += int(450 * delta_time)

        cam.offset(*cam_off)

        if keys[pygame.K_RIGHT] and not is_prim_next:
            is_prim_next = True
            prim_next = True
        elif not keys[pygame.K_RIGHT]:
            is_prim_next = False

        if keys[pygame.K_LEFT] and not is_prim_prev:
            is_prim_prev = True
            prim_prev = True
        elif not keys[pygame.K_LEFT]:
            is_prim_prev = False

        if keys[pygame.K_DOWN] and not is_sec_next:
            is_sec_next = True
            sec_next = True
        elif not keys[pygame.K_DOWN]:
            is_sec_next = False

        if keys[pygame.K_UP] and not is_sec_prev:
            is_sec_prev = True
            sec_prev = True
        elif not keys[pygame.K_UP]:
            is_sec_prev = False

        m = pygame.mouse.get_pressed()

        if m[0] and not left_hold:
            left_hold = True
            left_click = True
        elif not m[0]:
            left_hold = False

        if m[2] and not right_hold:
            right_hold = True
            right_click = True
        elif not m[2]:
            right_hold = False

        # map update

        screen.fill(BLACK)

        if not map_background_surf == None:
            bg_rect = map_background_surf.get_rect()
            bg_rect = (bg_rect[0] - bg_rect.centerx, bg_rect[1] - bg_rect.centery, bg_rect[2], bg_rect[3])

            screen.blit(map_background_surf, cam.translate(bg_rect))

        for i, prop in enumerate(map_props):
            prop_rect = cam.translate((*prop[2], *map_prop_surfs[i].get_size()))
            screen.blit(map_prop_surfs[i], prop_rect)

            for i in range(2):
                gfx.rectangle(screen, (prop_rect[0] + i, prop_rect[1] + i, prop_rect[2] - i * 2, prop_rect[3] - i * 2), (200, 127, 0, 200))

        if edit_mode == 2:
            selected_prop_surf.set_alpha(127)
            screen.blit(selected_prop_surf, pygame.mouse.get_pos())

        for coll in map_colliders:
            coll_rect = cam.translate(coll)
            gfx.box(screen, coll_rect, (0, 200, 0, 64))

            for i in range(2):
                gfx.rectangle(screen, (coll_rect[0] + i, coll_rect[1] + i, coll_rect[2] - i * 2, coll_rect[3] - i * 2), (0, 200, 0, 200))

            gfx.filled_circle(screen, coll_rect[0] + coll_rect[2] // 2, coll_rect[1] + coll_rect[3] // 2, 4, (0, 200, 0, 200))

        if edit_mode == 1 and is_coll_dragging:
            start_pos = cam.translate((*coll_start_drag, 0, 0))[0:2]
            m = pygame.mouse.get_pos()
            coll_rect = (*start_pos, m[0] - start_pos[0], m[1] - start_pos[1])

            gfx.box(screen, coll_rect, (0, 200, 0, 32))

            for i in range(2):
                gfx.rectangle(screen, (coll_rect[0] + i, coll_rect[1] + i, coll_rect[2] - i * 2, coll_rect[3] - i * 2), (0, 200, 0, 100))
        
        for team, point in map_spawnpoints.items():
            point = cam.translate((*point, 0, 0))

            common.game_font.render_to(screen, (point[0] - common.game_font.get_rect("spawn - " + team).centerx, point[1] - 20), "spawn - " + team, WHITE)
            gfx.filled_circle(screen, point[0], point[1], 6, TEAMS[team])
        
        for inter in map_interactibles:
            inter_pos = cam.translate((*inter[2], 0, 0))

            # common.game_font.render_to(screen, (inter_pos[0] - common.game_font.get_rect("interact").centerx, inter_pos[1] - 20), "interact", WHITE)
            gfx.filled_circle(screen, inter_pos[0], inter_pos[1], 6, (*BLUE, 127))
            
            for i in range(2):
                gfx.circle(screen, inter_pos[0], inter_pos[1], inter[1] - i, (*BLUE, 200))

        # editor ui update

        if sec_next:
            selector = min(max_sel[edit_mode], selector + 1)
        elif sec_prev:
            selector = max(0, selector - 1)

        if selector == 0:
            if prim_next:
                edit_mode = min(4, edit_mode + 1)
            elif prim_prev:
                edit_mode = max(0, edit_mode - 1)

        gfx.box(screen, (5, 5, 500, 180), (16, 16, 16, 200))
        common.game_font.render_to(screen, (15, 25 + 20 * selector), ">", ui_col)
        common.game_font.render_to(screen, (15, 135), "left,right arrows = interact with setting; up,down = select setting", (127, 127, 127))
        common.game_font.render_to(screen, (15, 155), "t = in-editor playtest (esc to exit playtest)", (127, 127, 127))

        if edit_mode == 0:
            if prim_next and selector == 1:
                map_background = min(len(bg_assets) - 1, map_background + 1)
                map_background_surf = reload_backg()
            elif prim_prev and selector == 1:
                map_background = max(0, map_background - 1)
                map_background_surf = reload_backg()

            if prim_next and selector == 2:
                map_background_scale = round(map_background_scale / .8, 6)
                map_background_surf = reload_backg()
            elif prim_prev and selector == 2:
                map_background_scale = round(max(0, map_background_scale * .8), 6)
                map_background_surf = reload_backg()

            common.game_font.render_to(screen, (35, 25), "Editor Mode: select background", ui_col)
            common.game_font.render_to(screen, (35, 45), f"Background Image: {bg_assets[map_background]}", ui_col)
            common.game_font.render_to(screen, (35, 65), f"Background Scale: {map_background_scale}", ui_col)

        elif edit_mode == 1:
            common.game_font.render_to(screen, (35, 25), "Editor Mode: edit colliders", ui_col)

            common.game_font.render_to(screen, (15, 90), "left click and drag = add new wall collider", (127, 127, 127))
            common.game_font.render_to(screen, (15, 110), "right click = remove a wall collider", (127, 127, 127))

            if left_click:
                coll_start_drag = cam.translate_inverse(pygame.mouse.get_pos())
                is_coll_dragging = True
            elif is_coll_dragging and not left_hold:
                coll = (*coll_start_drag, *cam.translate_inverse(pygame.mouse.get_pos()))

                # convert [x1 y1 x2 y2] to [left top width height] 
                coll = (min(coll[0], coll[2]), min(coll[1], coll[3]), max(coll[0], coll[2]) - min(coll[0], coll[2]), max(coll[1], coll[3]) - min(coll[1], coll[3]))
                
                if not min(coll[2], coll[3]) == 0:
                    map_colliders.append(coll)
                is_coll_dragging = False

            if right_click:
                scan_pos = cam.translate_inverse(pygame.mouse.get_pos())

                for i in range(len(map_colliders) - 1, -1, -1):
                    coll = pygame.Rect(map_colliders[i])

                    if coll.collidepoint(scan_pos):
                        map_colliders.pop(i)
                        break

        elif edit_mode == 2:
            if prim_next and selector == 1:
                selected_prop = min(len(prop_assets) - 1, selected_prop + 1)
                selected_prop_surf = reload_prop((prop_assets[selected_prop], selected_prop_scale))
            elif prim_prev and selector == 1:
                selected_prop = max(0, selected_prop - 1)
                selected_prop_surf = reload_prop((prop_assets[selected_prop], selected_prop_scale))
            
            if prim_next and selector == 2:
                selected_prop_scale = round(selected_prop_scale / .8, 6)
                selected_prop_surf = reload_prop((prop_assets[selected_prop], selected_prop_scale))
            elif prim_prev and selector == 2:
                selected_prop_scale = round(max(0, selected_prop_scale * .8), 6)
                selected_prop_surf = reload_prop((prop_assets[selected_prop], selected_prop_scale))

            common.game_font.render_to(screen, (35, 25), "Editor Mode: edit props", ui_col)
            common.game_font.render_to(screen, (35, 45), f"Prop Image: {prop_assets[selected_prop]}", ui_col)
            common.game_font.render_to(screen, (35, 65), f"Prop Scale: {selected_prop_scale}", ui_col)

            common.game_font.render_to(screen, (15, 90), "left click = add a new prop", (127, 127, 127))
            common.game_font.render_to(screen, (15, 110), "right click = remove a prop", (127, 127, 127))

            if left_click:
                prop_pos = cam.translate_inverse(pygame.mouse.get_pos())

                prop = (prop_assets[selected_prop], selected_prop_scale, prop_pos)
                map_props.append(prop)

                map_prop_surfs.append(reload_prop(prop))

            if right_click:
                scan_pos = cam.translate_inverse(pygame.mouse.get_pos())

                for i in range(len(map_props) - 1, -1, -1):
                    prop = map_props[i]
                    prop_pos = pygame.Rect(prop[2][0], prop[2][1], *map_prop_surfs[i].get_size())

                    if prop_pos.collidepoint(scan_pos):
                        map_props.pop(i)
                        map_prop_surfs.pop(i)
                        break
        
        elif edit_mode == 3:
            if prim_next and selector == 1:
                selected_team_index = min(len(TEAMS) - 1, selected_team_index + 1)
            elif prim_prev and selector == 1:
                selected_team_index = max(0, selected_team_index - 1)

            common.game_font.render_to(screen, (35, 25), "Editor Mode: edit spawnpoints", ui_col)
            common.game_font.render_to(screen, (35, 45), f"Selected Team: {list(TEAMS.keys())[selected_team_index]}", ui_col)

            common.game_font.render_to(screen, (15, 90), "left click = place a spawn point", (127, 127, 127))
            common.game_font.render_to(screen, (15, 110), "right click = remove a spawn point", (127, 127, 127))

            if left_click:
                spawn_pos = cam.translate_inverse(pygame.mouse.get_pos())

                map_spawnpoints[list(TEAMS.keys())[selected_team_index]] = spawn_pos

            if right_click:
                scan_pos = cam.translate_inverse(pygame.mouse.get_pos())

                keys = list(map_spawnpoints.keys())
                for i in range(len(keys) - 1, -1, -1):
                    spawn = map_spawnpoints[keys[i]]
                    spawn_pos = pygame.Rect(spawn[0] - 6, spawn[1] - 6, 12, 12)

                    if spawn_pos.collidepoint(scan_pos):
                        map_spawnpoints.pop(keys[i])
                        break

        elif edit_mode == 4:
            # if lest here if more types are added
            # if prim_next and selector == 1:
            #     selected_interactible_type = min(len(TEAMS) - 1, selected_interactible_type + 1)
            # elif prim_prev and selector == 1:
            #     selected_interactible_type = max(0, selected_interactible_type - 1)

            if prim_next and selector == 2:
                selected_interactible_dist = max(selected_interactible_dist + 1, int(selected_interactible_dist // .9))
            elif prim_prev and selector == 2:
                selected_interactible_dist = max(1, int(selected_interactible_dist * .9))

            common.game_font.render_to(screen, (35, 25), "Editor Mode: edit interactibles", ui_col)
            common.game_font.render_to(screen, (35, 45), "Interactible Type: minigame", ui_col)
            common.game_font.render_to(screen, (35, 65), f"Interactible Size: {selected_interactible_dist}", ui_col)

            common.game_font.render_to(screen, (15, 90), "left click = place an interactible", (127, 127, 127))
            common.game_font.render_to(screen, (15, 110), "right click = remove an interactible", (127, 127, 127))

            if left_click:
                spawn_pos = cam.translate_inverse(pygame.mouse.get_pos())

                map_interactibles.append((selected_interactible_type, selected_interactible_dist, spawn_pos))

            if right_click:
                scan_pos = cam.translate_inverse(pygame.mouse.get_pos())

                for i in range(len(map_interactibles) - 1, -1, -1):
                    inter = map_interactibles[i]
                    inter_pos = pygame.Rect(inter[2][0] - inter[1], inter[2][1] - inter[1], inter[1] * 2, inter[1] * 2)

                    if inter_pos.collidepoint(scan_pos):
                        map_interactibles.pop(i)
                        break

        pygame.display.update()


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
    # editor(screen)

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

    exit(0) # use atexit for cleaning up