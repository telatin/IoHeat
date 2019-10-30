from time import sleep
from sense_hat import SenseHat
import random 

# Here we define our very own function. See logo.py
def print_logo():
    colors1 = [ (255, 0, 0), (255, 255, 0), (255,0,255), (255,255,255)]
    colors2 = [ (0, 0, 255), (0 , 190, 0),  (100, 100, 100), (255,0,0)]
    X = colors1[random.randint(0, len(colors1)-1 ) ]
    
    T = colors2[random.randint(0, len(colors2)-1 ) ]
    O = (0, 0, 0)
    
    
    logo = [
    X, X, X, O, O, X, X, X,
    X, O, O, O, O, O, O, X,
    X, O, O, T, T, O, O, X,
    O, O, T, O, O, T, O, O,
    O, O, T, O, O, T, O, O,
    X, O, O, T, T, O, O, X,
    X, O, O, O, O, O, O, X,
    X, X, X, O, O, X, X, X
    ]

    
    sense.set_pixels(logo)
    
def print_die(number):
    X = (255, 255, 255)
    O = (0, 0, 127)
    x = (200, 200, 200)
    R = (255, 0, 0)
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
        O, O, O, O, O, O, O, O,
        O, O, O, x, x, O, O, O,
        O, O, O, X, X, O, O, O,
        O, O, O, O, O, O, O, O,
        O, X, X, O, O, X, X, O,
        O, O, O, O, O, O, O, O
        ],
         
                  
        [
        R, R, R, R, R, R, R, R,
        R, X, X, R, R, X, X, R,
        R, R, R, R, R, R, R, R,
        R, X, X, R, R, X, X, R,
        R, x, x, R, R, x, x, R,
        R, R, R, R, R, R, R, R,
        R, X, X, R, R, X, X, R,
        R, R, R, R, R, R, R, R
        ], 
    ]
    if number > 6 or number < 0:
        return print_logo()
    else:
        sense.set_pixels(numbers[number-1])
    
    
def get_rotation():
    """
    This function get the spatial position from the accelerometer
    and then returns the correct angle for the set_rotation function
    (see logo_rotate.py and accelerometer_X.py)
    """
    a = sense.get_accelerometer_raw()
    print('{}    {}    {}'.format(int(a['x']*100),  int(a['y']*100),int(a['z']*100)  ))
    
    # Accelerometer returns ratios from 0 to 1, to have simpler
    # number to work with we can scale it to an integer 0-100
    scale = 100
    
    # We define threshodls to accept the screen as "vertical"
    lower = 0.25 * scale
    upper = 0.75 * scale
    
    # We only need x and y to detect verticality of the device
    x = int(a['x'] * scale)
    y = int(a['y'] * scale)
    
    if (abs(x) < lower and y > upper):
        return 0
    elif (abs(x) < lower and y < -1 * upper):
        return 180
    elif (x > upper and abs(y) < lower):
        return 270
    elif (x < -1*upper and abs(y) < lower):
        return 90
    else:
        # This case covers the "horizontal" screen
        return -1
    
sense = SenseHat()

sense.clear()
i = 0


        
last_rotation = -1        
while True:
    
    # Detect the matrix rotation angle from the accelerometer using our own "get_rotation" function
    r = get_rotation()
    
    # Our function returns -1 if the screen is not vertical
    if r < 0:
        # If so... we save the current rotation in a variable
        last_rotation = r
        # and print a logo as "stand by" icon
        print_logo()
        sleep(0.4)
        # Continue means ignore the rest of the loop and go to the next cycle
        continue
    
    # elif (else if) the rotation changed:
    elif  last_rotation != r:
        # Set the new screen rotation
        sense.set_rotation(r)
        last_rotation = r
        # Get a random number
        random_number = random.randint(1,6)
        # and print it to the screen
        print_die(random_number)
        
    # The following instruction prints to the terminal (debug)
    print('Rotation={}'.format(r))
    sleep(1)