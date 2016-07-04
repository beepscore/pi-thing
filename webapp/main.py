#!/usr/bin/env python3

# import * to get render_template
from flask import *

import random
import time

from thing import PiThing

"""main.py uses Flask web server for network communications
and PiThing to read and write to raspberry pi gpio pins.
"""

# instantiate flask app
app = Flask(__name__)

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

# endpoint /switch
# Firefox asks if want to save or open with a program
# Chrome works
@app.route("/switch")
def switch():
    # http://flask.pocoo.org/docs/0.11/patterns/streaming/
    def get_switch_values():
        while True:
            # get current switch value 0 or 1
            switch_value = pi_thing.read_switch()

            # server sent event specifies format:
            # data: <value>\n\n
            # http://www.html5rocks.com/en/tutorials/eventsource/basics/
            yield('data: {0}\n\n'.format(switch_value))

            time.sleep(1.0)
    return Response(get_switch_values(), mimetype='text/event-stream')

@app.route("/foo")
def achoo():
    return "Achoo Foo!"

if __name__ == "__main__":
    # listen for connections from any machine on network
    # in browser enter url http://0.0.0.0:5000/
    # set threaed true so flask can use multiple threads
    # this keeps /switch infinite loop "while True" from hogging all execution time
    # also enables app to handle multiple requests
    app.run(host='0.0.0.0', debug=True, threaded=True)
