import atexit

import socket
import socketserver

import select
import json
import threading
import subprocess
import hashlib
import traceback
import zlib
import os

import time
from typing import Callable
import random

# TO ALL WHO DARE: do NOT import pygame in this file, it will cause a hang witch requires a trip to the task manager to solve

# == EPIT server/client backend netcode ==

protocol_version = 17
packet_len_bytes = 4
target_ticktime = (1 / 20) # ideal ~20 TPS target

# == client state ==

# an netcode specific exception which triggers the dc_screen in main.py
class GameDisconnect(Exception):
    what: str

    def __init__(self, what: str) -> None:
        self.what = what

class ClientState:
    __slots__ = ["server_conn", "player_name", "remote_player_states", "on_lobby_info", "game_state", "is_host", "on_game_result", "on_player_info", "on_game_score"]

    def __init__(self, uri, player_name, is_host, hooks) -> None:
        self.server_conn = socket.create_connection(uri)

        self.player_name = player_name
        self.remote_player_states = []

        self.game_state = 0

        self.is_host = is_host

        self.on_lobby_info = hooks[0]
        self.on_game_result = hooks[1]
        self.on_player_info = hooks[2]
        self.on_game_score = hooks[3]

    server_conn: socket.socket
    client_thread: threading.Thread

    # epit info (read by the game)

    player_name: str
    game_state: int # 0 = in lobby, 1 = in game

    on_lobby_info: Callable
    on_game_result: Callable

    on_player_info: Callable
    on_game_score: Callable

    # note: a random player can become a host when the current host disconnects (aka this value can change)
    is_host: bool

client_state: ClientState

# == client implementation ==

def send_packet(sock: socket.socket, obj):
    try:
        packet_data: bytes = zlib.compress(bytes(json.dumps(obj), 'utf-8'), 4)
        packet_len: int = len(packet_data)
        
        sock.sendall(packet_len.to_bytes(packet_len_bytes, "big", signed=False) + packet_data)
    except:
        pass

# note: only really used for server sends
def send_packets(socks: list[socket.socket], obj):
    try:
        packet_data: bytes = zlib.compress(bytes(json.dumps(obj), 'utf-8'), 4)
        packet_len: int = len(packet_data)

        packet_fin: bytes = packet_len.to_bytes(packet_len_bytes, "big", signed=False) + packet_data
        for sock in socks:
            sock.sendall(packet_fin)
    except:
        pass

def read_packet(sock: socket.socket) -> list:
    # read packet size header
    msg_len = sock.recv(packet_len_bytes)

    if not msg_len:
        raise ConnectionError

    # parse packet header
    msg_len = int.from_bytes(msg_len, "big", signed=False)

    message = b''

    while msg_len:
        fragment = sock.recv(min(msg_len, 4096))

        if not fragment:
            raise ConnectionError

        msg_len = max(0, msg_len - len(fragment))
        message += fragment
    
    try:
        return json.loads(zlib.decompress(message)) 
    except:
        print(message)
        raise

# called once per client frame to sync with server
def client_sync(watch_for_lock_response: bool = False) -> bool | None:
    # == parse server packets (if any) ==

    packets = []

    while True:
        read_sockets, _, _ = select.select((client_state.server_conn,), tuple(), tuple(), 0)

        if len(read_sockets) == 0:
            break

        for sock in read_sockets:
            # receive and parse packets from tcp stream

            try:
                packets.append(read_packet(sock))

            except TimeoutError:
                raise GameDisconnect("Connection timeout.")
            except ConnectionError:
                raise GameDisconnect("Connection with server interupted.")

    # == process received packets ==

    lock_response = None

    for packet in packets:
        if packet[0] == "s_game_tick":
            client_state.on_player_info(packet[1])
            client_state.on_game_score(packet[2])

        elif packet[0] == "s_game_event":
            event_type = packet[1]

            # lobby events
            if event_type == "game_state_change":
                if client_state.game_state == packet[2]:
                    continue

                client_state.game_state = packet[2]
                if client_state.game_state == 0:
                    # game ended, load lobby and display results

                    # client_state.on_game_result(packet[2]) TODO: results from lobby game tick
                    print("client: game end")

                elif client_state.game_state == 1:
                    # game started, load main map

                    print("client: game start")

            elif event_type == "lobby_update":
                # the lobby data has changed (client connects/disconnects, team/skin changes)

                client_state.on_lobby_info(packet[2])

            elif event_type == "client_update":
                # client state changed (only is_host flag for now)

                client_state.is_host = packet[2]
                print("client: became game host")
        
        elif packet[0] == "s_lock_response":
            if not watch_for_lock_response:
                raise ValueError("recieved lock response while not waiting for it!")
            
            else:
                lock_response = packet[1]
            
        elif packet[0] == "pong":
            print(packet)
        
        elif packet[0] == "s_server_quit":
            if not client_state.is_host:
                exit(-1) # server shutdown
        
        elif packet[0] == "s_unexpected_packet":
            raise GameDisconnect("Internal communication error... (spam the devs to punish them)")

    # handle/queue game state changes

    # send_packet(client_state.server_conn, ("ping", threading.current_thread().getName()))
    
    if not lock_response == None:
        return lock_response

