from models.reminder import Reminder
from database import db
from flask import current_app
from datetime import datetime

def delete_past_reminders(app):
    with app.app_context():
        now = datetime.utcnow()
        past_reminders = Reminder.query.filter(Reminder.created_at < now).all()

        for r in past_reminders:
            try:
                app.scheduler.remove_job(f"reminder_{r.id}") # type: ignore[attr-defined]
            except Exception:
                pass
            db.session.delete(r)

        db.session.commit()
        return len(past_reminders)