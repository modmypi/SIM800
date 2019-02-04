#!/usr/bin/python

from time import sleep, time
import serial
import RPi.GPIO as GPIO

SERIAL_PORT = "/dev/serial0"
DEBUG = False


def debug(verb):
    if DEBUG:
        print(verb)


sim800 = serial.Serial(SERIAL_PORT, baudrate=9600, timeout=1)


def sim800_answer(s):
    command = 'ATA\r'
    debug("answering call, sending command: %s" % command)
    s.write(command.encode())
    timeout = time() + 10
    while True:
        response = s.readline()
        debug(response)
        if response.decode().strip() == "OK":
            input("Press any key to hang up...")
            sim800_hangup(s)
            break
        elif time() > timeout:
            debug("answer timeout")
            break
        sleep(0.2)


def sim800_hangup(s):
    print("Hanging up...")
    command = 'ATH\r'
    debug("disconnecting call, sending command: %s" % command)
    s.write(command.encode())
    timeout = time() + 10
    while True:
        response = s.readline()
        debug(response)
        if response.decode().strip() == "OK":
            print("Hang up successful...")
            print("Waiting for call...")
            break
        elif time() > timeout:
            debug("hangup timeout")
            break
        sleep(0.2)


try:
    print("Waiting for call...")
    while True:
        response = sim800.readline()
        debug(response)
        if response.decode().strip() == "RING":
            print("Incoming call detected, answering...")
            sim800_answer(sim800)
except Exception as e:
    print(e)
