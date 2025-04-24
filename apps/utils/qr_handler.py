import qrcode
import os
from flask import current_app

def generate_qr(license_plate):
    folder_name = "static/qrcodes"  # ✅ Match this with the template
    os.makedirs(folder_name, exist_ok=True)

    filename = f"{license_plate}.png"
    full_path = os.path.join(folder_name, filename)

    img = qrcode.make(license_plate)
    img.save(full_path)

    current_app.logger.info(f"QR generated for {license_plate}")

    print(f"QR code saved at: {full_path}")

    return filename  # ✅ Return just the file name, not the full path