# Database schemes

To create the `ioheat.db` file:
```
sqlite3 < db_scheme.sqlite ioheat.db
```

## Devices

This table is meant to register "devices" (_i.e._ Raspberry Pi's used to control a IOheat device).


### Notes

To get a UUID from a Raspberry Pi (after [this thread](https://raspberrypi.stackexchange.com/questions/2086/how-do-i-get-the-serial-number)).
```
pi@raspberrypi:~$ cat /proc/cpuinfo
 Processor       : ARMv6-compatible processor rev 7 (v6l)
 BogoMIPS        : 697.95
 Features        : swp half thumb fastmult vfp edsp java tls
 CPU implementer : 0x41
 CPU architecture: 7
 CPU variant     : 0x0
 CPU part        : 0xb76
 CPU revision    : 7

 Hardware        : BCM2708
 Revision        : 1000002
 Serial          : 000000000000000d
```
You can use very basic bash piping
```
cat /proc/cpuinfo | grep Serial | cut -d ' ' -f 2
```
