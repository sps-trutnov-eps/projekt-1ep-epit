import pygame as pg
import random as random
from pygame import K_ESCAPE, KEYDOWN, QUIT

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
x = 0
y = 0

player_number = 4
# sem bychom jsme si mohli brat cislo hrace podle toho kolikaty se napoji do lobicka

obrazek = pg.image.load("pixil-frame-0 (3).png")
obrazekP = pg.image.load("red-hustler.png")

class Player():
    def __init__(self, player_x, player_y, player_team, player_number, player_skin_type):
        self.x = player_x
        self.y = player_y
        self.player_number = player_number
        self.player_team = player_team
        self.player_number = player_number
        self.player_skin_type = player_skin_type
        self.player_image = pg.image.load(self.player_skin_type)
        self.width = self.player_image.get_width()  # Získáme šířku obrázku
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
            self.player_skin_type = player_team_images[self.player_number - 1]  # Player number as index, but starting from 1
            return self.player_skin_type
        else:
            raise ValueError("Invalid player number")
        
    def keep_in_center(self, screen_width, screen_height):
        # Vypočteme novou pozici hráče tak, aby byl uprostřed obrazovky
        self.x = (screen_width - self.width) // 2
        self.y = (screen_height - self.height) // 2     
        
    def display_player(self, screen):
        self.player_image = pg.image.load(self.player_skin_type)
        screen.blit(self.player_image, (self.x, self.y))

def handle_events() -> bool:
    """Events handling function."""
    global x, y
    keys = pg.key.get_pressed()
    if keys[pg.K_w]:
        y += 20
    if keys[pg.K_s]:
        y -= 20
    if keys[pg.K_a]:
        x += 20
    if keys[pg.K_d]:
        x -= 20

    for event in pg.event.get():
        if (event.type == QUIT or
            (event.type == KEYDOWN and event.key == K_ESCAPE)):
            return False
    return True

def druhy_patro(screen: pg.Surface) -> None:
    """Level function."""
    clock = pg.time.Clock()
    sprites = pg.sprite.Group()
    player = Player(10, 10, 'ep', player_number, 'red-blondyna.png')

    while handle_events():
        sprites.update()
        sprites.draw(screen)
        screen.blit(obrazek, (x, y))
        player.choose_image()
        player.keep_in_center(SCREEN_WIDTH, SCREEN_HEIGHT)
        player.display_player(screen)    
        pg.display.update()
        clock.tick(100)

def init_game() -> pg.Surface:
    """Pygame init function."""
    pg.init()
    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pg.display.set_caption('Game')
    return screen

def main(scene_id: int = 0) -> None:
    """Main function."""
    screen = init_game()
    druhy_patro(screen)

if __name__ == '__main__':
    main()
    pg.quit()

