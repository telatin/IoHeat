"""
A script to create a check pattern
on the LED matrix of the SenseHAT
"""
from sense_hat import SenseHat
import random 
from time import sleep

# Import your SenseHAT as an object, we can call it "myHAT"
myHAT =  SenseHat()
myHAT.clear()
color1 = (255, 255,125)
color2 = (0, 0  , 125)

# This is an iteration in the range 0 <= x < 8
for row in range(0, 8):
    print('Row:{}'.format(row))
    # This is a nested iteration in the range 0 <= x < 8
    for col in range(0,8):
        print(' - Col: {}'.format(col))
        # The % operator returns the rest of the integer division
        if (col % 2 and not row % 2) or (row % 2 and not col % 2):
            color = color1
        else:
            color = color2
        
        # Here we light up a pixel using "row" and "col" as coordinates,
        
        myHAT.set_pixel(row, col, color)
        sleep(0.1)