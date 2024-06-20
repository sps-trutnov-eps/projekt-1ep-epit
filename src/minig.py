import pygame
import minigames.minigame_base as mini
import minigames.test as mini_test
import minigames.aim as mini_aim
import minigames.minihra_klikání as mini_klik

# tady odkažte svoji minihru s jejím jménem (stejně jako test)
minigame_lib = {
    "test": mini_test.test_minigame,
    "klikani": mini_klik.mini_klik,
    "aim": mini_aim.mini_aim,
}

def switch_to_minigame(name, sur: pygame.Surface):
    # minigame setup

    mini.mini_surface = sur
    mini_loop = minigame_lib[name]

    # run minigame

    result = mini_loop()

    # check result

    if result == None:
        raise ValueError(f"minigame {name} nevrátil jestli vyhrál/prohrál (`return False` pokud nejde vyhrát ani prohrát, např. automat)")
    elif result == False:
        pass # minihra nemá wil/fail state (např. automat)

    elif result.did_win == False: # win
        pass # TODO: pro Pavla
    
    elif result.did_win == True: # fail
        pass # TODO: pro Pavla