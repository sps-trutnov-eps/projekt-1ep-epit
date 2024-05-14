import pygame
import sys
import math

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
    pygame.Rect(200, 200, 100, 400)
]

# Define speed of the formula
formula_speed = 0.1  # Adjust as needed

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    window.fill((79, 121, 66))

    # Draw obstacles
    for obstacle in obstacles:
        pygame.draw.rect(window, (128, 128, 128), obstacle)

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
    clock.tick(120)  # Keep FPS at 60

    # Slow down the formula movement
    pygame.time.delay(int(1000 / 60 * formula_speed))  # 60 FPS equivalent delay with speed adjustment

