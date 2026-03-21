import os
import time
import random
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

# ==========================================
# 1. INITIALIZATION & CONFIGURATION
# ==========================================
app = Flask(__name__)
CORS(app) # อนุญาตให้ Acode คุยกับ Render ได้

# ตั้งค่า Logging เพื่อดูสถานะใน Render Dashboard
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ดึงรหัสลับจาก Environment Variables (ที่เราตั้งค่าใน Render)
API_KEY = os.environ.get("GOOGLE_API_KEY")
PORT = int(os.environ.get("PORT", 5000))

# ตรวจสอบว่ามี API Key ไหม
if API_KEY:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
    logger.info(">> Gemini AI Engine: READY")
else:
    logger.warning(">> Gemini AI Engine: API KEY MISSING")

# ==========================================
# 2. HELPER FUNCTIONS (ระบบเสริมความสมจริง)
# ==========================================

def get_matrix_reponse(cmd):
    """ระบบตอบโต้คำสั่งพื้นฐานแบบ Hacker"""
    responses = {
        "help": "AVAILABLE COMMANDS: [ls, whoami, clear, status, decrypt, ai --ask]",
        "ls": "drwxr-xr-x  root  root  4096  Jan 29 10:30  matrix_core\n-rw-r--r--  root  root  1024  Jan 29 10:31  secrets.txt",
        "whoami": "ID: CAPTAIN_AOMSIN\nLEVEL: SYSTEM_ARCHITECT\nSTATUS: ONLINE",
        "status": f"SERVER_LOC: SINGAPORE\nUPTIME: {random.randint(100, 999)}h\nLATENCY: {random.randint(10, 50)}ms",
        "decrypt": ">> DECRYPTING DATA... [##########] 100%\nACCESS DENIED: ENCRYPTION TOO STRONG."
    }
    return responses.get(cmd.lower())

def process_ai_request(prompt):
    """ระบบคุยกับ Google Gemini AI"""
    try:
        if not API_KEY:
            return "!! ERROR: AI_KEY_NOT_FOUND. PLEASE CHECK RENDER ENVIRONMENT."
        
        # ปรับแต่ง Prompt ให้ AI ตอบแบบ Matrix
        full_prompt = f"You are a Matrix System AI. Answer this briefly as a hacker: {prompt}"
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        logger.error(f"AI Error: {str(e)}")
        return f"!! AI_CRITICAL_FAILURE: {str(e)}"

# ==========================================
# 3. CORE API ENDPOINTS
# ==========================================

@app.route('/')
def home():
    """หน้าเช็กสถานะเวลาเปิดผ่าน Browser"""
    return jsonify({
        "status": "online",
        "system": "Matrix Terminal V.13",
        "author": "Captain Aomsin",
        "timestamp": time.time()
    })

@app.route('/execute', methods=['POST'])
def execute():
    """หัวใจหลัก: รับคำสั่งจากหน้าจอ Matrix ของออมสิน"""
    try:
        data = request.json
        if not data or 'command' not in data:
            return jsonify({"error": "No command received"}), 400

        user_command = data['command'].strip()
        logger.info(f"Executing: {user_command}")

        # --- กรณีที่ 1: คำสั่งคุยกับ AI ---
        if user_command.startswith("ai "):
            query = user_command.replace("ai ", "")
            ai_response = process_ai_request(query)
            return jsonify({"output": ai_response})

        # --- กรณีที่ 2: คำสั่งระบบทั่วไป ---
        system_output = get_matrix_reponse(user_command)
        if system_output:
            return jsonify({"output": system_output})

        # --- กรณีที่ 3: ถ้าหาคำสั่งไม่เจอ ให้ส่งให้ AI ตอบแทนอัตโนมัติ ---
        default_ai_reply = process_ai_request(user_command)
        return jsonify({"output": default_ai_reply})

    except Exception as e:
        logger.error(f"Global Error: {str(e)}")
        return jsonify({"error": "INTERNAL_SERVER_ERROR", "details": str(e)}), 500

# ==========================================
# 4. SERVER START (FOR RENDER)
# ==========================================

if __name__ == "__main__":
    # การตั้งค่าแบบนี้สำคัญมากเพื่อให้ Render รันติด 100%
    logger.info(f">> Matrix Server booting on port {PORT}...")
    app.run(host='0.0.0.0', port=PORT)

# ==========================================
# END OF CODE (Ver. 13 PRO MAX)
# ==========================================
