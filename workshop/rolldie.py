from time import sleep
from sense_hat import SenseHat
import random 

# Here we define our very own function. See logo.py
def print_logo():
    X = (255, 0, 0)
    O = (0, 0, 0)
    T = (0, 0, 255)
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

    sense = SenseHat()
    sense.set_pixels(logo)
    
def get_rotation():
    a = sense.get_accelerometer_raw()
    print('{}    {}    {}'.format(int(a['x']*100),  int(a['y']*100),int(a['z']*100)  ))
    
    scale = 100
    lower = 0.25 * scale
    upper = 0.75 * scale
    
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
        return -1
    
sense = SenseHat()

sense.clear()
i = 0
origin = (7, 7)

        
last_rotation = -1        
while True:
    a = sense.get_accelerometer_raw()
    r = get_rotation()
    if r < 0:
        last_rotation = r
        print_logo()
        sleep(0.4)
        continue

    
    if last_rotation != r:
        sense.set_rotation(r)
        last_rotation = r
        random_number = random.randint(1,6)
        sense.show_letter(str(random_number))
    print('Rotation={}'.format(r))
    sleep(1)