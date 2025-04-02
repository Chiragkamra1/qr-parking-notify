import qrcode
import os
from flask_mail import Mail, Message
from flask import current_app

mail = Mail()

def generate_qr(registration_number):
    qr = qrcode.make(registration_number)
    qr_path = f"static/qrcodes/{registration_number}.png"
    os.makedirs(os.path.dirname(qr_path), exist_ok=True)
    qr.save(qr_path)
    return qr_path

def send_email(to, subject, body):
    msg = Message(subject, recipients=[to], body=body, sender="normaltesting1@gmail.com")
    mail.send(msg)