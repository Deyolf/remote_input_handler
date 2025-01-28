from websockets.sync.server import serve
import pyautogui
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
ip = s.getsockname()[0]
s.close()
print(ip)

def echo(websocket):
    for message in websocket:
        x, y = pyautogui.position()
        obj = message.split(",")
        print(obj)
        response = "moved "+message
        websocket.send(response)
        pyautogui.moveTo(x + int(obj[0]), y+int(obj[1]))

def main():
    with serve(echo, ip, 8765) as server:
        server.serve_forever()

if __name__ == "__main__":
    try:
        print("Socket in ascolto")
        main()
    except KeyboardInterrupt:
        print("shutting down...")
        stop_event.set()