import threading
import time
from threading import Lock

from blueprints.api import getCurrentProgr, getAppConf
from blueprints.L_events import *

def testThread(param):
    # time.sleep(2)
    print("Test thread ", param)

def init():
    appConf = getAppConf()
    # currentProgram = getCurrentProgr()
    checkL = RepeatedTimer(
        int(appConf['readSerialInterval']), testThread, "param"
    )  # it auto-starts, no need of rt.start()

    obj_now = datetime.now()
    timeNow = str(obj_now.hour).zfill(2) + ":" + str(obj_now.minute).zfill(2)
    # app.logger.info("System started. System time is: " + timeNow)
    print("System started. System time is: " + timeNow)
