from blueprints.api import getMaintSchedule, getStatus
from flask import Blueprint
from flask import current_app as app
from flask import render_template
import config
from flask_login import login_required, current_user

# status = getStatus()
# currentProgram = getCurrentProgram()
# programs = getPrograms()

# Blueprint Configuration
maintenance_bp = Blueprint(
    "maintenance_bp", __name__, template_folder="templates", static_folder="static"
)


@maintenance_bp.route("/maintenance", methods=["POST", "GET"])
# @login_required
def maintenance():
    """Maintenance page."""
    return render_template(
        "maintenance-index.j2.html",
        title="Maintenance",
        subtitle="Demonstration of Flask blueprints in action.",
        template="maintenance-template",
        status=getStatus(),
        maintSchedule=getMaintSchedule(),
    )
