#!/usr/bin/python

from time import sleep, time
import serial

SERIAL_PORT = "/dev/serial0"
DEBUG = False


def debug(verb):
    if DEBUG:
        print(verb)


sim800 = serial.Serial(SERIAL_PORT, baudrate=9600, timeout=1)


def sim800_call(s):
    number = input("Enter number: ")
    # dial number
    command = 'ATD%s;\r' % number
    debug("establishing call, sending command: %s" % command)
    s.write(command.encode())
    timeout = time() + 10
    while True:
        response = s.readline()
        debug(response)
        if response.decode().strip() == "OK":
            debug("Establishing call...")
            input("Press any key to hang up...")
            sim800_hangup(s)
            break
        elif response.decode().strip() == "NO DIALTONE":
            debug("No dial tone...")
            break
        elif response.decode().strip() == "BUSY":
            debug("Line busy...")
            break
        elif response.decode().strip() == "NO CARRIER":
            debug("No signal...")
            break
        elif response.decode().strip() == "NO ANSWER":
            debug("No answer...")
            break
        elif response.decode().strip() == "ERROR":
            debug("Error, check number...")
            break
        elif time() > timeout:
            debug("call timeout")
            break
        sleep(0.2)


def sim800_hangup(s):
    command = 'ATH\r'
    debug("disconnecting call, sending command: %s" % command)
    s.write(command.encode())
    timeout = time() + 10
    while True:
        response = s.readline()
        debug(response)
        if response.decode().strip() == "OK":
            debug("Hang up successful")
            break
        elif time() > timeout:
            debug("hangup timeout")
            break
        sleep(0.2)


try:
    while True:
        sim800_call(sim800)
except Exception as e:
    print(e)
