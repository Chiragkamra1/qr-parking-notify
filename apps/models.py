from flask_sqlalchemy import SQLAlchemy
from apps.database import db
from sqlalchemy.orm import relationship
import phonenumbers
import base64
from sqlalchemy import Boolean




def format_phone_number(phone):
    try:
        parsed_number = phonenumbers.parse(phone, "IN")  # Change "IN" to the default country code
        if phonenumbers.is_valid_number(parsed_number):
            return phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)
    except phonenumbers.NumberParseException:
        pass
    return phone  # Return original if invalid

class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner_name = db.Column(db.String(100), nullable=False)
    owner_phone = db.Column(db.String(20), nullable=False)
    owner_email = db.Column(db.String(100), default="rahulgargp@gmail.com")  # Default email  
    license_plate = db.Column(db.String(50), unique=True, nullable=False)
    qr_code = db.Column(db.String(200))  # Nullable because it's generated later  


    notifications = relationship('Notification', backref='vehicle', cascade='all, delete-orphan')

    def __init__(self, owner_name, owner_phone, owner_email, license_plate, qr_code=None):
        self.owner_name = owner_name
        self.owner_phone = owner_phone  
        self.owner_email = owner_email
        self.license_plate = license_plate
        self.qr_code = qr_code

    def set_qr_code(self, image_path):
        with open(image_path, "rb") as img_file:
            self.qr_code = base64.b64encode(img_file.read()).decode('utf-8')

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id', ondelete='CASCADE'), nullable=False)
    sender_phone = db.Column(db.String(20), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    photo_filename = db.Column(db.String(255))  # New field to store image filename
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())
    acknowledged = db.Column(db.Boolean, default=False)

    def __init__(self, vehicle_id, sender_phone, location, photo_filename=None):
        self.vehicle_id = vehicle_id
        self.sender_phone = format_phone_number(sender_phone)
        self.location = location
        self.photo_filename = photo_filename
