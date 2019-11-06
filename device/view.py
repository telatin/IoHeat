#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
from time import sleep
from pprint import pprint
import RPi.GPIO as RPIGPIO
from grove.gpio import GPIO
import argparse
import os.path
import json
import os
import time
import datetime
import signal
import stat


def file_age(pathname):
    return time.time() - os.stat(pathname)[stat.ST_MTIME]

def nice_secs(secs):
    days = int(secs / 86400)
    secs -= days * 86400
    hours = int(secs/3600)
    secs -= hours * 3600
    minutes = int(secs/60)
    secs -= minutes * 60
    string = ''
    if (days > 0):
        string += '{}d '.format(days)
    if (hours > 0):
        string += '{}h '.format(hours)
    if (minutes > 0):
        string += '{}m '.format(minutes)
    string += '{}s'.format(secs)
    return string


def timestamp(format):
    if (format == 'time'):
        return '{:%H:%M:%S}'.format(datetime.datetime.now())
    else:
        return '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())


def ioh_shutdown(signum, frame):
    """
    When the program is interrupted, attempts to remove the lock file and to switch the heating off
    """
    signal.signal(signal.SIGINT, original_sigint)
    timestamp=timestamp('')
    try:
        humi, temp = sensor.read()
        eprint('{3} [{0}]\t{1:.1f}°C\t{2} ioh_shutdown()'.format(relay.status(), temp, tempbar(temp), timestamp))
        relay.off()
        eprint("Relay {}: {}".format(opt.warmerpin, relay.status()))
        if (is_warming(IoH_lock_file)):
            if (delete_warming_lock(IoH_lock_file)):
                eprint("Cleaning lock file")
            else:
                eprint("Unable to remove {}".format(IoH_lock_file))
        sys.exit(0)
    except KeyboardInterrupt:
        print("Ok ok, quitting")
        sys.exit(1)

    # restore the exit gracefully handler here
    signal.signal(signal.SIGINT, ioh_shutdown)

def eprint(*args, **kwargs):
	"""print to STDERR"""
	print(*args, file=sys.stderr, **kwargs)

def printjson(object):
    """print an object in JSON"""
    if opt.json:
        print(json.dumps(object, sort_keys=True, indent=4))
        return 1
    else:
        return 0

def create_warming_lock(filename):
    try:
        with open(filename, 'a') as lockfile:
            os.utime(filename, None)
            t=timestamp('')
            print('{}\t{}'.format(os.getpid(), t), file=lockfile)
        return 1
    except Exception as e:
        eprint("{}\tUnable to create lock file {} ({})".format(t, filename, e))
        return 0

def delete_warming_lock(filename):
    try:
        os.remove(filename)
        return 1
    except Exception as e:
        eprint("{}\tUnable to remove lock file {} ({})".format(timestamp(''), filename, e))
        return 0

def is_warming(filename):
    return os.path.isfile(filename)

def set_max_priority(): pass
def set_default_priority(): pass

# Thermometer init
RPIGPIO.setmode(RPIGPIO.BCM)
RPIGPIO.setwarnings(False)
IoH_lock_file = os.path.expanduser('~') + '/.IoHeat.lock';
PULSES_CNT = 41
IoH_data = {}
st = ts = time.time()
start_timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
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

    if temperature < 33:
        color = bcolors.OKBLUE
    elif temperature < 36:
        color = bcolors.WARNING
    else:
        color = bcolors.FAIL


    return color + ('░' * int(bar) ) + (' ' * int(length - bar )) + bcolors.ENDC

class GroveRelay(GPIO):
    '''
    Class for warming Relay
    '''
    def __init__(self, pin):
        #eprint('# Initializing heating unit: GPIO{}'.format(pin))
        super(GroveRelay, self).__init__(pin, GPIO.OUT)

    def on(self):
        self.write(1)

    def off(self):
        self.write(0)

    def ison(self):
        if self.read() == 1:
            return True
        else:
            return False

    def status(self):
        if self.read() == 1:
            return 'ON'
        else:
            return 'OFF'


