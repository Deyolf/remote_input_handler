from flask import Flask, request, jsonify
from flask_cors import CORS
import pyautogui
import socket
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from subprocess import Popen
import os
import time
from multiprocessing import Process, Event

# Get the IP address
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
ip = s.getsockname()[0]
s.close()
print(ip)

port = 50000

# Write IP to a file
if os.path.exists("../ip.txt"):
    os.remove("../ip.txt")

with open("../ip.txt", 'w') as file:
    file.write(ip)

# Initialize Flask app
app = Flask(__name__)
CORS(app, supports_credentials=True, resources={
    r"/*": {
        "origins": ["*"],
        "methods": ["GET", "POST", "OPTIONS", "DELETE", "PUT"],
        "allow_headers": ["Content-Type", "Authorization", "X-Requested-With"],
        "expose_headers": ["Content-Length", "X-Kuma-Revision"],
        "supports_credentials": True
    }
})

# Handle OPTIONS requests globally
@app.before_request
def handle_options_request():
    if request.method == "OPTIONS":
        response = app.make_response("")
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS, DELETE, PUT"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization, X-Requested-With"
        return response

# Audio setup
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
current_volume = float(volume.GetMasterVolumeLevelScalar())

# Define the path to your Node.js server
node_client_path = '../node_client/server.js'

# Function to start the Node.js server as a subprocess
def run_node_server(stop_event):
    process = Popen(['node', node_client_path])
    print("Node server started with PID:", process.pid)

    # Wait for the stop event
    while not stop_event.is_set():
        time.sleep(1)
    
    # Terminate the Node.js server when the event is set
    print("Terminating Node server...")
    process.terminate()
    process.wait()
    print("Node server stopped.")

# Set volume to a percentage (0 to 100)
def set_volume(vol_percentage):
    global current_volume
    scalar_value = vol_percentage / 100.0
    volume.SetMasterVolumeLevelScalar(scalar_value, None)
    current_volume = float(volume.GetMasterVolumeLevelScalar())
    print(f"Volume set to: {vol_percentage}%")

# Flask routes
@app.route('/receive_keycap_string', methods=['POST'])
def receive_keycap_string():
    data = request.get_json()
    string = data.get('keycap_string')
    if string:
        for letter in string:
            print(letter)
            pyautogui.press(letter)
        return jsonify({"message": f"Received keycap: {string}"}), 200
    return jsonify({"error": "Keycap data missing"}), 400

@app.route('/receive_keycap', methods=['POST'])
def receive_keycap():
    data = request.get_json()
    keycap = data.get('keycap')
    if keycap:
        print(keycap)
        pyautogui.press(keycap)
        return jsonify({"message": f"Received keycap: {keycap}"})
    return jsonify({"error": "Keycap data missing"}), 400

@app.route('/receive_keycap_hold', methods=['POST'])
def receive_keycap_hold():
    data = request.get_json()
    keycap = data.get('keycap')
    if keycap:
        print(keycap)
        pyautogui.keyDown(keycap)
        return jsonify({"message": f"Received keycap: {keycap}"})
    return jsonify({"error": "Keycap data missing"}), 400

@app.route('/receive_keycap_release', methods=['POST'])
def receive_keycap_release():
    data = request.get_json()
    keycap = data.get('keycap')
    if keycap:
        print(keycap)
        pyautogui.keyUp(keycap)
        return jsonify({"message": f"Received keycap: {keycap}"})
    return jsonify({"error": "Keycap data missing"}), 400

@app.route('/receive_volume', methods=['POST'])
def receive_volume():
    data = request.get_json()
    volume = data.get('volume')
    if volume is not None:
        print(volume)
        set_volume(int(volume))
        return jsonify({"message": f"Received volume: {volume}"})
    return jsonify({"error": "Volume data missing"}), 400

@app.route('/receive_mouse_move', methods=['POST'])
def receive_mouse_move():
    x, y = pyautogui.position()
    data = request.get_json()
    direction = data.get('direction')
    movement = data.get('movement', 0)
    
    if direction in ['left', 'right', 'up', 'down'] and isinstance(movement, int):
        if direction == 'left':
            pyautogui.moveTo(x - movement, y)
        elif direction == 'right':
            pyautogui.moveTo(x + movement, y)
        elif direction == 'up':
            pyautogui.moveTo(x, y - movement)
        elif direction == 'down':
            pyautogui.moveTo(x, y + movement)
        return jsonify({"message": f"Moved {direction} by {movement}"}), 200

    return jsonify({"error": "Invalid direction or movement"}), 400

@app.route("/get_volume")
def get_volume():
    current_volume_percentage = int(current_volume * 100)
    data = {"volume": current_volume_percentage}
    print(f"Current volume: {current_volume_percentage}%")
    return jsonify(data)

# Shutdown hook for the Flask app
@app.route('/shutdown', methods=['POST'])
def shutdown():
    stop_event.set()
    node_process.join()
    return jsonify({"message": "Node server is stopping..."}), 200

# Entry point
if __name__ == '__main__':
    # Create an event for stopping the Node server
    stop_event = Event()
    node_process = Process(target=run_node_server, args=(stop_event,))
    node_process.start()
    print("Eseguo normalmente")

    try:
        app.run(host=ip, port=port)
    except KeyboardInterrupt:
        print("Shutting down...")
        stop_event.set()
        node_process.join()