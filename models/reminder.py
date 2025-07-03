from datetime import datetime
from database import db
from sqlalchemy import String

class Reminder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    to = db.Column(db.String(20), nullable=False)
    message = db. Column(db.String(160), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)