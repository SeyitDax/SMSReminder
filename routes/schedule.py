from flask import Blueprint, request, jsonify, current_app
from datetime import datetime
from twilio.rest import Client
from database import db
from models.reminder import Reminder
from routes.tasks import delete_past_reminders

schedule_bp = Blueprint("schedule", __name__)

def send_sms(app, reminder_id):
    with app.app_context():
        reminder = Reminder.query.get(reminder_id)
        if not reminder:
            print(f"Reminder with ID {reminder_id} not found.")
            return

        client = Client(
            current_app.config["TWILIO_ACCOUNT_SID"],
            current_app.config["TWILIO_AUTH_TOKEN"]
        )

        client.messages.create(
            to=reminder.to,
            from_=current_app.config["TWILIO_PHONE_NUMBER"],
            body=reminder.message
        )

def clear_old_reminders_job():
    with current_app.app_context():
        delete_past_reminders()

@schedule_bp.route("/schedule", methods=["POST"])
def schedule_sms():
    data = request.get_json()

    # 1. Validate input
    required_fields = ["to", "message", "created_at"]
    if not data or not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        created_at = datetime.fromisoformat(data["created_at"])
    except ValueError:
        return jsonify({"error": "Invalid datetime format. Use ISO format like '2025-07-01T15:00:00'"}), 400

    # 2. Create reminder in DB
    reminder = Reminder(
        to=data["to"], # type: ignore[attr-defined]
        message=data["message"], # type: ignore[attr-defined]
        created_at=created_at # type: ignore[attr-defined]
    )
    db.session.add(reminder)
    db.session.commit()

    # 3. Schedule job
    job_id = f"sms-{reminder.id}"
    current_app.scheduler.add_job( # type: ignore[attr-defined]
        func=send_sms,
        trigger="date",
        run_date=created_at,
        args=[current_app._get_current_object(), reminder.id], # type: ignore[attr-defined]
        id=job_id,
        replace_existing=True
    )

    # 4. Return success response
    return jsonify({
        "message": "Reminder scheduled successfully.",
        "reminder_id": reminder.id
    }), 201
