import time

#import RPi.GPIO as GPIO
import serial

ser=serial.Serial("/dev/ttyACM0",9600)  #change ACM number as found from ls /dev/tty/ACM*
ser.baudrate=9600
def blink(pin):
    # GPIO.output(pin,GPIO.HIGH)
    # time.sleep(1)
    # GPIO.output(pin,GPIO.LOW)
    # time.sleep(1)
    print("BLINK!")
return

# GPIO.setmode(GPIO.BOARD)
# GPIO.setup(11, GPIO.OUT)

while True:

    read_ser=ser.readline()
    print(read_ser)
    if(read_ser=="Hello From Arduino!"):
        blink(11)
