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

# Global variables to be used later
timeStarted = datetime.now()
scheduler = None

# Function to initialize the serial port and start the thread to read from it.


def initSerial():
    LOG = logging.getLogger(config.Config.APPLOGNAME)
    port = config.Hardware.SERIALPORT
    baud = config.Hardware.SERIALBAUD

    # List available ports (for debugging)
    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        print(p)

    try:
        serial_port = serial.Serial(port, baud, timeout=None)
        LOG.info(
            f"Serial interface configured on {port}@{baud}. Pyserial version: {serial.VERSION}")
        print(
            f"Serial interface configured on {port}@{baud}. Pyserial version: {serial.VERSION}")
        time.sleep(2)
    except serial.SerialException:
        # Serial port initialization failed, enter simulation mode
        serial_port = None
        LOG.warning("Serial device not found. Entering simulation mode.")
        print("Serial device not found. Entering simulation mode.")
        # Handle any other necessary tasks for simulation mode.
        # Redirect to /dev/null for simulation mode
        config.Hardware.SERIALPORT = "/dev/null"

# Function to initialize the system, get the current program, start the serial port thread, and schedule periodic functions.


def initialize():
    global scheduler
    LOG = logging.getLogger(config.Config.APPLOGNAME)

    # Timer to track time from system start
    timeFromStart = blueprints.timer.Timer()
    timeFromStart.start()

    # Get the current program from the API
    currentProgram = getCurrentProgr()

    try:
        # Start the thread to read from the serial port
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
        # Redirect to /dev/null for simulation mode
        config.Hardware.SERIALPORT = "/dev/null"

    # Initialize the BackgroundScheduler
    scheduler = BackgroundScheduler()
    scheduler.start()

    # Schedule periodic functions
    scheduler.add_job(checkLights, "interval", seconds=int(
        config.Hardware.CHECKLIGHTSINTERVAL), id="checkL", args=[currentProgram], replace_existing=True)
    scheduler.add_job(activatePump, "interval", seconds=int(
        currentProgram["pumpStartEvery"]), id="checkP", args=[currentProgram], replace_existing=True)
    scheduler.add_job(broadcastTime, "interval", seconds=int(
        1), id="broadcastTime", args=[timeFromStart], replace_existing=True)
    scheduler.add_job(pingHost, "interval", seconds=int(
        config.Hardware.PING_EVERY), id="pingHost", replace_existing=True)

    # Print the current program and the scheduled jobs (for debugging)
    # print(str(scheduler.get_jobs()))

    # Schedule the guessHarvest function to be called once a day (not included in the provided code)
    # checkH = RepeatedTimer(24 * 60 * 60, guessHarvest, app
