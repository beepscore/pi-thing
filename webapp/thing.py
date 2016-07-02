#!/usr/bin/env python

import RPi.GPIO as GPIO

LED_PIN = 23
SWITCH_PIN = 24

# new style class
class PiThing(object):
    """Raspberry Pi Internet 'Thing'.
    PiThing reads and writes to raspberry pi gpio pins.
    It does not contain any networking code, and may be used and tested without a network.
    """

    def __init__(self):

        # Match Adafruit pi cobbler numbering BCM, don't use GPIO.BOARD.
        GPIO.setmode(GPIO.BCM)

        # led as output
        GPIO.setup(LED_PIN, GPIO.OUT)
        # switch as input
        GPIO.setup(SWITCH_PIN, GPIO.IN)

    def read_switch(self):
        """returns true if switch is high, false if switch is low
        """
        return GPIO.input(SWITCH_PIN)


    def set_led(self, value):
        """Set the LED to the passed in value, True for on, False for off.
        """
        GPIO.output(LED_PIN, value)

