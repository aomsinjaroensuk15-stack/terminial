import os # เพิ่ม import ตัวนี้ที่หัวไฟล์

# ... โค้ดส่วนอื่นๆ ของออมสิน ...

if __name__ == "__main__":
    # ดึง Port จาก Environment ของ Render ถ้าไม่มีให้ใช้ 5000
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
