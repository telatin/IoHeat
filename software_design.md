# IoHeat software design

Version 1.0

## The device

The Raspberry Pi will be connected to :
1. A temperature sensor: _sT1_
1. A relay connected to the heating system: _rH1_
1. A relay connected to the cooling system: _rC1_

The device will have a _status 0_ (not operative) and a _status 1_ (operative), that will start
the temperature controlled heating (or cooling) to reach the desired operating temperature (constT).

Autonomous scripts to implement (all should have a `-j` switch for JSON output). 
They will all update the **IoH Server** via web API.
* **ioh_register** -- register the device UUID to the online server
* **ioh_temperature** -- read the sensor\'s temperature, and register the temperature in the server\'s log
* **ioh_status** -- return the device status (0, 1), and current temperature
* **ioh_start** -- will set the status to 1 and run a script to control the temperature:
	* **ioh_thermostat** -- the script with the themperature controlling loop
* **ioh_stop** -- stop the _ioh\_thermostat_ script and set status to 0.


## User interface A: Telegram

Installing a Telegram BOT in the device, it's possible to bypass the need for an external webserver (the direct connection to the device is not implemented for security reasons).

The bot should expose these methods:
* **/status** returning temperature, humidity, if the warming cycle is active or not (and if the heater is on at the moment)
* **/start** will start the warming cycle to the desired temperature
  * This will support a specification of date/time
* **/stop** will stop the warming cycle


## User interface B: The webserver

The webserver is able to control multiple devices and multiple users.
With a responsive HTML interface it's a solution that is accessible from mobile devices, desktop computers and the device itself via touch screen.

* Users can register themselves (database table "users"), and associate a device (how? this issue will probably not addressed at this stage.)
* There is a set of administrators (database table "admins")
* Each device can register itself via _ioh\_register_. (database table "devices")
	* Each device can be operated by multiple registered users (table "device_users"), but initially one user will be the "device owner".
	* Each device has a "last_seen" property
	* Each device has a "status", and "status_timestamp" properties, identifying the **user**-defined status: the device will take decisions querying these values
* There is a history table "temperatures" where each _device-date-temperature array_ is logged. The _ioh\_temperature_ script will add an entry to this.
* There is a history table "reqs" where each user request is recorded. 
 
