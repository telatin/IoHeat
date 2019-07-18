#!/usr/bin/env python3
from pprint import pprint
from grove.gpio import GPIO


class GroveRelay(GPIO):
    def __init__(self, pin):
        super(GroveRelay, self).__init__(pin, GPIO.OUT)

    def on(self):
        self.write(1)

    def off(self):
        self.write(0)


Grove = GroveRelay


def main():
    import sys
    import time

    if len(sys.argv) < 2:
        print('Usage: {} pin'.format(sys.argv[0]))
        pin_number=16
    else:
        pin_number=int(sys.argv[1])

    relay = GroveRelay(pin_number)

    print(relay.read())

    while True:
        try:
            relay.on()
            print('After ON: {}'.format(relay.read()))
            time.sleep(1)
            
            relay.off()
            print('After OFF: {}'.format(relay.read()))
            time.sleep(1)

        except KeyboardInterrupt:
            relay.off()
            print("exit")
            exit(1)

if __name__ == '__main__':
    main()
