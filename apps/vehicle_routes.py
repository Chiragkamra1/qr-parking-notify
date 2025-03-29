import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from flask import Blueprint, request, jsonify
from apps.database import db
from apps.models import Vehicle
import qrcode
import io
import base64
from apps import db
from apps.models import Vehicle
from flask_mail import Message
from apps import mail

vehicle_bp = Blueprint("vehicle", __name__)

@vehicle_bp.route("/register", methods=["POST"])
def register_vehicle():
    data = request.json
    print("Received data:", data)  # Debugging output
    
    # Ensure all required fields are present
    if "license_plate" not in data or "owner_phone" not in data or "owner_name" not in data:
        return jsonify({"error": "Missing required fields"}), 400
    
     # Use test email for now
    owner_email = data.get("owner_email", "rahulgargp@gmail.com")  # Default for testing

    new_vehicle = Vehicle(
        license_plate=data["license_plate"], 
        owner_name=data["owner_name"],  
        owner_phone=data["owner_phone"],
        owner_email=owner_email  #  Add this field
    )
    
    db.session.add(new_vehicle)
    db.session.commit()

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



@vehicle_bp.route("/generate_qr/<license_plate>")
def generate_qr(license_plate):
    vehicle = Vehicle.query.filter_by(license_plate=license_plate).first()
    if not vehicle:
        return jsonify({"error": "Vehicle not found"}), 404

    # Generate QR code
    qr_data = f"https://your-website.com/notify/{license_plate}"
    qr = qrcode.make(qr_data)

    # Convert to Base64
    buffered = io.BytesIO()
    qr.save(buffered, format="PNG")
    qr_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

    return jsonify({"qr_code": qr_base64})
