#!/usr/bin/python
# -*- coding: utf-8 -*-

# This file manages the threaded functions such as reading teh serial port, checking lights and pump etc

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

dataJSON = ""
# LOG = logging.getLogger(__name__)
LOG = logging.getLogger('werkzeug')
def testThread(param):
    # time.sleep(2)
    print("Test thread ", param)

def handle_data(data):
    global dataJSON
    try:
        dataJSON = json.loads(data.decode())
        if dataJSON["type"] == "I":
            print(dataJSON)
            LOG.info("Info from Arduino: " + dataJSON["message"])
            # broadcastInfo(dataJSON["message"])

        if dataJSON["type"] == "T":
            print(dataJSON)
            # socketio.emit("telemetry", dataJSON)

    except ValueError as e:
        LOG.warning("Received non-JSON from Arduino: " + str(data) + e)


def read_from_port(ser):
    while True:
        # NB: for PySerial v3.0 or later, use property `in_waiting` instead of function `inWaiting()` below!
        try:
            if (
                ser.in_waiting > 0
            ):  # if incoming bytes are waiting to be read from the serial input buffer
                data_str = ser.readline(ser.in_waiting + 300)
                # read the bytes and convert from binary array to ASCII
                handle_data(data_str)
        except ValueError as e:
            LOG.warning(e)


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
    serial.Serial(config.Hardware.SERIALPORT, config.Hardware.SERIALBAUD, timeout=0.5).write(str(command + "\n").encode())
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
# TODO when the web UI set pump to off it returns an error (even with the try statement)
def checkLights(currentProgram):
    obj_now = datetime.now()
    timeNow = str(obj_now.hour).zfill(2) + ":" + str(obj_now.minute).zfill(2)
    if is_between(currentProgram["lightsON"], currentProgram["lightsOFF"], timeNow):

            # test = dataJSON["brightness"]
        
        try:
            if dataJSON["brightness"] == 0:  # print("Lights should be ON")
                arduinoCommand(
                    "setBrightness " + str(currentProgram["lightBrightness"])
                )
                LOG.info("RGB set to " + str(currentProgram["RGB"]))
                arduinoCommand("setLightRGB " + str(currentProgram["RGB"]))
                LOG.info("Lights set to " + str(currentProgram["lightBrightness"]))

        except ValueError as e:
            LOG.error(e)
    else:
        if dataJSON["brightness"] != 0:  # print("Lights should be ON")
            arduinoCommand("setBrightness 0")
            LOG.info("Lights set to " + str(currentProgram["lightBrightness"]))
