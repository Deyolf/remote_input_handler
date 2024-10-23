from flask import Flask, request, jsonify
from flask_cors import CORS
import pyautogui
import socket
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
import subprocess
import os

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
print(s.getsockname()[0])

ip = s.getsockname()[0]
port = 50000

s.close()

if os.path.exists("../ip.txt"):
    os.remove("../ip.txt")

with open("../ip.txt", 'w') as file:
    file.write(ip)

app = Flask(__name__)
CORS(app)

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

current_volume = float(volume.GetMasterVolumeLevelScalar())

in_debug_mode = False  # Set this based on your application's logic

# Define the path to your Node.js server
node_client_path = '../node_client/'

# Run the subprocess with the current working directory set
process = subprocess.run(
    ['node', 'server.js'],
    cwd=node_client_path,
    stdout=subprocess.DEVNULL if not in_debug_mode else None,
    stderr=subprocess.PIPE if not in_debug_mode else None
)

# Set volume to a percentage (0 to 100)
def set_volume(vol_percentage):

    global current_volume
    # Convert percentage to a scalar value (0.0 - 1.0)
    scalar_value = vol_percentage / 100.0
    
    # Set the master volume
    volume.SetMasterVolumeLevelScalar(scalar_value, None)
    print(f"Volume set to: {vol_percentage}%")
    current_volume = float(volume.GetMasterVolumeLevelScalar())


@app.route('/receive_keycap_string', methods=['POST'])
def receive_keycap_string():
    # Check if the request contains JSON data
    if request.is_json:
        data = request.get_json()
        
        # Retrieve keycap information
        string = data.get('keycap_string')
        
        if string:
            # Here, you can handle the keycap, e.g., log it or respond with a message.
            for letter in string:
                print(letter)
                pyautogui.press(letter)
            return jsonify({"message": f"Received keycap: {string}"}), 200
        else:
            return jsonify({"error": "Keycap data missing"}), 400
    else:
        return jsonify({"error": "Invalid input, expected JSON data"}), 400



# Route to accept key input
@app.route('/receive_keycap', methods=['POST'])
def receive_keycap():
    # Check if the request contains JSON data
    if request.is_json:
        data = request.get_json()
        
        # Retrieve keycap information
        keycap = data.get('keycap')
        
        if keycap:
            # Here, you can handle the keycap, e.g., log it or respond with a message.
            print(keycap)
            pyautogui.press(keycap)
            return jsonify({"message": f"Received keycap: {keycap}"})
        else:
            return jsonify({"error": "Keycap data missing"}), 400
    else:
        return jsonify({"error": "Invalid input, expected JSON data"}), 400

@app.route('/receive_keycap_hold', methods=['POST'])
def receive_keycap_hold():
    # Check if the request contains JSON data
    if request.is_json:
        data = request.get_json()
        
        # Retrieve keycap information
        keycap = data.get('keycap')
        
        if keycap:
            # Here, you can handle the keycap, e.g., log it or respond with a message.
            print(keycap)
            pyautogui.keyDown(keycap)
            return jsonify({"message": f"Received keycap: {keycap}"})
        else:
            return jsonify({"error": "Keycap data missing"}), 400
    else:
        return jsonify({"error": "Invalid input, expected JSON data"}), 400

@app.route('/receive_keycap_release', methods=['POST'])
def receive_keycap_release():
    # Check if the request contains JSON data
    if request.is_json:
        data = request.get_json()
        
        # Retrieve keycap information
        keycap = data.get('keycap')
        
        if keycap:
            # Here, you can handle the keycap, e.g., log it or respond with a message.
            print(keycap)
            pyautogui.keyUp(keycap)
            return jsonify({"message": f"Received keycap: {keycap}"})
        else:
            return jsonify({"error": "Keycap data missing"}), 400
    else:
        return jsonify({"error": "Invalid input, expected JSON data"}), 400

@app.route('/receive_volume', methods=['POST'])
def receive_volume():
    # Check if the request contains JSON data
    if request.is_json:
        data = request.get_json()
        
        # Retrieve keycap information
        volume = data.get('volume')
        
        if volume:
            # Here, you can handle the volume, e.g., log it or respond with a message.
            print(volume)
            # Set volume to 50%
            set_volume(int(volume))

            return jsonify({"message": f"Received volume: {volume}"})
        else:
            return jsonify({"error": "volume data missing"}), 400
    else:
        return jsonify({"error": "Invalid input, expected JSON data"}), 400

@app.route('/receive_mouse_move_left', methods=['POST'])
def receive_mouse_move_left():
    x,y=pyautogui.position()
    # Check if the request contains JSON data
    if request.is_json:
        data = request.get_json()
        
        # Retrieve keycap information
        movement = data.get('movement')
        
        if movement:
            print(movement)
            pyautogui.moveTo(x-movement,y)

            return jsonify({"message": f"Received left: {movement}"})
        else:
            return jsonify({"error": "movement data missing"}), 400
    else:
        return jsonify({"error": "Invalid input, expected JSON data"}), 400

@app.route('/receive_mouse_move_right', methods=['POST'])
def receive_mouse_move_right():
    x,y=pyautogui.position()
    # Check if the request contains JSON data
    if request.is_json:
        data = request.get_json()
        
        # Retrieve keycap information
        movement = data.get('movement')
        
        if movement:
            print(movement)
            pyautogui.moveTo(x+movement,y)

            return jsonify({"message": f"Received right: {movement}"})
        else:
            return jsonify({"error": "movement data missing"}), 400
    else:
        return jsonify({"error": "Invalid input, expected JSON data"}), 400

@app.route('/receive_mouse_move_up', methods=['POST'])
def receive_mouse_move_up():
    x,y=pyautogui.position()
    # Check if the request contains JSON data
    if request.is_json:
        data = request.get_json()
        
        # Retrieve keycap information
        movement = data.get('movement')
        
        if movement:
            print(movement)
            pyautogui.moveTo(x,y-movement)

            return jsonify({"message": f"Received up: {movement}"})
        else:
            return jsonify({"error": "movement data missing"}), 400
    else:
        return jsonify({"error": "Invalid input, expected JSON data"}), 400

@app.route('/receive_mouse_move_down', methods=['POST'])
def receive_mouse_move_down():
    x,y=pyautogui.position()
    # Check if the request contains JSON data
    if request.is_json:
        data = request.get_json()
        
        # Retrieve keycap information
        movement = data.get('movement')
        
        if movement:
            print(movement)
            pyautogui.moveTo(x,y+movement)

            return jsonify({"message": f"Received down: {movement}"})
        else:
            return jsonify({"error": "movement data missing"}), 400
    else:
        return jsonify({"error": "Invalid input, expected JSON data"}), 400

@app.route("/get_volume")
def get_volume():
    print("Getting volume")
    print(float(volume.GetMasterVolumeLevelScalar()))
    print(int(float(volume.GetMasterVolumeLevelScalar())*100))
    data = {
        "volume" : int(float(volume.GetMasterVolumeLevelScalar())*100)
    }
    return jsonify(data)

if __name__ == '__main__':
    app.run(host=ip, port=port)