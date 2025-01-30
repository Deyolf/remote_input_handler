import asyncio
from websockets.asyncio.server import serve
import pyautogui
import handling_ip

ip = handling_ip.ip()

async def echo(websocket):
    async for message in websocket:
        x, y = pyautogui.position()
        obj = message.split(",")
        #print(obj)
        response = "moved " + message
        websocket.send(response)
        pyautogui.moveTo(x + int(obj[0]), y + int(obj[1]))

async def main():
    async with serve(echo, ip, 8765) as server:
        await server.serve_forever()

if __name__ == "__main__":
    try:
        print("Socket in ascolto")
        asyncio.run(main())
    except KeyboardInterrupt:
        print("shutting down...")
        #stop_event.set()