#!/usr/bin/python
# -*- coding: utf-8 -*-
import threading
import time
from datetime import datetime

from threading import Lock
import serial
from serial.tools import list_ports
import config

import json

from blueprints.api import getCurrentProgr
from blueprints.L_events import *

def testThread(param):
    # time.sleep(2)
    print("Test thread ", param)

def handle_data(data):
    global dataJSON
    try:
        dataJSON = json.loads(data.decode())
        if dataJSON["type"] == "I":
            broadcastInfo(dataJSON["message"])
            # app.logger.info("Info from Arduino: " + dataJSON["message"])

        if dataJSON["type"] == "T":
            print(dataJSON)
            # socketio.emit("telemetry", dataJSON)

    except ValueError as e:
        # app.logger.warning("Received non-JSON from Arduino: " + str(data))
        print(data)


def read_from_port(ser):
    while True:
        # NB: for PySerial v3.0 or later, use property `in_waiting` instead of function `inWaiting()` below!
        if (
            ser.in_waiting > 0
        ):  # if incoming bytes are waiting to be read from the serial input buffer
            data_str = ser.readline(ser.in_waiting + 300)
            # read the bytes and convert from binary array to ASCII
            handle_data(data_str)


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


# This will be called to regulate the pump behaviour. TODO need to add thread and parameterd
def checkPump(duration):
    obj_now = datetime.now()
    timeNow = str(obj_now.hour).zfill(2) + ":" + str(obj_now.minute).zfill(2)
    if is_between(currentProgram["pumpON"], currentProgram["pumpOFF"], timeNow):
        print("pump ON")
        arduinoCommand2("pumpStart")
        # app.logger.info("Pump is ON")
        # We stop the thread so the pump continues pumping
        time.sleep(duration)
        print("pump OFF")
        arduinoCommand2("pumpStop")
        # app.logger.info("Pump is OFF")


# Function to check the lights. If we are in the time range it will switch the light on and give the current proram RGB color
# TODO when the web UI set pump to off it returns an error (even with the try statement)
def checkLights(currentProgram):
    obj_now = datetime.now()
    timeNow = str(obj_now.hour).zfill(2) + ":" + str(obj_now.minute).zfill(2)
    if is_between(currentProgram["lightsON"], currentProgram["lightsOFF"], timeNow):
        try:
            test = dataJSON["brightness"]

            if dataJSON["brightness"] == 0:  # print("Lights should be ON")
                arduinoCommand2(
                    "setBrightness " + str(currentProgram["lightBrightness"])
                )
                arduinoCommand2("setLightRGB " + str(currentProgram["RGB"]))
                print("Brightness set to default")
                # app.logger.info("Lights ON, RGB also set")

        except ValueError as e:
            print(e)
    else:
        if dataJSON["brightness"] != 0:  # print("Lights should be ON")
            arduinoCommand2("setBrightness 0")
            # app.logger.info("Lights OFF, RGB also set")


def initSerial():
    port = config.Hardware.SERIALPORT
    baud = config.Hardware.SERIALBAUD

    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        print(p)

    serial_port = serial.Serial(port, baud, timeout=0.5)

    print("serial interface configured. Pyserisal version: " + serial.VERSION)
    time.sleep(2)

def init():
    # currentProgram = getCurrentProgr()
    initSerial();

    # Setup and start the thread to read serial port
    thread_lock = Lock()
    thread = threading.Thread(target=read_from_port, args=(serial.Serial(config.Hardware.SERIALPORT, config.Hardware.SERIALBAUD, timeout=0.5),))
    thread.start()
    # print(config.ProdConfig.DEBUG)
    # print(config.JSON_Path.CURRENTPROGRAM)

    checkL = RepeatedTimer(
        int(config.Hardware.READSERIALINTERVAL), testThread, "param"
    )  # it auto-starts, no need of rt.start()

    obj_now = datetime.now()
    timeNow = str(obj_now.hour).zfill(2) + ":" + str(obj_now.minute).zfill(2)
    # app.logger.info("System started. System time is: " + timeNow)
    print("System started. System time is: " + timeNow)
