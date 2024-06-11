import pygame.freetype as freetype
import pygame

# == sdílené promněné a časti kódu použitelné v celém projektu ==

# dm @sk2 pokud kdokoli potřebuje pomoc s použitím
# kdokoli také může přidat další užitečné kousky kódů

# == ui ==

freetype.init()

# sdílený font pro celý project, prostě jen `game_font.render_to(sur, (x, y), "text", color)` tam kdeho chcete použít
# note: Kdyby někdo našel lepší font, než je ten defaultní, klidně ho mužeme změnit
game_font = freetype.SysFont(freetype.get_default_font(), 16)

# určí jestli `event` pygame event (typu pygame.MOUSEBUTTONDOWN) byl nad `ui` (pygame.Rect)
def is_click_on_ui(ui_rect: pygame.Rect, event: pygame.event.Event) -> bool:
    pos = event.dict["pos"]

    rel_pos = (pos[0] - ui_rect[0], pos[1] - ui_rect[1])

    return (rel_pos[0] >= 0 and rel_pos[0] <= ui_rect[2]) and (rel_pos[1] >= 0 and rel_pos[1] <= ui_rect[3])

# z rect vám vrátí střed daného rectu, užitečné pro text rendering
def center_in_rect(ui_rect: pygame.Rect, text_rect: pygame.Rect = (0, 0, 0, 0)) -> tuple:
    return (ui_rect[0] + ui_rect[2] // 2 - text_rect[2] // 2, ui_rect[1] + ui_rect[3] // 2 - text_rect[3] // 2)

pm_accel = 35
pm_friction = .985
pm_max_speed = 600

pm_player_size = 10

# player movement update, can be reused between levels, returns new vel which should be passed as an argument vel on the next update
# keys = pygame.key.get_pressed()
# delta_time = time (in seconds) since last update
# state = tuple of two lists, state[0] = current position of player, state[1] = current velocity of player (returns new state)
# coll_rects = list of Rects to serve as walls
#
# note: if your player is getting stuck on some colliders, it might be possible that there are multiple rects overlayed over each other which can cause the "bug"
#       just remove the duplicates, if you can't find duplicates, uncomment the line `print(colls)` to get the indexes (into the coll_rects argument) of the duplicate colliders

def player_move_update(keys: dict, delta_time: float, state: tuple[list[float], list[float]], coll_rects: list[pygame.Rect]) -> tuple[list[float], list[float]]:
    # update vel

    pos = state[0]
    vel = state[1]
    
    if keys[pygame.K_s]:
        vel[1] += delta_time * pm_accel * (pm_max_speed - abs(vel[1]))
    if keys[pygame.K_w]:
        vel[1] -= delta_time * pm_accel * (pm_max_speed - abs(vel[1]))
    if keys[pygame.K_d]:
        vel[0] += delta_time * pm_accel * (pm_max_speed - abs(vel[0]))
    if keys[pygame.K_a]:
        vel[0] -= delta_time * pm_accel * (pm_max_speed - abs(vel[0]))

    vel = [vel[0] * pm_friction, vel[1] * pm_friction]

    # test collisions

    test_pos = [pos[0] + vel[0] * delta_time, pos[1] + vel[1] * delta_time] # makes a non-reference copy and adds vel (normalized by delta_time)
    test_rect = pygame.Rect((test_pos[0] - pm_player_size, test_pos[1] - pm_player_size, pm_player_size * 2, pm_player_size * 2))

    colls = test_rect.collidelistall(coll_rects)

    # correct collisions
    
    # uncomment to show all touching colliders in this update
    # print(colls)

    for coll in colls:
        # test for x

        test_rect = pygame.Rect((pos[0] - pm_player_size, test_pos[1] - pm_player_size, pm_player_size * 2, pm_player_size * 2))
        if not test_rect.colliderect(coll_rects[coll]):
            test_pos[0] = pos[0]
            vel[0] = 0
            continue
                
        # test for y
        test_rect = pygame.Rect((test_pos[0] - pm_player_size, pos[1] - pm_player_size, pm_player_size * 2, pm_player_size * 2))
        if not test_rect.colliderect(coll_rects[coll]):
            test_pos[1] = pos[1]
            vel[1] = 0
            continue

    # perform move

    return (test_pos, vel)