from sense_hat import SenseHat

# We can change the name of our object as long as we are consisted within each script
sense = SenseHat()

# this function will retrieve a value from the sensor, we can assign it to a variable
pressure_mbars = sense.get_pressure()

# we can use basic math to manipulate variables
pressure_atm   = pressure_mbars / 1013.25

# The print function can be used to report to the terminal our variables
print("Pressure: {} Millibars ({} atm)".format(pressure_mbars, pressure_atm))
