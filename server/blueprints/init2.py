import serial
import threading
import logging
from blueprints.timer import Timer
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.base import JobLookupError
from config import Config, Hardware
from multiprocessing import Lock


def initialize():
    timeFromStart = Timer()
    timeFromStart.start()
    global scheduler
    LOG = logging.getLogger(Config.APPLOGNAME)
    # This gets the current program from the API.
    currentProgram = getCurrentProgr()

    # This starts the thread to read from the serial port.
    try:
        serial_port = serial.Serial(
            Hardware.SERIALPORT, Hardware.SERIALBAUD, timeout=None)
        thread_lock = Lock()
        thread = threading.Thread(target=readSer, args=(serial_port,))
        thread.start()
    except serial.SerialException:
        # Serial port initialization failed, enter simulation mode
        serial_port = None
        LOG.warning("Serial device not found. Entering simulation mode.")
        # Handle any other necessary tasks for simulation mode.

    # This schedules the checkLights function to be called periodically.
    scheduler = BackgroundScheduler()
    scheduler.start()

    # This schedules the activatePump function to be called periodically.
    try:
        scheduler.add_job(
            checkLights,
            "interval",
            seconds=int(Hardware.CHECKLIGHTSINTERVAL),
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
            seconds=int(Hardware.PING_EVERY),
            id="pingHost",
            replace_existing=True,
        )
    except JobLookupError as e:
        LOG.warning("Failed to schedule a job: %s", e)
