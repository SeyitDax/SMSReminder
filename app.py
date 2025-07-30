import os
from flask import Flask
from flask_migrate import Migrate
from flask_apscheduler import APScheduler

from config import Config
from database import db
from routes.schedule import clear_old_reminders_job
from datetime import datetime
from routes.health import health_bp
from routes.reminders import reminders_bp
from routes.schedule import schedule_bp
from routes.ui import ui_bp
from routes.api import api_bp

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
    app.register_blueprint(reminders_bp)
    app.register_blueprint(schedule_bp)
    app.register_blueprint(ui_bp)
    app.register_blueprint(api_bp)

    app.scheduler = scheduler # type: ignore[attr-defined]

    app.scheduler.add_job( # type: ignore[attr-defined]
        id="clear_old_reminders",
        func=clear_old_reminders_job,
        trigger="interval",
        days=2,
        next_run_time=datetime.utcnow()  # start immediately
    )

    return app

app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)


    