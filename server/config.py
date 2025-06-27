import os

SQLALCHEMY_DATABASE_URI = "sqlite:////home/ubuntu/uptime-arena/server/uptime.db"
SQLALCHEMY_TRACK_MODIFICATIONS = False

EMAIL_USER = os.environ.get("EMAIL_USER")
EMAIL_PASS = os.environ.get("EMAIL_PASS")
ALERT_RECIPIENT = os.environ.get("ALERT_RECIPIENT")
