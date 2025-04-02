import qrcode
import os

def generate_qr(vehicle_id):
    qr_data = f"http://127.0.0.1:5000/scan/{vehicle_id}"
    qr = qrcode.make(qr_data)
    
    qr_path = f"static/qrcodes/{vehicle_id}.png"
    os.makedirs("static/qrcodes", exist_ok=True)
    qr.save(qr_path)

    return qr_path