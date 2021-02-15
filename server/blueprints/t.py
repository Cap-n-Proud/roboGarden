# note that there are many other schedulers available
from apscheduler.schedulers.background import BackgroundScheduler
import time

sched = BackgroundScheduler()


def some_job():
    print("Every 10 seconds")


# seconds can be replaced with minutes, hours, or days
sched.add_job(some_job, "interval", seconds=1)
sched.start()

time.sleep(3)

sched.shutdown()
