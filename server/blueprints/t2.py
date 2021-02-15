from L_events import *
import time
import json

P1 = """
{
    "progID": "004",
    "progName": "Growth - quiet hours, low watering, more red light",
    "pumpStartEvery": 7200,
    "pumpRunTime": 15,
    "pumpON": "08:00",
    "pumpOFF": "21:00",
    "lightBrightness": 100,
    "RGB": "255 150 150",
    "lightsON": "06:00",
    "lightsOFF": "23:00",
    "notes": "Program designed to grow, less water."
}
"""

currentProgram = json.loads(P1)


def activatePump(currentProgram):
    print("Progamm is: " + currentProgram["progID"])


def activatePump2(currentProgram):
    print("Progamm is: " + currentProgram)


checkP = RepeatedTimer(1, activatePump, currentProgram)
checkT = RepeatedTimer(2, activatePump2, "T2")

time.sleep(3)
checkP.stop()
# checkT.stop()

print("Stopped")

P2 = """
{
    "progID": "999",
    "progName": "Growth - quiet hours, low watering, more red light",
    "pumpStartEvery": 7200,
    "pumpRunTime": 15,
    "pumpON": "08:00",
    "pumpOFF": "21:00",
    "lightBrightness": 100,
    "RGB": "255 150 150",
    "lightsON": "06:00",
    "lightsOFF": "23:00",
    "notes": "Program designed to grow, less water."
}
"""
currentProgram = json.loads(P2)

checkP = RepeatedTimer(1, activatePump, currentProgram)
