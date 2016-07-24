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

# use url last component to pass argument led_state to the server
# name of defined function doesn't matter
@app.route("/led/<int:led_state>", methods=['POST'])
def led(led_state):
    if led_state == 0:
        pi_thing.set_led(False)
    elif led_state == 1:
        pi_thing.set_led(True)
    else:
        # http status code 400 bad request error
        return ('Unknown LED state!', 400)
    return ('', 204)

# endpoint /thing
# Firefox asks if want to save or open with a program
# Chrome works
@app.route("/thing")
def thing():

    # http://flask.pocoo.org/docs/0.11/patterns/streaming/
    def read_thing_state():

        while True:
            # python dictionary
            thing_state = {
                    'switch': pi_thing.read_switch(),
                    'temperature': pi_thing.get_temperature(),
                    'humidity': pi_thing.get_humidity()
                    }

            # convert python dictionary to json string
            # dumps() can serialize either dictionary or array
            thing_state_json = json.dumps(thing_state)

            # server sent event specifies format:
            # data: <value>\n\n
            # http://www.html5rocks.com/en/tutorials/eventsource/basics/
            yield 'data: {0}\n\n'.format(thing_state_json)

            time.sleep(1.0)

    return Response(read_thing_state(), mimetype='text/event-stream')

@app.route("/foo")
def achoo():
    return "Achoo Foo!"

if __name__ == "__main__":
    # Listen for connections from any machine on network
    # In browser enter url http://0.0.0.0:5000/
    # Set threaded true so flask can use multiple threads.
    # Without threading, /switch infinite loop "while True" can hog all execution time,
    # starving led code from running.
    # Multiple threads also enable app to handle multiple requests.

    # start flask development server
    socketio.run(app, host='0.0.0.0', debug=True)
