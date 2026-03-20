from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import os

app = Flask(__name__)
CORS(app)  # อนุญาตให้มือถือออมสินยิงคำสั่งเข้ามาได้

@app.route('/terminal', methods=['POST'])
def terminal():
    try:
        data = request.get_json()
        command = data.get('command')
        
        # รันคำสั่ง Linux ใน Cloud Shell
        result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
        return jsonify({'result': result.decode('utf-8')})
    except subprocess.CalledProcessError as e:
        return jsonify({'result': e.output.decode('utf-8')})
    except Exception as e:
        return jsonify({'result': str(e)})

if __name__ == '__main__':
    # Google Cloud Shell มักใช้ Port 8080 หรือ 5000
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
