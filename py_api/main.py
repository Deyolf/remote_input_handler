from flask import Flask, request, jsonify
from flask_cors import CORS
import pyautogui
from subprocess import Popen
import time
from multiprocessing import Process, Event
import handling_ip
import handling_audio
import handling_data as mngdata

# Get the IP address
ip = handling_ip.ip()
handling_ip.save_ip(ip)

port = 50000
node_path = '../node_client/server.js'
websocket_path = './websocket.py'

current_volume = 0

# Initialize Flask app

app = Flask(__name__)

cors_resurces = {
    r"/*": {
        "origins": ["*"],
        "methods": ["GET", "POST", "OPTIONS", "DELETE", "PUT"],
        "allow_headers": ["Content-Type", "Authorization", "X-Requested-With"],
        "expose_headers": ["Content-Length", "X-Kuma-Revision"],
        "supports_credentials": True
    }
}

CORS(app, supports_credentials = True, resources = cors_resurces)

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


# Define the path to your Node.js server

# Function to start the Node.js server as a subprocess
def run_node_server(stop_event):
    process = Popen(['node', node_path])
    print("Node server started with PID:", process.pid)

    # Wait for the stop event
    while not stop_event.is_set():
        time.sleep(1)
    
    # Terminate the Node.js server when the event is set
    print("Terminating Node server...")
    process.terminate()
    process.wait()
    print("Node server stopped.")

def run_websocket_server(stop_event):
    process = Popen(['python', websocket_path])
    print("Websocekt server started with PID:", process.pid)

    # Wait for the stop event
    while not stop_event.is_set():
        time.sleep(1)
    
    # Terminate the websocekt.py server when the event is set
    print("Terminating Websocekt server...")
    process.terminate()
    process.wait()
    print("Websocekt server stopped.")

# Flask routes
@app.route('/receive_keycap_string', methods=['POST'])
def receive_keycap_string():
    string = mngdata.get(request,'keycap_string')
    if string:
        for letter in string:
            #print(letter)
            pyautogui.press(letter)
        return jsonify({"message": f"Received keycap: {string}"}), 200
    return jsonify({"error": "Keycap data missing"}), 400

@app.route('/receive_keycap', methods=['POST'])
def receive_keycap():
    keycap = mngdata.get(request,'keycap')
    if keycap:
        pyautogui.press(keycap)
        return jsonify({"message": f"Received keycap: {keycap}"})
    return jsonify({"error": "Keycap data missing"}), 400

@app.route('/receive_keycap_hold', methods=['POST'])
def receive_keycap_hold():
    keycap = mngdata.get(request,'keycap')
    if keycap:
        pyautogui.keyDown(keycap)
        return jsonify({"message": f"Received keycap: {keycap}"})
    return jsonify({"error": "Keycap data missing"}), 400

@app.route('/receive_keycap_release', methods=['POST'])
def receive_keycap_release():
    keycap = mngdata.get(request,'keycap')
    if keycap:
        pyautogui.keyUp(keycap)
        return jsonify({"message": f"Received keycap: {keycap}"})
    return jsonify({"error": "Keycap data missing"}), 400

@app.route('/recive_mouse_click', methods=['POST'])
def recive_mouse_click():
    btn = mngdata.get(request,'btn')
    pyautogui.click(button=btn)
    return "clicked"

@app.route('/receive_volume', methods=['POST'])
def receive_volume():
    volume = mngdata.get(request,'volume')
    if volume is not None:
        handling_audio.set_volume(int(volume))
        return jsonify({"message": f"Received volume: {volume}"})
    return jsonify({"error": "Volume data missing"}), 400

@app.route("/get_volume")
def get_volume():
    current_volume_percentage = int(handling_audio.current_volume() * 100)
    data = {"volume": current_volume_percentage}
    return jsonify(data) 

# Entry point
if __name__ == '__main__':
   
    stop_event = Event()

    node_process = Process(target=run_node_server, args=(stop_event,))
    websocket_process = Process(target=run_websocket_server,args=(stop_event,))

    node_process.start()
    websocket_process.start()

    try:
        # Run the Flask app
        app.run(host=ip, port=port)
    except KeyboardInterrupt:
        print("Shutting down...")
        
        stop_event.set()
        node_process.join()
        node_process.join()

        print("All processes stopped.")