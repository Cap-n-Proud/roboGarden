# Collection of functions to perform task on request of blueprints main files.
# This includes also filters for templates

import json
import config
import logging

from flask_socketio import SocketIO
from flask_socketio import emit, ConnectionRefusedError, disconnect

from flask import current_app as app
from datetime import datetime

# LOG = logging.getLogger(__name__)
LOG = logging.getLogger(config.Config.APPLOGNAME)
io = SocketIO(app)  # engineio_logger=True)

# Retrieve the current program, used to populate the indey.html file


def getCurrentProgr():
    with open(config.JSON_Path.CURRENTPROGRAM) as f:
        data = json.load(f)
    return data


def getMaintSchedule():
    with open("assets/maintSchedule.json") as f:
        data = json.load(f)
    return data


def getPrograms():
    with open(config.JSON_Path.PROGRAMS) as f:
        data = json.load(f)
    return data


def getPlantsDB(app):
    with open(config.JSON_Path.PLANTDB) as f:
        data = json.load(f)
    return data


def getStatus():
    with open(config.JSON_Path.STATUS) as f:
        data = json.load(f)
    return data


def getAppLog():
    with open(config.Config.APPLOGFILE) as f:
        d = '{"records":[' + f.read()[:-2] + "]}"
        # print(d)
        data = json.loads(d)
    return data


def sendArduinoCmd(cmd):
    print(cmd)


def newPlant(r):
    from blueprints.threads import guessHarvest

    # print(config.JSON_Path.STATUS)
    with open(config.JSON_Path.STATUS, "r") as f:
        data = json.load(f)
        try:
            newPlant = r["plantName"]
            l = r["podID"].split("-")
            currentPod = data["towers"][int(l[0])]["levels"][int(l[1])]["pods"][
                int(l[2])
            ]
            currentPod["plantName"] = r["plantName"]
            currentPod["plantID"] = r["plantID"]
            currentPod["plantedDate"] = r["plantedDate"]
            json.dump(data, open(config.JSON_Path.STATUS, "w"), indent=4)
            I = (
                "Planted: "
                + currentPod["plantID"]
                + " "
                + newPlant
                + " in "
                + r["podID"]
            )
            LOG.info(
                "New plant planted: "
                + currentPod["plantName"]
                + " ID:"
                + currentPod["plantID"]
                + " in "
                + r["podID"]
            )
            guessHarvest(app)
        # app.logging.info("Planted!!!")
        except Exception as e:
            print(e)


def resetMaintInterval(task):
    maint = getStatus()
    maint["maintenance"][0][task["taskPerformed"]] = task["newDate"]
    json.dump(maint, open(config.JSON_Path.STATUS, "w"), indent=4)
    LOG.info("Reset maint interval: " + str(task))


def changePrg(prg):
    global checkL
    global checkP
    from blueprints.init import scheduler
    from blueprints.threads import checkLights, activatePump
    from apscheduler.schedulers.background import BackgroundScheduler

    programs = getPrograms()
    for program in programs:
        if program["progID"] == prg:
            json.dump(program, open(config.JSON_Path.CURRENTPROGRAM, "w"), indent=4)
            scheduler.remove_job(job_id="checkL")
            scheduler.add_job(
                checkLights,
                "interval",
                seconds=int(config.Hardware.CHECKLIGHTSINTERVAL),
                id="checkL",
                args=[program],
                replace_existing=True,
            )

            scheduler.remove_job(job_id="checkP")
            scheduler.add_job(
                activatePump,
                "interval",
                seconds=int(program["pumpStartEvery"]),
                id="checkP",
                args=[program],
                replace_existing=True,
            )
            data = "Program changed to: " + prg
            LOG.info("New program: " + str(program))
            io.emit("info", data)


def newPlantedDate(cmd):
    from blueprints.threads import guessHarvest

    status = getStatus()
    status["towers"][int(cmd["podID"][0:2])]["levels"][int(cmd["podID"][3:5])]["pods"][
        int(cmd["podID"][6:8])
    ]["plantedDate"] = cmd["plantedDate"]
    json.dump(status, open(config.JSON_Path.STATUS, "w"), indent=4)
    LOG.info("Updated planted date: " + str(cmd))
    guessHarvest(app)


@app.template_filter("upperstring")
def upperstring(input):
    """Custom filter"""
    return input.upper()


# https://stackabuse.com/converting-strings-to-datetime-in-python/
@app.template_filter("formatDate")
def formatDate(input):
    from datetime import datetime

    if len(input) == 20:
        format = "%Y-%m-%dT%H:%M:%SZ"
    else:
        format = "%Y-%m-%dT%H:%M:%S.%fZ"
    d = datetime.strptime(input, format)
    return d.date()
