import pygame
import sys
import random

# Inicializace pygame
pygame.init()

# Získání velikosti obrazovky
screen_info = pygame.display.Info()
screen_width = screen_info.current_w
screen_height = screen_info.current_h

# Nastavení displeje v režimu celé obrazovky
window = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
pygame.display.set_caption("Připraven?")

# Barvy
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Příznaky
game_ready = False
game_ongoing = False
question_asked = False

# Definice seznamu otázek s možnostmi a správnými odpověďmi
questions = [
    {
        "question": "Kdo vstřelil zlatý gól na MS v hokeji 2024?",
        "options": ["A. Roman Červenka", "B. Lukáš Sedlák", "C. Dominik Kubalík", "D. David Pastrňák"],
        "correct_answer": "D"
    },
    {
        "question": "Kdo byl vyhlášen brankářem MS v hokeji 2024?",
        "options": ["A. Lukáš Dostál", "B. Alex Lyon", "C. Emil Larmi", "D. Eriks Vitols"],
        "correct_answer": "A"
    },
    {
        "question": "Kdo byl vyhlášen obráncem MS v hokeji 2024?",
        "options": ["A. Roman Josi", "B. Owen Power", "C. Lukas Kälble", "D. Oliwer Kaski"],
        "correct_answer": "A"
    },
    {
        "question": "Kdo byl vyhlášen útočníkem MS v hokeji 2024?",
        "options": ["A. Roman Červenka", "B. Kevin Fiala", "C. Libor Hudáček", "D. JJ Peterka"],
        "correct_answer": "B"
    },
    {
        "question": "Jaké bylo složení All-Star týmu na MS v hokeji 2024:",
        "options": ["A. Kevin Fiala, Roman Červenka, Dylan Cozens, Erik Karlsson, Roman Josi, Lukáš Dostál", "B. JJ Peterka, Matt Boldy, Roman Červenka, Owen Power, Lukas Kälble, Kristers Gudlevskis", "C. Oliver Kapanen, Dylan Cozens, Roman Červenka, Oliwer Kaski, Zach Werenski, Emil Larmi", "D. Dylan Cozens, Matt Boldy, Evan Mosey, Lukas Kälble, Jonas Müller, Emil Larmi"],
        "correct_answer": "A"
    },
    {
        "question": "Kdo měl nejlepší úspěšnost na vhazování na MS v hokeji 2024?",
        "options": ["A. Nick Paul", "B. Kevin Hayes", "C. John Tavares", "D. Nico Hischier"],
        "correct_answer": "C"
    },
    {
        "question": "Jaký brankář byl vyhlášen brankářem s nejmenpším počtem obdržených gólů na zápas na MS v hokeji 2024?",
        "options": ["A. Leonardo Genoni", "B. Trey Augustine", "C. Samuel Hlavaj", "D. Emil Larmi"],
        "correct_answer": "A"
    },
    {
        "question": "Jaký hráč byl vyhlášen jako nejlepší ve statistice +/- na MS v hokeji 2024?",
        "options": ["A. Marcus Johansson", "B. Michael Bunting", "C. Colton Parayko", "D. Erik Karlsson"],
        "correct_answer": "A"
    },
    {
        "question": "Jaký brankář byl vyhlášen jako brankář s nejlepší úspěšnpostí zákroků na MS v hokeji 2024?",
        "options": ["A. Leonardo Genoni", "B. Alex Lyon", "C. Samuel Hlavaj", "D. Kristers Gudlevskis"],
        "correct_answer": "A"
    },
    {
        "question": "Jaký tým vyhrál bronzovou medaili na MS v hokeji 2024?",
        "options": ["A. Švédsko", "B. Lotyšsko", "C. Česko", "D. USA"],
        "correct_answer": "A"
    },
    {
        "question": "Jaký tým vyhrál zlatou medaili na MS v hokeji 2024?",
        "options": ["A. Česko", "B. Kanada", "C. Finsko", "D. Švédsko"],
        "correct_answer": "A"
    },
    {
        "question": "Jaký hráč měl nejvíc asistencí na MS v Hokeji 2024?",
        "options": ["A. Libor Hudáček", "B. Mats Zuccarello", "C. Rasmus Dahlin", "D. John Tavares"],
        "correct_answer": "D"
    },
    {
        "question": "Jaký obránce měl nejvíc asistencí na MS v hokeji 2024?",
        "options": ["A. Oliwer Kaski", "B. David Špaček", "C. Roman Josi", "D. Zach Werenski"],
        "correct_answer": "C"
    },
    {
        "question": "Jaký hráč dal nejvíc gólů na MS v hokeji 2024?",
        "options": ["A. Joel Eriksson Ek", "B. Lukáš Sedlák", "C. Dylan Cozens", "D. Evan Mosey"],
        "correct_answer": "C"
    },
    {
        "question": "Jaký obránce dal nejvíc gólů na MS v hokeji 2024?",
        "options": ["A. Marcus Johansson", "B. Roman Josi", "C. Šimon Nemec", "D. Erik Karlsson"],
        "correct_answer": "D"
    },
    {
        "question": "Jaký hráč měl nejvíc trestných minut na MS v hokeji 2024?",
        "options": ["A. Oskars Batna", "B. Marco Rossi", "C. Hugo Gallet", "D. Miloš Kelemen"],
        "correct_asnwer": "A"
    },
    {
        "question": "Jaký hráč měl nejvíce bodů na MS v hokeji 2024?",
        "options": ["A. Pierre-Luc Dubois", "B. Matt Boldy", "C. Libor Hudáček", "D. Roman Červenka"],
        "correct_answer": "B"
    },
    {
        "question": "Jaký obránce měl nejvíce bodů na MS v hokeji 2024?",
        "options": ["A. Victor Hedman", "B. Rasmus Dahlin", "C. Erik Karlsson", "D. Roman Josi"],
        "correct_answer": "D"
    },
    {
        "question": "Jaký hráč v kategorii U18 měl nejvíce bodů na MS v hokeji 2024?",
        "options": ["A. Stian Solberg", "B. Konsta Helenius", "C. Michael Brandsegg-Nygård", "D. Felix Unger Sörum"],
        "correct_answer": "B"
    },
    {
        "question": "Jaký hráč v kategorii U20 měl nejvíce budů na MS v hokeji 2024?", 
        "options": ["A. Juraj Slafkovský", "B. David Špaček", "C. Connor Bedard", "D. Šimon Nemec"],
        "correct_answer": "C"
    },
    {
        "question": "Jaký hráč byl vyhlášen nejhodnotnějším hráčem MS v hokeji 2024?",
        "options": ["A. Roman Červenka", "B. Erik Karlsson", "C. Kevin Fiala", "D. Roman Josi"],
        "correct_answer": "C"
    },
    {
        "question": "Jaký tým vyhrál stříbrnou medaili na MS v hokeji 2024?",
        "options": ["A. Česko", "B. Švýcarsko", "C. Švédsko", "D. Kanada"],
        "correct_answer": "B"
    }
]

