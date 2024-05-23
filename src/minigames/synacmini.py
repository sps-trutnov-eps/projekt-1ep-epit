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
        "question": "Jaké jsou praktické aplikace Newtonova třetího zákona pohybu?",
        "options": ["A. Gravitace je odpovědná za pohyb planet", "B. Síla tření je nezávislá na hmotnosti tělesa", "C. Objekty se pohybují, když na ně působí menší síla", "D. Pohybující se těleso vyvolává opačnou reakci na jiné těleso"],
        "correct_answer": "D"
    },
    {
        "question": "Jaká je hlavní tématická linka v románech Karla Čapka?",
        "options": ["A. Kritika moderní společnosti", "B. Láska a vášeň", "C. Hledání identity postav", "D. Obrana před mimozemským útokem"],
        "correct_answer": "A"
    },
    {
        "question": "Jaká je definice obsahu obvodu čtverce?",
        "options": ["A. Obvod je roven dvojnásobku obsahu", "B. Obvod je roven čtyřnásobku jedné délky", "C. Obvod je roven odmocnině součtu délek všech stran", "D. Obvod je roven součtu délek všech stran umocněných na druhou"],
        "correct_answer": "B"
    },
    {
        "question": "Co je to procesor a jak funguje?",
        "options": ["A. Paměťové zařízení", "B. Zařízení pro přenos dat", "C. Centrální procesní jednotka, která provádí instrukce programu", "D. Zobrazovací jednotka monitoru"],
        "correct_answer": "C"
    },
    {
        "question": "Jaké jsou hlavní složky vzduchu a jejich vliv na životní prostředí?",
        "options": ["A. Kyslík, dusík, vodní pára; podporuje život na Zemi", "B. Kyslík, argon, oxid uhličitý; znečišťuje ovzduší", "C. Vodík, metan, ozón; podporuje ozónovou díru", "D. Oxid uhličitý, ozón, dusičnany; negativně ovlivňuje kvalitu ovzduší"],
        "correct_answer": "A"
    },
    {
        "question": "Jaký je vztah mezi poloměrem a obvodem kruhu?",
        "options": ["A. Obvod je roven součinu poloměru a čísla π", "B. Obvod je roven součtu poloměru a čísla π", "C. Poloměr je roven součinu obvodu a čísla π", "D. Poloměr je roven podílu obvodu a čísla π"],
        "correct_answer": "D"
    },
    {
        "question": "Která událost vedla k vzniku Americké revoluce v roce 1775?",
        "options": ["A. Vyhlášení Deklarace nezávislosti", "B. Bitva u Lexingtonu a Concordu", "C. Boston Tea Party", "D. Podepsání Pařížské mírové smlouvy"],
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

