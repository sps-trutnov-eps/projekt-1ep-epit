import pygame
import random
import math
import os

pygame.init()

black = (0, 0, 0)
white = (255, 255, 255)

# Získání rozměrů obrazovky
screen_info = pygame.display.Info()
screen_width = screen_info.current_w
screen_height = screen_info.current_h

# Vytvoření plného obrazovkového režimu
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
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

player_img = load_image(os.path.join(current_dir, '../player.png'), scale=(128, 128))
enemy_img = load_image(os.path.join(current_dir, '../enemy.png'), scale=(96, 96))
bullet_img = load_image(os.path.join(current_dir, '../bullet.png'), scale=(32, 32))
background_img = load_image(os.path.join(current_dir, '../background.png'), scale=(screen_width, screen_height))
loading_screen_img = load_image(os.path.join(current_dir, '../loading_screen.png'), scale=(screen_width, screen_height))

player_x = screen_width // 2 - 64  # Středování hráče
player_y = screen_height - 128  # Posun hráče směrem nahoru
player_x_change = 0
player_speed = 20  # Zvýšení rychlosti hráče

enemy_img_list = []
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = []
enemy_speed = 6  # Zvýšení rychlosti nepřátel
num_of_enemies = 6

def reset_game():
    global player_x, player_y, player_x_change, score_value, shot_count, bullet_x, bullet_y, bullet_state, enemy_x, enemy_y, enemy_x_change, enemy_y_change
    player_x = screen_width // 2 - 64
    player_y = screen_height - 128
    player_x_change = 0
    score_value = 0
    shot_count = 0
    bullet_x = 0
    bullet_y = screen_height - 128
    bullet_state = "ready"
    for i in range(num_of_enemies):
        enemy_x[i] = random.randint(0, screen_width - 96)
        enemy_y[i] = random.randint(50, 150)
        enemy_x_change[i] = enemy_speed  # Změna rychlosti nepřátel
        enemy_y_change[i] = 50

for i in range(num_of_enemies):
    enemy_img_list.append(enemy_img)
    enemy_x.append(random.randint(0, screen_width - 96))
    enemy_y.append(random.randint(50, 150))
    enemy_x_change.append(enemy_speed)  # Změna rychlosti nepřátel
    enemy_y_change.append(50)

bullet_x = 0
bullet_y = screen_height - 128
bullet_y_change = 40
bullet_state = "ready"

score_value = 0
shot_count = 0
font = pygame.font.Font('freesansbold.ttf', 32)

text_x = 10
text_y = 10

over_font = pygame.font.Font('freesansbold.ttf', 64)
start_font = pygame.font.Font('freesansbold.ttf', 48)
title_font = pygame.font.Font('freesansbold.ttf', 72)

paused = False

def show_score(x, y):
    score = font.render("Skóre: " + str(score_value), True, white)
    screen.blit(score, (x, y))

