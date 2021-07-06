#!/usr/bin/python3

from servo import RanServo
from time import sleep
import sys

def main(argv):
    try:
        gpio = 27 if argv[0] == 'v' else 17
        degree = int(argv[1])

        servo = RanServo(gpio)
        servo.toDegree(degree)

        print('GPIO: %d value: %f' % (gpio, servo.getVal()))

        for i in list(range(4)):
            servo.toDegree(degree)
            sleep(0.1)

    except IndexError:
        print('servo.py <axis v or h> <degree -90 -> 90>')
        sys.exit(2)

if __name__ == "__main__":
    main(sys.argv[1:])
