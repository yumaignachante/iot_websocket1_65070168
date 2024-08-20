import asyncio
import websockets

connected_clients = set()

async def echo(websocket: websockets.WebSocketServerProtocol, path):
    connected_clients.add(websocket)
    try:
        async for message in websocket:
            print(f"Received from client: {message}")
            for client in connected_clients:
                await client.send(message)
    finally:
        connected_clients.remove(websocket)

async def main():
    server = await websockets.serve(echo, "0.0.0.0", 8765)
    print("Server started, waiting for communication...")
    await server.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())