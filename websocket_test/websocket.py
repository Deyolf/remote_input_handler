from websockets.sync.server import serve
import pyautogui

def echo(websocket):
    for message in websocket:
        x, y = pyautogui.position()
        obj = message.split(",")
        print(obj)
        response = "moved "+message
        websocket.send(response)
        pyautogui.moveTo(x + int(obj[0]), y+int(obj[1]))

def main():
    with serve(echo, "localhost", 8765) as server:
        server.serve_forever()

if __name__ == "__main__":
    try:
        print("Socket in ascolto")
        main()
    except KeyboardInterrupt:
        print("shutting down...")
        stop_event.set()