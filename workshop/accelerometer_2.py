# We import a new function, sleep, that will "pause" for some seconds our script
from time import sleep
from sense_hat import SenseHat
sense = SenseHat()
step_count = 0

# This is an infinite loop, we can break it using Ctrl-C during the script execution

while True:
    step_count = step_count + 1
    acceleration = sense.get_accelerometer_raw()
    sense.clear()
    
    # We can multiply and round the coordinates
    x = int( acceleration['x'] * 100 )
    y = int( acceleration['y'] * 100 )
    z = int( acceleration['z'] * 100 )
    
    # Each pixel of the display has a coordinate from 0 to 7
    xcoord = 3 + int( acceleration['x'] * 4 )
    ycoord = 3 + int( acceleration['y'] * 4 )
    sense.set_pixel(xcoord, ycoord, (0,255,255) )
    
    # We can always print some "debug" info on the terminal
    print('[Step {}]'.format(step_count))
    print('Acceleration {} / {} / {}'.format(x, y, z) )
    print('             {} / {} (screen)'.format(xcoord, ycoord))
    sleep(1)
