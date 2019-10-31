"""
This script will read data from the accelerometer every 1 second
printing the data received to the terminal
"""
# We import a new function, sleep, that will "pause" for some seconds our script
from time import sleep
from sense_hat import SenseHat
sense = SenseHat()


# This is an infinite loop, we can break it using Ctrl-C during the script execution
step_count = 0
while True:
    step_count = step_count + 1
    acceleration = sense.get_accelerometer_raw()
    
    # Acceleration is a data structure that has 3 keys ('x', 'y', 'z'), each containing
    # a value (a floating point from 0 to 1)
    print('Step {}: Acceleration {}'.format(step_count,acceleration))
    sleep(1)
