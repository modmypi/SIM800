# SIM800

## sim800_call.py
This script allows you to make a phone call. Simply enter the number when prompted.

## sim800_incoming_call.py
This script will automatically answer an incoming phone call.

## sim800_power_on.py
This script allows you to power on the SIM800 without having to manually press the ON button. Requires the SIM800 board to have the "P" pin connected to a GPIO pin on the Pi.

## sim800_send_sms.py
This script lets you send a SMS message to another mobile phone. You will be prompted for the phone number, then the message.

## sim800_sms_responder.py
This script will wait for a test message, containing the word "update", and then send a text to a specified number.