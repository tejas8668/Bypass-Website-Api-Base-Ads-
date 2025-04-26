from flask import Flask, render_template, request, jsonify, session
import os
import requests
import threading
from auth import auth, login_required, token_required

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Register blueprint
app.register_blueprint(auth)

# List of API endpoints (serial order maintained)
api_endpoints = [
    "https://bypass-api-1.onrender.com/api/decode_url?url={}",
    "https://perfect-bria-tej-fded6488.koyeb.app/api/decode_url?url={}",
    "https://bypass-api-3.vercel.app/api/decode_url?url={}",
]

# Counter for round-robin
api_counter = 0
api_counter_lock = threading.Lock()

@app.route('/')
@login_required
def home():
    return render_template('index.html')

@app.route('/71bb2d29716a1d6c9e4d.txt')
def hilltopads_txt_verification():
    return app.send_static_file('71bb2d29716a1d6c9e4d.txt')

@app.route('/supported')
def supported():
    return render_template('supported.html')

@app.route('/check_url', methods=['POST'])
@login_required
@token_required
def check_url():
    global api_counter

    url = request.json.get('url', '').strip()
    if not url:
        return jsonify({'result': 'No URL provided.'})

    # Select API serially
    with api_counter_lock:
        selected_api = api_endpoints[api_counter % len(api_endpoints)]
        api_counter += 1

    api_url = selected_api.format(url)

    try:
        response = requests.get(api_url, timeout=60)
        data = response.json()

        if not data:
            result = "Request Timeout, NO Data Found, Try Again"
        elif "final_url" in data:
            result = data["final_url"]
        else:
            result = json.dumps(data, indent=2)

    except Exception as e:
        print(f"API request error: {e}")
        result = "Failed to connect to decoding server."

    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(debug=True)
