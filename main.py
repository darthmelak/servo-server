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

def is_pizero():
    with open('/proc/device-tree/model') as f:
        model = f.read()
    return model.find("Zero W") != -1

piZero = is_pizero()

HPos = 0      #Sets the initial position
VPos = 0      #Sets the initial position
HStep = 0
VStep = 0
nv = True
led = False

Address = ''
refreshRate = 0.05

@get("/")
def index():
    global Address,nv,led
    return template("index", address=Address, nv=nv, led=led)

@route("/<filename>")
def server_static(filename):
    return static_file(filename, root='./')

@post("/cmd")
def cmd():
    global HStep,VStep,nv,led,LedSwitch
    code = request.body.read().decode()
    print ("code ", code)
    # speed = request.POST.get('speed')
    # print(code)
    # if(speed != None):
        # print(speed)

    if code == "stop":
        HStep = 0
        VStep = 0
        print("stop")
    elif code == "up":
        VStep = 1
        print("up")
    elif code == "down":
        VStep = -1
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
                GPIO.output(40, GPIO.HIGH)
            else:
                os.system("nvstart")
    elif code == "nvstop":
        if(nv):
            nv = False
            if(piZero):
                GPIO.output(40, GPIO.LOW)
            else:
                os.system("nvstop")
    elif code == "ledswitch":
        LedSwitch.toggle()
        led = not led
    return "OK"

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
        GPIO.output(40, GPIO.HIGH)

    t = threading.Timer(refreshRate, timerfunc)
    t.setDaemon(True)
    t.start()

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))
    Address = s.getsockname()[0]

    run(host=Address, port="8000")
except Exception as err:
    print("\nServer exiting.")
    print(err)
    exit()
