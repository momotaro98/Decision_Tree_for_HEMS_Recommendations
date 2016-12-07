# coding: utf-8

import unittest
import csv
from datetime import datetime as dt

from home_electric_usage_recommendation_modules \
    import (SettingTemp, ReduceUsage, ChangeUsage)

CSVFILE_PATH = "tests/test.csv"


class RowData:
    '''
    想定しているデータカラム
    --------------------------------------------------------------------------------------------
    timestamp,on_off,operating,set_temperature,wind,temperature,pressure,humidity,IP_Address
    --------------------------------------------------------------------------------------------
    ...
    '''
    def __init__(self, timestamp, on_off=None, operating=None,
                 set_temperature=None, wind=None,
                 temperature=None, pressure=None, humidity=None,
                 IP_Address=None):
        self.timestamp = dt.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
        self.on_off = str(on_off) if on_off else on_off
        self.operating = str(operating) if operating else operating
        self.set_temperature = int(set_temperature)\
            if set_temperature else set_temperature
        self.wind = str(wind) if wind else wind
        self.temperature = float(temperature) if temperature else wind
        self.pressure = float(pressure) if pressure else pressure
        self.humidity = float(humidity) if humidity else humidity
        self.IP_Address = str(IP_Address) if IP_Address else IP_Address
