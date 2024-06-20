import pygame
import dataclasses

import netcode

# funckce pro přepínaní do minigame modu a zpět

@dataclasses.dataclass()
class MinigameEndState:
    did_win: bool

class MinigameInterupt(BaseException):
    reason: str

# prohrál minihru, zavolej `return fail_minigame()` aby ses vrátil do hry
def fail_minigame():
    return MinigameEndState(True)

# překonal minihru, zavolej `return win_minigame()` aby ses vrátil do hry
def win_minigame():
    return MinigameEndState(False)

# zavolej tuto funkci každý frame ve tvé minihře
def mini_frame():
    netcode.client_sync()
    
    if not netcode.client_state.game_state == 1:
        raise MinigameInterupt("game_ended")

# pygame surface pro rendering
mini_surface: pygame.Surface = None