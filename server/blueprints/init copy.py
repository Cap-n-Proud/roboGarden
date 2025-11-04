# This is the main script. It initializes the key functionalities such as serial port, threads, etc.

import threading
import time
from datetime import datetime
import logging

from threading import Lock
import serial
from serial.tools import list_ports
import config

import blueprints.timer

import json

from blueprints.api import getCurrentProgr
from blueprints.threads import *
from flask import current_app as app

from apscheduler.schedulers.background import BackgroundScheduler

# This is the time when the system started.
timeStarted = datetime.now()
# This is the checkLights function that will be called periodically.
checkL = ""
# This is the activatePump function that will be called periodically.
checkP = ""
# This is the scheduler object that will be used to schedule the periodic functions.
scheduler = ""

# This function initializes the serial port and starts the thread to read from it.


def initSerial():
    LOG = logging.getLogger(config.Config.APPLOGNAME)
    port = config.Hardware.SERIALPORT
    baud = config.Hardware.SERIALBAUD

    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        print(p)

    serial_port = serial.Serial(port, baud, timeout=None)
    # serial.flushInput()
    LOG.info(
        "Serial interface configured on "
        + port
        + "@"
        + str(baud)
        + " Pyserisal version: "
        + serial.VERSION
    )

    print(
        "Serial interface configured on "
        + port
        + "@"
        + str(baud)
        + " Pyserisal version: "
        + serial.VERSION
    )
    time.sleep(2)

# This function initializes the system. It gets the current program, starts the serial port thread, and schedules the periodic functions.


def initialize():
    timeFromStart = blueprints.timer.Timer()
    timeFromStart.start()
    global scheduler
    LOG = logging.getLogger(config.Config.APPLOGNAME)
    # This gets the current program from the API.
    currentProgram = getCurrentProgr()
   # This starts the thread to read from the serial port.
    try:
        serial_port = serial.Serial(
            config.Hardware.SERIALPORT, config.Hardware.SERIALBAUD, timeout=None)
        thread_lock = Lock()
        thread = threading.Thread(target=readSer, args=(serial_port,))
        thread.start()
    except serial.SerialException:
        # Serial port initialization failed, enter simulation mode
        serial_port = None
        LOG.warning("Serial device not found. Entering simulation mode.")
        print("Serial device not found. Entering simulation mode.")
        # Handle any other necessary tasks for simulation mode.
        config.Hardware.SERIALPORT = "/dev/null"
    # This schedules the checkLights function to be called periodically.
    # scheduler.add_job(checkLights, "interval", seconds=int(config.Hardware.CHECKLIGHTSINTERVAL), id="checkL", args=[currentProgram], replace_existing=True)
    scheduler = BackgroundScheduler()
    scheduler.start()

    # This schedules the activatePump function to be called periodically.
    scheduler.add_job(
        checkLights,
        "interval",
        seconds=int(config.Hardware.CHECKLIGHTSINTERVAL),
        id="checkL",
        args=[currentProgram],
        replace_existing=True,
    )
    scheduler.add_job(
        activatePump,
        "interval",
        seconds=int(currentProgram["pumpStartEvery"]),
        id="checkP",
        args=[currentProgram],
        replace_existing=True,
    )
    scheduler.add_job(
        broadcastTime,
        "interval",
        seconds=int(1),
        id="broadcastTime",
        args=[timeFromStart],
        replace_existing=True,
    )
    scheduler.add_job(
        pingHost,
        "interval",
        seconds=int(config.Hardware.PING_EVERY),
        id="pingHost",
        replace_existing=True,
    )

    # This prints the current program and the scheduled jobs.
    # print(str(scheduler.get_jobs()))
    # This schedules the guessHarvest function to be called once a day.
    # checkH = RepeatedTimer(24 * 60 * 60, guessHarvest, app
