import pygame
import random

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("PC Component Prší Game")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHT_BLUE = (173, 216, 230)
BROWN = (139, 69, 19)

clock = pygame.time.Clock()
running = True

font = pygame.font.Font(None, 36) 

class Component:
    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.position = 'hand'
    
    def draw(self, x, y, offset=0):
        pygame.draw.rect(screen, LIGHT_BLUE, [x + offset, y + offset, 70, 100], 0)
        pygame.draw.rect(screen, BLACK, [x + offset, y + offset, 70, 100], 2)
        
        text = font.render(self.name, True, BLACK)
        text_rect = text.get_rect(center=(x + 35 + offset, y + 50 + offset))
        screen.blit(text, text_rect)
    
class Deck:
    def __init__(self, components):
        self.components = components
        random.shuffle(self.components)
        
    def draw_card(self):
        if self.components:
            return self.components.pop(0)
        return None

class Player:
    def __init__(self, hand=None, table=None):
        self.hand = hand if hand else []
        self.table = table if table else []
    
    def draw(self, deck):
        card = deck.draw_card()
        if card:
            self.hand.append(card)
    
    def play_card(self, index):
        if index < len(self.hand):
            self.table.append(self.hand.pop(index))
        
player_hand = []
deck = Deck([Component("CPU", "Processor"), Component("GPU", "Graphics"), Component("RAM", "Memory"), Component("HDD", "Hard Disk"), Component("MB", "Motherboard")])
components = [ 
    Component("CPU", "Processor"), 
    Component("GPU", "Graphics"), 
    Component("RAM", "Memory"),
    Component("HDD", "Hard Disk"),
    Component("MB", "Motherboard")
    ]
player = Player()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            
            if 100 <= mouse_x <= 170 and 150 <= mouse_y <= 250 and len(player_hand) < 4:            
                card = deck.draw_card()
                if card:
                    player_hand.append(card)
                
                for index, card in enumerate(player_hand):
                    card_x = 300 + index * 100
                    if card_x <= mouse_x <= card_x + 70 and 400 <= mouse_y <= 500:
                                                                player.play_card(index)
                                                                break
            
    screen.fill(GRAY)
    pygame.draw.rect(screen, BROWN, [100, 150, 600, 300], 0)
    
    stack_start_x = 110
    stack_start_y = 160
    
    for index, card in enumerate(player.table):
        card.draw(350 + index * 5, 200)
        
    for index, card in enumerate(player_hand):
        card.draw(300 + index * 100, 400)
        
    for i, comp in enumerate(components):
        comp.draw(stack_start_x, stack_start_y, i * 2)
    
    pygame.display.flip()
    clock.tick(30)
    
pygame.quit()
