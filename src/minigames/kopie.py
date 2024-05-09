import pygame
import minigames.minigame_base as mini

def kopie():
    vyhrál = False
    completion_meter = pygame.Rect(50, 50, 300, 30)
    backdrop = pygame.Rect(0, 0, 1280, 960)
    player = pygame.Rect(1100, 500, 100, 100)
    while True:
        for event in pygame.event.get():
            if (event.type == pygame.QUIT or
                (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE)):
                quit()
        
        # stiskni e abys vyhrál
        if pygame.key.get_pressed()[pygame.K_e]:
            return mini.fail_minigame()
        
        # stiskni q abys prohrál
        elif pygame.key.get_pressed()[pygame.K_q]:
            return mini.win_minigame()

        # zavolej tuto funkci každý frame (kvůli ostatním věcem jako multiplayer)
        mini.mini_frame()
        
        pygame.draw.rect(mini.mini_surface, (255, 255, 255), backdrop)
        pygame.draw.rect(mini.mini_surface, (255, 0, 255), player)
        pygame.draw.rect(mini.mini_surface, (200, 200, 200), completion_meter)
        pygame.display.update()