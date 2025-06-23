from flask import Flask, request, jsonify
from twilio.rest import Client
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()
import os

app = Flask(__name__)
scheduler = BackgroundScheduler()
scheduler.start()

#load Twilio credentials from environment variables
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

def send_sms(to, body):
    try:
        message = client.messages.create(
            body=body,
            from_=TWILIO_PHONE_NUMBER,
            to=to
        )
        return message.sid
    except Exception as e:
        return str(e)
    
@app.route('/schedule', methods=['POST'])
def send_sms_endpoint():
    data = request.json
    to = data.get('to')
    body = data.get('body')
    send_time_Str = data.get('send_time')

    if not all([to, body, send_time_Str]):
        return jsonify({"error": "Missing required fields"}), 400
    
    try:
        send_time_Str = datetime.fromisoformat(send_time_Str)
    except ValueError:
        return jsonify({"error": "Invalid send_Time format. Please use ISO 8601 format."}), 400
    
    if send_time_Str < datetime.now():
        return jsonify({"error": "Send time must be in the future"}), 400
    
    job = scheduler.add_job(
        send_sms, "date",
        run_date=send_time_Str, args=[to, body])
    
    return jsonify({"message": "SMS Scheduled", "job_id": job.id}), 200


if __name__ == '__main__':
    app.run(debug=True)
