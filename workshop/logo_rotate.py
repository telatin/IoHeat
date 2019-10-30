"""
A script to print an image using a list of colors
(our LED matrix can be thought as a list of 8x8 values)
"""

from sense_hat import SenseHat
import random 

sense = SenseHat()

sense.clear()

# We define a list of colors 
X = (255, 0, 0)       # red
O = (0, 0, 0)         # black
H = (255, 155, 155)   # pink
    
# We define 'logo' as a list of triplets
# We will use the defined triplets (X, O, H) to make
# the code clearer
logo = [
    O, H, H, O, H, H, O, O,
    H, X, X, H, X, X, H, O,
    H, X, X, X, X, X, H, O,
    H, X, X, X, X, X, H, O,
    O, H, X, X, X, H, O, O,
    O, O, H, X, H, O, O, O,
    O, O, O, H, O, O, O, O,
    O, O, O, O, O, O, O, O,
]

if len(logo) != 64: 
    print("The logo must be a list of 64 values")
    exit()

angles = [0, 90, 180, 270]


for angle in angles:
    print("Now displaying the logo with r={}°".format(angle))
    sense.set_rotation(angle)
    sense.set_pixels(logo)
    sleep(1)
    