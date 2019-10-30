"""
A script to generate random patterns
on the LED matrix of the SenseHAT
"""
from sense_hat import SenseHat
import random 

# Import your SenseHAT as an object, we can call it "myHAT"
myHAT =  SenseHat()

colors = [(0,0,255), (0,255,255), (0,0,0)]

for row in range(0, 8):
    print('Row:{}'.format(row))
    for col in range(0,8):
        print(' - Col: {}'.format(col))
        color_index = random.randint(0, len(colors)-1)
        color = colors[color_index]
        myHAT.set_pixel(row, col, color )