# locks a server-side lock, returns True if locked (and the lock was free) or False if the lock was already locked
# remember to `remote_unlock` after the lock is not needed, otherwise the lock will be locked forever
# note: this def is fully synchronous and *very* slow, never do it in every frame (only loading screens and such)
def remote_try_lock(lock_name: str) -> bool:
    send_packet(client_state.server_conn, ("c_lock_acquire", lock_name))

    while True:
        res = client_sync(True)

        if not res == None:
            return res

# unlocks the lock so other clients can lock the lock
def remote_unlock(lock_name: str):
    send_packet(client_state.server_conn, ("c_lock_release", lock_name))

# start game (only as host)
def start_game():
    if not client_state.is_host:
        raise ValueError("client is not host!")
    
    send_packet(client_state.server_conn, ("c_host_game_start",))

def change_team(team: str):
    if not client_state.game_state == 0:
        raise ValueError("player can only change teams if in lobby, not in game!") # can be changed if we allow changing teams while in-game

    send_packet(client_state.server_conn, ("c_change_team", team))

def update_player_info(pos: list[float], vel: list[float]):
    send_packet(client_state.server_conn, ("c_player_info", pos, vel))

# note: called only by the server!!!
def game_end():
    server_state.game_state = 0

    print("server: ending game...")

def connect_as_client(uri: tuple, player_name: str, is_host: bool, client_hooks: tuple) -> tuple[bool, str | None]:
    # setup client state and connection

    try:
        global client_state
        client_state = ClientState(uri, player_name, is_host, client_hooks)
    except ConnectionError:
        return (False, "Connection refused by server.")
    except TimeoutError:
        return (False, "Timeout connecting to server.")

    # init client with the server
    try:
        send_packet(client_state.server_conn, ("c_init", player_name, protocol_version, is_host))

        # await server response
        response = read_packet(client_state.server_conn)

        if response[0] == "s_init_success":
            client_state.on_lobby_info(response[1])
            client_state.game_state = response[2]
            
            # print("client: i'm i host?", response[3])

            return (True, None)
        else:
            if response[0] == "s_init_name_taken":
                return (False, "Player name is already taken.")

            elif response[0] == "s_init_ingame":
                return (False, "Game has already started, wait for it to end.")

            elif response[0] == "s_unexpected_packet":
                return (False, "Internal communication error... (spam the devs to punish them)")
            
            elif response[0] == "s_version_mismatch":
                return (False, "Version mismatch between client and server.")

            else:
                raise ValueError("client netcode: unhandled server response type") 

    except TimeoutError:
        return (False, "Connection timeout.")

    except ConnectionError:
        return (False, "Connection with server interupted.")

def disconnect_as_client():
    try:
        client_state.server_conn.close()
    except:
        pass # don't look here

# == server state ==

class ServerState:
    __slots__ = ["lobby", "remote_locks", "player_info", "is_shuting_down", "game_state", "host_players", "score", "land"]

    def __init__(self) -> None:
        # init the server infrastructure

        self.remote_locks = {}

        # the server should be under a lock but i don't care for a 5 milisecond race condition
        # assert self.server_lock.acquire(False)

        self.is_shuting_down = False

        self.lobby = {}
        self.host_players = set()

        self.player_info = {}
        self.game_state = 0
        self.score = {"ep": 0, "it": 0}
        self.land = {"ep":["T10"], "it": ["T7"]}

    server: socketserver.ThreadingTCPServer

    remote_locks: dict[str, threading.Lock]
    
    # lobby data (dict indexed by player_name containing [team_name, skin_index])
    lobby_players: dict[str, tuple[str, int]]
    host_players: set[str]

    # in-game data (dict indexed by player_name containing [position, velocity]
    player_info: dict[str, list]
    game_state: int
    score: dict[str, int]
    land: dict[str, list]

server_state: ServerState
server_process: subprocess.Popen # only used when running internal server

# == server implementation ==

def server_handle_disconnect(player):
    print(f"server: client {player} disconnected")

    server_state.lobby.pop(player)
    server_state.player_info.pop(player, None)
    server_state.host_players.discard(player)

