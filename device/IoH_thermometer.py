import RPi.GPIO as RPIGPIO
# -*- coding: utf-8 -*-
def set_max_priority(): pass
def set_default_priority(): pass
from time import sleep

RPIGPIO.setmode(RPIGPIO.BCM)
RPIGPIO.setwarnings(False)

PULSES_CNT = 41

class DHT(object):
    DHT_TYPE = {
        'DHT11': '11',
        'DHT22': '22'
    }

    MAX_CNT = 320

    def __init__(self, dht_type, pin):        
        self.pin = pin
        if dht_type != self.DHT_TYPE['DHT11'] and dht_type != self.DHT_TYPE['DHT22']:
            print('ERROR: Please use 11|22 as dht type [{}].'.format(dht_type) )
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
                # print("pullup by host 20-40us failed")
                set_default_priority()
                return None, "pullup by host 20-40us failed"

        pulse_cnt = [0] * (2 * PULSES_CNT)
        fix_crc = False
        for i in range(0, PULSES_CNT * 2, 2):
            while not RPIGPIO.input(self.pin):
                pulse_cnt[i] += 1
                if pulse_cnt[i] > self.MAX_CNT:
                    # print("pulldown by DHT timeout %d" % i)
                    set_default_priority()
                    return None, "pulldown by DHT timeout %d" % i

            while RPIGPIO.input(self.pin):
                pulse_cnt[i + 1] += 1
                if pulse_cnt[i + 1] > self.MAX_CNT:
                    # print("pullup by DHT timeout %d" % (i + 1))
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
        # print("low level average loop = %d" % average_cnt)

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
            # print("checksum error!")
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

Grove = DHT

def tempbar(temperature):
    length = 30
    mintemp = 10
    maxtemp = 40
    bar = 0
    if temperature > maxtemp:
        bar = length
    elif temperature > mintemp:
        bar = temperature - mintemp
    return ('░' * bar ) + (' ' * (length - bar ))

def main():
    import sys
    import time

    #Defaults
    typ = 22
    gpio_id = 5

    if len(sys.argv) == 3:
        typ = sys.argv[1]
        gpio_id = sys.argv[2]
        print('Setting:\tGPIO={} and DHT_type={}'.format(gpio_id, typ) )
    else:
        print('Assuming:\tGPIO={} and DHT_type={}'.format(gpio_id, typ) )

    

    sensor = DHT(typ, int(gpio_id))

    
    iteration = 0
    while True:
        iteration += 1
        humi, temp = sensor.read()
        bar_len = int( (int(temp) - 20) / 2 ) 
        bar = '░' * bar_len
        if not humi is None:
            print(' {4}\t{1:.1f}%\t {2:.1f}°C\t{3}\r'.format( sensor.dht_type, humi, temp, iteration, bar), end="")
        else:
            print('DHT{0}, humidity & temperature: {1}\r'.format(sensor.dht_type, temp), end="")
        time.sleep(5)


if __name__ == '__main__':
    main()