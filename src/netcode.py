import asyncio
import websockets

import json
import threading

# == EPIT server/client netcode ==
# EPIT works on a server/client architecture, i a match, the host is both a server (redistributor) and a (localhost) client 

def server_handle_disconnect():
    pass

async def server_client_handler(socket):
    # new client connected

    while True:
        try:
            # await client packet
            message = await socket.recv()
        except websockets.ConnectionClosedOK:
            server_handle_disconnect()

        # TODO:
        # - player move event
        # - score change



async def server_main():
    async with websockets.serve(server_client_handler, "", 42069):
        await asyncio.Future()  # run forever

def start_server():
    asyncio.run(server_main())