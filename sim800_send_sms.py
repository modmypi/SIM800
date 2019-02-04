#!/usr/bin/python

from time import sleep, time
import serial

SERIAL_PORT = "/dev/serial0"
DEBUG = True


def debug(verb):
    if DEBUG:
        print(verb)


sim800 = serial.Serial(SERIAL_PORT, baudrate=9600, timeout=1)


def sim800_sms(s):
    number = input("Enter number: ")
    message = input("Enter message: ")
    ## set text mode
    command = 'AT+CMGF=1\r'
    debug("set text mode, sending command: %s" % command)
    s.write(command.encode())
    timeout = time() + 10
    timedout = False
    while True:
        response = s.readline()
        debug(response)
        if response.decode().strip() == "OK":
            break
        elif time() > timeout:
            timedout = True
            debug("text mode timeout")
            break
        sleep(0.2)
    if timedout:
        return
    ## set to number
    command = 'AT+CMGS="%s"\r' % number
    debug("set to number, sending command: %s" % command)
    s.write(command.encode())
    timeout = time() + 10
    while True:
        response = s.readline()
        debug(response)
        if response.decode().strip() == ">":
            ## send message
            command = message + chr(26) + '\r'
            debug("sending message, sending command: %s" % command)
            s.write(command.encode())
            timeout = time() + 10
            while True:
                response = s.readline()
                debug(response)
                if response.decode().strip() == "OK":
                    debug("Message sent")
                    break
                elif time() > timeout:
                    timedout = True
                    debug("message timeout")
                    break
                sleep(0.2)
            if timedout:
                return
            break
        elif response.decode().strip() == "ERROR":
            debug("There was an error! Please check the number and try again")
            s.write(chr(27).encode())
            break
        elif time() > timeout:
            debug("set number timeout")
            break
        sleep(0.2)


try:
    sim800_sms(sim800)
except Exception as e:
    print(e)
