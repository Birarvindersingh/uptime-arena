import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'uptime.db')}"
SQLALCHEMY_TRACK_MODIFICATIONS = False

EMAIL_USER = os.environ.get("EMAIL_USER")
EMAIL_PASS = os.environ.get("EMAIL_PASS")
ALERT_RECIPIENT = os.environ.get("ALERT_RECIPIENT")