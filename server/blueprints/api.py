# Collection of functions to perform task on request of blueprints main files.
# This includes also filters for templates

import json
import config
import logging

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
        # app.logging.info("Planted!!!")
        except Exception as e:
            print(e)


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
