import os
import subprocess
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/terminal', methods=['POST'])
def terminal():
    try:
        data = request.json
        cmd = data.get('command', '')
        # รันคำสั่งจริง
        output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, timeout=5)
        return jsonify({"result": output.decode('utf-8')})
    except Exception as e:
        error_msg = getattr(e, 'output', str(e))
        if isinstance(error_msg, bytes): error_msg = error_msg.decode('utf-8')
        return jsonify({"result": f"Error: {error_msg}"}), 400

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
