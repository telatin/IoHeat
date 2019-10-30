"""
A script to create a gradient
on the LED matrix of the SenseHAT
"""
from sense_hat import SenseHat
import random 
from time import sleep

# Import your SenseHAT as an object, we can call it "myHAT"
myHAT =  SenseHat()
myHAT.clear()

intensity3 = 0  # Try changing to 255

# This is an iteration in the range 0 <= x < 8
for row in range(0, 8):
    print('Row:{}'.format(row))
    # This is a nested iteration in the range 0 <= x < 8
    for col in range(0,8):
        
        # we can blend a color according to the coordinates
        intensity1 = int( 255 * row/8)
        intensity2 = int( 255 * col/8)
        color = (intensity1, intensity2, intensity3)
        
        
        # Here we light up a pixel using "row" and "col" as coordinates,
        myHAT.set_pixel(row, col, color)
        sleep(0.02)
        print(' - Col: {} ({},{},{})'.format(col, intensity1, intensity2, 0))