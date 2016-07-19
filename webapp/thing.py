#!/usr/bin/env python

import Adafruit_DHT
import RPi.GPIO as GPIO
import threading

# humidity/temperature sensor
DHT_TYPE = Adafruit_DHT.AM2302
DHT_PIN = 18

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
        # use prefix _ to show intent treat _lock as "private"
        # Some Python developers follow this naming convention.
        self._lock = threading.Lock()

    def get_humidity(self):
        """returns humidity as a percentage 0 - 100
        """
        # 'with' is a context, lock makes method thread safe.
        with self._lock:
            humidity, temperature = Adafruit_DHT.read_retry(DHT_TYPE, DHT_PIN)
            return humidity

    def get_temperature(self):
        """returns temperature in degrees Celsius
        """
        # 'with' is a context, lock makes method thread safe.
        with self._lock:
            humidity, temperature = Adafruit_DHT.read_retry(DHT_TYPE, DHT_PIN)
            return temperature

    def read_switch(self):
        """returns true if switch is high, false if switch is low.
        Uses lock for thread safety.
        """
        # 'with' is a context, lock makes method thread safe.
        with self._lock:
            return GPIO.input(SWITCH_PIN)

    def set_led(self, value):
        """Set the LED to the passed in value, True for on, False for off.
        Uses lock for thread safety.
        """
        with self._lock:
            GPIO.output(LED_PIN, value)

