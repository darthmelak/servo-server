#!/usr/bin/python3

# note:

from gpiozero import OutputDevice
import sys

def main(argv):
    try:
        gpio = int(argv[0])
        state = int(argv[1])

        device = OutputDevice(gpio)

        if state == 1:
            device.on()
            print('GPIO: %d on' % (gpio))
        else:
            device.off()
            print('GPIO: %d off' % (gpio))

        input('Press any kay to stop.')

    except IndexError:
        print('gpio.py <nr> <state>')
        sys.exit(2)

if __name__ == "__main__":
    main(sys.argv[1:])
