#!/usr/bin/env python3

# import * to get render_template
from flask import *
from flask_socketio import SocketIO

import json
import random
import time

from thing import PiThing

"""main.py uses Flask web server for network communications
and PiThing to read and write to raspberry pi gpio pins.
"""

# instantiate flask app
app = Flask(__name__)
# can use SECRET_KEY to increase security
#app.config['SECRET_KEY'] = 'secret!'

# On flask development server, "WebSocket transport not available"
# must fall back to long polling
# https://flask-socketio.readthedocs.io/en/latest/
socketio = SocketIO(app)

# instantiate pi_thing as a global variable
pi_thing = PiThing()

# default route raspberry pi /
@app.route("/")
def index():
    # get current switch value
    switch_value = pi_thing.read_switch()
    # render index.html, passing in switch_value
    return render_template('index.html', switch=switch_value)

@socketio.on('change_led')
def change_led(led_state):
    if led_state == 'off':
        pi_thing.set_led(False)
    elif led_state == 'on':
        pi_thing.set_led(True)

@app.route("/foo")
def achoo():
    return "Achoo Foo!"

# Internal callback that will be called when the switch changes state.
def switch_changed(switch_state):
    # Broadcast a switch_changed event.
    socketio.emit('switch_changed', { 'switch': switch_state })

def temperature_humidity_changed(temperature, humidity):
    # Broadcast a temperature_humidity_changed event.
    socketio.emit('temperature_humidity_changed', { 'temperature': temperature,
        'humidity': humidity})

if __name__ == "__main__":

    # Register callbacks
    # pi_thing will run switch_changed as a callback
    pi_thing.configure_switch_callback(switch_changed)
    # pi_thing will run temperature_humidity_changed as a callback
    pi_thing.configure_temperature_humidity_callback(temperature_humidity_changed)

    # Listen for connections from any machine on network
    # In browser enter url http://0.0.0.0:5000/
    # Set threaded true so flask can use multiple threads.
    # Without threading, /switch infinite loop "while True" can hog all execution time,
    # starving led code from running.
    # Multiple threads also enable app to handle multiple requests.

    # start flask development server
    socketio.run(app, host='0.0.0.0', debug=True)