class DHT(object):
    '''
    class for Thermomether
    '''
    DHT_TYPE = {
        'DHT11': '11',
        'DHT22': '22'
    }

    MAX_CNT = 320

    def __init__(self, dht_type, pin):
        dht_type=str(dht_type)
        self.pin = pin
        if dht_type != self.DHT_TYPE['DHT11'] and dht_type != self.DHT_TYPE['DHT22']:
            eprint('ERROR: Please use {} or {} as dht type (not {})'.format(self.DHT_TYPE['DHT11'], self.DHT_TYPE['DHT22'],dht_type))

            exit(1)
        self._dht_type = '22'
        self.dht_type = dht_type
        RPIGPIO.setup(self.pin, RPIGPIO.OUT)

    @property
    def dht_type(self):
        return self._dht_type

    @dht_type.setter
    def dht_type(self, type):
        self._dht_type = type
        self._last_temp = 0.0
        self._last_humi = 0.0

    def _read(self):
        # Send Falling signal to trigger sensor output data
        # Wait for 20ms to collect 42 bytes data
        RPIGPIO.setup(self.pin, RPIGPIO.OUT)
        set_max_priority()

        RPIGPIO.output(self.pin, 1)
        sleep(.2)

        RPIGPIO.output(self.pin, 0)
        sleep(.018)

        RPIGPIO.setup(self.pin, RPIGPIO.IN)
        # a short delay needed
        for i in range(10):
            pass

        # pullup by host 20-40 us
        count = 0
        while RPIGPIO.input(self.pin):
            count += 1
            if count > self.MAX_CNT:
                # eprint("pullup by host 20-40us failed")
                set_default_priority()
                return None, "pullup by host 20-40us failed"

        pulse_cnt = [0] * (2 * PULSES_CNT)
        fix_crc = False
        for i in range(0, PULSES_CNT * 2, 2):
            while not RPIGPIO.input(self.pin):
                pulse_cnt[i] += 1
                if pulse_cnt[i] > self.MAX_CNT:
                    # eprint("pulldown by DHT timeout %d" % i)
                    set_default_priority()
                    return None, "pulldown by DHT timeout %d" % i

            while RPIGPIO.input(self.pin):
                pulse_cnt[i + 1] += 1
                if pulse_cnt[i + 1] > self.MAX_CNT:
                    # eprint("pullup by DHT timeout %d" % (i + 1))
                    if i == (PULSES_CNT - 1) * 2:
                        # fix_crc = True
                        # break
                        pass
                    set_default_priority()
                    return None, "pullup by DHT timeout %d" % i

        # back to normal priority
        set_default_priority()

        total_cnt = 0
        for i in range(2, 2 * PULSES_CNT, 2):
            total_cnt += pulse_cnt[i]

        # Low level ( 50 us) average counter
        average_cnt = total_cnt / (PULSES_CNT - 1)
        # eprint("low level average loop = %d" % average_cnt)

        data = ''
        for i in range(3, 2 * PULSES_CNT, 2):
            if pulse_cnt[i] > average_cnt:
                data += '1'
            else:
                data += '0'

        data0 = int(data[ 0: 8], 2)
        data1 = int(data[ 8:16], 2)
        data2 = int(data[16:24], 2)
        data3 = int(data[24:32], 2)
        data4 = int(data[32:40], 2)

        if fix_crc and data4 != ((data0 + data1 + data2 + data3) & 0xFF):
            data4 = data4 ^ 0x01
            data = data[0: PULSES_CNT - 2] + ('1' if data4 & 0x01 else '0')

        if data4 == ((data0 + data1 + data2 + data3) & 0xFF):
            if self._dht_type == self.DHT_TYPE['DHT11']:
                humi = int(data0)
                temp = int(data2)
            elif self._dht_type == self.DHT_TYPE['DHT22']:
                humi = float(int(data[ 0:16], 2)*0.1)
                temp = float(int(data[17:32], 2)*0.2*(0.5-int(data[16], 2)))
        else:
            # eprint("checksum error!")
            return None, "checksum error!"

        return humi, temp

    def read(self, retries = 15):
        for i in range(retries):
            humi, temp = self._read()
            if not humi is None:
                break
        if humi is None:
            return self._last_humi, self._last_temp
        self._last_humi,self._last_temp = humi, temp
        return humi, temp


opt_parser = argparse.ArgumentParser(description='IoHeat thermostat')

opt_parser.add_argument("-x", '--maxtemp', help="Safety max temperature", type=int, default=48)
opt_parser.add_argument('-a', '--action',
                        help='What to do [status,on,off]',
                        default='status')

opt_parser.add_argument('-t', '--temperature',
                        type=float,
                        help='Final temperature to control',
                        default=36.5)

opt_parser.add_argument('-w', '--warmerpin',
                        type=int,
                        help='GPIO pin for the warming unit relay',
                        default=16)

opt_parser.add_argument('-m', '--mode',
                        type=int,
                        help='Thermomether reading mode [21/22]',
                        default=22)

opt_parser.add_argument('-T', '--thermopin',
                        type=int,
                        help='GPIO pin for the thermomether unit relay',
                        default=5)

opt_parser.add_argument('-j', '--json',
                         action='store_true',
                        help='Send JSON object')
