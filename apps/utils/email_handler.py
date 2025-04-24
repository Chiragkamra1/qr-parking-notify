# from flask_mail import Mail, Message
# from flask import current_app

# mail = Mail()

# def send_email(to_email, subject, body):
#     try:
#         print("MAIL CONFIG DEBUG:")
#         print("MAIL_SERVER:", current_app.config.get("MAIL_SERVER"))
#         print("MAIL_PORT:", current_app.config.get("MAIL_PORT"))
#         print("MAIL_USERNAME:", current_app.config.get("MAIL_USERNAME"))
#         print("MAIL_PASSWORD:", current_app.config.get("MAIL_PASSWORD"))

#         msg = Message(
#             subject=subject,
#             sender=current_app.config.get("MAIL_USERNAME"),
#             recipients=[to_email]
#         )
#         msg.body = body
#         mail.send(msg)

#         print("[Email Sent] Successfully sent to:", to_email)

#     except Exception as e:
#         print("[Email Error]", str(e))