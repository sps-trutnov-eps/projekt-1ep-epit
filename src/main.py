import pygame as pg
from pygame.locals import K_ESCAPE, KEYDOWN, QUIT, K_w, K_s, K_a, K_d

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

player_number = 4

obrazek_patra = pg.image.load("1-patro.png")

class Player():
    def __init__(self, player_x, player_y, player_team, player_number):
        self.x = player_x
        self.y = player_y
        self.player_number = player_number
        self.player_team = player_team
        self.player_skin_type = self.choose_image()
        self.player_image = pg.image.load(self.player_skin_type)
        self.width = self.player_image.get_width()
        self.height = self.player_image.get_height()

    def choose_image(self):
        player_images_skin_type_red = ['red-blondyna.png', 'red-emogirl.png', 'red-hustler.png', 'red-nerd.png', 'red-smazka.png']
        player_images_skin_type_blue = ['blue-blondyna.png', 'blue-emogirl.png', 'blue-hustler.png', 'blue-nerd.png', 'blue-smazka.png']
        
        if self.player_team == 'it':
            player_team_images = player_images_skin_type_red
        elif self.player_team == 'ep':
            player_team_images = player_images_skin_type_blue
        else:
            raise ValueError("Invalid player team")
        
        if 1 <= self.player_number <= len(player_team_images):
            return player_team_images[self.player_number - 1]
        else:
            raise ValueError("Invalid player number")

    def display_player(self, screen, bg_offset_x, bg_offset_y):
        screen.blit(self.player_image, (self.x + bg_offset_x, self.y + bg_offset_y))

def handle_events(player, background) -> bool:
    keys = pg.key.get_pressed()
    dx, dy = 0, 0

    if keys[K_w]:
        dy = -20
    if keys[K_s]:
        dy = 20
    if keys[K_a]:
        dx = -20
    if keys[K_d]:
        dx = 20

    new_x = player.x + dx
    new_y = player.y + dy

    if not is_collision(new_x, new_y, player.width, player.height, background):
        player.x = new_x
        player.y = new_y

    for event in pg.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            return False
    return True

def is_collision(x, y, width, height, background):
    screen_width, screen_height = background.get_size()
    for i in range(width):
        for j in range(height):
            check_x = x + i
            check_y = y + j
            if 0 <= check_x < screen_width and 0 <= check_y < screen_height:
                if background.get_at((check_x, check_y)) == BLACK:
                    return True
    return False

def druhy_patro(screen: pg.Surface) -> None:
    clock = pg.time.Clock()
    player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 'ep', player_number)

    while handle_events(player, obrazek_patra):
        bg_offset_x = SCREEN_WIDTH // 2 - player.x
        bg_offset_y = SCREEN_HEIGHT // 2 - player.y

        screen.fill(WHITE)
        screen.blit(obrazek_patra, (bg_offset_x, bg_offset_y))
        player.display_player(screen, bg_offset_x, bg_offset_y)
        pg.display.update()
        clock.tick(60)

def init_game() -> pg.Surface:
    pg.init()
    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pg.display.set_caption('Game')
    return screen

def main(scene_id: int = 0) -> None:
    screen = init_game()
    druhy_patro(screen)
    pg.quit()

if __name__ == '__main__':
    main()

