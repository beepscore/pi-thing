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

        # User defined callbacks
        self._switch_callback = None
        self._temperature_humidity_callback = None

        # Create and start background thread for humidity/temperature
        self._dht_thread = threading.Thread(target=self._dht_update)
        self._dht_thread.daemon = True
        self._dht_thread.start()

        # Configure rpio.gpio to fire an internal callback when the switch changes
        # event detect returns pin but doesn't return state of pin
        # event fires on BOTH i.e. pin transition RISING or FALLING
        # event calls _switch_changed
        # callback doesn't show argument "pin", is that implicit??
        # 20 ms may be too short for app to handle, especially if not running via sudo
        bouncetime_ms = 500
        GPIO.add_event_detect(SWITCH_PIN, GPIO.BOTH, callback=self._switch_changed, bouncetime=bouncetime_ms)

    def _switch_changed(self, pin):
        """Called by the RPI.GPIO library when the switch pin changes state.
        gets switch state and then calls _switch_callback
        """
        if self._switch_callback is not None:
            # read switch
            switch_state = GPIO.input(SWITCH_PIN)
            # now that we have switch_state, can call _switch_callback
            self._switch_callback(switch_state)

    # renamed from on_switch_change
    def configure_switch_callback(self, callback):
        """Sets property _switch_callback, a function that other methods can run when switch changes state.
        Parameter callback: callback function should take one parameter, a boolean representing current switch state
        """
        self._switch_callback = callback

    def configure_temperature_humidity_callback(self, callback):
        """Sets property _temperature_humidity_callback, a function that other methods can run
        Parameter callback: callback function should take two parameters,
        temperature in degrees Celsius and humidity in percent
        """
        self._temperature_humidity_callback = callback

    def _dht_update(self):
        """Main function for DHT update thread.
        Make thread safe to avoid problems with multiple concurrent requests to one sensor.
        Uses lock for thread safety, e.g. avoid race condition 
        if user tries to read _humidity while this method is trying to write it.
        """
        while True:
            with self._lock:
                # Sensor updates every 2 seconds.
                # humidity as a percentage 0 - 100
                # temperature in degrees Celsius
                humidity, temperature = Adafruit_DHT.read_retry(DHT_TYPE, DHT_PIN)
                if self._temperature_humidity_callback is not None:
                    self._temperature_humidity_callback(temperature, humidity)

            delay_seconds = 2.0
            time.sleep(delay_seconds)

    def read_switch(self):
        """returns 1 if switch is high, 0 if switch is low.
        Uses lock for thread safety.
        """
        with self._lock:
            return GPIO.input(SWITCH_PIN)

    def set_led(self, value):
        """Set the LED to the passed in value, True for on, False for off.
        Uses lock for thread safety.
        """
        with self._lock:
            GPIO.output(LED_PIN, value)

