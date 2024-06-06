import pygame
import sys
import math

pygame.init()

screen = pygame.display.set_mode((800, 600))

pygame.display.set_caption('lobby')

black = (0, 0, 0)
brown = (139, 69, 19)
gray = (169, 169, 169)
light_brown = (205, 133, 63)
blue = (0, 0, 255)

player_x, player_y = 400, 300

def draw_table_and_chairs(surface, table_color, chair_color, table_rect, chair_size, gap):
    pygame.draw.rect(surface, table_color, table_rect)
    
    table_x, table_y, table_width, table_height = table_rect
    chair_width, chair_height = chair_size
    
    pygame.draw.rect(surface, chair_color, (table_x + (table_width - chair_width * 2 - gap) / 2, table_y - chair_height - 5, chair_width, chair_height))
    pygame.draw.rect(surface, chair_color, (table_x + (table_width + gap) / 2, table_y - chair_height - 5, chair_width, chair_height))
    
def draw_square(surface, color, center, size):
    top_left = (center[0] - size // 2, center[1] - size // 2)
    pygame.draw.rect(surface, color, (*top_left, size, size))
    
def draw_teacher_table_and_chair(surface, table_color, chair_color, table_rect, chair_rect):
    pygame.draw.rect(surface, table_color, table_rect)
    pygame.draw.rect(surface, chair_color, chair_rect) 
    
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    screen.fill(black)
    
    center = (400, 300)
    square_size = 550
    
    draw_square(screen, gray, center, square_size + 20)
    draw_square(screen, brown, center, square_size)
    
    table_width, table_height = 60, 30
    chair_width, chair_height = 25, 25
    rows = 4
    cols = 4
    spacing = 40
    gap = 5
    vertical_offset = -40
    horizontal_offset = -40 
    
    start_x = center[0] - (cols * (table_width + spacing) / 2) + (table_width / 2) + horizontal_offset
    start_y = center[1] - (cols * (table_height + chair_height + spacing) / 2) + chair_height + (table_height / 2) + vertical_offset
    
    for row in range(rows):
        for col in range(cols):
            table_x = start_x + col * (table_width + spacing)
            table_y = start_y + row * (table_height + chair_height + spacing)
            chair_x = start_x + col * (table_width + spacing)
            chair_y = start_y + row * (table_height + chair_height + spacing)
            table_rect = (table_x, table_y, table_width, table_height)
            chair_rect = (chair_x, chair_y, chair_width, chair_height)
            draw_table_and_chairs(screen, light_brown, light_brown, table_rect, (chair_width, chair_height), gap)
            
            teacher_table_width, teacher_table_height = 35, 25 #je to naopak, table width, height zaznamenává velikost židle a chair width, height zaznamenává velikost stolu
            teacher_chair_width, teacher_chair_height = 100, 40
            
            
            teacher_table_x = center[0] - square_size // 2 + 10
            teacher_table_y = center[1] + square_size // 2 - teacher_table_height - 10
            
            teacher_chair_x = teacher_table_x + (teacher_table_width - teacher_table_width) // 2
            teacher_chair_y = teacher_table_y - teacher_chair_height - 5
            
            teacher_table_rect = (teacher_table_x, teacher_table_y, teacher_table_width, teacher_table_height)
            teacher_chair_rect = (teacher_chair_x, teacher_chair_y, teacher_chair_width, teacher_chair_height)
            
            draw_teacher_table_and_chair(screen, black, light_brown, teacher_table_rect, teacher_chair_rect)
            
            #pygame.draw.rect(screen, blue, (player_x, player_y, player_width, player_height))
    
    pygame.display.flip()
    
pygame.quit()
sys.exit()
    



