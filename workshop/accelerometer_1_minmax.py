"""
This version will keep track of the minimum and maximum value
received from the accelerometer
"""
# We import a new function, sleep, that will "pause" for some seconds our script
from time import sleep
from sense_hat import SenseHat
sense = SenseHat()

# Here we create to "dictionaries" to store our minimi and maximi
Min = {}
Max = {}

# This is an infinite loop, we can break it using Ctrl-C during the script execution
step_count = 0
while True:
    step_count = step_count + 1
    acceleration = sense.get_accelerometer_raw()

    print('Step {}: Acceleration {}'.format(step_count,acceleration))
    
    # Check the stored min/max values and in case update them
    for axis in ['x', 'y', 'z']:
        if not axis in Min:
            Min[axis] = round(acceleration[axis], 2)
        elif Min[axis] > acceleration[axis]:
            Min[axis] = round(acceleration[axis], 2)
            
        if not axis in Max:
            Max[axis] = round(acceleration[axis], 2)
        elif Max[axis] < acceleration[axis]:
            Max[axis] = round(acceleration[axis], 2)
        print('\t {}: min={}\tmax={}'.format(axis, Min[axis], Max[axis]))
        
    # Acceleration is a data structure that has 3 keys ('x', 'y', 'z'), each containing
    # a value (a floating point from 0 to 1)
    
    
    
    sleep(1)
