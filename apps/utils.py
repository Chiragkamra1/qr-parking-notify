# utils.py

import os
import qrcode
from flask import current_app
from flask_mail import Message

# No Mail() object here!

# QR Code Utilities
def generate_qr(license_plate):
    folder_name = "static/qrcodes"
    os.makedirs(folder_name, exist_ok=True)

    filename = f"{license_plate}.png"
    full_path = os.path.join(folder_name, filename)

    img = qrcode.make(license_plate)
    img.save(full_path)

    current_app.logger.info(f"✅ QR code generated and saved at: {full_path}")

    return filename

# Email Utilities
def send_email(mail, to_email, subject, body):
    try:
        msg = Message(
            subject=subject,
            sender=current_app.config.get("MAIL_USERNAME"),
            recipients=[to_email]
        )
        msg.body = body
        mail.send(msg)

        current_app.logger.info(f"✅ Email sent successfully to {to_email}")

    except Exception as e:
        current_app.logger.error(f"❌ Email sending failed: {str(e)}")