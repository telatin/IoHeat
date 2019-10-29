# We import a new function, sleep, that will "pause" for some seconds our script
from time import sleep
from sense_hat import SenseHat
sense = SenseHat()
step_count = 0

# This is an infinite loop, we can break it using Ctrl-C during the script execution

while True:
    step_count = step_count + 1
    acceleration = sense.get_accelerometer_raw()
    x = int( acceleration['x'] * 100 )
    y = int( acceleration['y'] * 100 )
    z = int( acceleration['z'] * 100 )

    print('Step {}: Acceleration {} / {} / {}'.format(step_count, x, y, z) )
    sleep(1)
