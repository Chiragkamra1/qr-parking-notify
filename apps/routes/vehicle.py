from flask import Blueprint, request, jsonify, current_app, render_template, redirect, url_for
from apps.database import db
from apps.models import Vehicle
from apps.utils import generate_qr, send_email
import os

vehicle_bp = Blueprint("vehicle", __name__)

@vehicle_bp.route("/register", methods=["GET", "POST"])
def register_vehicle():
    if request.method == "POST":
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form

        owner_name = data.get("owner_name")
        license_plate = data.get("license_plate")
        owner_phone = data.get("owner_phone")

        if not (owner_name and license_plate and owner_phone):
            return jsonify({"error": "Missing required fields"}), 401

        # Check for duplicate license plate
        existing_vehicle = Vehicle.query.filter_by(license_plate=license_plate).first()
        if existing_vehicle:
            return jsonify({"error": "License plate already registered"}), 402

        # Create and save new vehicle
        new_vehicle = Vehicle(
            owner_name=owner_name,
            owner_phone=owner_phone,
            owner_email=current_app.config["DEFAULT_OWNER_EMAIL"],
            license_plate=license_plate
        )
        db.session.add(new_vehicle)
        db.session.commit()

        # Generate QR Code
        qr_path = generate_qr(new_vehicle.license_plate)
        new_vehicle.qr_code = qr_path
        db.session.commit()

        # Logging registration
        current_app.logger.info(f"✅ Vehicle registered: {license_plate} | Owner: {owner_name}")

        # Send email
        try:
            send_email(
                new_vehicle.owner_email,
                "Vehicle Registered",
                f"""Your vehicle has been successfully registered.\n
                You can view your QR code at: {request.url_root}vehicle/qr/{new_vehicle.license_plate}"""
            )
            current_app.logger.info(f"📧 Email sent to: {new_vehicle.owner_email}")
        except Exception as e:
            current_app.logger.warning(f"[⚠️ Email Error] Could not send to {new_vehicle.owner_email}: {e}")

        return jsonify({
            "message": "Vehicle registered successfully!",
            "redirect_url": url_for("vehicle.display_qr", license_plate=new_vehicle.license_plate)
        }), 201

    return render_template("register.html")


@vehicle_bp.route("/vehicle/qr/<license_plate>", methods=["GET"])
def display_qr(license_plate):
    vehicle = Vehicle.query.filter_by(license_plate=license_plate).first()
    if not vehicle:
        return "Vehicle not found", 404

    qr_filename = f"{license_plate}.png"
    return render_template("qr_display.html", vehicle=vehicle, qr_filename=qr_filename)