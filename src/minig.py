import pygame
import netcode
import minigames.minigame_base as mini
import minigames.test as mini_test
import minigames.piano as piano
import minigames.podvadeni as mini_podvadeni
import minigames.invaders as invaders
import minigames.aim as mini_aim
import minigames.minihra_klikání as mini_klik

# tady odkažte svoji minihru s jejím jménem (stejně jako test)
minigame_lib = {
    "test": mini_test.test_minigame,
    "piano": piano.piano,
    "podvadeni": mini_podvadeni.podvadeni,
    "invaders": invaders.mini_invaders,
    "klikani": mini_klik.mini_klik,
    "aim": mini_aim.mini_aim,
}

def switch_to_minigame(name: str, team, room, land, score: int, screen: pygame.Surface):
    # minigame setup

    mini.mini_surface = screen
    mini_loop = minigame_lib[name]

    # run minigame

    try:
        result = mini_loop()
    except mini.MinigameInterupt as e:
        if e.reason == "game_ended":
            return

        result = None

    # check result

    if result == None:
        raise ValueError(f"minigame {name} nevrátil jestli vyhrál/prohrál (`return False` pokud nejde vyhrát ani prohrát, např. automat)")
    elif result == False:
        return None

    elif result.did_win == False: # win
        netcode.send_packet(netcode.client_state.server_conn, (str("score_" + team), int(score + (len(land) * 100))))
        netcode.send_packet(netcode.client_state.server_conn, (str("land_" + team), land.append(room)))

    elif result.did_win == True: # fail
        return None
