#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import subprocess
import importlib
import inspect
import logging
import sys

from datetime import timedelta
from glucometerutils import common
from glucometerutils import exceptions

# glucometerutils/glucometer.py --driver fsprecisionneo --device /dev/hidraw3

def main():
    driver = importlib.import_module('glucometerutils.drivers.' + 'fsprecisionneo')

    device = driver.Device('/dev/hidraw3')
    device.connect()
    device_info = device.get_meter_info()

    try:
        time_str = device.get_datetime()
    except NotImplementedError:
        time_str = 'N/A'
    
    print("{device_info}Time: {time}".format(device_info = str(device_info), time = time_str))


    # UNIT_MGDL = 'mg/dL'
    # UNIT_MMOLL = 'mmol/L'
    unit = common.UNIT_MMOLL
    time = device.get_datetime()
    counter = 0

    readings = device.get_readings()
    readings = (reading for reading in readings if not isinstance(reading, common.KetoneReading))

    for reading in readings:
        print(reading.as_csv(unit))
        if reading.timestamp >= time - timedelta(days = 1, hours = 2):
            message = 'Резултат {0}'.format(reading.get_value_as(unit))
            counter += 1
   
    if counter > 1:
        message = 'Има грешка!'
    elif counter == 0:
        message = 'Няма резултат'

    print(device.get_datetime())
    print(message)
    
    os.system('espeak -vbg+f2 -k4 "{0}"'.format(message))
    
    device.disconnect()

if __name__ == "__main__":
    main()

