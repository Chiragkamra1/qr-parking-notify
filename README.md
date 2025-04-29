<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/Flask-2.3+-green.svg" alt="Flask Version">
  <img src="https://img.shields.io/badge/License-MIT-lightgrey.svg" alt="License">
</p>

# QR Parking Notify System 🚗🔔

Welcome to the QR Parking Notify System – a simple yet powerful solution to parking management and vehicle-owner notification without exposing personal contact information.

---

## 🚗 Problem Statement

Parking issues such as blocking gates, wrong parking, or obstructing driveways are common, but people hesitate to address them directly due to privacy concerns.

---

## 🔵 Challenges

- Vehicle owners are hard to contact without revealing personal numbers.
- Parking disputes escalate without easy communication.
- No way to alert a car owner anonymously and securely.

---

## 💡 Solution

The QR Parking Notify System allows anyone to:

- Scan a QR code placed on a vehicle.
- Report parking issues anonymously with location and optional photo evidence.
- Instantly notify the vehicle owner via email without exposing anyone’s private details.

Meanwhile, vehicle owners:

- Receive quick alerts.
- Can acknowledge that they are coming to move their vehicle.
- Stay anonymous — no phone number or name sharing!

---

## 🛠️ Features

| Feature              | Description                                                                 |
|----------------------|-----------------------------------------------------------------------------|
| Vehicle Registration | Owners register their vehicle and generate a QR code.                      |
| QR Code Generation   | Each registered vehicle has a unique scannable QR linked to it.            |
| Complaint Submission | Anyone can report a parking issue by scanning the QR and filling a form.   |
| Email Notification   | Owners receive an automated email with complaint details and photo evidence.|
| Acknowledge Mechanism| Owners can acknowledge complaints with a single click.                     |
| Photo Upload         | Complainants can attach a photo as proof (optional).                       |
| Admin API Routes     | Retrieve complaints, filter by plate, view unacknowledged reports, etc.    |

---

## 📷 Workflow

1. **Vehicle Owner:**
   - Registers vehicle with name, license plate, and phone number.
   - Receives a QR code to print and place on their car.

2. **Complainant:**
   - Scans the QR code → opens a complaint form.
   - Submits location, phone number, and optional photo.

3. **System:**
   - Notifies the owner via email with complaint details.
   - Owner can acknowledge if they’re coming to resolve it.

---

## 🧩 Project Structure

apps/
├── app.py             # Main Flask app
├── database.py        # Database setup (SQLAlchemy)
├── models.py          # Database models (Vehicle, Notification)
├── utils.py           # Utility functions (send_email, generate_qr)
├── routes/
│   ├── vehicle.py     # Routes related to vehicle registration
│   └── complaint.py   # Routes related to complaints
static/
├── evidence/          # Uploaded complaint photos
templates/
├── register.html      # Vehicle registration form
├── complaint.html     # Complaint submission form
├── success.html       # Success page after complaint
├── qr_display.html    # Display generated QR code
README.md
requirements.txt

---

## 🚀 How to Run Locally

### 1. Clone the Repository

```bash
git clone https://github.com/Chiragkamra1/qr-parking-notify.git
cd qr-parking-notify

2. Set Up a Virtual Environment

python -m venv venv
source venv/bin/activate      # Linux / macOS
venv\Scripts\activate         # Windows

3. Install Dependencies

pip install -r requirements.txt

4. Configure Environment Variables

Create a .env file or set these in app.py:
	•	SECRET_KEY
	•	EMAIL_SERVER (SMTP server)
	•	EMAIL_PORT
	•	EMAIL_USERNAME
	•	EMAIL_PASSWORD
	•	DEFAULT_OWNER_EMAIL

5. Initialize the Database

flask shell
>>> from apps.database import db
>>> db.create_all()
>>> exit()

6. Run the App

flask run --port=5002

The app will be available at: http://localhost:5002/

⸻

📈 Future Enhancements
	•	WhatsApp Notification Integration 📱
	•	Admin Dashboard to view all complaints
	•	OTP/Authentication for complainants
	•	Multi-language support
	•	Rate limiting on complaint submissions

⸻

🤝 Contributions

Feel free to open issues, suggest features, or contribute via pull requests.
Let’s make parking easier for everyone! 🚘

⸻

📜 License

This project is licensed under the MIT License.

⸻

Thank you for checking out QR Parking Notify System!
A small step towards making our streets more organized and communication easier.

---
