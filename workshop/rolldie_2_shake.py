"""
A script that will roll a die every time the user flip 
the LED matrix vertically.
Put the matrix horizontally to rest.
This version will print a number if the device is "shaked" i.e. checking
the strength of the motion
"""
from time import sleep
from sense_hat import SenseHat
import random 


def splash_screen():    
    for i in range(1,7):
        print_die(i)
        sleep(0.31)
    sense.clear()
    
def print_die(number):
    
    # "X" is the white color used for the dots
    X = (255, 255, 255)
    x = (100, 100, 100)
 
    
    # Here is a list of background colors
    backgrounds = [(0, 55, 0), (0, 55, 55), (   0, 0, 55),
                   (55, 0, 55), (55, 0, 55) ]
    
    # If the number is 6 we want a red background
    if number == 6:
        O = ( 100, 0, 0)
    else:
        O = backgrounds[random.randint(0,len(backgrounds)-1) ]
    
    # we make a list of matrices, one per "die face"
    numbers = [
         [
        O, O, O, O, O, O, O, O,
        O, O, O, O, O, O, O, O,
        O, O, O, O, O, O, O, O,
        O, O, O, X, X, O, O, O,
        O, O, O, X, X, O, O, O,
        O, O, O, O, O, O, O, O,
        O, O, O, O, O, O, O, O,
        O, O, O, O, O, O, O, O
        ],
         
        [
        O, O, O, O, O, O, O, O,
        O, X, X, O, O, O, O, O,
        O, X, X, O, O, O, O, O,
        O, O, O, O, O, O, O, O,
        O, O, O, O, O, O, O, O,
        O, O, O, O, O, X, X, O,
        O, O, O, O, O, X, X, O,
        O, O, O, O, O, O, O, O
        ],
         
                  
        [
        O, O, O, O, O, O, O, O,
        O, X, X, O, O, O, O, O,
        O, X, X, O, O, O, O, O,
        O, O, O, X, X, O, O, O,
        O, O, O, X, X, O, O, O,
        O, O, O, O, O, X, X, O,
        O, O, O, O, O, X, X, O,
        O, O, O, O, O, O, O, O
        ],
         
                  
        [
        O, O, O, O, O, O, O, O,
        O, X, X, O, O, X, X, O,
        O, X, X, O, O, X, X, O,
        O, O, O, O, O, O, O, O,
        O, O, O, O, O, O, O, O,
        O, X, X, O, O, X, X, O,
        O, X, X, O, O, X, X, O,
        O, O, O, O, O, O, O, O
        ],
         
                  
        [
        O, O, O, O, O, O, O, O,
        O, X, X, O, O, X, X, O,
        O, x, x, O, O, O, O, O,
        O, O, O, x, x, O, O, O,
        O, O, O, X, X, O, O, O,
        O, x, x, O, O, x, x, O,
        O, X, X, O, O, X, X, O,
        O, O, O, O, O, O, O, O
        ],
         
                  
        [
        O, O, O, O, O, O, O, O,
        O, X, X, O, O, X, X, O,
        O, O, O, O, O, O, O, O,
        O, X, X, O, O, X, X, O,
        O, x, x, O, O, x, x, O,
        O, O, O, O, O, O, O, O,
        O, X, X, O, O, X, X, O,
        O, O, O, O, O, O, O, O
        ], 
    ]
    if number > 6 or number < 0:
        return print_logo()
    else:
        sense.set_pixels(numbers[number-1])
    
    
def is_shaked():
    """
    This function get the spatial position from the accelerometer
    and then returns the correct angle for the set_rotation function
    (see logo_rotate.py and accelerometer_X.py)
    """
    a = sense.get_accelerometer_raw()
    
    acc_threshold = 1.1
    # If the acceleration in one of the axis is > a threshold... shaked!
    if abs(a['x']) > acc_threshold or abs(a['y']) > acc_threshold or abs(a['z']) > acc_threshold:
      return True
    else:
      return False
    
sense = SenseHat()

sense.clear()
splash_screen() 


    
while True:
    if is_shaked():
        random_number = random.randint(1,6)
        print_die(random_number)
        print("Shaked! Got {}".format(random_number))
        sleep(1)
        
    sleep(0.2)

 
    