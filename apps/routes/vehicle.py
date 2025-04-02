from flask import Blueprint, request, jsonify, current_app
from apps.database import db
from apps.models import Vehicle
from apps.utils import generate_qr, send_email

vehicle_bp = Blueprint("vehicle", __name__)

@vehicle_bp.route("/register", methods=["POST"])
def register_vehicle():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid request format. JSON expected"}), 400

    owner_name = data.get("owner_name")
    license_plate = data.get("license_plate")
    owner_phone = data.get("owner_phone")

    if not (owner_name and license_plate and owner_phone):
        return jsonify({"error": "Missing required fields"}), 400

    # Ensure the license plate is unique
    existing_vehicle = Vehicle.query.filter_by(license_plate=license_plate).first()
    if existing_vehicle:
        return jsonify({"error": "License plate already registered"}), 400

    # Create new vehicle
    new_vehicle = Vehicle(
        owner_name=owner_name,
        owner_phone=owner_phone,
        owner_email=current_app.config["DEFAULT_OWNER_EMAIL"],  # Default email
        license_plate=license_plate
    )
    db.session.add(new_vehicle)
    db.session.commit()

    # Generate QR Code
    qr_path = generate_qr(new_vehicle.license_plate)
    new_vehicle.qr_code = qr_path
    db.session.commit()

    # Send email
    send_email(
        new_vehicle.owner_email,  # Use correct field
        "Vehicle Registered",
        f"You vehicle has been Successfully registered /nYour QR code is ready: {qr_path}"
    )

    return jsonify({"message": "Vehicle registered successfully!", "qr_code": qr_path}), 201