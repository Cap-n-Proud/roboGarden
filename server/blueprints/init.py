# Main script. Although this is not the entry point this collates all the pieces.
# This initializes the key functionalites such as serial port,threads etc

import threading
import time
from datetime import datetime
import logging

from threading import Lock
import serial
from serial.tools import list_ports
import config

import json

from blueprints.api import getCurrentProgr
from blueprints.L_events import *
from blueprints.threads import *
from flask import current_app as app

timeStarted = datetime.now()

# from apscheduler.schedulers.background import BackgroundScheduler
def initSerial():
    port = config.Hardware.SERIALPORT
    baud = config.Hardware.SERIALBAUD

    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        print(p)

    serial_port = serial.Serial(port, baud, timeout=None)

    print("serial interface configured. Pyserisal version: " + serial.VERSION)
    time.sleep(2)


def initialize():
    # currentProgram = getCurrentProgr()
    initSerial()
    currentProgram = getCurrentProgr()
    # Setup and start the thread to read serial port
    thread_lock = Lock()
    thread = threading.Thread(
        target=read_from_port,
        args=(
            serial.Serial(
                config.Hardware.SERIALPORT, config.Hardware.SERIALBAUD, timeout=None
            ),
        ),
    )
    thread.start()

    checkL = RepeatedTimer(
        int(config.Hardware.CHECKLIGHTSINTERVAL), checkLights, currentProgram
    )

    checkH = RepeatedTimer(24 * 60 * 60, guessHarvest, app)

    checkP = RepeatedTimer(
        int(currentProgram["pumpStartEvery"]), activatePump, currentProgram
    )

    timeNow = str(obj_now.hour).zfill(2) + ":" + str(obj_now.minute).zfill(2)
    app.logger.info("System started. System time is: " + timeNow)
    app.logger.info("Current program: " + str(currentProgram))
    print(
        "System started. System time is: "
        + timeNow
        + " current program "
        + str(currentProgram)
    )
