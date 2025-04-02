import os

class Config:
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://parking_user:parking19@localhost/parking_db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEFAULT_OWNER_EMAIL = "rahulgargp@gmail.com"

    # Email settings
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = "normaltesting1@gmail.com"
    MAIL_PASSWORD = "pkqb gyzp cxcr kspy"