from flask import Blueprint, request, jsonify, current_app
import os
from werkzeug.utils import secure_filename
from apps.database import db
from apps.models import Notification, Vehicle
from apps.utils import send_email
from flask import render_template
import time


complaint_bp = Blueprint("complaint", __name__)
UPLOAD_FOLDER = os.path.join("static", "evidence")
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@complaint_bp.route("/form", methods=["GET"])
def complaint_form():
    license_plate = request.args.get("plate")
    if not license_plate:
        return "License plate missing", 405
    return render_template("complaint.html", license_plate=license_plate)

@complaint_bp.route("/", methods=["POST"])  # Just "/" here
def submit_complaint():
    license_plate = request.form.get("license_plate")
    sender_phone = request.form.get("sender_phone")
    location = request.form.get("location")
    photo = request.files.get("photo")

    if not (license_plate and sender_phone and location):
        return jsonify({"error": "Missing required fields"}), 406

    vehicle = Vehicle.query.filter_by(license_plate=license_plate).first()
    if not vehicle:
        return jsonify({"error": "Vehicle not found"}), 407

    photo_filename = None
    if photo and allowed_file(photo.filename):
        filename = secure_filename(photo.filename)
        unique_filename = f"{int(time.time())}_{filename}"
        photo_path = os.path.join(UPLOAD_FOLDER, unique_filename)
        photo.save(photo_path)
        photo_filename = unique_filename

    complaint = Notification(
        vehicle_id=vehicle.id,
        sender_phone=sender_phone,
        location=location,
        photo_filename=photo_filename
    )
    db.session.add(complaint)
    db.session.commit()

    # Send email to vehicle owner (Person1)
    try:
        email_subject = "Parking Issue Alert – Action Needed"
        host_url = request.host_url.rstrip("/")
        image_url = f"{host_url}/static/evidence/{photo_filename}" if photo_filename else "No photo attached"

        email_body = f"""
        Dear {vehicle.owner_name},

        Someone has reported a parking issue involving your vehicle (License Plate: {license_plate}).

        📍 Location: {location}
        🆔 Complaint ID: {complaint.id}
        🖼️ Evidence: {image_url}

        Please check and take necessary action. Your personal contact details have not been shared.

        – QR Parking Notify System
        """

        send_email(
            vehicle.owner_email,
            email_subject,
            email_body
        )
        current_app.logger.info(f"Email sent to: {vehicle.owner_email}")

    except Exception as e:
        current_app.logger.error(f"Failed to send email: {str(e)}")

    # ✅ Instead of returning jsonify, return success page with complaint ID
    return render_template("success.html", complaint_id=complaint.id)

@complaint_bp.route("/acknowledge/<int:complaint_id>", methods=["POST"])
def acknowledge_complaint(complaint_id):
    complaint = Notification.query.get(complaint_id)
    if not complaint:
        return jsonify({"error": "Complaint not found"}), 404

    if complaint.acknowledged:
        return jsonify({"message": "Complaint already acknowledged"}), 200

    complaint.acknowledged = True
    db.session.commit()

    return jsonify({"message": "Complaint acknowledged successfully"}), 200

@complaint_bp.route("/<int:complaint_id>", methods=["GET"])
def get_complaint(complaint_id):
    complaint = Notification.query.get(complaint_id)
    if not complaint:
        return jsonify({"error": "Complaint not found"}), 408

    vehicle = Vehicle.query.get(complaint.vehicle_id)

    photo_url = f"{request.host_url.rstrip('/')}/static/evidence/{complaint.photo_filename}" if complaint.photo_filename else None

    return jsonify({
        "complaint_id": complaint.id,
        "license_plate": vehicle.license_plate,
        "location": complaint.location,
        "acknowledged": complaint.acknowledged,
        "photo_url": photo_url
    }), 200

@complaint_bp.route("/license/<license_plate>", methods=["GET"])
def get_complaints_by_license(license_plate):
    vehicle = Vehicle.query.filter_by(license_plate=license_plate).first()
    if not vehicle:
        return jsonify({"error": "Vehicle not found"}), 409

    complaints = Notification.query.filter_by(vehicle_id=vehicle.id).all()

    results = []
    host_url = request.host_url.rstrip("/")

    for c in complaints:
        photo_url = f"{host_url}/static/evidence/{c.photo_filename}" if c.photo_filename else None
        results.append({
            "complaint_id": c.id,
            "location": c.location,
            "acknowledged": c.acknowledged,
            "photo_url": photo_url
        })

    return jsonify({
        "license_plate": vehicle.license_plate,
        "complaints": results
    }), 200

@complaint_bp.route("/unacknowledged", methods=["GET"])
def get_unacknowledged_complaints():
    complaints = Notification.query.filter_by(acknowledged=False).all()

    results = []
    host_url = request.host_url.rstrip("/")

    for c in complaints:
        vehicle = Vehicle.query.get(c.vehicle_id)
        photo_url = f"{host_url}/static/evidence/{c.photo_filename}" if c.photo_filename else None

        results.append({
            "complaint_id": c.id,
            "license_plate": vehicle.license_plate if vehicle else None,
            "owner_name": vehicle.owner_name if vehicle else None,
            "location": c.location,
            "photo_url": photo_url
        })

    return jsonify({"unacknowledged_complaints": results}), 200

@complaint_bp.route("/success", methods=["GET"])
def success_page():
    return render_template("success.html")