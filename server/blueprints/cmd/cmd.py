from blueprints.threads import arduinoCommand
from blueprints.api import (
    newPlant,
    getStatus,
    getPlantsDB,
    changePrg,
    resetMaintInterval,
)
import config

# from flask import render_template
from flask import Blueprint, Flask, send_file
from flask import current_app as app
from flask import (
    jsonify,
    make_response,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

# status = getStatus()
# currentProgram = getCurrentProgram()
# programs = getPrograms()

# Blueprint Configuration
cmd_bp = Blueprint("cmd", __name__, template_folder="templates", static_folder="static")


@cmd_bp.route("/api/plant", methods=["POST", "GET"])
def plant():
    req = request.get_json()
    newPlant(req)
    plantsDB = getPlantsDB(app)
    status = getStatus()
    # return make_response("Test worked!", 200)
    # print(config.Config.ASSETS_FOLDER)
    return redirect(url_for("status_bp.status", message="OK"))


@cmd_bp.route("/api/arduinocmd", methods=["POST", "GET"])
def arduinocmd():
    req = request.get_json()
    arduinoCommand(req["command"])
    return redirect(url_for("control_bp.control", message="OK"))


@cmd_bp.route("/api/changeprogram", methods=["POST", "GET"])
def changeprogram():
    req = request.get_json()
    changePrg(req["command"])
    return redirect(url_for("control_bp.control", message="OK"))


@cmd_bp.route("/api/resetMaintInterval", methods=["POST", "GET"])
def rMaintInterval():
    req = request.get_json()
    resetMaintInterval(req["command"])
    # print(req["command"])
    return redirect(url_for("maintenance_bp.maintenance", message="OK"))


@cmd_bp.route("/api/getlog")
def getlog():
    return send_file("../" + config.Config.APPLOGFILE, as_attachment=True)
