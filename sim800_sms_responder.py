#!/usr/bin/python

from time import sleep, time
import serial

SERIAL_PORT = "/dev/serial0"
NUMBER = "00000000000"
DEBUG = True


def debug(verb):
    if DEBUG:
        print(verb)


sim800 = serial.Serial(SERIAL_PORT, baudrate=9600, timeout=1)

## set text mode
command = 'AT+CMGF=1\r'
debug("set text mode, sending command: %s" % command)
sim800.write(command.encode())
timeout = time() + 10

while True:
    response = sim800.readline()
    debug(response)
    if response.decode().strip() == "OK":
        break
    elif time() > timeout:
        debug("text mode timeout")
        break
    sleep(0.2)


def sim800_delete_all(s):
    command = 'AT+CMGDA="DEL ALL"\r'
    debug("delete all previous messages, sending command: %s" % command)
    s.write(command.encode())
    timeout = time() + 10

    while True:
        response = s.readline()
        debug(response)
        if response.decode().strip() == "OK":
            break
        elif time() > timeout:
            debug("delete all timeout")
            break
        sleep(0.2)


def sim800_sms(s, msg):
    number = NUMBER
    message = msg
    ## set to number
    command = 'AT+CMGS="%s"\r' % number
    debug("set to number, sending command: %s" % command)
    s.write(command.encode())
    timeout = time() + 10
    timedout = False
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
                if time() > timeout:
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


def sim800_sms_responder(s):
    response = s.readline()
    debug(response)
    if "CMTI" in response.decode().strip():
        debug("New message received")
        debug("Getting message...")
        command = "AT+CMGR=1\r"
        s.write(command.encode())
        timeout = time() + 10
        while True:
            response = s.readline()
            debug(response)
            if "update" in response.decode().strip().lower():
                debug("an update has been requested, send a reply!")
                ##
                #
                # Message received contains the word "update" send a reply SMS.
                #
                ##
                sim800_sms(s, "You have requested an update! Here it is!")
                break
            elif time() > timeout:
                debug("sms responder timeout")
                break
            sleep(0.2)
        sim800_delete_all(s)
    sleep(1)


try:
    sim800_delete_all(sim800)
    while True:
        sim800_sms_responder(sim800)
except Exception as e:
    print(e)
