#!/usr/bin/env python

# import * to get render_template
from flask import *
app = Flask(__name__)

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