def show_shots(x, y):
    shots = font.render("Výstřely: " + str(shot_count), True, white)
    screen.blit(shots, (x, y + 40))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, white)
    over_rect = over_text.get_rect(center=(screen_width // 2, screen_height // 2 - 50))
    screen.blit(over_text, over_rect)

def game_completed_text():
    complete_text = over_font.render("SPLNĚNO", True, white)
    complete_rect = complete_text.get_rect(center=(screen_width // 2, screen_height // 2 - 50))
    screen.blit(complete_text, complete_rect)

def play_again_text():
    play_again_text = start_font.render("PLAY AGAIN", True, white)
    play_again_rect = play_again_text.get_rect(center=(screen_width // 2, screen_height // 2 + 50))
    screen.blit(play_again_text, play_again_rect)
    return play_again_rect

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

def draw_button(text, font, color, rect):
    text_surf = font.render(text, True, color)
    text_rect = text_surf.get_rect(center=rect.center)
    screen.blit(text_surf, text_rect)

def show_start_screen():
    screen.fill(black)
    screen.blit(loading_screen_img, (0, 0))
    title_text = title_font.render("Space Invaders", True, white)
    screen.blit(title_text, (200, 150))
    
    start_rect = pygame.Rect((screen_width // 2 - 100, screen_height // 2 + 200), (200, 100))  # Posunutí tlačítka START dolů
    draw_button("START", start_font, white, start_rect)
    
    pygame.display.update()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if start_rect.collidepoint(mouse_pos):
                    waiting = False

clock = pygame.time.Clock()
running = True

# Zobrazíme úvodní obrazovku
show_start_screen()

# Hlavní herní smyčka
while running:
    screen.fill(black)
    screen.blit(background_img, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if not paused:
                    paused = True
                else:
                    paused = False
            if event.key == pygame.K_LEFT:
                player_x_change = -player_speed
            if event.key == pygame.K_RIGHT:
                player_x_change = player_speed
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_x = player_x
                    fire_bullet(bullet_x, bullet_y)
                    shot_count += 1  # Zvýšení počtu výstřelů zde
            if event.key == pygame.K_q and paused:
                pygame.quit()
                exit()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_change = 0
        if event.type == pygame.MOUSEBUTTONDOWN and not running:
            mouse_pos = pygame.mouse.get_pos()
            if play_again_rect and play_again_rect.collidepoint(mouse_pos):
                reset_game()
                running = True

    if not paused:
        player_x += player_x_change
        if player_x <= 0:
            player_x = 0
        elif player_x >= screen_width - 128:
            player_x = screen_width - 128

        for i in range(num_of_enemies):
            if enemy_y[i] > screen_height - 128:
                for j in range(num_of_enemies):
                    enemy_y[j] = 2000
                game_over_text()
                play_again_rect = play_again_text()
                running = False
                break

            enemy_x[i] += enemy_x_change[i]
            if enemy_x[i] <= 0:
                enemy_x_change[i] = enemy_speed  # Změna rychlosti nepřátel
                enemy_y[i] += enemy_y_change[i]
            elif enemy_x[i] >= screen_width - 96:
                enemy_x_change[i] = -enemy_speed  # Změna rychlosti nepřátel
                enemy_y[i] += enemy_y_change[i]
                enemy_x_change[i]   = -enemy_speed  # Změna rychlosti nepřátel
                enemy_y[i] += enemy_y_change[i]             
            

            collision = is_collision(enemy_x[i], enemy_y[i], bullet_x, bullet_y)
            if collision:
                bullet_y = screen_height - 128
                bullet_state = "ready"
                score_value += 1
                enemy_x[i] = random.randint(0, screen_width - 96)
                enemy_y[i] = random.randint(50, 150)

            enemy(enemy_x[i], enemy_y[i], i)

        if bullet_y <= 0:
            bullet_y = screen_height - 128
            bullet_state = "ready"
        if bullet_state == "fire":
            fire_bullet(bullet_x, bullet_y)
            bullet_y -= bullet_y_change

        player(player_x, player_y)
        show_score(text_x, text_y)
        show_shots(text_x, text_y)

        if score_value >= 10:
            game_completed_text()
            pygame.display.update()
            pygame.time.wait(3000)  # Počkej 3 sekundy
            running = False

        if shot_count >= 30 and score_value < 10:
            game_over_text()
            play_again_rect = play_again_text()
            pygame.display.update()
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        waiting = False
                        running = False
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                        if play_again_rect.collidepoint(mouse_pos):
                            reset_game()
                            waiting = False

    else:
        # Pokud je hra pozastavena, zobrazíme "PAUSED" text
        paused_text = over_font.render("PAUSED", True, white)
        paused_rect = paused_text.get_rect(center=(screen_width // 2, screen_height // 2))
        screen.blit(paused_text, paused_rect)

        # Přidáme možnost ukončení hry v pause menu
        quit_text = start_font.render("QUIT GAME", True, white)
        quit_rect = quit_text.get_rect(center=(screen_width // 2, screen_height // 2 + 100))
        screen.blit(quit_text, quit_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    exit()
            if event.type == pygame.MOUSEBUTTONDOWN and paused:
                mouse_pos = pygame.mouse.get_pos()
                if quit_rect.collidepoint(mouse_pos):
                    pygame.quit()
                    exit()

    pygame.display.update()
    clock.tick(60)

pygame.quit()

