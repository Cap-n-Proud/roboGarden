from blueprints.api import getCurrentProgr
from flask import Blueprint
from flask import current_app as app
from flask import render_template
import config

# status = getStatus()
# currentProgram = getCurrentProgram()
# programs = getPrograms()

# Blueprint Configuration
currentProgram_bp = Blueprint(
    "currentProgram_bp", __name__, template_folder="templates", static_folder="static"
)


@currentProgram_bp.route("/currentProgram", methods=["POST", "GET"])
def currentProgram():
    """currentProgram page."""
    return render_template(
        "indexCurrentProgram.jinja2",
        title="currentProgram",
        subtitle="Demonstration of Flask blueprints in action.",
        template="currentProgram-template",
        currentProgram=getCurrentProgr(),
    )
