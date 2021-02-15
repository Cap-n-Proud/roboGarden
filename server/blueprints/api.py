# Collection of functions to perform task on request of blueprints main files.
# This includes also filters for templates

import json
import config
import logging
from blueprints.L_events import *

from flask import current_app as app

# LOG = logging.getLogger(__name__)
LOG = logging.getLogger(config.Config.APPLOGNAME)

# Retrieve the current program, used to populate the indey.html file


def getCurrentProgr():
    with open(config.JSON_Path.CURRENTPROGRAM) as f:
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


def getStatus(app):
    with open(config.JSON_Path.STATUS) as f:
        data = json.load(f)
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


def changePrg(prg):
    global checkL
    global checkP
    from blueprints.init import checkL, checkP
    from blueprints.threads import checkLights, activatePump

    print("changed! " + prg)
    programs = getPrograms()
    for program in programs:
        if program["progID"] == prg:
            print(str(program))
            json.dump(program, open(config.JSON_Path.CURRENTPROGRAM, "w"), indent=4)
            # import os
            # try this https://stackoverflow.com/questions/16578652/threading-timer
            checkL.cancel()

            del checkL
            checkL = RepeatedTimer(
                int(config.Hardware.CHECKLIGHTSINTERVAL), checkLights, program
            )

            # checkP.stop()

            # checkP = RepeatedTimer(
            #     int(program["pumpStartEvery"]), activatePump, program
            # )
            # os.system("sudo service robogarden restart")


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
