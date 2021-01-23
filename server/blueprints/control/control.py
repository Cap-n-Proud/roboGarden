from flask import Blueprint
from flask import current_app as app
from blueprints.api import getPlantsDB, getPrograms, getCurrentProgr
from flask import render_template

# Blueprint Configuration
control_bp = Blueprint(
    "control_bp", __name__, template_folder="templates", static_folder="static"
)


@control_bp.route("/control", methods=["POST", "GET"])
def status():
    """Control page."""
    programs = getPrograms()
    currentProgr = getCurrentProgr()
    return render_template(
        "indexControl.jinja2",
        title="Flask Blueprint Demo",
        subtitle="Demonstration of Flask blueprints in action.",
        template="control-template",
        programs=programs,
        currentProgram=getCurrentProgr,
    )
