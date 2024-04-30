import pygame
import sys

# Initialize pygame
pygame.init()

# Get the screen size
screen_info = pygame.display.Info()
screen_width = screen_info.current_w
screen_height = screen_info.current_h

# Set up the display in fullscreen mode
window = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
pygame.display.set_caption("Ready?")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# Flag to track if the game is ready to start
game_ready = False

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and not game_ready:
            if event.button == 1:  # Left mouse button
                # Check if the mouse click is inside the button rectangle
                if button_rect.collidepoint(event.pos):
                    # Mark the game as ready to start
                    game_ready = True

    # Clear the screen
    window.fill(WHITE)

    if not game_ready:
        # Draw "READY?" text
        font = pygame.font.SysFont(None, 64)
        ready_text = font.render("READY?", True, BLACK)
        ready_text_rect = ready_text.get_rect(center=(screen_width // 2, screen_height // 2 - 100))
        window.blit(ready_text, ready_text_rect)

        # Draw rectangle as button with text "Start the game"
        button_width = 200
        button_height = 50
        button_x = (screen_width - button_width) // 2
        button_y = (screen_height - button_height) // 2 + 100
        button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
        pygame.draw.rect(window, GRAY, button_rect)
        
        # Draw text inside the button
        button_font = pygame.font.SysFont(None, 36)
        button_text = button_font.render("Start the game", True, BLACK)
        button_text_rect = button_text.get_rect(center=button_rect.center)
        window.blit(button_text, button_text_rect)
    else:
        # Draw white screen for the next stage
        window.fill(WHITE)

    pygame.display.flip()

# Quit pygame
pygame.quit()
sys.exit()
