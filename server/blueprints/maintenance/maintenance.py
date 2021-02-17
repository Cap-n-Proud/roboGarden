from blueprints.api import getPlantsDB, getStatus, getCurrentProgr
from flask import Blueprint
from flask import current_app as app
from flask import render_template
import config
from blueprints.init import timeStarted

# status = getStatus()
# currentProgram = getCurrentProgram()
# programs = getPrograms()

# Blueprint Configuration
maintenance_bp = Blueprint(
    "maintenance_bp", __name__, template_folder="templates", static_folder="static"
)


@telemetry_bp.route("/maitenance", methods=["POST", "GET"])
def telemetry():
    """Maintenance page."""
    return render_template(
        "indexMaintenance.html.j2",
        title="Maintenance",
        subtitle="Demonstration of Flask blueprints in action.",
        template="maintenance-template",
    )
