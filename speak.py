#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import importlib

from time import sleep
from datetime import timedelta
from glucometerutils import common
from glucometerutils import exceptions

# glucometerutils/glucometer.py --driver fsprecisionneo --device /dev/hidraw3
# http://www.reactivated.net/writing_udev_rules.html
# http://hintshop.ludvig.co.nz/show/persistent-names-usb-serial-devices/
# udev rule alias

def main():
    counter = 0
    driver = importlib.import_module('glucometerutils.drivers.' + 'fsprecisionneo')

    while True:
        name = '/dev/hidraw {0}'.format(counter % 4)
        try:
            device = driver.Device(name)
            break
        except:
            print('Error opening {0}'.format(name))
        
        counter += 1
        sleep(1)
        
    device.connect()

    # UNIT_MGDL = 'mg/dL'
    # UNIT_MMOLL = 'mmol/L'
    unit = common.UNIT_MMOLL
    time = device.get_datetime()
    counter = 0

    readings = device.get_readings()
    readings = (reading for reading in readings if not isinstance(reading, common.KetoneReading))

    for reading in readings:
        print(reading.as_csv(unit))
        if reading.timestamp >= time - timedelta(minutes = 5):
            message = 'Резултат {0}'.format(reading.get_value_as(unit))
            counter += 1
   
    if counter > 1:
        message = 'Има грешка!'
    elif counter == 0:
        message = 'Няма резултат'

    print(device.get_datetime())
    print(message)
    
    # os.system('espeak -vbg+f2 -k4 "{0}"'.format(message))
    
    device.disconnect()

if __name__ == "__main__":
    main()

