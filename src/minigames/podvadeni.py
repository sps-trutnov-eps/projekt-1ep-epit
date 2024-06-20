import pygame
import minigames.minigame_base as mini
import random
def podvadeni(screen: pygame.Surface):
    vyhrál = False
    completion_meter = pygame.Rect(50, 50, 300, 30)
    completion = pygame.Rect(50, 50, 300, 30)
    percent = 0
    timer = pygame.Rect(50, 130, 300, 30)
    timer_frame = pygame.Rect(35, 115, 330, 60) 
    time = pygame.Rect(50, 130, 300, 30)
    seconds = 30000
    teacher_looking = False
    teacher_time = random.randint(0, 10)
    teacher_timer = 0
    teacher_looking_timer = 240
    teacher_set = False
    teacher_color = (200, 0, 0)
    warning_movement = 1
    
    backdrop = pygame.Rect(0, 0, 1280, 960)
    
    player = pygame.Rect(1100, 460, 100, 100)
    teacher = pygame.Rect(100, 360, 100, 150)
    teacher_warning = pygame.Rect(250, 250, 50, 100)
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if (event.type == pygame.QUIT or
                (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE)):
                quit()
        clock.tick(60)
        stisknute_klavesy = pygame.key.get_pressed()
        # rychlá prohra: E
        if pygame.key.get_pressed()[pygame.K_e]:
            return mini.fail_minigame()
        # rychlá výhra: Q
        elif pygame.key.get_pressed()[pygame.K_q]:
            return mini.win_minigame()
        
        #časovač - minuta
        if time.width >= 0:
            seconds -= 8
            time.width = seconds/100
        if time.width <= 0:
            return mini.fail_minigame()
        
        #podvádění - MEZERNÍK
        if stisknute_klavesy[pygame.K_SPACE]:
            percent += 1
        if percent <= 1800:
            completion.width = percent/6
        if percent >= 1800:
            return mini.win_minigame()
        
        #UČITEL
        if not teacher_set:
            teacher_timer = teacher_time * 60
            teacher_set = True 
        if teacher_set:
            teacher_timer -= 1
        if teacher_timer <= 60:
            teacher_warning.left = 250
        if teacher_timer > 60:
            teacher_warning.left = -250
        #učitel - varování
        if teacher_warning.top <= 230:
            warning_movement = 1
        if teacher_warning.top >= 250:
            warning_movement = -1
        teacher_warning.top += warning_movement
        
        #učitel - časování
        if teacher_timer <= 0:
            teacher_looking = True    
        if teacher_looking:
            teacher_color = (200, 0, 200)
            teacher_looking_timer -= 1
        if not teacher_looking:
            teacher_color = (200, 0, 0)
        if teacher_looking_timer <= 0:
            teacher_looking = False
            teacher_time = random.randint(0, 10)
            teacher_set = False
            teacher_looking_timer = 240
            
        if teacher_looking and stisknute_klavesy[pygame.K_SPACE]: #prohra
            return mini.fail_minigame()
        
        # zavolej tuto funkci každý frame (kvůli ostatním věcem jako multiplayer)
        mini.mini_frame()
        
        pygame.draw.rect(mini.mini_surface, (255, 255, 255), backdrop)
        pygame.draw.rect(mini.mini_surface, (0, 0, 0), player)
        pygame.draw.rect(mini.mini_surface, teacher_color, teacher)
        pygame.draw.rect(mini.mini_surface, (255, 0, 0), teacher_warning)
        pygame.draw.rect(mini.mini_surface, (70, 0, 0), completion_meter)
        pygame.draw.rect(mini.mini_surface, (180, 0, 0), completion)
        pygame.draw.rect(mini.mini_surface, (50, 50, 25), timer_frame)
        pygame.draw.rect(mini.mini_surface, (0, 0, 100), timer)
        pygame.draw.rect(mini.mini_surface, (0, 0, 180), time)
        pygame.display.update()