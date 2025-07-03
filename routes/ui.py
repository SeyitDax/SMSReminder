from flask import render_template, Blueprint

# Create a blueprint for the UI routes

ui_bp = Blueprint("ui", __name__, template_folder="templates")

@ui_bp.route("/")
def index():
    """Render the main UI page."""
    return render_template("index.html")   
