import json


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


def format_datetime(value, format="%d %b %Y %I:%M %p"):
    """Format a date time to (Default): d Mon YYYY HH:MM P"""
    if value is None:
        return ""
    return value.strftime(format)
