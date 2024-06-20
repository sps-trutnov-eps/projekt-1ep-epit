import pygame
import netcode
import minigames.minigame_base as mini
import minigames.test as mini_test
import minigames.piano as piano
import minigames.podvadeni as mini_podvadeni
import minigames.invaders as invaders
import minigames.aim as mini_aim
import minigames.minihra_klikání as mini_klik
import minigames.více_koleček as vice
import minigames.clickni_na_kolečko as kol
import minigames.multitasking as multi
import minigames.přepis as prepis
import minigames.zapamatuj_si_číslo as mem

# tady odkažte svoji minihru s jejím jménem (stejně jako test)
minigame_lib = {
    "piano": piano.piano,
    "podvadeni": mini_podvadeni.podvadeni,
    "invaders": invaders.mini_invaders,
    "klikani": mini_klik.mini_klik,
    "aim": mini_aim.mini_aim,
    "vice": vice.mini_vic_kolecek,
    "kolecka": kol.mini_kolecko,
    "multitasking": multi.mini_multi,
    "prepis": prepis.mini_prepis,
    "zapamatuj": mem.mini_memory,
}

def switch_to_minigame(name: str, team: str, room: str, screen: pygame.Surface):
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
        netcode.send_packet(netcode.client_state.server_conn, (str("score_" + team), 100))
        netcode.send_packet(netcode.client_state.server_conn, (str("land_" + team), land.append(room)))

    elif result.did_win == True: # fail
        return None
