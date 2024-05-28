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