#!/usr/bin/env python

import time

from thing import PiThing


# Instantiate a PiThing
pi_thing = PiThing()

# Get the current switch state
switch = pi_thing.read_switch()
print('Switch: {0}'.format(switch))

def switch_changed(switch_state):
    """function takes one argument, a boolean.
    Can be provided to pi_thing as a callback
    """
    if switch_state:
        print('Switch is ON')
    else:
        print('Switch is OFF')

# tell pi_thing to run switch_changed as a callback
pi_thing.configure_switch_callback(switch_changed)

# Blink the LED forever.
print('Blinking LED (Ctrl-C to stop)...')
while True:
    pi_thing.set_led(True)
    time.sleep(0.1)
    pi_thing.set_led(False)
    time.sleep(0.9)

    humidity = pi_thing.get_humidity()
    temperature = pi_thing.get_temperature()
    print('TemperatureDegreesC: {0:0.2F} Humidity: {1:0.2F}'.format(temperature, humidity))

