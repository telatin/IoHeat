"""
A script to generate random patterns
on the LED matrix of the SenseHAT
"""

from sense_hat import SenseHat
import random 
from time import sleep

# Import your SenseHAT as an object, we can call it "myHAT"
myHAT =  SenseHat()
myHAT.clear()

# This is a list [...] of triplets ( , , )
colors = [(0,0,255), (0,255,255), (255,250,250)]

# First we draw a random pattern

# Iteration from 0 to 8 (excluded): each row
for row in range(0, 8):
    print('Row:{}'.format(row))
    # Nested iteration from 0 to 7 for the columns
    for col in range(0,8):
        print(' - Col: {}'.format(col))
        color_index = random.randint(0, len(colors)-1)
        color = colors[color_index]
        myHAT.set_pixel(row, col, color )
sleep(2)
        
# Now we can "fade out" reducing the color values at each step

# FIRST: we define a function "darkening" a color (triplet of values)
def darken(color):
    step = 10
    if color[0] > step:
        color[0] -= step
     
    if color[1] > step:
        color[1] -= step
     
    if color[2] > step:
        color[2] -= step
         
    return color
 

# Second we make a loop that at each iteration darken the "image"
for i in range(0, 50):
    pixel_list = myHAT.get_pixels()
    
    # We create a new list of colors to store the new values
    new_list = []
    
    # We need to get the current status of each LED
    for pixel in pixel_list:
        print(type(pixel))
        # For each pixel we darken the color and store it in new_list
        pixel = darken(pixel)
        new_list.append(pixel)
        
    # Finally we draw the new image    
    myHAT.set_pixels(new_list)
    sleep(0.1)