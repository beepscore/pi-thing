Steve Baker Beepscore LLC

# Purpose
Record info about making a Raspberry Pi "Thing" for internet of Things.

# References

## Adafrut tutorial

### video
#### Part 1 use request/response, led and switch
Raspberry Pi & Python Internet 'Thing' pt. 1 with Tony D! @adafruit #LIVE
https://www.youtube.com
#### Part 2 use server sent events
#### Part 3 use digital humidity temperature sensor and chart.js
https://www.youtube.com/watch?v=oeGI5OMAheg
#### Part 4 use web socket via socketIO
https://www.youtube.com/watch?v=cAymVFeoz3s

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

## WebSocket
Enables bidirectional open connection between server and client.  
Handshakes over HTTP, then requests upgrade to WebSocket protocol.  
 ws:// - not encrypted, port 80 (same port as http://)  
wss:// - encrypted, port 443 (same port as https://)  

https://en.wikipedia.org/wiki/WebSocket  
http://www.html5rocks.com/en/tutorials/#websockets  

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

### digital humidity temperature (DHT) sensor
AM2302 (wired DHT22)  
https://www.adafruit.com/products/393  
Uses timing to read, not i2c or spi.  
https://learn.adafruit.com/dht-humidity-sensing-on-raspberry-pi-with-gdocs-logging/overview  
https://github.com/adafruit/Adafruit_Python_DHT
3 volts - red  (AM2302 already has 4.7 kohm resistor built in)
ground - black wire
pin 18 - data, yellow

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

Note: when flask debug server is connected to a browser via server sent events,
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

####### pihole

    http://10.0.0.17:5000/


# Appendix - Install DHT library
In pi_thing, activated venv.  

As described at https://github.com/adafruit/Adafruit_Python_DHT

    sudo apt-get update
    sudo apt-get install build-essential python-dev

On pi, cd out of project directory pi_thing to parent directory.

    git clone https://github.com/adafruit/Adafruit_Python_DHT.git

Later I forked the library. On pihole I cloned fork.

    git clone https://github.com/beepscore/Adafruit_Python_DHT.git

## cd to pi_thing, activate venv, and run setup.py
    pi@pika:~/beepscore $ cd pi_thing
    pi@pika:~/beepscore/pi_thing $ source venv/bin/activate

Try python3, not python

    (venv) pi@pika:~/beepscore/pi_thing $ python3 ../Adafruit_Python_DHT/setup.py install

### this failed as shown below
    running install
    running bdist_egg
    running egg_info
    creating Adafruit_DHT.egg-info
    writing top-level names to Adafruit_DHT.egg-info/top_level.txt
    writing Adafruit_DHT.egg-info/PKG-INFO
    writing dependency_links to Adafruit_DHT.egg-info/dependency_links.txt
    writing manifest file 'Adafruit_DHT.egg-info/SOURCES.txt'
    warning: manifest_maker: standard file 'setup.py' not found

    reading manifest file 'Adafruit_DHT.egg-info/SOURCES.txt'
    writing manifest file 'Adafruit_DHT.egg-info/SOURCES.txt'
    installing library code to build/bdist.linux-armv7l/egg
    running install_lib
    running build_ext
    building 'Adafruit_DHT.Raspberry_Pi_2_Driver' extension
    creating build
    creating build/temp.linux-armv7l-3.4
    creating build/temp.linux-armv7l-3.4/source
    creating build/temp.linux-armv7l-3.4/source/Raspberry_Pi_2
    arm-linux-gnueabihf-gcc -pthread -DNDEBUG -g -fwrapv -O2 -Wall -Wstrict-prototypes -g -fstack-protector-strong -Wformat -Werror=format-security -D_FORTIFY_SOURCE=2 -fPIC -I/home/pi/beepscore/pi_thing/venv/include -I/usr/include/python3.4m -c source/_Raspberry_Pi_2_Driver.c -o build/temp.linux-armv7l-3.4/source/_Raspberry_Pi_2_Driver.o -std=gnu99
    arm-linux-gnueabihf-gcc: error: source/_Raspberry_Pi_2_Driver.c: No such file or directory
    arm-linux-gnueabihf-gcc: fatal error: no input files
    compilation terminated.
    error: command 'arm-linux-gnueabihf-gcc' failed with exit status 4