opt = opt_parser.parse_args()





def main():
    eprint('Initializing...')
    # Warming relay init
    start_ts = timestamp('')
    Grove = GroveRelay
    relay = GroveRelay(opt.warmerpin)

    typ = int(opt.mode)
    sensor = DHT(typ, int(opt.thermopin))

    IoH_data['interface'] = {}
    IoH_data['messages'] = {}
    IoH_data['status'] = {}

    IoH_data['interface']['heating_relay_pin'] = opt.warmerpin
    IoH_data['interface']['thermo_sensor_pin'] = opt.thermopin
    IoH_data['interface']['thermo_sensor_mode'] = opt.mode
    IoH_data['interface']['IoH_lock_file'] = IoH_lock_file
    IoH_data['interface']['start_timestamp'] = start_ts
    # Initialize with a first Temp reading
    humi, temp = sensor.read()

    # Add delay for future temperature readings
    sleep(1)

    if opt.action == 'status':
        eprint("- IoHeat Status")
        eprint("Heating Relay {}: {}".format(opt.warmerpin, relay.status()))
        humi, temp = sensor.read()
        IoH_data['status']['temperature'] = temp
        IoH_data['status']['humidity'] = humi
        IoH_data['status']['date'] = start_timestamp
        IoH_data['status']['heater_active'] = relay.status()
        IoH_data['status']['heating_cycle'] = 'OFF'
        if is_warming(IoH_lock_file):
            IoH_data['status']['heating_cycle'] = 'ON'

        eprint('{3} Sensor DHT{0}, humidity {1:.1f}%, temperature {2:.1f}*'.format(sensor.dht_type, humi, temp, start_ts))
        eprint(' {0:.1f}°C\t{1} '.format(temp, tempbar(temp)))

        if (is_warming(IoH_lock_file)):
            eprint("INFO: Warming cycle detected ({})".format(nice_secs(file_age(IoH_lock_file))))

        if temp > opt.maxtemp:
            IoH_data['messages']['too_hot'] = "Switching the unit off as temperature is >{}".format(opt.x)
            eprint('WARNING: device too hot (>{}°C), switching the heating unit off'.format(opt.x))
            if (is_warming(IoH_lock_file)):
                eprint('WARNING: the device was set to heating_cycle=ON.')
                delete_warming_lock(IoH_lock_file)
            relay.off()

        printjson(IoH_data)

    elif opt.action == 'view':
        while 1:
            humi, temp = sensor.read()
            if is_warming(IoH_lock_file):
                if relay.status():
                    heating = ' [HEATING NOW] '
                else:
                    heating = ' [  HEATING  ] '
            else:
                heating =     ' [   Ready   ] '



            eprint('{2} {0:.1f}°C\t{1} '.format(temp, tempbar(temp), heating))
            time.sleep(2)

    elif opt.action == 'on':
        eprint("- IoHeat ON")
        eprint("- This is dangerous: heating will be on until manually switched off!")
        relay.on()
        eprint("Relay {}: {}".format(opt.warmerpin, relay.status()))
    elif opt.action == 'off':
        eprint("- IoHeat OFF")
        relay.off()
        eprint("Relay {}: {}".format(opt.warmerpin, relay.status()))
        if (is_warming(IoH_lock_file)):
            if (delete_warming_lock(IoH_lock_file)):
                eprint("Cleaning lock file")
            else:
                eprint("Unable to remove {}".format(IoH_lock_file))

    elif opt.action == 'start':

        # Try the cycle
        try:
            if (not is_warming(IoH_lock_file) ):
                create_warming_lock(IoH_lock_file)

            while (1):
                humi, temp = sensor.read()

                # Check if lock file is still present 
                if (not is_warming(IoH_lock_file)):
                    eprint("Lock file deleted: probably time to quit at {}°C!".format(temp))
                    relay.off()
                    break

                

                if temp < (opt.temperature):
                    if (relay.read() == 0):
                        relay.on()

                elif temp > (opt.temperature + 1):
                    if (relay.read() == 1):
                        relay.off()
                else:
                    pass

                eprint(' [{0}]\t{1:.1f}°C\t{2} '.format(relay.status(), temp, tempbar(temp)))
                sleep(15)
        except Exception as e:
            # Exit clean
            relay.off()
            if (is_warming(IoH_lock_file)):
                eprint('')
                eprint('# Removing lock file')
                delete_warming_lock(IoH_lock_file)
            eprint('Exiting after Exception')

if __name__ == '__main__':
    original_sigint = signal.getsignal(signal.SIGINT)
    signal.signal(signal.SIGINT, ioh_shutdown)
    main()
