from flask import Blueprint, request, jsonify
from models.reminder import Reminder
from database import db
from flask import current_app
from datetime import datetime
from routes.schedule import send_sms  # reuse existing function
from routes.tasks import delete_past_reminders

api_bp = Blueprint("api", __name__)

@api_bp.route("/api/reminders", methods=["POST"])
def create_reminder():
    data = request.get_json()
    required_fields = ["to", "message", "created_at"]
    
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        created_at = datetime.fromisoformat(data["created_at"])
    except ValueError:
        return jsonify({"error": "Invalid datetime format. Use ISO format."}), 400

    reminder = Reminder(
        to=data["to"], # type: ignore[attr-defined]
        message=data["message"], # type: ignore[attr-defined]
        created_at=created_at # type: ignore[attr-defined]
    )
    db.session.add(reminder)
    db.session.commit()

    current_app.scheduler.add_job( # type: ignore[attr-defined]
        func=send_sms,
        trigger="date",
        run_date=created_at,
        args=[current_app._get_current_object(), reminder.id], # type: ignore[attr-defined]
        id=f"reminder_{reminder.id}"
    )

    return jsonify({"message": "Reminder scheduled", "reminder_id": reminder.id})


@api_bp.route("/api/reminders", methods=["GET"])
def list_reminders():
    reminders = Reminder.query.order_by(Reminder.created_at.desc()).all()
    result = [{
        "id": r.id,
        "to": r.to,
        "message": r.message,
        "created_at": r.created_at.isoformat()
    } for r in reminders]
    return jsonify(result)


@api_bp.route("/api/reminders/<int:reminder_id>", methods=["DELETE"])
def delete_reminder(reminder_id):
    reminder = Reminder.query.get(reminder_id)
    if not reminder:
        return jsonify({"error": "Reminder not found"}), 404

    try:
        current_app.scheduler.remove_job(f"reminder_{reminder.id}") # type: ignore[attr-defined]
    except Exception:
        pass  # Job may have already run

    db.session.delete(reminder)
    db.session.commit()

    return jsonify({"message": "Reminder deleted"})


@api_bp.route("/api/reminders/<int:reminder_id>", methods=["GET"])
def get_reminder(reminder_id):
    reminder = Reminder.query.get(reminder_id)
    if not reminder:
        return jsonify({"error": "Reminder not found"}), 404

    return jsonify({
        "id": reminder.id,
        "to": reminder.to,
        "message": reminder.message,
        "created_at": reminder.created_at.isoformat()
    })

@api_bp.route("/api/reminders/past", methods=["DELETE"])
def delete_past_reminders_api():
    """Delete all past reminders."""
    num_deleted = delete_past_reminders()
    return jsonify({"message": f"{num_deleted} past reminders deleted."})
