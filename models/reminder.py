from datetime import datetime
from database import db

class Reminder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    to = db.Column(db.string(20), nullable=False)
    body = db. Column(db.String(160), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)