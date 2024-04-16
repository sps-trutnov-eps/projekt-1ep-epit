import pygame
import minigames.minigame_base as mini

def test_minigame():
    vyhrál = False

    while True:
        # stiskni e abys vyhrál
        if pygame.key.get_pressed()[pygame.K_e]:
            return mini.fail_minigame()
        
        # stiskni q abys prohrál
        elif pygame.key.get_pressed()[pygame.K_q]:
            return mini.win_minigame()

        # zavolej tuto funkci každý frame (kvůli ostatním věcem jako multiplayer)
        mini.mini_frame()