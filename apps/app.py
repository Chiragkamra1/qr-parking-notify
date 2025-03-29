import os
import sys
import qrcode
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail, Message
from apps.models import db, Vehicle  # Import database models

# Adjusting the system path to locate project modules
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(current_dir, "apps"))
sys.path.insert(0, os.path.abspath(os.path.join(current_dir, "..")))

app = Flask(__name__)

# Configure MySQL Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://parking_user:parking19@localhost/parking_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database and migrations
db.init_app(app)
migrate = Migrate(app, db)

# Configure Email (SMTP)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'normaltesting1@gmail.com'  # Replace with your email
app.config['MAIL_PASSWORD'] = 'pkqb gyzp cxcr kspy'  # Replace with App Password

mail = Mail(app)
mail.init_app(app)

# Function to generate and save QR code
def generate_qr_code(license_plate):
    """Generates a QR code for the given license plate."""
    qr = qrcode.make(license_plate)
    qr_path = f"static/qrcodes/{license_plate}.png"
    os.makedirs(os.path.dirname(qr_path), exist_ok=True)  # Ensure directory exists
    qr.save(qr_path)
    return qr_path

# @app.route("/test_email")
# def test_email():
#     msg = Message("Test Email", sender="normaltesting1@gmail.com", recipients=["rahulgargp@gmail.com"])
#     msg.body = "This is a test email from Flask."
#     mail.send(msg)
#     return "Test email sent!"

# Vehicle Registration Endpoint
@app.route('/register', methods=['POST'])
def register_vehicle():
    data = request.json
    print("Received data:", data)  # Debugging output
    
    # Ensure all required fields are present
    if "license_plate" not in data or "owner_phone" not in data or "owner_name" not in data:
        print("❌ Missing required fields")
        return jsonify({"error": "Missing required fields"}), 400

    # Use test email for now
    owner_email = data.get("owner_email", "rahulgargp@gmail.com")  # Default for testing
    print(f"📩 Using email: {owner_email}")  # Debugging

    new_vehicle = Vehicle(
        license_plate=data["license_plate"], 
        owner_name=data["owner_name"],  
        owner_phone=data["owner_phone"],
        owner_email=owner_email  
    )
    
    db.session.add(new_vehicle)
    db.session.commit()
    print("✅ Vehicle registered in DB")  # Debugging

    # Send email notification
    msg = Message("Vehicle Registered",
                  sender="rahulgargp@gmail.com",
                  recipients=[owner_email])
    msg.body = f"Hello {data['owner_name']}, your vehicle {data['license_plate']} has been registered successfully."
    
    try:
        print("📩 Attempting to send email...")  # Debugging
        mail.send(msg)
        print("✅ Email sent successfully.")  # Debugging
    except Exception as e:
        print("❌ Error sending email:", e)  # Debugging

    return jsonify({"message": "Vehicle registered successfully!"})


# QR Code Scanning Endpoint
@app.route('/scan_qr', methods=['POST'])
def scan_qr():
    """Retrieves vehicle details when QR code is scanned."""
    data = request.json
    license_plate = data.get("license_plate")

    if not license_plate:
        return jsonify({"error": "License plate is required!"}), 400

    vehicle = Vehicle.query.filter_by(license_plate=license_plate).first()
    if not vehicle:
        return jsonify({"error": "Vehicle not found!"}), 404

    return jsonify({
        "message": "Vehicle found!",
        "owner_name": vehicle.owner_name,
        "owner_phone": vehicle.owner_phone,
        "license_plate": vehicle.license_plate
    })

# Email Notification Endpoint
@app.route('/send_email', methods=['POST'])
def send_email():
    """Sends an email notification to the vehicle owner."""
    data = request.json
    email = data.get("email")

    if not email:
        return jsonify({"error": "Email address is required!"}), 400

    subject = "Parking Notification"
    body = "Your vehicle is parked incorrectly. Please take action."

    try:
        msg = Message(subject, sender=app.config['MAIL_USERNAME'], recipients=[email])
        msg.body = body
        mail.send(msg)
        return jsonify({"message": "Email sent successfully!"})
    except Exception as e:
        return jsonify({"error": "Failed to send email", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5002)