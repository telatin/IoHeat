from sense_hat import SenseHat
from time import sleep

sense = SenseHat()
sense.clear()

gray = [33,66,33]

def lighter(color):
    bright_col = None
    for i in [0,1,2]:
        color[i] += 10
        if color[i] > 255:
            color[i] = 255
    return color
            
last_dir = None
color = None

while True:
    if sense.stick.get_events():
        sense.stick.get_events()
    for event in sense.stick.get_events():
        initial = event.direction[0]
        
        
        
        if last_dir == event.direction[0]:
            color = lighter(color)
            print("[{}] The joystick was {} again {}".format(initial, event.action, event.direction))
        else:
            color = gray.copy()
            print("[{}] The joystick was {} {}".format(initial, event.action, event.direction))
            
        sense.show_letter(initial, color)
        last_dir = event.direction[0]
        