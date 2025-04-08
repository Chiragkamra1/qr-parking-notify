from flask import Blueprint, request, jsonify, current_app
import os
from werkzeug.utils import secure_filename
from apps.database import db
from apps.models import Notification, Vehicle

complaint_bp = Blueprint("complaint", __name__)
UPLOAD_FOLDER = os.path.join("apps", "static", "evidence")
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@complaint_bp.route("/", methods=["POST"])  # Just "/" here
def submit_complaint():
    license_plate = request.form.get("license_plate")
    sender_phone = request.form.get("sender_phone")
    location = request.form.get("location")
    photo = request.files.get("photo")

    if not (license_plate and sender_phone and location):
        return jsonify({"error": "Missing required fields"}), 400

    vehicle = Vehicle.query.filter_by(license_plate=license_plate).first()
    if not vehicle:
        return jsonify({"error": "Vehicle not found"}), 404

    photo_filename = None
    if photo and allowed_file(photo.filename):
        filename = secure_filename(photo.filename)
        photo_path = os.path.join(UPLOAD_FOLDER, filename)
        photo.save(photo_path)
        photo_filename = filename

    complaint = Notification(
        vehicle_id=vehicle.id,
        sender_phone=sender_phone,
        location=location,
        photo_filename=photo_filename
    )
    db.session.add(complaint)
    db.session.commit()

    return jsonify({"message": "Complaint submitted successfully"}), 201