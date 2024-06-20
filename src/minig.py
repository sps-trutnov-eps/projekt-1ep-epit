import pygame
import netcode
import minigames.minigame_base as mini
import minigames.test as mini_test
import minigames.piano as piano
import minigames.podvadeni as mini_podvadeni
# tady odkažte svoji minihru s jejím jménem (stejně jako test)
minigame_lib = {
    "test": mini_test.test_minigame,
    "piano": piano.piano,
    "podvadeni": mini_podvadeni.podvadeni
}

def switch_to_minigame(name: str, team, room, screen: pygame.Surface):
    # minigame setup

    mini.mini_surface = screen
    mini_loop = minigame_lib[name]

    # run minigame

    result = mini_loop(screen)

    # check result

    if result == None:
        raise ValueError(f"minigame {name} nevrátil jestli vyhrál/prohrál (`return False` pokud nejde vyhrát ani prohrát, např. automat)")
    elif result == False:
        return None

    elif result.did_win == False: # win
        netcode.send_packet(client_state.server_conn, (str("score_" + team), (len(land) * 100), player_name, protocol_version))
        netcode.send_packet(client_state.server_conn, (str("land_" + team), room, player_name, protocol_version))

    elif result.did_win == True: # fail
        return None