def server_handle_connect(req: socket.socket) -> list | None:
    try:
        init_packet = read_packet(req)
    except:
        print("server: new client<->server connection failed while initing client")
        raise

    if not init_packet[0] == "c_init":
        print("server: refused new connection due to faulty client init! (this should never happen if running vanilla EPIT)")

        send_packet(req, ("s_unexpected_packet",))
        return

    elif not init_packet[2] == protocol_version:
        print("server: refused new connection due to version mismatch!")

        send_packet(req, ("s_version_mismatch",))
        return

    elif init_packet[1] in server_state.lobby:
        print("server: refused new connection due to name being taken!")

        send_packet(req, ("s_init_name_taken",))
        return

    elif not server_state.game_state == 0:
        print("server: refused new connection due to not being in lobby!")

        send_packet(req, ("s_init_ingame",))
        return

    return init_packet

# single-threaded server, keeps track of all clients assigned to it
# maybe-TODO: might rewrite with python selector module, not sure if worth it
def server_tickloop():
    # server sockets
    server_sock = socket.create_server(('', 15533), backlog=8)
    active_client_socks = []
    client_player_names = {}

    # client data versioning
    #   the server keeps track of which clients have outdated data by swaping them between "fresh/outdated" lists
    #   clients will be sent s_game_event packets with refreshed data on the next available tick

    lobby_fresh_clients = []
    lobby_outdated_clients = []

    def invalidate_lobby():
        lobby_outdated_clients.extend(lobby_fresh_clients)
        lobby_fresh_clients.clear()

    game_state_fresh_clients = []
    game_state_outdated_clients = []

    def invalidate_game_state():
        game_state_outdated_clients.extend(game_state_fresh_clients)
        game_state_fresh_clients.clear()

    t_perf = 0
    perf_tps = 0
    perf_util = 0

    while True:
        t = time.time()

        # == check for new clients ==

        awaiting_socks, _, _ = select.select([server_sock], [], [], 0)
        for sock in awaiting_socks:
            c_sock, addr = sock.accept()
            init_packet = server_handle_connect(c_sock)

            if init_packet == None: # failed to init with client
                c_sock.close()
                continue

            # init client handler

            active_client_socks.append(c_sock)

            player_name = init_packet[1]
            client_player_names[c_sock] = player_name

            server_state.lobby[player_name] = ["it", random.randint(1, 5)]
            invalidate_lobby()

            lobby_fresh_clients.append(c_sock)
            game_state_fresh_clients.append(c_sock)

            if init_packet[3]:
                server_state.host_players.add(player_name)

            send_packet(c_sock, ("s_init_success", server_state.lobby, server_state.game_state, player_name in server_state.host_players))

            print(f"server: client {player_name} connected!")

        # == check for client packets ==

        client_packets = []

        # FIXME: this while true needs proper rewrite, cause of most server freezes when under load (and server no keeping up)
        while True:
            if len(active_client_socks) == 0:
                break

            awaiting_socks, _, _ = select.select(active_client_socks, [], [], 0)

            if len(awaiting_socks) == 0: # all packets read, break to tick
                break

            if len(client_packets) > len(active_client_socks) * 256: # break when can't keep up reading new packets to avoid deadlock
                print("server: can't keep up! recieved more than 256 packets per client on avg!")
                break

            for sock in awaiting_socks:
                # read bytestream and parse a packet from sock

                try:
                    client_packets.append((read_packet(sock), sock, client_player_names[sock]))
                
                except ConnectionError: # graceful dc
                    server_handle_disconnect(client_player_names[sock])
                    invalidate_lobby()
                    client_player_names.pop(sock)
                    active_client_socks.remove(sock)
                except: # abnormal dc, print trace
                    server_handle_disconnect(client_player_names[sock])
                    invalidate_lobby()

                    print("handling of player", client_player_names[sock], "crashed!")
                    print("----------------------------------")
                    print(traceback.format_exc(), end="")
                    print("----------------------------------")

                    client_player_names.pop(sock)
                    active_client_socks.remove(sock)
            
        # == process client packets ==

        for packet, client_sock, player_name in client_packets:
            if not client_sock in active_client_socks:
                continue # ignore packets from a disconeccted client

            if packet[0] == "c_lock_acquire":
                lock = server_state.remote_locks.get(packet[1])

                if lock == None:
                    # create new lock

                    lock = threading.Lock()
                    server_state.remote_locks[packet[1]] = lock

                did_acquire = lock.acquire(False)

                send_packet(client_sock, ("s_lock_response", did_acquire))
                    
            elif packet[0] == "c_lock_release":
                server_state.remote_locks[packet[1]].release()

            # player packets

            elif packet[0] == "c_player_info":
                server_state.player_info[player_name] = [packet[1], packet[2]]

            # host packets

            elif packet[0] == "c_host_game_start":
                if not player_name in server_state.host_players:
                    continue # player is not host

                if not server_state.game_state == 0:
                    continue

                server_state.game_state = 1
                invalidate_game_state()

            elif packet[0] == "c_host_server_quit":
                if not player_name in server_state.host_players:
                    continue # player is not host

                server_state.is_shuting_down = True
                
                send_packet(client_sock, ("server_quit",))
                return

            # lobby packets

            elif packet[0] == "c_change_team":
                server_state.lobby[player_name][0] = packet[1]
                invalidate_lobby()

            elif packet[0] == "ping":
                send_packet(client_sock, ("pong",*packet))
                
            else:
                send_packet(client_sock, ("s_unexpected_packet",))

            # score packets
                
            if packet[0] == "score_ep":
                server_state.score["ep"] += packet[1]

            elif packet[0] == "score_it":
                server_state.score["it"] += packet[1]

            # land packets
                
            elif packet[0] == "land_ep":
                server_state.land["ep"].append(packet[1])

            elif packet[0] == "land_it":
                server_state.land["it"].append(packet[1])

        # == process and send game events ==

        if server_state.is_shuting_down:
            send_packets(active_client_socks, ("s_server_quit",))

        if len(server_state.host_players) == 0 and not len(active_client_socks) == 0: # always at least one person must be a "host" player
            new_host = active_client_socks[0]
            server_state.host_players.add(client_player_names[new_host])
            
            send_packet(new_host, ("s_game_event", "client_update", True))

        send_packets(lobby_outdated_clients, ("s_game_event", "lobby_update", server_state.lobby))
        lobby_fresh_clients += lobby_outdated_clients
        lobby_outdated_clients.clear()

        send_packets(game_state_outdated_clients, ("s_game_event", "game_state_change", server_state.game_state))
        lobby_fresh_clients += game_state_outdated_clients
        game_state_outdated_clients.clear()

        # == process and send game tick ==

        game_tick = ("s_game_tick", {}, {})

        for name, p in server_state.player_info.items():
            game_tick[1][name] = (p[0], p[1])

        if server_state.game_state == 1:
            # game score
            game_tick[2]["game_score_ep"] = (server_state.score["ep"] + len(server_state.land["ep"]))
            game_tick[2]["game_score_it"] = (server_state.score["it"] + len(server_state.land["ep"]))

        send_packets(active_client_socks, game_tick)

        # == server tickloop timing ==

        delta_time = time.time() - t

        # throttle io loop if server is too fast
        time.sleep(max(0, target_ticktime - delta_time))

        t_perf += 1
        perf_tps += 1 / (time.time() - t)
        perf_util += delta_time / target_ticktime

        if t_perf > 40:
            print(f"server: avg_tps: {round(perf_tps / t_perf, 2)} avg_util: {round((perf_util / t_perf) * 100, 2)}%")
            t_perf = 0
            perf_tps = 0
            perf_util = 0
            

