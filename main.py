#!/usr/bin/python3
# -*- coding:utf-8 -*-
from bottle import get,post,run,route,request,template,static_file
from servo import RanServo
import threading
import socket
import os

HPos = 0      #Sets the initial position
VPos = 0      #Sets the initial position
HStep = 0
VStep = 0

Address = ''
refreshRate = 0.05

@get("/")
def index():
    global Address
    return template("index", address=Address)

@route("/<filename>")
def server_static(filename):
    return static_file(filename, root='./')

@post("/cmd")
def cmd():
    global HStep,VStep
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
        os.system("nvstart")
    elif code == "nvstop":
        os.system("nvstop")
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
    VServo = RanServo(27)
    HServo = RanServo(17)

    t = threading.Timer(refreshRate, timerfunc)
    t.setDaemon(True)
    t.start()

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))
    Address = s.getsockname()[0]

    run(host=Address, port="8000")
except:
    print("\nServer exiting.")
    exit()
