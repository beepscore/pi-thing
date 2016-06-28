#!/usr/bin/env python

from thing import PiThing


# Instantiate a PiThing
pi_thing = PiThing()

# Get the current switch state
switch = pi_thing.read_switch()
print('Switch: {0}'.format(switch))