# starts the server python thread in the backgound
def start_server():
    # load and init the server infrastructure on this thread

    global server_state
    server_state = ServerState()

    # dispatch the server on a background thread
    
    print(f"\nstarting EPIT dedicated server... (protocol version {protocol_version})\n")

    try:
        server_tickloop()
    except KeyboardInterrupt:
        exit(0)

# stops the server, game might refuse to exit if hosting and not terminating the server
def terminate_server():
    global server_state

    print("server: waiting for server to terminate...")

    server_state.is_shuting_down = True

# == netcode api ==

# not to confuse with client_state.is_host, this signals if server_process is running under this client
is_hosting: bool = False

def setup_netcode(addr, player_name: str, is_host: bool, client_hooks: tuple):
    global server_process
    global is_hosting
    is_hosting = is_host

    atexit.register(quit_netcode)
    
    if is_hosting:
        server_process = subprocess.Popen(("python", os.path.realpath(__file__)))
        time.sleep(.2) # wait for server to start
    
    print("client: connecting to server...")
    result = connect_as_client(addr, player_name, is_host, client_hooks)

    if result[0]:
        print(f"client: connected as {client_state.player_name}!")
    else:
        raise GameDisconnect(result[1])

# handles netcode clean up at exit
def quit_netcode():
    if is_hosting:
        send_packet(client_state.server_conn, ("host_server_quit",))

    disconnect_as_client()

    if is_hosting:
        # if i try to server.shutdown() everything deadlocks so..

        print("server: shuting down server...")

        server_process.terminate()

# `python netcode.py` to start a dedicated server
if __name__ == '__main__':
    atexit.register(terminate_server)
    start_server()