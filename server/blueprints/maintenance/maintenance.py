from blueprints.api import getMaintSchedule, getStatus
from flask import Blueprint
from flask import current_app as app
from flask import render_template
import config

# status = getStatus()
# currentProgram = getCurrentProgram()
# programs = getPrograms()

# Blueprint Configuration
maintenance_bp = Blueprint(
    "maintenance_bp", __name__, template_folder="templates", static_folder="static"
)


@maintenance_bp.route("/maintenance", methods=["POST", "GET"])
def maintenance():
    """Maintenance page."""
    return render_template(
        "indexMaintenance.html.j2",
        title="Maintenance",
        subtitle="Demonstration of Flask blueprints in action.",
        template="maintenance-template",
        status=getStatus(),
        maintSchedule=getMaintSchedule(),
    )