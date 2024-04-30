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
    
    def draw(self, x, y, offset):
        pygame.draw.rect(screen, LIGHT_BLUE, [x + offset, y + offset, 70, 100], 0)
        pygame.draw.rect(screen, BLACK, [x + offset, y + offset, 70, 100], 2)
        
        text = font.render(self.name, True, BLACK)
        text_rect = text.get_rect(center=(x + 35, y + 50 + offset))
        screen.blit(text, text_rect)

        
components = [
    Component("CPU", "Processor"),
    Component("GPU", "Graphics"),
    Component("RAM", "Memory")
    ]

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    screen.fill(GRAY)
    pygame.draw.rect(screen, BROWN, [100, 150, 600, 300], 0)
    stack_start_x = 110
    stack_start_y = 160
    for i, comp in enumerate(components):
        comp.draw(stack_start_x, stack_start_y, i * 2)
    
    pygame.display.flip()
    clock.tick(30)
    
pygame.quit()