## With pi_thing venv active, cd to Adafruit_Python_DHT and run setup.py
    (venv) pi@pika:~/beepscore/pi_thing $ cd ..
    (venv) pi@pika:~/beepscore $ ls
    Adafruit_Python_DHT  pi_cam  pi_thing
    (venv) pi@pika:~/beepscore $ cd Adafruit_Python_DHT/
    (venv) pi@pika:~/beepscore/Adafruit_Python_DHT $ python3 setup.py install
    ...
    Installed /home/pi/beepscore/pi_thing/venv/lib/python3.4/site-packages/Adafruit_DHT-1.3.0-py3.4-linux-armv7l.egg
    Processing dependencies for Adafruit-DHT==1.3.0
    Finished processing dependencies for Adafruit-DHT==1.3.0

This installed DHT library to project venv as desired.

    pi_thing/venv/lib/python3.4/site-packages/Adafruit_DHT-1.3.0-py3.4-linux-armv7l.egg

Note RPi.GPIO is also installed to pi_thing/venv/lib/python3.4/site-packages

## install python-smbus as shown on video, not shown on web site
Maybe don't need this anymore?

    sudo apt-get install python-dev python-smbus

## Check install
Use library simpletest.py to check we can use library and sensor.  
Whenever adding a sensor, best practice check sensor and library work before adding more project code.  

### git branch
Outside project directory pi_thing, in sibling directory Adafruit_Python_DHT, make a new branch.  

    git branch beepscore

### edit Adafruit_Python_DHT/examples/simpletest.py

#### change sensor
  27 # sensor = Adafruit_DHT.DHT22
+  28 sensor = Adafruit_DHT.AM2302

#### comment out beaglebone, set to raspberry pi pin 18
   30 # Example using a Beaglebone Black with DHT sensor
   31 # connected to pin P8_11.
!  32 # pin = 'P8_11'
   33
   34 # Example using a Raspberry Pi with DHT sensor
   35 # connected to GPIO23.
   36 #pin = 23
+  37 pin = 18

#### git commit changes

On pihole, in Adafruit_Python_DHT ran sudo python setup.py install
This generated a binary file dist/Adafruit_DHT-1.3.0-py2.7-linux-armv7l.egg.
On pihole committed to git.
Then I manually generated a patch file, used Filezilla to copy to mac.

##### check before apply
cd Adafruit_Python_DHT
git branch beepscore
git apply --check ~/Desktop/0001-Ran-sudo-python-setup.py-install.patch

git am --signoff < ~/Desktop/0001-Ran-sudo-python-setup.py-install.patch

## On pihole run examples

### AdafruitDHT.py
pi@pihole:~/beepscore/Adafruit_Python_DHT/examples $ sudo ./AdafruitDHT.py 2302 18
Temp=25.4*  Humidity=57.5%

### simpletest.py
pi@pihole:~/beepscore/Adafruit_Python_DHT/examples $ python simpletest.py
Temp=24.9*C  Humidity=83.0%

## Changed endpoint /switch to /thing
video  Raspberry Pi & Python Internet 'Thing' Pt. 3 with Tony D! @adafruit
0:00 - 1:05

### thing_test.py
    source venv/bin/activate
    (venv) pi@pihole:~/beepscore/pi_thing $ python3 webapp/thing_test.py

### pihole couldn't see flask
re-ran venv setup, that fixed problem

    source venv/bin/activate

video suggests run as sudo, but seems to be working without that

    python3 webapp/main.py

In brower entered 10.0.0.17:5000

tools/web developer/web console shows output stream

    data: {"humidity": 56.599998474121094, "switch": 0, "temperature": 24.100000381469727}
    data: {"humidity": 56.599998474121094, "switch": 0, "temperature": 24.100000381469727}

