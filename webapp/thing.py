#!/usr/bin/env python

import RPi.GPIO as GPIO

LED_PIN = 23
SWITCH_PIN = 24

# new style class
class PiThing(object):
    """Raspberry Pi Internet 'Thing'."""
    
    def __init__(self):
        # use BCM numbering scheme when using Adafruit pi cobbler. Don't use board scheme.

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

