#!/usr/bin/python
# -*- coding: utf-8 -*-

# This file manages the threaded functions such as reading the serial port, checking lights and pump etc

import json
import threading
import time
from datetime import datetime
import logging
from flask_socketio import SocketIO
from flask_socketio import emit, ConnectionRefusedError, disconnect

from threading import Lock
import serial
from serial.tools import list_ports
import config

from blueprints.L_events import *

dataJSON = ""
from flask import current_app as app
from blueprints.api import getCurrentProgr, getPlantsDB, getStatus

# LOG = logging.getLogger(__name__)
LOG = logging.getLogger(config.Config.APPLOGNAME)
io = SocketIO(app)  # engineio_logger=True)


def testThread(param):
    # time.sleep(2)
    print("Test thread ", param)


# Broadcast info to every client
def broadcastInfo(data):
    socketio.emit("info", data)
    # print(data + " sent")


def handle_data(data):
    global dataJSON
    try:
        dataJSON = json.loads(data.decode())
        if dataJSON["type"] == config.Config.INFOTAG:
            print(dataJSON)
            LOG.info("Info from Arduino: " + dataJSON["message"])
            io.emit(config.Config.INFOTAG, dataJSON["message"])

        if dataJSON["type"] == config.Config.TELEMETRYTAG:
            print(dataJSON)
            io.emit(config.Config.TELEMETRYTAG, dataJSON)
            # print(threading.active_count())

    except ValueError as e:
        # We need to replace double quotes with single ones to save it in the json logs
        LOG.warning(
            "Received non-JSON from Arduino: " + str(data).replace('"', "'") + str(e)
        )


# https://stackoverflow.com/questions/17553543/pyserial-non-blocking-read-loop
def read_from_port(ser):
    except_counter = ""
    while ser.is_open:
        # NB: for PySerial v3.0 or later, use property `in_waiting` instead of function `inWaiting()` below!
        try:
            if (
                ser.in_waiting > 0
            ):  # if incoming bytes are waiting to be read from the serial input buffer
                data_str = ser.read(ser.in_waiting)
                # read the bytes and co nvert from binary array to ASCII
                handle_data(data_str)
            time.sleep(0.2)
        except serial.serialutil.SerialException:
            except_counter += 1
            LOG.warning(ser.serialutil.SerialException)
            if except_counter == 5:
                break
                time.sleep(1)

        except serial.SerialTimeoutException:
            LOG.warning(serial.SerialTimeoutException)


def write_to_ser(ser, message):
    ser.write(str(message + "\n\c").encode())


# Calculate if a time is between a time range (specified as list)
def is_between(startTime, endTime, nowTime):
    endTime = datetime.strptime(endTime, "%H:%M")
    startTime = datetime.strptime(startTime, "%H:%M")
    nowTime = datetime.strptime(nowTime, "%H:%M")

    if startTime < endTime:
        return nowTime >= startTime and nowTime <= endTime
    else:  # Over midnight
        return nowTime >= startTime or nowTime <= endTime


# Send command to Arduino, used for python calls
def arduinoCommand(command):
    serial.Serial(
        config.Hardware.SERIALPORT, config.Hardware.SERIALBAUD, timeout=0.5
    ).write(str((str(command) + "\n")).encode())
    time.sleep(0.5)


# This will be called to regulate the pump behaviour. TODO need to add thread and parameterd
def activatePump(currentProgram):
    obj_now = datetime.now()
    timeNow = str(obj_now.hour).zfill(2) + ":" + str(obj_now.minute).zfill(2)
    if is_between(currentProgram["pumpON"], currentProgram["pumpOFF"], timeNow):
        # Pump ON
        arduinoCommand("pumpStart")
        LOG.info("Pump is ON")
        # We stop the thread so the pump continues pumping
        time.sleep(currentProgram["pumpRunTime"])
        # Pump OFF
        arduinoCommand("pumpStop")
        LOG.info("Pump is OFF")


# Function to check the lights. If we are in the time range it will switch the light on and give the current proram RGB color
def checkLights(currentProgram):
    obj_now = datetime.now()
    timeNow = str(obj_now.hour).zfill(2) + ":" + str(obj_now.minute).zfill(2)
    # # DEBUG:
    # print(currentProgram["progID"])
    # print(currentProgram)
    if is_between(currentProgram["lightsON"], currentProgram["lightsOFF"], timeNow):
        if "brightness" in dataJSON:
            # print("D " + str(dataJSON) + str(currentProgram))
            try:
                if int(dataJSON["brightness"]) != int(
                    currentProgram["lightBrightness"]
                ):
                    arduinoCommand(
                        "setBrightness " + str(currentProgram["lightBrightness"])
                    )
                    LOG.info("RGB set to " + str(currentProgram["RGB"]))
                # if dataJSON["RGB"] != currentProgram["RGB"]:
                # print("Different RGB")
                if dataJSON["RGB"] != currentProgram["RGB"]:
                    arduinoCommand("setLightRGB " + str(currentProgram["RGB"]))
                    LOG.info("Lights set to " + str(currentProgram["lightBrightness"]))

            except ValueError as e:
                LOG.error(e)

    else:
        if dataJSON["brightness"] != 0:  # print("Lights should be ON")
            arduinoCommand("setBrightness 0")
            LOG.info("Lights set to " + str(currentProgram["lightBrightness"]))


def formatDate(input):
    from datetime import datetime

    if len(input) == 20:
        format = "%Y-%m-%dT%H:%M:%SZ"
    else:
        format = "%Y-%m-%dT%H:%M:%S.%fZ"
    d = datetime.strptime(input, format)
    return d.date()


# This function is called once a day and writes in each plant the days between harvest
def guessHarvest(app):
    from datetime import date
    from datetime import datetime

    dt = datetime.combine(date.today(), datetime.min.time())
    dt = date.today()

    plantsDB = getPlantsDB(app)
    status = getStatus()
    ready = 0
    # print(plantsDB["plants"][0]["plantID"])
    for tower in status["towers"]:
        # print(tower["name"])
        for level in tower["levels"]:
            # print(level)pod["plantedDate"]
            for pod in level["pods"]:
                # print(pod["podID"], pod["plantedDate"])
                for i in plantsDB["plants"]:
                    if i["plantID"] == pod["plantID"]:
                        daysPlanted = (dt - formatDate(pod["plantedDate"])).days
                        # print(i["DtH"].isnumeric())

                        pod["harvestTime"] = str(daysPlanted - int(float(i["DtH"])))
                        # print(pod["harvestTime"])
                        if daysPlanted - int(float(i["DtH"])) > 0:
                            ready = ready + 1
                        # print(
                        #     "Harvest "
                        #     + pod["podID"]
                        #     + " "
                        #     + str(daysPlanted - int(float(i["DtH"])))
                        #     + " days after DtH"
                        # )
                        break
    json.dump(status, open(config.JSON_Path.STATUS, "w"), indent=4)
    LOG.info("Time to harvest computed.  " + str(ready) + " plants should be ready!")
