import atexit

import socket
import socketserver

import select
import json
import threading
import subprocess

# == EPIT server/client backend netcode ==

protocol_version = 7
packet_len_bytes = 2

# == client state ==

class ClientState:
    __slots__ = ["server_conn", "player_name", "remote_player_states"]

    def __init__(self, uri, player_name) -> None:
        self.server_conn = socket.create_connection(uri)

        self.player_name = player_name
        self.remote_player_states = []

    server_conn: socket.socket
    client_thread: threading.Thread

    player_name: str

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

# TODO: player continuos updates (score, player world position)
# TODO: player events (eg. game ended) <- must be able to affect minigames

# called once per client frame to sync with server
def client_sync(watch_for_lock_response: bool = False) -> tuple[bool, str | None]:
    # parse server packets (if any)

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
                return (True, None) # no server packets
            except ConnectionError:
                return (False, "Stráta spojení se serverem.")

    # process received packets

    lock_response = None

    for packet in packets:
        if packet[0] == "s_game_tick":
            # client_state.remote_player_states = packet[1]
            pass

        elif packet[0] == "s_game_event":
            event_type = packet[1]

            # lobby events
            if event_type == "game_start":
                pass
            elif event_type == "game_end":
                pass

            elif event_type == "score_update":
                pass
        
        elif packet[0] == "s_lock_response":
            if not watch_for_lock_response:
                raise ValueError("recieved lock response while not waiting for it!")
            
            else:
                lock_response = packet[1]
            
        elif packet[0] == "pong":
            print(packet)

    # handle/queue game state changes

    # send_packet(client_state.server_conn, ("ping", threading.current_thread().getName()))
    
    if not lock_response == None:
        return (lock_response, "lr")

    return (True, None)

# locks a server-side lock, returns True if locked (and the lock was free) or False if the lock was already locked
# remember to `remote_unlock` after the lock is not needed, otherwise the lock will be locked forever
# note: this def is fully synchronous and *very* slow, never do it in every frame (only loading screens and such)
def remote_try_lock(lock_name: str) -> bool:
    send_packet(client_state.server_conn, ("lock_acquire", lock_name))

    while True:
        res = client_sync(True)

        if res[1] == "lr":
            return res[0]

# unlocks the lock so other clients can lock the lock
def remote_unlock(lock_name: str):
    send_packet(client_state.server_conn, ("lock_release", lock_name))

def connect_as_client(uri: tuple, player_name: str) -> tuple[bool, str | None]:
    # setup client state and connection

    try:
        global client_state
        client_state = ClientState(uri, player_name)
    except ConnectionError:
        return (False, "Server odmíta připojení.")

    # init client with the server
    try:
        send_packet(client_state.server_conn, ("p_init", player_name, protocol_version))

        # await server response
        response = read_packet(client_state.server_conn)[0]

        if response == "s_init_success":
            return (True, None)
        else:
            if response == "s_init_name_taken":
                return (False, "Server: Jméno hráče je už zabrané.")

            elif response == "s_init_match_running":
                return (False, "Server: Hra už byla hostujícím spuštěna.")

            elif response == "s_unexpected_packet":
                return (False, "Server: Interní chyba komunikace...")
            
            elif response == "s_version_mismatch":
                return (False, "Verze Hry Hráče a Serveru se liší.")

            else:
                raise ValueError("client netcode: unhandled server response type") 

    except TimeoutError:
        return (False, "Timeout při připojování k serveru.")

    except ConnectionError:
        return (False, "Spojení se serverem přerušeno.")

def disconnect_as_client():
    try:
        client_state.server_conn.close()
    except:
        pass # don't look here

# == server state ==

