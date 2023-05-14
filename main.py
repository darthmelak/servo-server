#!/usr/bin/python3
# -*- coding:utf-8 -*-
from bottle import get,post,run,route,request,template,static_file
from servo import RanServo
from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import Device, OutputDevice
import RPi.GPIO as GPIO
import threading
import socket
import os
import sys

def is_pizero():
    with open('/proc/device-tree/model') as f:
        model = f.read()
    return model.find("Zero W") != -1

def loadStatic(file):
    with open("static/" + file) as f:
        return f.read()

piZero = is_pizero()

HPos = 0      #Sets the initial position
VPos = 0      #Sets the initial position
HStep = 0
VStep = 0
nv = True
led = False

devMode = True if (len(sys.argv) > 1 and sys.argv[1] == "dev") else False
Address = ''
refreshRate = 0.05

style = loadStatic("style.css")
script = loadStatic("script.js")

@get("/")
def index():
    global Address,nv,led,style,script,devMode
    return template("template/index", address=Address, nv=nv, led=led, style=style, script=script, dev=devMode)

@route("/<filename>")
def server_static(filename):
    return static_file(filename, root='static/')

@post("/cmd")
def cmd():
    global HStep,VStep,nv,led,LedSwitch
    code = request.body.read().decode()
    print ("code ", code)

    if code == "stop":
        HStep = 0
        VStep = 0
        print("stop")
    elif code == "up":
        VStep = -1
        print("up")
    elif code == "down":
        VStep = 1
        print("down")
    elif code == "left":
        HStep = -1
        print("left")
    elif code == "right":
        HStep = 1
        print("right")
    elif code == "nvstart":
        if(not nv):
            nv = True
            if(piZero):
                GPIO.output(40, GPIO.LOW)
            else:
                os.system("nvstart")
    elif code == "nvstop":
        if(nv):
            nv = False
            if(piZero):
                GPIO.output(40, GPIO.HIGH)
            else:
                os.system("nvstop")
    elif code == "ledswitch":
        LedSwitch.toggle()
        led = not led
    return "OK"

@post("/speed")
def speed():
    global HStep,VStep
    req = request.json
    HStep = req.get("stepX")
    VStep = req.get("stepY")

    return "{H} {V}".format(H = HStep, V = VStep)

def timerfunc():
    global HPos,VPos,HStep,VStep,HServo,VServo,refreshRate
    
    if(HStep != 0):
        HPos += HStep
        if(HPos > 90): 
            HPos = 90
        if(HPos < -90):
            HPos = -90
    HServo.toDegree(HPos)

    if(VStep != 0):
        VPos += VStep
        if(VPos > 90): 
            VPos = 90
        if(VPos < -90):
            VPos = -90
    VServo.toDegree(VPos)

    global t        #Notice: use global variable!
    t = threading.Timer(refreshRate, timerfunc)
    t.start()

try:
    Device.pin_factory = PiGPIOFactory()
    LedSwitch = OutputDevice(22)

    VServo = RanServo(17)
    HServo = RanServo(27)

    if (piZero):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(40, GPIO.OUT)
        GPIO.output(40, GPIO.LOW)

    t = threading.Timer(refreshRate, timerfunc)
    t.setDaemon(True)
    t.start()

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))
    Address = s.getsockname()[0]

    run(host=Address, port="8000", debug=devMode)
except Exception as err:
    print("\nServer exiting.")
    print(err)
    exit()
