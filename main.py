#!/usr/bin/python3
# -*- coding:utf-8 -*-
from bottle import get,post,run,route,request,template,static_file
import threading
import socket
import time

HStep = 0      #Sets the initial step length
VStep = 0      #Sets the initial step length

Address = ''
start = int(time.time())

@get("/")
def index():
    global Address
    return template("index", address=Address)

@route('/<filename>')
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
        VStep = -5
        print("up")
    elif code == "down":
        VStep = 5
        print("down")
    elif code == "left":
        HStep = 5
        print("left")
    elif code == "right":
        HStep = -5
        print("right")
    return "OK"

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))
    Address = s.getsockname()[0]

    run(host=Address, port="8000")
except:
    print("\nServer exiting.")
    exit()
