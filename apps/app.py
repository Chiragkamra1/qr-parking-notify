# app.py

from flask import Flask
from flask_migrate import Migrate
from flask_mail import Mail
from apps.database import db
from apps.config import Config
import logging
from apps.utils import generate_qr, send_email

mail = Mail()

def create_app():
    app = Flask(__name__)

    # Set up minimal logging
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('[%(levelname)s] %(message)s')
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)
    
    # Load config
    app.config.from_object(Config)
    app.config["MAX_CONTENT_LENGTH"] = 2 * 1024 * 1024  # 2 MB

    # Initialize extensions
    db.init_app(app)
    mail.init_app(app)  # ✅ initialize mail properly
    Migrate(app, db)

    # Register Blueprints
    from apps.routes.vehicle import vehicle_bp
    app.register_blueprint(vehicle_bp, url_prefix="/vehicle")

    from apps.routes.complaint import complaint_bp
    app.register_blueprint(complaint_bp, url_prefix="/complaint")

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5002)