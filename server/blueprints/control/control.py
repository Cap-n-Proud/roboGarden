# Import required modules
from flask import Blueprint
from flask import current_app as app
from blueprints.api import getPlantsDB, getPrograms, getCurrentProgr
from flask import render_template
import config
from blueprints.init import timeStarted
from flask_login import login_required, current_user

# Blueprint Configuration
control_bp = Blueprint(
    "control_bp", __name__, template_folder="templates", static_folder="static"
)


@control_bp.route("/control", methods=["POST", "GET"])
if config.LOGIN == "True":
    @login_required
def control():
    """Control page."""
    # Get the available programs from the API
    programs = getPrograms()
    # Get the current program from the API
    currentProgr = getCurrentProgr()

    return render_template(
        "control-index.html.j2",
        title="Control",
        subtitle="Use this to control lights, pump and other features.",
        template="control-template",
        programs=programs,
        INFOTAG=config.Config.INFOTAG,
        TELEMETRYTAG=config.Config.TELEMETRYTAG,
        timeStarted=timeStarted,
        currentProgram=getCurrentProgr(),
    )
