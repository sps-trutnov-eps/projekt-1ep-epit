import common
import websockets

import json
import threading

# == EPIT server/client backend netcode ==

protocol_version = 2

# == client state ==

import websockets.sync.client as webclient

class ClientState:
    __slots__ = ["server_conn", "player_name"]

    def __init__(self, uri, player_name) -> None:
        self.server_conn = webclient.connect(uri)
        self.player_name = player_name

    server_conn: webclient.ClientConnection
    player_name: str

client_state: ClientState | None

# == client implementation ==

# TODO: player continuos updates (score, player world position)
# TODO: player events (eg. game ended) <- must be able to affect minigames

def sync_with_server():
    pass

def connect_as_client(uri: str, player_name: str) -> tuple[bool, str | None]:
    # setup client state and connection

    try:
        global client_state
        client_state = ClientState(uri, player_name)
    except ConnectionError:
        client_state = None
        return (False, "Server odmíta připojení.")

    # init client with the server
    try:
        init_packet = ["p_init", player_name, protocol_version]
        client_state.server_conn.send(json.dumps(init_packet))

        # await server response
        response = client_state.server_conn.recv()

        if response == "s_init_success":
            return (True, None)
        else:
            if response == "s_init_name_taken":
                return (False, "Server: Jméno hráče je už zabrané.")

            elif response == "s_init_match_running":
                return (False, "Server: Hra už byla hostujícím spuštěna.")

            elif response == "s_unexpected_packet":
                return (False, "Server: Neočekávaná kommunikace???")
            
            elif response == "s_version_mismatch":
                return (False, "Verze Hry Hráče a Serveru se liší.")

            else:
                raise ValueError("client netcode: unhandled server response type") 

    except websockets.InvalidURI:
        return (False, "Adresa URI serveru není správně formátovaná.")

    except TimeoutError:
        return (False, "Timeout při připojování k serveru.")

    except websockets.ConnectionClosed:
        return (False, "Spojení se serverem přerušeno.")

def disconnect_as_client():
    if client_state == None:
        return

    client_state.server_conn.close()

# == server state ==

import websockets.sync.server as webserver

class ServerState:
    __slots__ = ["server_thread", "server", "server_lock"]

    def __init__(self) -> None:
        # init the server infrastructure
        
        self.server_thread = threading.Thread(target=server_thread_main, args=(self,))
        self.server_lock = threading.Lock()

        # lock server until server thread boots up
        assert self.server_lock.acquire(False)

        # server will be created in the server thread

    server_thread: threading.Thread
    server_lock: threading.Lock
    
    server: webserver.WebSocketServer

server_state: ServerState

# == server implementation ==

def server_handle_disconnect(player):
    print(f"server: client {player} disconnected")

# started for every connected client to the server, handles all transport level io for that client
def server_connection_handler(websocket: webserver.ServerConnection):
    # new client connected, await clients "init" message

    try:
        message = websocket.recv()
    except:
        print("new client<->server connection failed while initing client")
        raise

    # TODO: register new player, add to lobby

    init_packet = json.loads(message)

    if not init_packet[0] == "p_init":
        websocket.send("s_unexpected_packet")
        return

    elif not init_packet[2] == protocol_version:
        websocket.send("s_version_mismatch")
        return

    else: # elif is already player with name
        websocket.send("s_init_success")
    
    player = init_packet[1]

    print(f"server: client {player} connected!")

    # start client io loop
    while True:
        try:
            # await client packet
            message = websocket.recv()
        except websockets.ConnectionClosed:
            server_handle_disconnect(player)
            return

        # TODO:
        # - player move event
        # - score change


def server_thread_main(server_state: ServerState):
    server_state.server = webserver.serve(server_connection_handler, "", 15533)
    
    # server ready, release server lock
    server_state.server_lock.release()

    server_state.server.serve_forever()

# starts the server python thread in the backgound
def start_server():
    # load and init the server infrastructure on this thread

    global server_state
    server_state = ServerState()

    # dispatch the server on a background thread
    
    server_state.server_thread.start()

# stops the server, game might refuse to exit if hosting and not terminating the server
def terminate_server():
    global server_state
    server_state.server_lock.acquire()

    server_state.server.shutdown()
    server_state.server_thread.join()

# == netcode api ==

hosting: bool = False

def setup_netcode(is_host: bool):
    global hosting
    
    if is_host:
        hosting = True
        start_server()
    
    print("client: connecting to server...")
    result = connect_as_client("ws://127.0.0.1:15533", "player #1")

    if result[0]:
        print(f"client: connected as {client_state.player_name}!")
    else:
        print(f"failed to connect: {result[1]}")
        common.game_quit()

def quit_netcode():
    disconnect_as_client()

    if hosting:
        terminate_server()