from flask_mail import Mail, Message
from flask import current_app

mail = Mail()

def send_email(to_email, subject, body):
    msg = Message(subject, sender=current_app.config["MAIL_USERNAME"], recipients=[to_email])
    msg.body = body
    mail.send(msg)