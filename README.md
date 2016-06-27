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

## flask
http://flask.pocoo.org/

## Equipment

### Raspberry Pi 2 - Model B - ARMv7 with 1G RAM
http://www.adafruit.com/products/2358

# Results

## Flask
On macos, with virtual environment active, ran

    pip install flask.
    pip install --upgrade pip

This installed flask to venv, ignored by git.

## raspberry pi
Cloned repo beepscore/pi-thing, pulled latest changes.

Tried to create virtual environment on pi.

    pyvenv venv

pyvenv command not found
https://www.raspberrypi.org/forums/viewtopic.php?f=32&t=129797

    sudo apt-get install python3-venv
    pyvenv venv
    source ./venv/bin/activate
    (venv) pi@pika:~/beepscore/pi-thing $

### install flask

    pip install flask
