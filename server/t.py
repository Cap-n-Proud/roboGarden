import blueprints.config as config
import json
from datetime import datetime


def getPrograms():
    with open(config.JSON_Path.PROGRAMS) as f:
        data = json.load(f)
    return data


def getPlantsDB():
    with open(config.JSON_Path.PLANTDB) as f:
        data = json.load(f)
    return data


def getStatus():
    with open(config.JSON_Path.STATUS) as f:
        data = json.load(f)
    return data


def formatDate(input):
    from datetime import datetime

    if len(input) == 20:
        format = "%Y-%m-%dT%H:%M:%SZ"
    else:
        format = "%Y-%m-%dT%H:%M:%S.%fZ"
    d = datetime.strptime(input, format)
    return d.date()


# This function is called once a day and writes in each plant the days between harvest
def guessHarvest():
    from datetime import date
    from datetime import datetime

    dt = datetime.combine(date.today(), datetime.min.time())
    dt = date.today()

    plantsDB = getPlantsDB()
    status = getStatus()
    # print(plantsDB["plants"][0]["plantID"])
    for tower in status["towers"]:
        print(tower["name"])
        for level in tower["levels"]:
            # print(level)pod["plantedDate"]
            for pod in level["pods"]:
                # print(pod["podID"], pod["plantedDate"])
                for i in plantsDB["plants"]:
                    if i["plantID"] == pod["plantID"]:
                        daysPlanted = (dt - formatDate(pod["plantedDate"])).days
                        # print(i["DtH"].isnumeric())

                        pod["harvestTime"] = str(daysPlanted - int(float(i["DtH"])))

                        print(
                            "Harvest "
                            + pod["podID"]
                            + " "
                            + str(daysPlanted - int(float(i["DtH"])))
                            + " days after DtH"
                        )
                    break
                json.dump(status, open(config.JSON_Path.STATUS, "w"), indent=4)


# currentPod = data["towers"][int(l[0])]["levels"][int(l[1])]["pods"][
guessHarvest()
