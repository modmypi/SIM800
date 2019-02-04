#!/usr/bin/python

from time import sleep, time
import serial
import RPi.GPIO as GPIO

POWER_BUTTON = 19
powered = False
SERIAL_PORT = "/dev/serial0"
DEBUG = False


def debug(verb):
    if DEBUG:
        print(verb)


GPIO.setmode(GPIO.BCM)
GPIO.setup(POWER_BUTTON, GPIO.OUT, initial=0)

sim800 = serial.Serial(SERIAL_PORT, baudrate=9600, timeout=1)


def checkpower():
    command = "ATE0\r"
    debug("sending command: %s" % command)
    sim800.write(command.encode())
    sleep(1)
    timeout = time() + 5
    while True:
        response = sim800.readline()
        debug(response)
        if response.decode().strip() == "OK":
            print("SIM800 Powered")
            powered = True
            break
        elif time() > timeout:
            print("SIM800 timed out, probably not powered")
            powered = False
            break
        sleep(0.2)
    return powered


def powerupdown(updown):
    print("Power " + updown + " SIM800")
    GPIO.output(POWER_BUTTON, 1)
    sleep(1.5)
    GPIO.output(POWER_BUTTON, 0)
    sleep(3)


try:
    while not checkpower():
        powerupdown("up")
    sleep(0.2)
except Exception as e:
    GPIO.cleanup()
    print(e)

GPIO.cleanup()
