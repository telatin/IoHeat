from time import sleep
from sense_hat import SenseHat
import random 
 
 
sense = SenseHat()

sense.clear()
i = 0


        
last_rotation = -1        
while True:
    
    # Detect the matrix rotation angle from the accelerometer using our own "get_rotation" function
    for event in sense.stick.get_events():
        # Events detected have properties like 'action' (pressed or released) and 'direction' (up, left..)
        if event.action == 'pressed':
            sense.show_letter('?')
        elif event.action == 'released':
            # Generate 
            random_number = random.randint(1,6)
            # and print it to the screen
            sense.show_letter(str(random_number), (0,255,0))
            # The following instruction prints to the terminal (debug)
            print('Event:{} - Number: {}'.format(event, random_number))
    sleep(1)