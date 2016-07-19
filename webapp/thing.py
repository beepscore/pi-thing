#!/usr/bin/env python

import Adafruit_DHT
import RPi.GPIO as GPIO
import threading
import time

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

        # humidity as a percentage 0 - 100
        self._humidity = None
        # temperature in degrees Celsius
        self._temperature = None
        # Create and start background thread for humidity/temperature
        self._dht_thread = threading.Thread(target=self._dht_update)
        self._dht_thread.daemon = True
        self._dht_thread.start()

    def _dht_update(self):
        """Main function for DHT update thread.
        Make thread safe to avoid problems with multiple requests to one sensor.
        """
        while True:
            self._humidity, self._temperature = Adafruit_DHT.read_retry(DHT_TYPE, DHT_PIN)
            # sensor updates every 2 seconds, so read at same frequency
            time.sleep(2.0)

    def get_humidity(self):
        """returns humidity as a percentage 0 - 100. Sensor updates every 2 seconds.
        """
        return self._humidity

    def get_temperature(self):
        """returns temperature in degrees Celsius. Sensor updates every 2 seconds.
        """
        return self._temperature

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

