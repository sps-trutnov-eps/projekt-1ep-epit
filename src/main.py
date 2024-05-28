import pygame as pg
from pygame.locals import K_ESCAPE, KEYDOWN, QUIT
import os

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
player_size = 50

# Player position
player_x = SCREEN_WIDTH // 2
player_y = SCREEN_HEIGHT // 2

# Wall positions and sizes
walls = [
    pg.Rect(0, 0, 73, 3000),
    pg.Rect(0, 0, 4200, 90),
    pg.Rect(4070, 0, 95, 3000),
    pg.Rect(1374, 0, 95, 1114),
    pg.Rect(0, 1020, 910, 95),
    pg.Rect(1187, 1020, 1025, 95),
    pg.Rect(2674, 0, 95, 1114),
    pg.Rect(2490, 1020, 469, 95),
    pg.Rect(0, 2880, 1470, 95),
    pg.Rect(628, 1074, 95, 250),
    pg.Rect(628, 1574, 95, 1310),
    pg.Rect(1374, 1760, 95, 1610),
    pg.Rect(1000, 1760, 95, 1310),
    pg.Rect(1374, 1760, 280, 98),
    pg.Rect(1930, 1760, 1040, 98),
    pg.Rect(3232, 1760, 280, 98),
    pg.Rect(3232, 1020, 850, 95),
    pg.Rect(3420, 1100, 95, 200),
    pg.Rect(3420, 1575, 95, 1310),
    pg.Rect(2750, 2880, 1500, 95),
    pg.Rect(2675, 1830, 95, 1500),
    pg.Rect(1450, 3250, 1400, 95),
]

# File paths for images
file_path = os.path.join(os.path.dirname(__file__), "pixil-frame-0 (3).png")
file_path2 = os.path.join(os.path.dirname(__file__), "pixil-frame-0 (5).png")

# Load images
try:
    obrazek = pg.image.load(file_path)
    obrazekP = pg.image.load(file_path2)
except Exception as e:
    print(f"Error loading images: {e}")
    pg.quit()
    exit(1)

def handle_events() -> bool:
    keys = pg.key.get_pressed()
    move_x, move_y = 0, 0

    if keys[pg.K_w]:
        move_y = 20
    if keys[pg.K_s]:
        move_y = -20
    if keys[pg.K_a]:
        move_x = 20
    if keys[pg.K_d]:
        move_x = -20

    # Move walls
    for wall in walls:
        wall.move_ip(move_x, move_y)

    # Player's rectangle
    player_rect = pg.Rect(player_x, player_y, player_size, player_size)

    # Check for collisions
    for wall in walls:
        if player_rect.colliderect(wall):
            # Undo movement if collision
            for wall in walls:
                wall.move_ip(-move_x, -move_y)
            break

    for event in pg.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            return False

    return True

def draw_walls(screen: pg.Surface):
    for wall in walls:
        pg.draw.rect(screen, WHITE, wall)

def level(screen: pg.Surface) -> None:
    clock = pg.time.Clock()
    sprites = pg.sprite.Group()

    while handle_events():
        sprites.update()
        screen.fill(BLACK)
        sprites.draw(screen)
        # Draw player image
        screen.blit(obrazekP, (player_x, player_y))
        # Draw environment image
        for wall in walls:
            screen.blit(obrazek, (wall.x, wall.y))
        draw_walls(screen)
        pg.display.update()
        clock.tick(100)

def init_game() -> pg.Surface:
    pg.init()
    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pg.display.set_caption('Game')
    return screen

def main() -> None:
    screen = init_game()
    level(screen)

if __name__ == '__main__':
    main()
    pg.quit()
