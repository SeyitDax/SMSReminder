# SMS Scheduler Bot

A Flask-based SMS Scheduler Bot that allows you to schedule SMS reminders via a web interface, API requests, or integration with chatbots and other applications. Built with Twilio for SMS delivery, Flask for the backend, and SQLite for storage, this tool is ideal for automating reminders and notifications.

---

## Features

- **Schedule SMS Reminders:** Set up SMS reminders for any future date and time.
- **RESTful API:** Easily integrate with chatbots, Postman, or any application via HTTP requests.
- **Web UI:** User-friendly web interface for manual scheduling and management.
- **Automatic Cleanup:** Old reminders are periodically deleted to keep your database clean.
- **Health Check Endpoint:** For monitoring and uptime checks.

---

## Demo

- **Web UI:** Visit `http://localhost:5000/` after running the app.
- **API:** Use `/api/reminders` endpoints for programmatic access.

---

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/SeyitDax/SMSReminder
   cd SMS_Reminder
   ```

2. **Create and activate a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**

   Create a `.env` file in the project root with your Twilio credentials:
   ```
   TWILIO_ACCOUNT_SID=your_account_sid
   TWILIO_AUTH_TOKEN=your_auth_token
   TWILIO_PHONE_NUMBER=your_twilio_number
   ```

5. **Initialize the database:**
   ```bash
   flask db upgrade
   ```

6. **Run the application:**
   ```bash
   python app.py
   ```
   The app will be available at `http://localhost:5000/`.

---

## Configuration

All configuration is handled via the `config.py` file and environment variables. The most important are:

- `TWILIO_ACCOUNT_SID`
- `TWILIO_AUTH_TOKEN`
- `TWILIO_PHONE_NUMBER`
- `SQLALCHEMY_DATABASE_URI` (default: SQLite)

---

## Usage

### Web Interface

- Go to `http://localhost:5000/`
- Fill in the phone number, message, and scheduled time (ISO format, e.g., `2025-07-01T15:00:00`)
- Click "Schedule Reminder"
- Use the "Clear Past Reminders" button to delete reminders scheduled for times in the past

### API Endpoints

#### Create a Reminder

- **POST** `/api/reminders`
- **Body:**
  ```json
  {
    "to": "+1234567890",
    "message": "Your reminder message",
    "created_at": "2025-07-01T15:00:00"
  }
  ```
- **Response:**
  ```json
  { "message": "Reminder scheduled", "reminder_id": 1 }
  ```

#### List All Reminders

- **GET** `/api/reminders`
- **Response:** List of reminders

#### Get a Specific Reminder

- **GET** `/api/reminders/<reminder_id>`

#### Delete a Reminder

- **DELETE** `/api/reminders/<reminder_id>`

#### Delete All Past Reminders

- **DELETE** `/api/reminders/past`
- **Response:** `{ "message": "X past reminders deleted." }`

#### Health Check

- **GET** `/health`
- **Response:** `{ "status": "ok" }`

---

## Model

The `Reminder` model has the following fields:

- `id`: Integer, primary key
- `to`: String, recipient phone number
- `message`: String, SMS content (max 160 chars)
- `created_at`: DateTime, when the SMS should be sent

---

## Database & Migrations

- Uses SQLite by default (`instance/sms_scheduler.db`)
- Migrations handled by Flask-Migrate (Alembic)
- To create or upgrade the database:
  ```bash
  flask db upgrade
  ```

---

## Integrating with Chatbots or Other Apps

- Use the API endpoints to schedule reminders from your chatbot or any application.
- Example (Python, using `requests`):
  ```python
  import requests
  requests.post("http://localhost:5000/api/reminders", json={
      "to": "+1234567890",
      "message": "Hello from my bot!",
      "created_at": "2025-07-01T15:00:00"
  })
  ```

---

## Dependencies

- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- Flask-APScheduler
- Twilio
- python-dotenv
- (See `requirements.txt` for full list)

---

## Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

---

## License

[MIT](LICENSE)

---

## Acknowledgements

- [Twilio](https://www.twilio.com/) for SMS delivery
- [Flask](https://flask.palletsprojects.com/) for the web framework

---