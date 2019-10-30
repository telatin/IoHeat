from time import sleep
from sense_hat import SenseHat
import random 

# Here we define our very own function. See logo.py
def print_logo():
    X = (255, 90, 55)    # pink
    O = (0, 0, 0)        # black
    T = (0, 155, 255)    # cyan
    
    # We define 'logo' as a list of triplets (colors)
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
        sense.show_letter(str(random_number), (0,255,0))
        # The following instruction prints to the terminal (debug)
    print('Rotation={}'.format(r))
    sleep(1)