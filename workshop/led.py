# To use our SenseHat we need to import its "library"
from sense_hat import SenseHat

# Using the library we can now create an object (we can call it as we wish)
# We will interact with the created object to access our SenseHat
myHat = SenseHat()

# A function the object has is show_message(): try it!
myHat.show_message('IoHeat')
