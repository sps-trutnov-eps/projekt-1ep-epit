import pygame as pg
from pygame import K_ESCAPE, KEYDOWN, QUIT
import os

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

walls = [
    [0, 0, 73, 3000],
    [0, 0, 4200, 90],
    [4070, 0, 95, 3000],
    [1374, 0, 95, 1114],
    [0, 1020, 910, 95],
    [1187, 1020, 1025, 95],
    [2674, 0, 95, 1114],
    [2490, 1020, 469, 95],   
    [0, 2880, 1470, 95],
    [628, 1074, 95, 250],
    [628, 1574, 95, 1310],
    [1374, 1760, 95, 1610],
    [1000, 1760, 95, 1310],
    [1374, 1760, 280, 98],
    [1930, 1760, 1040, 98],
    [3232, 1760, 280, 98],
    [3232, 1020, 850, 95],
    [3420, 1100, 95, 200],
    [3420, 1575, 95, 1310],
    [2750, 2880, 1500, 95],
    [2675, 1830, 95, 1500],
    [1450, 3250, 1400, 95]
]

x = 0
y = 0
xp = 500
yp = 500

file_path = os.path.join(os.path.dirname(__file__), "pixil-frame-0 (3).png")
file_path2 = os.path.join(os.path.dirname(__file__), "pixil-frame-0 (5).png")
try:
    obrazek = pg.image.load(file_path)
    obrazekP = pg.image.load(file_path2)
except Exception as e:
    print(f"Error loading images: {e}")
    pg.quit()
    exit(1)

print("Images loaded successfully.")

def handle_events() -> bool:
    """Events handling function."""
    global walls, y, x

    keys = pg.key.get_pressed()
    move_allowed = True

    if keys[pg.K_w]:
        for wall in walls:
            if check_collision((xp, yp, obrazekP.get_width(), obrazekP.get_height()), wall):
                move_allowed = False
                break
        if move_allowed:
            y += 20
            for wall in walls:
             wall[1] += 20

    if keys[pg.K_s]:
        for wall in walls:
            if check_collision((xp, yp, obrazekP.get_width(), obrazekP.get_height()), wall):
                move_allowed = False
                break
        if move_allowed:
            y -= 20
            for wall in walls:
             wall[1] -= 20

    if keys[pg.K_a]:
        for wall in walls:
            if check_collision((xp, yp, obrazekP.get_width(), obrazekP.get_height()), wall):
                move_allowed = False
                break
        if move_allowed:
            x += 20
            for wall in walls:
                wall[0] += 20

    if keys[pg.K_d]:
        for wall in walls:
            if check_collision((xp, yp, obrazekP.get_width(), obrazekP.get_height()), wall):
                move_allowed = False
                break
        if move_allowed:
            x -= 20
            for wall in walls:
                wall[0] -= 20

    for event in pg.event.get():
        if (event.type == QUIT or
            (event.type == KEYDOWN and event.key == K_ESCAPE)):
            return False
    return True

def check_collision(rect1, rect2):
    return pg.Rect(rect1).colliderect(rect2)

def level(screen: pg.Surface) -> None:
    global move_allowed
    clock = pg.time.Clock()
    sprites = pg.sprite.Group()

    while handle_events():
        sprites.update()
        move_allowed = True
        screen.fill(BLACK)
        sprites.draw(screen)
        screen.blit(obrazek, (x, y))
        screen.blit(obrazekP, (xp, yp))
        draw_walls(screen)
        pg.display.update()
        clock.tick(100)

def draw_walls(screen):
    """Draw walls on the screen."""
    for wall in walls:
        pg.draw.rect(screen, (255, 255, 255), wall)

def init_game() -> pg.Surface:
    global screen
    """Pygame init function."""
    pg.init()
    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pg.display.set_caption('Game')
    
    return screen

def main(scene_id: int = 0) -> None:
    """Main function."""
    screen = init_game()
    level(screen)

if __name__ == '__main__':
    main()
    pg.quit()
