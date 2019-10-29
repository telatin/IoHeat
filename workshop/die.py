from sense_hat import SenseHat
import random 

# Import your SenseHAT as an object, we can call it "myHAT"
myHAT =  SenseHat()

# Generate a random integer from 1 to 6, store it as "number"
number = random.randint(1,6)

# Print the result to the terminal
print('You got {}'.format(number))

# "number" is an integer, but the function show_letter()
# requires a string. We can convert number with the str() functino
number_as_string = str(number)
myHAT.show_letter( number_as_string )