class ServerState:
    __slots__ = ["server_thread", "server_tick_thread", "server", "lobby", "remote_locks", "player_info", "is_shuting_down"]

    def __init__(self) -> None:
        # init the server infrastructure
        
        self.server = socketserver.ThreadingTCPServer(('', 15533), ServerClientConnectionHandler)
        # self.server_thread = threading.Thread(target=self.server.serve_forever)
        # self.server_thread.daemon = True

        # self.server_tick_thread = threading.Thread(target=)
        # self.server_tick_thread.daemon = True

        self.remote_locks = {}

        # the server should be under a lock but i don't care for a 5 milisecond race condition
        # assert self.server_lock.acquire(False)

        self.lobby = []
        self.player_info = {}

    # TODO: replace with dedicated-server subprocess
    # server_thread: threading.Thread
    server_tick_thread: threading.Thread

    server: socketserver.ThreadingTCPServer

    remote_locks: dict[str, threading.Lock]
    
    lobby: list
    player_info: dict

server_state: ServerState
server_process: subprocess.Popen # only used when running internal server

# == server implementation ==

def server_handle_disconnect(player):
    print(f"server: client {player} disconnected")

    server_state.lobby.remove(player)

class ServerClientConnectionHandler(socketserver.BaseRequestHandler):

    # started for every connected client to the server, handles all transport level io for that client
    def handle(self):
        # new client connected, await clients "init" message

        try:
            init_packet = read_packet(self.request)
        except:
            print("server: new client<->server connection failed while initing client")
            raise

        if not init_packet[0] == "p_init":
            print("server: refused new connection due to protocol error!")

            send_packet(self.request, ("s_unexpected_packet",))
            return

        elif not init_packet[2] == protocol_version:
            print("server: refused new connection due to version mismatch!")

            send_packet(self.request, ("s_version_mismatch",))
            return

        elif init_packet[1] in server_state.lobby:
            print("server: refused new connection due to name being taken!")

            send_packet(self.request, ("s_init_name_taken",))
            return

        else: # elif is already player with name
            send_packet(self.request, ("s_init_success",))
        
        player = init_packet[1]
        server_state.lobby.append(player)

        print(f"server: client {player} connected!")

        # start client io loop
        while True:
            try:
                if server_state.is_shuting_down:
                    send_packet(self.request, ("s_server_quit",))
                    return

                # await client packet
                packet = read_packet(self.request)

                # process client packet

                if packet[0] == "lock_acquire":
                    lock = server_state.remote_locks.get(packet[1])

                    if lock == None:
                        # create new lock

                        lock = threading.Lock()
                        server_state.remote_locks[packet[1]] = lock

                    did_acquire = lock.acquire(False)

                    send_packet(self.request, ("s_lock_response", did_acquire))
                
                elif packet[0] == "lock_release":
                    server_state.remote_locks[packet[1]].release()

                elif packet[0] == "host_game_start":
                    server_state.server_tick_thread.start()

                # TODO: server quit handling

                elif packet[0] == "ping":
                    send_packet(self.request, ("pong",*packet))

            except ConnectionError:
                server_handle_disconnect(player)
                return
            
            # send server tick to client

            game_tick = ("s_game_tick", {}, {})

            # player updates (position, held item, etc.)

            for p in server_state.player_info:
                game_tick[1][p.name] = (p.pos, p.delayed_pos, p.held_item, p.health)
            
            # game score

            game_tick[2]["game_score"] = () # TODO: Pavel, send to clients what you want

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
    # server_state.server_thread.join()

# == netcode api ==

hosting: bool = False

def setup_netcode(addr, player_name: str, is_host: bool = False):
    global hosting
    global server_process
    
    if is_host:
        hosting = True

        server_process = subprocess.Popen(("python", "./src/netcode.py"))
    
    print("client: connecting to server...")
    result = connect_as_client(addr, player_name)

    if result[0]:
        print(f"client: connected as {client_state.player_name}!")
    else:
        print(f"failed to connect: {result[1]}")
        exit(-1)

# handles netcode clean up at exit
@atexit.register
def quit_netcode():
    if hosting:
        send_packet(client_state.server_conn, ("host_server_quit",))

    disconnect_as_client()

    if hosting:
        server_process.communicate()

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