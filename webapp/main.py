#!/usr/bin/env python

# import * to get render_template
from flask import *

from thing import PiThing

# instantiate flask app
app = Flask(__name__)

# instantiate pi_thing as a global variable
pi_thing = PiThing()

# default route raspberry pi /
@app.route("/")
def hello():
    # get current switch value
    switch_value = pi_thing.read_switch()
    # render index.html, passing in switch_value
    return render_template('index.html', switch=switch_value)

@app.route("/foo")
def achoo():
    return "Achoo Foo!"

if __name__ == "__main__":
    # listen for connections from any machine on network
    # in browser enter url http://0.0.0.0:5000/
    app.run(host='0.0.0.0', debug=True)
    pass
