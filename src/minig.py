import pygame
import minigames.minigame_base as mini
import minigames.test as mini_test
import minigames.piano as piano
# tady odkažte svoji minihru s jejím jménem (stejně jako test)
minigame_lib = {
    "test": mini_test.test_minigame,
    "piano": piano.piano,
}

def switch_to_minigame(name, screen: pygame.Surface):
    # minigame setup

    mini.mini_surface = screen
    mini_loop = minigame_lib[name]

    # run minigame

    result = mini_loop(screen)

    # check result

    if result == None:
        raise ValueError(f"minigame {name} nevrátil jestli vyhrál/prohrál (`return False` pokud nejde vyhrát ani prohrát, např. automat)")
    elif result == False:
        pass # minihra nemá wil/fail state (např. automat)

    elif result.did_win == False: # win
        pass # TODO: pro Pavla
    
    elif result.did_win == True: # fail
        pass # TODO: pro Pavla