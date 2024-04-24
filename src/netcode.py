import common

import socket
import socketserver

import json
import threading

# == EPIT server/client backend netcode ==

protocol_version = 4

# == client state ==

# import websockets.sync.client as webclient

class ClientState:
    __slots__ = ["server_conn", "player_name"]

    def __init__(self, uri, player_name) -> None:
        self.server_conn = socket.create_connection(uri)
        self.player_name = player_name

    server_conn: socket.socket
    player_name: str

client_state: ClientState | None

# == client implementation ==

# TODO: player continuos updates (score, player world position)
# TODO: player events (eg. game ended) <- must be able to affect minigames

def sync_with_server() -> tuple[bool, str | None]:
    # accept server messages

    try:
        message = str(client_state.server_conn.recv(0), 'utf-8')

        if message == '':
            raise ConnectionError
        
    except TimeoutError:
        return (True, None) # no server packets
    except ConnectionError:
        return (False, "Stráta spojení se serverem.")

    packet = json.dumps(message)

    if packet[0] == "s_game_tick":
        pass
    elif packet[0] == "s_game_event":
        pass # game start

    return (True, None)

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
        client_state.server_conn.sendall(bytes(json.dumps(init_packet), 'utf-8'))

        # await server response
        response = str(client_state.server_conn.recv(1024), 'utf-8')

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

    #except websockets.InvalidURI:
    #    return (False, "Adresa URI serveru není správně formátovaná.")

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
        
        self.server = socketserver.ThreadingTCPServer(('127.0.0.1', 15533), ServerClientConnectionHandler)
        self.server_thread = threading.Thread(target=self.server.serve_forever)

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
            message = self.request.recv(1024)
        except:
            print("new client<->server connection failed while initing client")
            raise

        # TODO: register new player, add to lobby

        init_packet = json.loads(message)

        if not init_packet[0] == "p_init":
            print("server: refused new connection due to protocol error!")

            self.request.sendall(bytes("s_unexpected_packet", 'utf-8'))
            return

        elif not init_packet[2] == protocol_version:
            print("server: refused new connection due to version mismatch!")

            self.request.sendall(bytes("s_version_mismatch", 'utf-8'))
            return

        elif init_packet[1] in server_state.lobby:
            print("server: refused new connection due to name being taken!")

            self.request.sendall(bytes("s_init_name_taken", 'utf-8'))
            return

        else: # elif is already player with name
            self.request.sendall(bytes("s_init_success", 'utf-8'))
        
        player = init_packet[1]
        server_state.lobby.append(player)

        print(f"server: client {player} connected!")

        # start client io loop
        while True:
            try:
                # await client packet
                message = str(self.request.recv(1024), 'utf-8')

                if message == '': # 
                    raise ConnectionError

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
    # server_state.server_lock.acquire()

    print("server: waiting for server to terminate...")

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
    result = connect_as_client(("127.0.0.1", 15533), "player #1")

    if result[0]:
        print(f"client: connected as {client_state.player_name}!")
    else:
        print(f"failed to connect: {result[1]}")
        common.game_quit()

def quit_netcode():
    disconnect_as_client()

    if hosting:
        terminate_server()

# `python netcode.py` to start a dedicated server
if __name__ == '__main__':
    start_server()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        terminate_server()