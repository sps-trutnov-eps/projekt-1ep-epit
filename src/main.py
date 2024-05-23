import pygame as pg
import os
from pygame.locals import *

# Screen settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Initialize Pygame
pg.init()

# Load images and resize player image
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

# Define map size
MAP_WIDTH = 2000
MAP_HEIGHT = 1500

# Define player size
PLAYER_WIDTH, PLAYER_HEIGHT = obrazek.get_size()

# Define initial player position
player_x = (SCREEN_WIDTH - PLAYER_WIDTH) // 2
player_y = (SCREEN_HEIGHT - PLAYER_HEIGHT) // 2

# Define initial map offset
map_offset_x = 0
map_offset_y = 0

# Define scroll speed
SCROLL_SPEED = 5

# Define blocked areas (walls)
blocked_areas = [
    pg.Rect(100, 100, 200, 30),   # First wall
    pg.Rect(400, 300, 150, 25),   # Second wall
    # Add more walls as needed
]

def handle_events() -> bool:
    global player_x, player_y, map_offset_x, map_offset_y

    for event in pg.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            return False

    keys = pg.key.get_pressed()
    if keys[pg.K_w]:
        player_y -= SCROLL_SPEED
        if player_y < 0:
            player_y = 0
        map_offset_y += SCROLL_SPEED
    if keys[pg.K_s]:
        player_y += SCROLL_SPEED
        if player_y > SCREEN_HEIGHT - PLAYER_HEIGHT:
            player_y = SCREEN_HEIGHT - PLAYER_HEIGHT
        map_offset_y -= SCROLL_SPEED
    if keys[pg.K_a]:
        player_x -= SCROLL_SPEED
        if player_x < 0:
            player_x = 0
        map_offset_x += SCROLL_SPEED
    if keys[pg.K_d]:
        player_x += SCROLL_SPEED
        if player_x > SCREEN_WIDTH - PLAYER_WIDTH:
            player_x = SCREEN_WIDTH - PLAYER_WIDTH
        map_offset_x -= SCROLL_SPEED

    # Clamp map offset to stay within map bounds
    map_offset_x = max(min(map_offset_x, MAP_WIDTH - SCREEN_WIDTH), 0)
    map_offset_y = max(min(map_offset_y, MAP_HEIGHT - SCREEN_HEIGHT), 0)

    return True

def level(screen: pg.Surface) -> None:
    clock = pg.time.Clock()
    while handle_events():
        screen.fill(BLACK)
        # Draw map background (just a white rectangle for now)
        pg.draw.rect(screen, WHITE, (0, 0, MAP_WIDTH, MAP_HEIGHT))
        # Draw blocked areas (walls)
        for wall in blocked_areas:
            pg.draw.rect(screen, BLACK, wall.move(-map_offset_x, -map_offset_y))
        # Draw player and image P
        screen.blit(obrazek, (player_x, player_y))
        screen.blit(obrazekP, (SCREEN_WIDTH // 2 - PLAYER_WIDTH // 2, SCREEN_HEIGHT // 2 - PLAYER_HEIGHT // 2))
        pg.display.update()
        clock.tick(60)

def init_game() -> pg.Surface:
    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pg.display.set_caption('Game')
    return screen

def main() -> None:
    screen = init_game()
    level(screen)
    pg.quit()

if __name__ == '__main__':
    main()
