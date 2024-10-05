from flask import Flask, request, jsonify
from flask_cors import CORS
import pyautogui

app = Flask(__name__)
CORS(app)

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

if __name__ == '__main__':
    app.run(host='192.168.178.89', port=50000)