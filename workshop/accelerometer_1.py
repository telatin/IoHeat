# We import a new function, sleep, that will "pause" for some seconds our script
from time import sleep
from sense_hat import SenseHat
sense = SenseHat()
step_count = 0

# This is an infinite loop, we can break it using Ctrl-C during the script execution

while True:
    step_count = step_count + 1
    acceleration = sense.get_accelerometer_raw()
    print('Step {}: Acceleration {}'.format(step_count,acceleration))
    sleep(1)
