from flask import Blueprint, jsonify
from models.reminder import Reminder

reminders_bp = Blueprint("reminders", __name__)

@reminders_bp.route("/reminders", methods=["GET"])
def list_reminders():
    """List all reminders."""
    reminders = Reminder.query.order_by(Reminder.send_time.desc()).all()
    return jsonify([
        {
            "id": r.id,
            "to": r.to,
            "message": r.message,
            "send_time": r.send_time.isoformat(),
        } for r in reminders
    ])