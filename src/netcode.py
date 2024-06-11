import atexit

import socket
import socketserver

import select
import json
import threading
import subprocess
import hashlib
import os

import time
from typing import Callable

# == EPIT server/client backend netcode ==

protocol_version = 13
packet_len_bytes = 2

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

    # list of teams which is a list of players which is a (p_name, p_color, p_model)
    on_lobby_info: Callable
    on_game_result: Callable

    on_player_info: Callable
    on_game_score: Callable

    # note: a random player can become a host when the current host disconnects (aka this value can change)
    is_host: bool

client_state: ClientState

# == client implementation ==

def send_packet(sock: socket.socket, obj):
    packet_data: bytes = bytes(json.dumps(obj), 'utf-8')
    packet_len: int = len(packet_data)

    sock.sendall(packet_len.to_bytes(packet_len_bytes, "big", signed=False) + packet_data)

def read_packet(sock: socket.socket) -> list:
    # read packet size header
    msg_len = sock.recv(packet_len_bytes)

    if not msg_len:
        raise ConnectionError

    # parse packet header
    msg_len = int.from_bytes(msg_len, "big", signed=False)

    message = ''
    len_read = 0

    while len_read < msg_len:
        message = sock.recv(min(msg_len, 4096))

        if not message:
            raise ConnectionError

        len_read += len(message)

    return json.loads(message) 

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
            if event_type == "game_start":
                # game started, load main map

                client_state.game_state = 1
                print("client: game start")
            
            elif event_type == "game_end":
                # game ended, load lobby and display results

                client_state.game_state = 0
                client_state.on_game_result(packet[2])
                print("client: game end")

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

def change_team(index: int):
    if not client_state.game_state == 0:
        raise ValueError("player can only change teams if in lobby, not in game!") # can be changed if we allow changing teams while in-game

    send_packet(client_state.server_conn, ("c_change_team", index))

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

            elif response[0] == "s_init_match_running":
                return (False, "Match has already started, wait for it to end.")

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
    __slots__ = ["server_thread", "server_tick_thread", "server", "lobby", "remote_locks", "player_info", "is_shuting_down", "game_state", "host_players", "score_ep", "score_it", "land_ep", "land_it"]

    def __init__(self) -> None:
        # init the server infrastructure
        
        self.server = socketserver.ThreadingTCPServer(('', 15533), ServerClientConnectionHandler)
        self.server.daemon_threads = True

        # note: tick thread is setup on host_game_start

        self.remote_locks = {}

        # the server should be under a lock but i don't care for a 5 milisecond race condition
        # assert self.server_lock.acquire(False)

        self.is_shuting_down = False

        self.lobby = {}
        self.host_players = set()

        self.player_info = {}
        self.game_state = 0
        self.score_ep = 0
        self.score_it = 0
        self.land_ep = ["T10"]
        self.land_it = ["T7"]

    # used to detect lobby changes between clients
    def hash_lobby(self) -> bytes:
        return hashlib.sha1(json.dumps(self.lobby).encode('utf-8'), usedforsecurity=False).digest()

    server: socketserver.ThreadingTCPServer

    remote_locks: dict[str, threading.Lock]
    
    # lobby data (dict indexed by player_name containing [team_index])
    lobby_players: dict[str, list[int]]
    host_players: set[str]

    # in-game data (dict indexed by player_name containing [position, velocity]
    player_info: dict[str, list]
    game_state: int
    score_ep: int
    score_it: int
    land_ep: list
    land_it: list

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

    return init_packet

