from blueprints.api import getAppLog
from flask import Blueprint
from flask import current_app as app
from flask import render_template
import config
from blueprints.init import timeStarted

# Blueprint Configuration
getlog_bp = Blueprint(
    "getlog_bp", __name__, template_folder="templates", static_folder="static"
)


@logtail_bp.route("/getlog", methods=["POST", "GET"])
def getlog():
    """currentProgram page."""
    return render_template(
        "indexLogTail.html.j2",
        title="logtail",
        subtitle="Demonstration of Flask blueprints in action.",
        template="logtail-template",
        log=getAppLog(),
    )
