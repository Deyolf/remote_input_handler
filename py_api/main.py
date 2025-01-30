from flask import Flask, request, jsonify
from flask_cors import CORS
import pyautogui
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from subprocess import Popen
import time
from multiprocessing import Process, Event
import ip_handling

# Get the IP address
ip = ip_handling.ip()
ip_handling.save_ip(ip)

port = 50000

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
    #print(f"Volume set to: {vol_percentage}%")

# Flask routes
@app.route('/receive_keycap_string', methods=['POST'])
def receive_keycap_string():
    data = request.get_json()
    string = data.get('keycap_string')
    if string:
        for letter in string:
            #print(letter)
            pyautogui.press(letter)
        return jsonify({"message": f"Received keycap: {string}"}), 200
    return jsonify({"error": "Keycap data missing"}), 400

@app.route('/receive_keycap', methods=['POST'])
def receive_keycap():
    data = request.get_json()
    keycap = data.get('keycap')
    if keycap:
        #print(keycap)
        pyautogui.press(keycap)
        return jsonify({"message": f"Received keycap: {keycap}"})
    return jsonify({"error": "Keycap data missing"}), 400

@app.route('/receive_keycap_hold', methods=['POST'])
def receive_keycap_hold():
    data = request.get_json()
    keycap = data.get('keycap')
    if keycap:
        #print(keycap)
        pyautogui.keyDown(keycap)
        return jsonify({"message": f"Received keycap: {keycap}"})
    return jsonify({"error": "Keycap data missing"}), 400

@app.route('/receive_keycap_release', methods=['POST'])
def receive_keycap_release():
    data = request.get_json()
    keycap = data.get('keycap')
    if keycap:
        #print(keycap)
        pyautogui.keyUp(keycap)
        return jsonify({"message": f"Received keycap: {keycap}"})
    return jsonify({"error": "Keycap data missing"}), 400

@app.route('/receive_volume', methods=['POST'])
def receive_volume():
    data = request.get_json()
    volume = data.get('volume')
    if volume is not None:
        #print(volume)
        set_volume(int(volume))
        return jsonify({"message": f"Received volume: {volume}"})
    return jsonify({"error": "Volume data missing"}), 400

@app.route('/receive_mouse_move', methods=['POST'])
def receive_mouse_move():
    x, y = pyautogui.position()
    data = request.get_json()
    x_movement = data.get('x_movement', 0)
    y_movement = data.get('y_movement', 0)
    
    if isinstance(x_movement, int) and isinstance(y_movement, int):
        pyautogui.moveTo(x + x_movement, y+y_movement)
        return jsonify({"message": f"Moved x:{x_movement} y:{y_movement}"}), 200

    return jsonify({"error": "Invalid direction or movement"}), 400

@app.route('/recive_mouse_click', methods=['POST'])
def recive_mouse_click():
    data = request.get_json()
    btn = data.get('btn')
    pyautogui.click(button=btn)
    return "clicked"


@app.route("/get_volume")
def get_volume():
    current_volume = float(volume.GetMasterVolumeLevelScalar())
    current_volume_percentage = int(current_volume * 100)
    data = {"volume": current_volume_percentage}
    #print(f"Current volume: {current_volume_percentage}%")
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

    # Start the Node server process
    node_process = Process(target=run_node_server, args=(stop_event,))
    node_process.start()

    # Start the websocket.py script as a subprocess
    websocket_process = Popen(['python', 'websocket.py'])
    #api_process = Popen(['python', 'api.py'])

    print("Eseguo normalmente")

    try:
        # Run the Flask app
        app.run(host=ip, port=port)
    except KeyboardInterrupt:
        print("Shutting down...")
        # Stop the Node server process
        stop_event.set()
        node_process.join()

        # Terminate the websocket.py subprocess
        websocket_process.terminate()
        #api_process.terminate()
        websocket_process.wait()
        #api_process.wait()

        print("All processes stopped.")