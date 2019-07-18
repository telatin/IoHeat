
from time import sleep
def tempbar(temperature):
    class bcolors:
        HEADER = '\033[95m'
        OKBLUE = '\033[94m'
        OKGREEN = '\033[92m'
        WARNING = '\033[93m'
        FAIL = '\033[91m'
        ENDC = '\033[0m'
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'
      
    length = 30
    mintemp = 10
    maxtemp = 40
    bar = 0
    if temperature > maxtemp:
        bar = length
    elif temperature > mintemp:
        bar = temperature - mintemp

    if temperature < 25:
        color = bcolors.OKBLUE
    elif temperature < 30:
        color = bcolors.OKGREEN
    elif temperature < 36:
        color = bcolors.WARNING
    elif temperature > 38:
        color = bcolors.FAIL

    return color + ('░' * bar ) + (' ' * (length - bar )) + bcolors.ENDC
i = 18
while i < 45:
    print('{} {}\r'.format(i, tempbar(i)), end="")
    sleep(2)
    i += 2
