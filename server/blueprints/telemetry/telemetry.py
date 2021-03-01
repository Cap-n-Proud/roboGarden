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
telemetry_bp = Blueprint(
    "telemetry_bp", __name__, template_folder="templates", static_folder="static"
)


@telemetry_bp.route("/telemetry", methods=["POST", "GET"])
def telemetry():
    """Telemetry page."""
    return render_template(
        "indexTelemetry.html.j2",
        title="Telemetry",
        subtitle="Demonstration of Flask blueprints in action.",
        template="telemetry-template",
        INFOTAG=config.Config.INFOTAG,
        TELEMETRYTAG=config.Config.TELEMETRYTAG,
        timeStarted=timeStarted,
        currentProgram=getCurrentProgr(),
    )
