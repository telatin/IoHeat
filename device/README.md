# Raspberry Pi configuration notes

## ioheat.py




# Unused documentation

## DS18B20 themperature sensor

 -  See: [tutorial](http://www.circuitbasics.com/raspberry-pi-ds18b20-temperature-sensor-tutorial/)

#### Installation

Our setup involves enabling, via `raspi-config` ([see here](https://www.raspberrypi.org/documentation/configuration/raspi-config.md))
the interface for [1-wire](https://en.wikipedia.org/wiki/1-Wire) protocol.

Alternative [method](https://pinout.xyz/pinout/1_wire) involves adding `dtoverlay=w1–gpio` to '/boot/config.txt' as described in the [tutorial](http://www.circuitbasics.com/raspberry-pi-ds18b20-temperature-sensor-tutorial/).

#### Usage
To read the temperature:
```
cat /sys/devices/w1_bus_master1/28-*/w1_slave | grep -oP "t=\d+" | cut -f 2 -d '='
```
