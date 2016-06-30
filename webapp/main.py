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
    return render_template('index.html')

@app.route("/foo")
def achoo():
    return "Achoo Foo!"

if __name__ == "__main__":
    # listen for connections from any machine on network
    # in browser enter url http://0.0.0.0:5000/
    app.run(host='0.0.0.0', debug=True)
    pass
