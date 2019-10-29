from sense_hat import SenseHat
from time import sleep

sense = SenseHat()
while True:
    if sense.stick.get_events():
        sense.stick.get_events()
    for event in sense.stick.get_events():
        initial = event.direction[0]
        print("[{}] The joystick was {} {}".format(initial, event.action, event.direction))
        
        sense.show_letter(initial)