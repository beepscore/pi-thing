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
### pin numbering
set to BCM to match pi cobbler
https://sourceforge.net/p/raspberry-gpio-python/wiki/BasicUsage/

## systemd
systemd: Writing and Enabling a Service
https://learn.adafruit.com/running-programs-automatically-on-your-tiny-computer/systemd-writing-and-enabling-a-service

## Stream Updates with Server-Sent Events
http://www.html5rocks.com/en/tutorials/eventsource/basics/
Enables server to continually push to client.
Client does not have to poll server.

## Websockets
http://www.html5rocks.com/en/tutorials/#websockets
Enables bidirectional open connection between server and client.

## Introduction to Service Worker
http://www.html5rocks.com/en/tutorials/service-worker/introduction/

## Equipment

### Raspberry Pi 2 - Model B - ARMv7 with 1G RAM
http://www.adafruit.com/products/2358

### Pi Cobbler +
https://www.adafruit.com/products/2029
Uses BCM numbering, not board numbering
https://www.raspberrypi.org/forums/viewtopic.php?t=103382

### led (long leg is anode +, short leg on flat side is cathode -
### Resistor 1 kohm
### switch spdt

# Results

## Raspberry Pi inputs/outputs
Pin numbers match Pi Cobbler
### output LED + resistor
BCM pin 23 -> LED anode -> LED cathode -> 560 ohm resistor -> ground

### input slide switch
pin 24 -> pole (middle leg)
one throw 3.3V
one throw gnd

## ssh
Connect to rpi via ssh, either by ethernet cable + sharing/internet sharing or via wifi.
Note: If flask app encounters an error, flask server may stop.
In addition, pi may disconnect from ssh session with mac, even if using ethernet!
I don't know why this happens.

## Flask

### raspberry pi
Cloned repo beepscore/pi-thing, pulled latest changes.

Tried to create virtual environment on pi.

    pyvenv venv

pyvenv command not found
venv wasn't working. To start over, I deleted directory venv
http://stackoverflow.com/questions/31252791/flask-importerror-no-module-named-flask?lq=1

#### install python3-venv
https://www.raspberrypi.org/forums/viewtopic.php?f=32&t=129797

    sudo apt-get install python3-venv

    python3 -m venv venv
    source ./venv/bin/activate
    (venv) pi@pika:~/beepscore/pi_thing $ which python3
    /home/pi/beepscore/pi_thing/venv/bin/python3

==> venv is working!

#### install packages

    pip3 install flask
    pip3 install RPi.GPIO

#### start flask server

    cd <project root directory>
    source ./venv/bin/activate
    python3 webapp/main.py

If main.py starts with

    #!/usr/bin/env python3

can start via

    cd <project root directory>
    source ./venv/bin/activate
    webapp/main.py

#### browser

##### url

###### rpi desktop
url http://0.0.0.0:5000/

###### local network
Can use browswer on any machine on local network
Fing.app shows pi wifi address

####### USB wifi adapter, body length ~ 6 mm

    http://10.0.0.19

####### USB wifi adapter "OURLINK", body length ~ 30 mm
Use adapter with larger antenna to attempt to reduce disconnect errors e.g. 'broken pipe'.

    http://10.0.0.20

##### server response
http://10.0.0.19:5000/  
Returns rendered index.html "Hello World"

http://0.0.0.0:5000/foo  
Returns "Achoo Foo!"

#### stop flask server

    ctrl-c

Note: when flask debug server is connected to a browser via server sent event,
ctrl-c will not completely stop server until browser is closed or process is killed.

Can see this in terminal by running process status and filtering for python

    ps aux | grep python

Shows main.py

Close browser to stop process. Re-run process status

    ps aux | grep python

Doesn't show main.py

#### safely shutdown raspberry pi
avoid corrupting SD card

    sudo halt

to reboot

    sudo reboot

### POST request
#### curl
empty data
curl --data '' http://10.0.0.19:5000/led/1

#### Postman
http://10.0.0.19:5000/led/1
body form-data key:data value:''

### How app works
Developer runs main.py to start flask app and instantiate pi_thing.  
User uses browser to make a GET request to app root url http://10.0.0.19:5000/  
flask app main.py routes request to method index()  
flask app main.py routes request to matching @app.route "/".  
The function name under the  does not matter, but here it is index().  
index() uses pi_thing to read switch state  
index() renders template/index.html using switch value.  
flask app responds to GET request by sending rendered index.html
Rendered index.html includes buttons with ids, and javascript from source thing.js
javascript has jquery onclick listeners for buttons.
If user clicks a button in browser, click listener logs the click  
and sends a POST request to server /led to turn led on or off.  

flask app main.py routes request to matching @app.route "/led/<int:led_state>".  
The function name under the  does not matter, but here it is led().  
led() uses pi_thing to set led state  

### systemd
Raspbian Jessie includes systemd, can be used to start a service  
to run a web server running when pi boots.
#### How to activate virtual environment before running main.py?

# Appendix - Running flask on macos
mac can run earliest version of webapp without RPi.GPIO.  

## install
On macos, with virtual environment active, ran

    pip install flask
    pip install --upgrade pip

This installed flask to venv, ignored by git.

## start flask server

    cd <project root directory>
    source ./venv/bin/activate
    python3 webapp/main.py

If main.py starts with

    #!/usr/bin/env python3

can start via

    webapp/main.py

## browser
When macos is running flask, on mac browser go to url

    http://0.0.0.0:5000/
or
    http://10.0.0.11:5000/

