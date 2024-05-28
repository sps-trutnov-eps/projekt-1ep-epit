import pygame
import random
import math
import os

pygame.init()

black = (0, 0, 0)
white = (255, 255, 255)

screen_width = 1024
screen_height = 768

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Space Invaders")

def load_image(image_path, scale=(64, 64)):
    try:
        image = pygame.image.load(image_path)
        image = pygame.transform.scale(image, scale)
        return image
    except pygame.error as e:
        print(f"Obrázek {image_path} se nepodařilo načíst: {e}")
        exit()

current_dir = os.path.dirname(os.path.abspath(__file__))

player_img = load_image(os.path.join(current_dir, 'player.png'), scale=(128, 128))
enemy_img = load_image(os.path.join(current_dir, 'enemy.png'), scale=(96, 96))
bullet_img = load_image(os.path.join(current_dir, 'bullet.png'), scale=(32, 32))

player_x = 480
player_y = 680
player_x_change = 0
player_speed = 7

enemy_img_list = []
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemy_img_list.append(enemy_img)
    enemy_x.append(random.randint(0, screen_width - 96))
    enemy_y.append(random.randint(50, 150))
    enemy_x_change.append(4)
    enemy_y_change.append(50)

bullet_x = 0
bullet_y = 680
bullet_y_change = 20
bullet_state = "ready" 

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

text_x = 10
text_y = 10

over_font = pygame.font.Font('freesansbold.ttf', 64)

def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, white)
    screen.blit(score, (x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, white)
    screen.blit(over_text, (350, 250))

def player(x, y):
    screen.blit(player_img, (x, y))

def enemy(x, y, i):
    screen.blit(enemy_img_list[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img, (x + 16, y + 10))

def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt((math.pow(enemy_x - bullet_x, 2)) + (math.pow(enemy_y - bullet_y, 2)))
    return distance < 27

clock = pygame.time.Clock()
running = True
while running:

    screen.fill(black)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change = -player_speed
            if event.key == pygame.K_RIGHT:
                player_x_change = player_speed
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_x = player_x
                    fire_bullet(bullet_x, bullet_y)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_change = 0

    
    player_x += player_x_change
    if player_x <= 0:
        player_x = 0
    elif player_x >= screen_width - 128:
        player_x = screen_width - 128

    for i in range(num_of_enemies):

        
        if enemy_y[i] > 640:
            for j in range(num_of_enemies):
                enemy_y[j] = 2000
            game_over_text()
            break

        enemy_x[i] += enemy_x_change[i]
        if enemy_x[i] <= 0:
            enemy_x_change[i] = 4
            enemy_y[i] += enemy_y_change[i]
        elif enemy_x[i] >= screen_width - 96:
            enemy_x_change[i] = -4
            enemy_y[i] += enemy_y_change[i]

      
        collision = is_collision(enemy_x[i], enemy_y[i], bullet_x, bullet_y)
        if collision:
            bullet_y = 680
            bullet_state = "ready"
            score_value += 1
            enemy_x[i] = random.randint(0, screen_width - 96)
            enemy_y[i] = random.randint(50, 150)

        enemy(enemy_x[i], enemy_y[i], i)

    if bullet_y <= 0:
        bullet_y = 680
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bullet_x, bullet_y)
        bullet_y -= bullet_y_change

    player(player_x, player_y)
    show_score(text_x, text_y)
    pygame.display.update()

    clock.tick(60)

pygame.quit()
