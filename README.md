Steve Baker Beepscore LLC

# Purpose
Record info about making a Raspberry Pi "Thing" for internet of Things.

# References

## Adafrut tutorial

### video
Raspberry Pi & Python Internet 'Thing' pt. 1 with Tony D! @adafruit #LIVE
https://www.youtube.com

### github repository
https://github.com/adafruit/Pi_Internet_Thing_Videos
MIT license

## pip
Use apt-get instead of pip where possible.
If package is not available via apt-get, can use pip
https://www.raspberrypi.org/documentation/linux/software/python.md

## flask
http://flask.pocoo.org/

## html templates
https://html5boilerplate.com/

## RPi.GPIO
https://pypi.python.org/pypi/RPi.GPIO

## Equipment

### Raspberry Pi 2 - Model B - ARMv7 with 1G RAM
http://www.adafruit.com/products/2358

# Results

## Flask

### macos
On macos, with virtual environment active, ran

    pip install flask.
    pip install --upgrade pip

This installed flask to venv, ignored by git.

#### start flask server

    cd webapp
    python main.py

On macos browser go to url http://0.0.0.0:5000/ or http://10.0.0.11:5000/
mac can see "Hello World"
url http://0.0.0.0:5000/foo shows "Achoo Foo!"

### raspberry pi
Cloned repo beepscore/pi-thing, pulled latest changes.

Tried to create virtual environment on pi.

    pyvenv venv

pyvenv command not found

#### install python3-venv
https://www.raspberrypi.org/forums/viewtopic.php?f=32&t=129797

    sudo apt-get install python3-venv
    pyvenv venv
    source ./venv/bin/activate
    (venv) pi@pika:~/beepscore/pi-thing $

#### install flask

    pip install flask

#### start flask server

    cd webapp
    python main.py

On raspberry pi desktop browser go to url http://0.0.0.0:5000/
Pi can see "Hello World"

Fing.app shows pi wifi address is http://10.0.0.19
On macos browser go to url http://10.0.0.19:5000/
mac can see "Hello World"
