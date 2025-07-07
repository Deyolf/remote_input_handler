from flask import Flask, send_from_directory
from flask_sock import Sock
import pyautogui
import json
import threading
import time

# 🔊 Audio handling
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL

# variabili puntamento server
host = "0.0.0.0"
port = 50050

# misc
app = Flask(__name__)
sock = Sock(app)

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

def set_volume(vol_percentage):
    scalar_value = vol_percentage / 100.0
    volume.SetMasterVolumeLevelScalar(scalar_value, None)
    return float(volume.GetMasterVolumeLevelScalar())

def current_volume():
    return float(volume.GetMasterVolumeLevelScalar())

# WebSocket clients
active_clients = []

# 🔄 Volume monitor thread
def monitor_volume():
    last_volume = int(current_volume() * 100)
    while True:
        time.sleep(0.3)
        new_volume = int(current_volume() * 100)
        if new_volume != last_volume:
            last_volume = new_volume
            for client in active_clients[:]:
                try:
                    client.send(json.dumps({"volume": new_volume}))
                except:
                    active_clients.remove(client)

# API endpoints
@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/mouse')
def mouse():
    return send_from_directory('static/mouse', 'mouse.html')

@app.route('/keyboard')
def keyboard():
    return send_from_directory('static/keyboard', 'keyboard.html')

# WebSocket endpoint
@sock.route('/ws')
def websocket(ws):
    print("🔌 WebSocket connesso")
    active_clients.append(ws)
    try:
        while True:
            message = ws.receive()
            if message is None:
                break

            try:
                data = json.loads(message)
                msg_type = data.get("type")
                action = data.get("action")

                # 🎹 KEYCAP
                if msg_type == "keycap":
                    keycap = data.get("keycap")
                    if not keycap:
                        ws.send(json.dumps({"error": "Missing keycap"}))
                        continue

                    if action == "press":
                        pyautogui.press(keycap)
                    elif action == "hold":
                        pyautogui.keyDown(keycap)
                    elif action == "release":
                        pyautogui.keyUp(keycap)
                    else:
                        ws.send(json.dumps({"error": "Invalid keycap action"}))
                        continue
                    ws.send(json.dumps({"status": f"Keycap {action}: {keycap}"}))

                # 🖱️ MOUSE
                elif msg_type == "mouse":
                    btn = data.get("btn", "left")
                    if action == "click":
                        pyautogui.click(button=btn)
                    elif action == "hold":
                        pyautogui.mouseDown(button=btn)
                    elif action == "release":
                        pyautogui.mouseUp(button=btn)
                    else:
                        ws.send(json.dumps({"error": "Invalid mouse action"}))
                        continue
                    ws.send(json.dumps({"status": f"Mouse {action} on {btn}"}))

                # 🔊 VOLUME
                elif msg_type == "volume":
                    if action == "set":
                        volume_val = data.get("volume")
                        if volume_val is not None:
                            vol = set_volume(int(volume_val))
                            ws.send(json.dumps({"status": f"Volume set to {int(vol * 100)}%"}))
                        else:
                            ws.send(json.dumps({"error": "Missing volume value"}))
                    elif action == "get":
                        current = int(current_volume() * 100)
                        ws.send(json.dumps({"volume": current}))
                    else:
                        ws.send(json.dumps({"error": "Invalid volume action"}))
                else:
                    ws.send(json.dumps({"error": "Unknown type"}))

            except Exception as e:
                ws.send(json.dumps({"error": f"Exception: {str(e)}"}))

    finally:
        if ws in active_clients:
            active_clients.remove(ws)
        print("❌ Connessione chiusa")

# 🏁 Start server and volume monitor
if __name__ == "__main__":
    threading.Thread(target=monitor_volume, daemon=True).start()
    app.run(host, port)
