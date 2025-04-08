from flask import Flask
from flask_migrate import Migrate
from flask_mail import Mail
from apps.database import db
from apps.config import Config


mail = Mail()

def create_app():
    app = Flask(__name__)
    
    # Load config
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    mail.init_app(app)
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