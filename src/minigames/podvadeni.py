import pygame
import minigames.minigame_base as mini

def podvadeni():
    vyhrál = False
    completion_meter = pygame.Rect(50, 50, 300, 30)
    timer = pygame.Rect(50, 130, 300, 30)
    time = pygame.Rect(50, 130, 300, 30)
    seconds = 30000
    
    backdrop = pygame.Rect(0, 0, 1280, 960)
    
    player = pygame.Rect(1100, 460, 100, 100)
    teacher = pygame.Rect(100, 360, 100, 150)
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if (event.type == pygame.QUIT or
                (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE)):
                quit()
        clock.tick(60)
        # stiskni e abys vyhrál
        if pygame.key.get_pressed()[pygame.K_e]:
            return mini.fail_minigame()
        
        # stiskni q abys prohrál
        elif pygame.key.get_pressed()[pygame.K_q]:
            return mini.win_minigame()
        
        if time.width >= 0:
            seconds -= 8
            time.width = seconds/100
        
        if time.width <= 0:
            return mini.fail_minigame()

        # zavolej tuto funkci každý frame (kvůli ostatním věcem jako multiplayer)
        mini.mini_frame()
        
        pygame.draw.rect(mini.mini_surface, (255, 255, 255), backdrop)
        pygame.draw.rect(mini.mini_surface, (0, 0, 0), player)
        pygame.draw.rect(mini.mini_surface, (255, 0, 0), teacher)
        pygame.draw.rect(mini.mini_surface, (160, 0, 0), completion_meter)
        pygame.draw.rect(mini.mini_surface, (0, 0, 70), timer)
        pygame.draw.rect(mini.mini_surface, (0, 0, 180), time)
        pygame.display.update()