"""
A script that will roll a die every time the user uses the joystick

"""

from time import sleep
from sense_hat import SenseHat
import random 
 
 
# Usual initialization of our SenseHat
sense = SenseHat()
sense.clear()


# We start an infinite loop to "listen" to joystick events    
while True:
    
    # we collect the listened events in the 'event' variable
    for event in sense.stick.get_events():
        # Events detected have properties like 'action' (pressed or released) and 'direction' (up, left..)

        # If the action is 'pressed' we print a '?', when it's released with will print the number
        if event.action == 'pressed':
            sense.show_letter('?')
        elif event.action == 'released':
            # Generate a random number
            random_number = random.randint(1,6)
            # and print it to the screen
            sense.show_letter(str(random_number), (0,255,0))
            # The following instruction prints to the terminal (debug)
            print('Event:{} - Number: {}'.format(event, random_number))
            
    sleep(1)