class ServerClientConnectionHandler(socketserver.BaseRequestHandler):
    # started for every connected client to the server, handles all transport level io for that client
    def handle(self):
        # new client connected, await clients "init" message

        init_packet = server_handle_connect(self.request)

        if init_packet == None:
            return # failed to init with client

        # init client handler

        player_name = init_packet[1]
        server_state.lobby[player_name] = [0]
        
        client_lobby_hash = server_state.hash_lobby()
        client_game_state = server_state.game_state

        if init_packet[3]:
            server_state.host_players.add(player_name)

        send_packet(self.request, ("s_init_success", server_state.lobby, client_game_state, player_name in server_state.host_players))

        print(f"server: client {player_name} connected!")

        target_ticktime = (1 / 20) # ideal ~20 TPS target

        # client io loop
        while True:
            # update client handler

            t = time.time()

            if len(server_state.host_players) == 0: # always at least one person must be a "host" player
                server_state.host_players.add(player_name)

                # inform client that it has become host
                send_packet(self.request, ("s_game_event", "client_update", True))

            # check for received client packets
            try:
                packets = []

                while True:
                    read_sockets, _, _ = select.select((self.request,), tuple(), tuple(), 0)

                    if len(read_sockets) == 0:
                        break

                    if len(packets) > 32: # check to avoid infinitely reading client packets without processing them, backlog reached at this point, server surenders and can't keep up, things WILL get out of sync
                        print(f"server: can't keep up! over 32 packets in a single tick from client \"{player_name}\"!")
                        break

                    for sock in read_sockets:
                        # receive and parse packets from tcp stream

                        p = read_packet(sock)

                        if len(packets) > 16: # danger of packet backlog, start ignoring noisy update packets (will cause visual lags of this client for others)
                            if p[0] == "c_player_info" or p[0] == "ping":
                                continue

                        packets.append(p)

                # == process client packets ==

                for packet in packets:
                    if packet[0] == "c_lock_acquire":
                        lock = server_state.remote_locks.get(packet[1])

                        if lock == None:
                            # create new lock

                            lock = threading.Lock()
                            server_state.remote_locks[packet[1]] = lock

                        did_acquire = lock.acquire(False)

                        send_packet(self.request, ("s_lock_response", did_acquire))
                    
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

                    elif packet[0] == "c_host_server_quit":
                        if not player_name in server_state.host_players:
                            continue # player is not host

                        server_state.is_shuting_down = True
                        
                        send_packet(self.request, ("server_quit",))
                        return

                    # lobby packets

                    elif packet[0] == "c_change_team":
                        server_state.lobby[player_name][0] = packet[1]

                    elif packet[0] == "ping":
                        send_packet(self.request, ("pong",*packet))
                    
                    else:
                        send_packet(self.request, ("s_unexpected_packet",))

                    # score packets
                    
                    elif packet[0] == "score_ep":
                        server_state.score_ep = packet[1]

                    elif packet[0] == "score_it":
                        server_state.score_it = packet[1]

                    # land packets
                    
                    elif packet[0] == "land_ep":
                        server_state.land_ep = packet[1]

                    elif packet[0] == "land_it":
                        server_state.land_it = packet[1]

            except ConnectionError:
                server_handle_disconnect(player_name)
                return
            
            # == send server packets to client ==

            game_tick = ("s_game_tick", {}, {})

            # player updates (position, held item, etc.)

            for name, p in server_state.player_info.items():
                game_tick[1][name] = (p[0], p[1])
                
            if server_state.game_state == 1:
                # game score

            game_tick[2]["game_score_ep"] = (server_state.score_ep + len(server_state.land_ep))
            game_tick[2]["game_score_it"] = (server_state.score_it + len(server_state.land_it))
                game_tick[2]["game_score"] = () # TODO: Pavel, send to clients what you want
            else:
                game_tick[2]["game_score"] = None # no score updates when in lobby

            send_packet(self.request, game_tick)

            # check for changed synced data

            if server_state.is_shuting_down:
                send_packet(self.request, ("s_server_quit",))
                return

            if not client_game_state == server_state.game_state:
                client_game_state = server_state.game_state

                if client_game_state == 0: # return to lobby (game end)
                    send_packet(self.request, ("s_game_event", "game_end", None))
                elif client_game_state == 1: # switch to game (game start)
                    send_packet(self.request, ("s_game_event", "game_start"))

            lob_hash = server_state.hash_lobby()
            if not client_lobby_hash == lob_hash:
                client_lobby_hash = lob_hash

                send_packet(self.request, ("s_game_event", "lobby_update", server_state.lobby))

            delta_time = time.time() - t

            # throttle io loop if server is too fast
            time.sleep(max(0, target_ticktime - delta_time))

# starts the server python thread in the backgound
def start_server():
    # load and init the server infrastructure on this thread

    global server_state
    server_state = ServerState()

    # dispatch the server on a background thread
    
    print(f"\nstarting EPIT dedicated server... (protocol version {protocol_version})\n")

    try:
        server_state.server.serve_forever()
    except KeyboardInterrupt:
        exit(0)

# stops the server, game might refuse to exit if hosting and not terminating the server
def terminate_server():
    global server_state

    print("server: waiting for server to terminate...")

    server_state.server.shutdown()

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

    try:
        while True:
            pass
    except KeyboardInterrupt:
        pass
    
    print("exit")

    exit(0)