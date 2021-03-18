from blueprints.api import getAppLog
from flask import Blueprint
from flask import current_app as app
from flask import render_template
import config
from blueprints.init import timeStarted
from flask_login import login_required, current_user

# Blueprint Configuration
logtail_bp = Blueprint(
    "logtail_bp", __name__, template_folder="templates", static_folder="static"
)


@logtail_bp.route("/getlog", methods=["POST", "GET"])
# @log  in_required
def getapplog():
    """currentProgram page."""
    return render_template(
        "logTail-index.j2.html",
        title="logtail",
        subtitle="Demonstration of Flask blueprints in action.",
        template="logtail-template",
        log=getAppLog(),
    )
