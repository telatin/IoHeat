# IoHeat - Device scripts

## ioheat.py

Main script to check the temperature, start and stop the heating.

```
Usage:
ioheat.py [options] [-a action] 
```

#### Options

 - **-a, --action** [status|on|off|start, default="status"]
   - _status_: will print the current temperature and humidity, the status of the heating relay (on/off) and if the heating cycle is active. As a safety measure, if the current temperature is above the maximum temperature (see `-x`) will switch the heating relay off and terminate the heating cycle.  The heating cycle is updated every 15 seconds.
   - _start_: will start the heating cycle and maintain the temperature in a range around the desider temperature (creates a lock_file in the home directory)
   - _on_: will turn the heating on (use with care)
   - _off_: will switch the heating on and terminate the heating cycle
 - **-t, --temperature** [float, default=37.5]
 Desired temperature for the heating cycle (see `-a start`)
 - **-x, --maxtemp** [int, default=45]
 Safety maximum temperature. If during a status check the temperature is above this value, the heating will be terminated.
 - **-w, --warmerpin** [int, default=16]
 GPIO pin for the heating relay
 - **-T, --thermopin** [int, default=5]
 GPIO pin for the temperature/humidity sensor
 - **-m, --mode** [21|22, default=22]
 Temperature reading mode
 - **-j, --json**
 If used with `-a status`, will print the output in JSON format
 
 
Suggestion: add to the _crontab_ a job for `ioheat.py -a status` to prevent accidental overheat (e.g. every 30 minutes).
 
## giovanni_bot.py (beta)

Starts the Telegram BOT. This is a preliminary release.