# Funkce pro vykreslení úvodní obrazovky
def draw_start_screen():
    window.fill(WHITE)
    font = pygame.font.SysFont(None, 64)
    ready_text = font.render("PŘIPRAVEN?", True, BLACK)
    ready_text_rect = ready_text.get_rect(center=(screen_width // 2, screen_height // 2 - 100))
    window.blit(ready_text, ready_text_rect)

    button_x = (screen_width - 200) // 2
    button_y = (screen_height - 50) // 2 + 100
    button_rect = pygame.Rect(button_x, button_y, 200, 50)
    pygame.draw.rect(window, GRAY, button_rect)

    button_font = pygame.font.SysFont(None, 36)
    button_text = button_font.render("Začít hru", True, BLACK)
    button_text_rect = button_text.get_rect(center=button_rect.center)
    window.blit(button_text, button_text_rect)
    pygame.display.flip()

# Funkce pro vykreslení obrazovky s otázkou
def draw_question_screen(question_data):
    window.fill(WHITE)
    font = pygame.font.SysFont(None, 32)
    question = question_data["question"]
    options = question_data["options"]

    question_text = font.render(question, True, BLACK)
    question_text_rect = question_text.get_rect(center=(screen_width // 2, screen_height // 2 - 100))
    window.blit(question_text, question_text_rect)

    option_y = screen_height // 2
    option_rects = []
    for option in options:
        option_text = font.render(option, True, BLACK)
        option_text_rect = option_text.get_rect(midtop=(screen_width // 2, option_y))
        window.blit(option_text, option_text_rect)
        option_rects.append((option_text_rect, option[0]))
        option_y += 40

    pygame.display.flip()
    return option_rects

# Funkce pro vykreslení obrazovky se zpětnou vazbou
def draw_feedback_screen(is_correct):
    window.fill(WHITE)
    font = pygame.font.SysFont(None, 64)
    if is_correct:
        feedback_text = font.render("Správně!", True, GREEN)
    else:
        feedback_text = font.render("Špatně!", True, RED)
    feedback_text_rect = feedback_text.get_rect(center=(screen_width // 2, screen_height // 2))
    window.blit(feedback_text, feedback_text_rect)
    pygame.display.flip()
    pygame.time.delay(2000)

# Hlavní smyčka
running = True
current_question = None
option_rects = []
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if not game_ready:
                    button_x = (screen_width - 200) // 2
                    button_y = (screen_height - 50) // 2 + 100
                    button_rect = pygame.Rect(button_x, button_y, 200, 50)
                    if button_rect.collidepoint(event.pos):
                        game_ready = True
                        game_ongoing = True
                elif game_ongoing:
                    for rect, answer in option_rects:
                        if rect.collidepoint(event.pos):
                            is_correct = (answer == current_question["correct_answer"])
                            draw_feedback_screen(is_correct)
                            question_asked = False

    window.fill(WHITE)

    if not game_ready:
        draw_start_screen()
    elif game_ongoing and not question_asked:
        current_question = random.choice(questions)
        option_rects = draw_question_screen(current_question)
        question_asked = True

pygame.quit()
sys.exit()