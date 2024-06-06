import pygame
import sys
import math
import time

pygame.init()

# Set up the window
window_width = 1200
window_height = 800
window = pygame.display.set_mode((window_width, window_height))

# Load the car image
car_image_path = "./obrazky racegame/formula.png"
car_image = pygame.image.load(car_image_path)
car_rect = car_image.get_rect()

# Car starting position
car_pos_x = 500
car_pos_y = 500

tree_path = "./obrazky racegame/backgroundTree.png"
tree_image = pygame.image.load(tree_path)
scaled_tree = pygame.transform.scale(tree_image, (70, 30))
tree_rect = scaled_tree.get_rect()
# Car starting angle
car_angle = 0

clock = pygame.time.Clock()

# Load and scale the formula image
formula_path = "./obrazky racegame/formula.png"
formula = pygame.image.load(formula_path)
scaled_formula = pygame.transform.scale(formula, (70, 30))  # Adjust size as needed
formula_rect = scaled_formula.get_rect()

# Define obstacles
obstacles = [
    pygame.Rect(200, 500, 500, 100),
    pygame.Rect(600, 500, 100, 200),
    pygame.Rect(600, 600, 400, 100),
    pygame.Rect(900, 200, 100, 400),
    pygame.Rect(900, 200, 200, 100),
    pygame.Rect(1000, 0, 100, 300),
    pygame.Rect(800, 0, 300, 100),
    pygame.Rect(800, 0, 100, 200),
    pygame.Rect(200, 100, 700, 100),
]

# Define speed of the formula
formula_speed = 0.3  # Adjust as needed

# Define button properties
button_font = pygame.font.Font(None, 74)
button_text = button_font.render('Start Game', True, (255, 255, 255))
button_rect = button_text.get_rect(center=(window_width / 2, window_height / 2))

# Define the lap completion point (e.g., crossing the start line at y=100)
lap_completion_rect = pygame.Rect(200, 100, 20, 100)  # Adjust as needed

def main_menu():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    return  # Exit the main menu to start the game

        window.fill((0, 0, 0))  # Fill the screen with black
        window.blit(button_text, button_rect)  # Draw the start game button
        pygame.display.flip()
        clock.tick(60)

def game_loop():
    global car_pos_x, car_pos_y, car_angle, tree_image, tree_rect

    start_time = time.time()
    lap_completed = False

    while True:
        elapsed_time = time.time() - start_time
        if elapsed_time > 20:  # Check if more than 60 seconds have passed
            pygame.quit()
            sys.exit()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        window.fill((79, 121, 66))

        # Draw obstacles
        for obstacle in obstacles:
            pygame.draw.rect(window, (128, 128, 128), obstacle)

        # Draw lap completion line
        pygame.draw.rect(window, (0, 0, 0), lap_completion_rect)

        # Rotate the car
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            car_angle += 1
        if keys[pygame.K_d]:
            car_angle -= 1

        # Move the car forward
        if keys[pygame.K_w]:
            new_pos_x = car_pos_x + math.cos(math.radians(car_angle)) * 2
            new_pos_y = car_pos_y - math.sin(math.radians(car_angle)) * 2

            # Check if the new position is within the area defined by obstacles
            within_bounds = False
            for obstacle in obstacles:
                if obstacle.collidepoint(new_pos_x, new_pos_y):
                    within_bounds = True
                    break

            if within_bounds:
                car_pos_x = new_pos_x
                car_pos_y = new_pos_y
        
        window.blit(scaled_tree, (100, 100))
        
        # Check if the car crosses the lap completion line
        if lap_completion_rect.collidepoint(car_pos_x, car_pos_y):
            lap_completed = True

        if lap_completed:
            break  # Exit the game loop if lap is completed

        # Wrap around screen
        if car_pos_x > window_width:
            car_pos_x = 0
        elif car_pos_x < 0:
            car_pos_x = window_width
        if car_pos_y > window_height:
            car_pos_y = 0
        elif car_pos_y < 0:
            car_pos_y = window_height

        # Draw the scaled formula
        rotated_formula = pygame.transform.rotate(scaled_formula, car_angle)  # Rotate the formula
        formula_rect = rotated_formula.get_rect(center=car_rect.center)  # Set rotation point to center
        formula_rect.topleft = (car_pos_x - formula_rect.width / 2, car_pos_y - formula_rect.height / 2)
        window.blit(rotated_formula, formula_rect.topleft)

        pygame.display.flip()
        clock.tick(300)  # Keep FPS at 60
        
       
        
        # Slow down the formula movement
        pygame.time.delay(int(1000 / 60 * formula_speed))  # 60 FPS equivalent delay with speed adjustment

# Main loop
while True:
    main_menu()
    game_loop()

