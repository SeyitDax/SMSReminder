from flask import Blueprint, jsonify
from models.reminder import Reminder

reminders_bp = Blueprint("reminders", __name__)

@reminders_bp.route("/reminders", methods=["GET"])
def list_reminders():
    """List all reminders."""
    reminders = Reminder.query.order_by(Reminder.created_at.desc()).all()
    return jsonify([
        {
            "id": r.id,
            "to": r.to,
            "message": r.message,
            "created_at": r.created_at.isoformat(),
        } for r in reminders
    ])