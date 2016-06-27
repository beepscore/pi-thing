#!/usr/bin/env python

from flask import Flask
app = Flask(__name__)

# default route raspberry pi /
@app.route("/")
def hello():
    return "Hello World!"

@app.route("/foo")
def achoo():
    return "Achoo Foo!"

if __name__ == "__main__":
    # listen for connections from any machine on network
    # in browser enter url http://0.0.0.0:5000/
    app.run(host='0.0.0.0', debug=True)
    pass
