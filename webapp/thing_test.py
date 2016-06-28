#!/usr/bin/env python

from thing import PiThing


# Instantiate a PiThing
pi_thing = PiThing()

# Get the current switch state
switch = pi_thing.read_switch()
print('Switch: {0}'.format(switch))

# Blink the LED forever.
print('Blinking LED (Ctrl-C to stop)...')
while True:
    pi_thing.set_led(True)
    time.sleep(0.5)
    pi_thing.set_led(False)
    time.sleep(0.5)
