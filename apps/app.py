from flask import Flask
from apps.database import db  # Ensure this path is correct
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from apps.config import Config
from flask_mail import Mail

mail = Mail()


def create_app():
    app = Flask(__name__)
    # Config
    app.config.from_object("apps.config.Config")  # Ensure config exists
    # Initialise db
    db.init_app(app)
    mail.init_app(app)
    migrate = Migrate(app, db)


    from apps.routes.vehicle import vehicle_bp
    app.register_blueprint(vehicle_bp, url_prefix="/vehicle")

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5002)