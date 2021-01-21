import json

from flask import current_app as app


# Retrieve the current program, used to populate the indey.html file
def getCurrentProgr():
    with open("currentProgram.json") as f:
        data = json.load(f)
    return data

def getAppConf():
    with open("assets/appConfig.json") as f:
        data = json.load(f)
    return data

def getPlantsDB(app):
    with open("plants.json") as f:
        data = json.load(f)
    return data


def getStatus(app):
    with open("status.json") as f:
        data = json.load(f)
    return data

    # plantsDB = getPLantsDB()
    # status = getStatus()
    # currentProgram = getCurrentProgram()
    # programs = getPrograms()


def newPlant(r):
    with open("status.json", "r") as f:
        data = json.load(f)
        try:
            newPlant = r["plantName"]
            l = r["podID"].split("-")
            currentPod = data["towers"][int(l[0])]["levels"][int(l[1])]["pods"][
                int(l[2])
            ]
            print(currentPod["plantName"])
            currentPod["plantName"] = r["plantName"]
            currentPod["plantID"] = r["plantID"]
            currentPod["plantedDate"] = r["plantedDate"]
            json.dump(data, open("status.json", "w"), indent=4)
            I = (
                "Planted: "
                + currentPod["plantID"]
                + " "
                + newPlant
                + " in "
                + r["podID"]
            )

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

    # 2021-01-19T23:02:27.000Z
    # 2016-04-26T18:09:16Z
    if len(input) == 20:
        format = "%Y-%m-%dT%H:%M:%SZ"
    else:
        format = "%Y-%m-%dT%H:%M:%S.%fZ"
    d = datetime.strptime(input, format)
    return d.date()
