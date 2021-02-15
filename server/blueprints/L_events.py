import json
import threading
import time
from datetime import datetime
from threading import Lock
from threading import Timer

# https://stackoverflow.com/questions/2398661/schedule-a-repeating-event-in-python-3
# https://www.educba.com/python-threading-timer/

# CURRENT https://stackoverflow.com/questions/474528/what-is-the-best-way-to-repeatedly-execute-a-function-every-x-seconds


class RepeatedTimer(object):
    """
    A periodic task running in threading.Timers
    """

    def __init__(self, interval, function, *args, **kwargs):
        self._timer = None
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.is_running = False
        self.next_call = time.time()
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self.next_call += self.interval
            self._timer = threading.Timer(self.next_call - time.time(), self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False


"""
{ "progName": "This is the current program",
  "pumpStartEvery": 60,
  "pumpRunTime": 5,
  "pumpStopHours":"20:00, 04:00",
  "lightBrightness": 80,
  "RGB": "10 100 210",
  "lightsON":"04:00, 20:00"
}

{"type":"T","pumpON":false,"RGB":null,"brightness":0,"PH":0,"waterLevel":0}

"""
