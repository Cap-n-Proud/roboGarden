from blueprints.threads import arduinoCommand, setLightRGB
from blueprints.api import (
    newPlant,
    getStatus,
    getPlantsDB,
    changePrg,
    resetMaintInterval,
    newPlantedDate,
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
from flask_login import login_required, current_user

# Blueprint Configuration
cmd_bp = Blueprint("cmd", __name__, template_folder="templates", static_folder="static")


@cmd_bp.route("/api/plant", methods=["POST", "GET"])
@login_required
def plant():
    req = request.get_json()
    newPlant(req)
    plantsDB = getPlantsDB(app)
    status = getStatus()
    return redirect(url_for("status_bp.status", message="OK"))


@cmd_bp.route("/api/arduinocmd", methods=["POST", "GET"])
@login_required
def arduinocmd():
    from threading import Timer

    req = request.get_json()
    arduinoCommand(req["command"])
    cmd = req["command"].split()
    #
    # if cmd[0] == "pumpRunFor":
    #     l = Timer(int(cmd[1]) + 1, setLightRGB, [0, 0, 255])
    #     l.start()
    return redirect(url_for("control_bp.control"))


@cmd_bp.route("/api/restartserver", methods=["POST", "GET"])
@login_required
def restartserver():
    req = request.get_json()
    command = "sudo service robogarden restart"
    c = os.system(command)
    return redirect(url_for("control_bp.control", message="Restarting server"))


@cmd_bp.route("/api/changeprogram", methods=["POST", "GET"])
@login_required
def changeprogram():
    req = request.get_json()
    changePrg(req["command"])
    return redirect(url_for("control_bp.control", message="OK"))


@cmd_bp.route("/api/resetMaintInterval", methods=["POST", "GET"])
@login_required
def rMaintInterval():
    req = request.get_json()
    resetMaintInterval(req["command"])
    # print(req["command"])
    return redirect(url_for("maintenance_bp.maintenance", message="OK"))


@cmd_bp.route("/api/newPlantedDate", methods=["POST", "GET"])
@login_required
def newPlantedD():
    req = request.get_json()
    newPlantedDate(req["command"])
    return redirect(url_for("status_bp.status", message="OK"))


@cmd_bp.route("/api/getlog")
@login_required
def getlog():
    return send_file("../" + config.Config.APPLOGFILE, as_attachment=True)


import zipfile
import os


@cmd_bp.route("/api/download_logs")
@login_required
def download_logs():
    zipf = zipfile.ZipFile("logs.zip", "w", zipfile.ZIP_DEFLATED)
    for root, dirs, files in os.walk("logs/"):
        for file in files:
            zipf.write("logs/" + file)
    zipf.close()

    return send_file(
        "../logs.zip",
        mimetype="zip",
        attachment_filename="logs.zip",
        as_attachment=True,
    )


@cmd_bp.route("/api/download_assets")
@login_required
def download_assets():
    zipf = zipfile.ZipFile("assets.zip", "w", zipfile.ZIP_DEFLATED)
    for root, dirs, files in os.walk("assets/"):
        for file in files:
            zipf.write("assets/" + file)
    zipf.close()

    return send_file(
        "../assets.zip",
        mimetype="zip",
        attachment_filename="assets.zip",
        as_attachment=True,
    )
