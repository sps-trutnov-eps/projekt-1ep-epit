import pygame
import netcode

# == sdílené časti kódu použitelné v celém projektu ==

# může být zavolána kdekoli aby hra byla správně ukončena
def game_quit():
    netcode.quit_netcode()

    pygame.quit()
    exit(0)