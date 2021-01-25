from blueprints.api import getPlantsDB, getStatus
from flask import Blueprint
from flask import current_app as app
from flask import render_template
import config

# status = getStatus()
# currentProgram = getCurrentProgram()
# programs = getPrograms()

# Blueprint Configuration
status_bp = Blueprint(
    "status_bp", __name__, template_folder="templates", static_folder="static"
)


@status_bp.route("/status", methods=["POST", "GET"])
def status():
    """Status page."""
    plantsDB = getPlantsDB(app)
    status = getStatus(app)
    # print(config.Config.ASSETS_FOLDER)
    return render_template(
        "index.jinja2",
        title="Status",
        subtitle="Demonstration of Flask blueprints in action.",
        template="status-template",
        plantsDB=plantsDB,
        status=status,
        INFOTAG=config.Config.INFOTAG,
        TELEMETRYTAG=config.Config.TELEMETRYTAG,
    )
