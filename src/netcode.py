import atexit

import socket
import socketserver

import select
import json
import threading

# == EPIT server/client backend netcode ==

protocol_version = 5
packet_len_bytes = 2

# == client state ==

class ClientState:
    __slots__ = ["server_conn", "player_name"]

    def __init__(self, uri, player_name) -> None:
        self.server_conn = socket.create_connection(uri)

        self.player_name = player_name

    server_conn: socket.socket
    client_thread: threading.Thread

    player_name: str

client_state: ClientState | None = None

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
def client_sync() -> tuple[bool, str | None]:
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

    for packet in packets:
        if packet[0] == "s_game_tick":
            pass
        elif packet[0] == "s_game_event":
            pass # game start
        elif packet[0] == "pong":
            print(packet)

    # handle/queue game state changes

    send_packet(client_state.server_conn, ("ping",threading.current_thread().getName()))
    
    return (True, None)

def connect_as_client(uri: tuple, player_name: str) -> tuple[bool, str | None]:
    # setup client state and connection

    try:
        global client_state
        client_state = ClientState(uri, player_name)
    except ConnectionError:
        client_state = None
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
    if client_state == None:
        return

    client_state.server_conn.close()

# == server state ==

class ServerState:
    __slots__ = ["server_thread", "server", "lobby"]

    def __init__(self) -> None:
        # init the server infrastructure
        
        self.server = socketserver.ThreadingTCPServer(('', 15533), ServerClientConnectionHandler)
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.server_thread.daemon = True

        # the server should be under a lock but i don't care for a 5 milisecond race condition
        # assert self.server_lock.acquire(False)

        self.lobby = []

    # TODO: replace with dedicated-server subprocess
    server_thread: threading.Thread
    server: socketserver.ThreadingTCPServer
    
    lobby: list

server_state: ServerState

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
                # await client packet
                packet = read_packet(self.request)

                # process client packet

                if packet[0] == "ping":
                    print(packet)
                    send_packet(self.request, ("pong",*packet))

            except ConnectionError:
                server_handle_disconnect(player)
                return

            # TODO:
            # - player move event
            # - score change

# starts the server python thread in the backgound
def start_server():
    # load and init the server infrastructure on this thread

    global server_state
    server_state = ServerState()

    # dispatch the server on a background thread
    
    print(f"\nstarting EPIT dedicated server... (protocol version {protocol_version})\n")

    server_state.server_thread.start()

# stops the server, game might refuse to exit if hosting and not terminating the server
def terminate_server():
    global server_state

    print("server: waiting for server to terminate...")

    server_state.server.shutdown()
    server_state.server_thread.join()

# == netcode api ==

hosting: bool = False

def setup_netcode(addr, player_name: str, is_host: bool = False):
    global hosting
    
    if is_host:
        hosting = True
        start_server()
    
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
    disconnect_as_client()

    if hosting:
        terminate_server()

# `python netcode.py` to start a dedicated server
if __name__ == '__main__':
    hosting = True
    start_server()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        exit(0)