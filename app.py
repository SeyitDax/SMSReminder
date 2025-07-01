from flask import Flask
from flask_migrate import Migrate
from flask_apscheduler import APScheduler

from config import Config
from database import db
from routes.health import health_bp
from routes.reminders import reminder_bp
from routes.schedule import schedule_bp

class ConfigScheduler:
    JOBS = []
    SCHEDULER_API_ENABLED = True    

def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config.from_object(ConfigScheduler)

    db.init_app(app)
    migrate = Migrate(app, db)

    # Initialize the APScheduler
    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.start()
    
    app.register_blueprint(health_bp)
    app.register_blueprint(reminder_bp)
    app.register_blueprint(schedule_bp)

    app.scheduler = scheduler

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=5000)


    