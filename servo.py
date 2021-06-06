#!/usr/bin/python3

from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import Device, Servo

corrections = {
    17: 0.24,
    27: 0.33
}

class RanServo:
    servo = 0

    def __init__(self, gpio):
        Device.pin_factory = PiGPIOFactory()

        correction = corrections[gpio]
        maxPw=(2.0+correction)/1000
        minPw=(1.0-correction)/1000

        self.servo = Servo(gpio, min_pulse_width=minPw, max_pulse_width=maxPw)

    def setVal(self, value):
        self.servo.value = value

    def getVal(self):
        return self.servo.value

    def toDegree(self, degree):
        if degree > 90:
            degree = 90
        if degree < -90:
            degree = -90

        self.setVal(degree / 90)
