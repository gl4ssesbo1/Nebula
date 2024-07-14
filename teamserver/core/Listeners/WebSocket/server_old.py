import asyncio
import websockets

# create handler for each connection

async def handler(websocket, path):
    print("A new connection from: {}:{}".format("",""))
    data = await websocket.recv()
    reply = f"{data}"
    

    await websocket.send(reply)

start_server = websockets.serve(handler, "localhost", 8000)

#loop = asyncio.new_event_loop()
#asyncio.set_event_loop(loop)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

