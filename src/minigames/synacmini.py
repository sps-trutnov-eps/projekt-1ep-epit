import pygame
import sys
import random

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

# Flag to track if the game is ongoing
game_ongoing = False

# Define a list of questions with options and correct answers
questions = [
    {
        "question": "What is the capital of France?",
        "options": ["A. Paris", "B. Rome", "C. London", "D. Berlin"],
        "correct_answer": "A"
    },
    {
        "question": "Who wrote 'To Kill a Mockingbird'?",
        "options": ["A. Mark Twain", "B. Harper Lee", "C. J.K. Rowling", "D. Charles Dickens"],
        "correct_answer": "B"
    },
    {
        "question": "What is the chemical symbol for water?",
        "options": ["A. O", "B. H2O", "C. CO2", "D. H2O2"],
        "correct_answer": "B"
    },
    {
        "question": "What year did the Titanic sink?",
        "options": ["A. 1912", "B. 1921", "C. 1905", "D. 1917"],
        "correct_answer": "A"
    },
    {
        "question": "Who painted the Mona Lisa?",
        "options": ["A. Leonardo da Vinci", "B. Vincent van Gogh", "C. Pablo Picasso", "D. Claude Monet"],
        "correct_answer": "A"
    }
]

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and not game_ready:
            if event.button == 1:  # Left mouse button
                # Check if the mouse click is inside the button rectangle
                button_x = (screen_width - 200) // 2
                button_y = (screen_height - 50) // 2 + 100
                button_rect = pygame.Rect(button_x, button_y, 200, 50)
                if button_rect.collidepoint(event.pos):
                    # Mark the game as ready to start
                    game_ready = True

        elif event.type == pygame.MOUSEBUTTONDOWN and game_ongoing:
            if event.button == 1:  # Left mouse button
                # Generate a random question
                question_data = random.choice(questions)
                question = question_data["question"]
                options = question_data["options"]
                correct_answer = question_data["correct_answer"]
                
                # Clear the screen
                window.fill(WHITE)

                # Draw the question
                font = pygame.font.SysFont(None, 32)
                question_text = font.render(question, True, BLACK)
                question_text_rect = question_text.get_rect(center=(screen_width // 2, screen_height // 2 - 50))
                window.blit(question_text, question_text_rect)

                # Draw options
                option_y = screen_height // 2
                for option in options:
                    option_text = font.render(option, True, BLACK)
                    option_text_rect = option_text.get_rect(midtop=(screen_width // 2, option_y))
                    window.blit(option_text, option_text_rect)
                    option_y += 40

                pygame.display.flip()

    # Clear the screen
    window.fill(WHITE)

    if not game_ready:
        # Draw "READY?" text
        font = pygame.font.SysFont(None, 64)
        ready_text = font.render("READY?", True, BLACK)
        ready_text_rect = ready_text.get_rect(center=(screen_width // 2, screen_height // 2 - 100))
        window.blit(ready_text, ready_text_rect)

        # Draw rectangle as button with text "Start the game"
        button_x = (screen_width - 200) // 2
        button_y = (screen_height - 50) // 2 + 100
        button_rect = pygame.Rect(button_x, button_y, 200, 50)
        pygame.draw.rect(window, GRAY, button_rect)
        
        # Draw text inside the button
        button_font = pygame.font.SysFont(None, 36)
        button_text = button_font.render("Start the game", True, BLACK)
        button_text_rect = button_text.get_rect(center=button_rect.center)
        window.blit(button_text, button_text_rect)
    else:
        # Draw white screen for the next stage
        window.fill(WHITE)
        game_ongoing = True

    pygame.display.flip()

# Quit pygame
pygame.quit()
sys.exit()
