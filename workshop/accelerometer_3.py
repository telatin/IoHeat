"""
A script that will light a pixel of the LED matrix
according to gravity (i.e. gyroscope information)
this will print a trace of visited pixels
UNDER DEVELOPMENT
"""

# We import a new function, sleep, that will "pause" for some seconds our script
from time import sleep
from sense_hat import SenseHat

sense = SenseHat()
positions = []

def print_trace(pos_list):
    lux = 0
    sense.clear()
    for coord in pos_list:
        if (lux < 250):
            lux += 50
        print('[trace:{}] intensity: {}'.format(coord, lux))
        sense.set_pixel(coord[0], coord[1], (lux,lux,lux) )
    
        


# We initialize a counter setting it to 0
step_count = 0

# This is an infinite loop, we can break it using Ctrl-C during the script execution
while True:
    # We increment the counter by 1 (to know what cycle of the loop we are in)
    step_count = step_count + 1
    
    # We retrieve the position and store it in the "acceleration" dictionary
    acceleration = sense.get_accelerometer_raw()
    sense.clear()
    
    # We can multiply and round the coordinates
    x = int( acceleration['x'] * 100 )
    y = int( acceleration['y'] * 100 )
    z = int( acceleration['z'] * 100 )
    
    # Each pixel of the display has a coordinate from 0 to 7
    xcoord = 3 + int( acceleration['x'] * 4 )
    ycoord = 3 + int( acceleration['y'] * 4 )
    
    if len(positions) == 0 or (xcoord != positions[-1][0] and ycoord != positions[-1][1]):
        positions.append( (xcoord, ycoord) )
        
    if len(positions) > 5:
        positions.pop()
        
    print_trace(positions)
    sense.set_pixel(xcoord, ycoord, (255,0,0) )

    
    # We can always print some "debug" info on the terminal
    print('[Step {}]'.format(step_count))
    print('Acceleration {} / {} / {}'.format(x, y, z) )
    print('             {} / {} (screen)'.format(xcoord, ycoord))
    sleep(1)