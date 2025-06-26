from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    site = db.relationship('Site', backref='user', lazy=True)

class Site(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255), nullable=False)
    is_up = db.Column(db.Boolean, default=True)
    last_checked = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    last_alert_time = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    statuses = db.relationship('Status', backref='site', lazy=True)

    __table_args__ = (db.UniqueConstraint('user_id', 'url', name='unique_user_url'),)

class Status(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    is_up = db.Column(db.Boolean, nullable=False)
    response_time_ms = db.Column(db.Integer, nullable=True)
    site_id = db.Column(db.Integer, db.ForeignKey('site.id'), nullable=False)
