# coding: utf-8

import unittest

import os
import csv
from datetime import datetime as dt

from decision_tree_for_hems_recommendations import RecommnedationDecisionTree

CSVFILE_PATH = "tests/test.csv"


class RowData:
    '''
    想定しているデータカラム
    --------------------------------------------------------------------------------------------
    timestamp,on_off,operating,set_temperature,wind,indoor_temperature,indoor_pressure,indoor_humidity,operate_ipaddress
    --------------------------------------------------------------------------------------------
    ...
    '''
    def __init__(self, timestamp, on_off=None, operating=None,
                 set_temperature=None, wind=None,
                 indoor_temperature=None, indoor_pressure=None,
                 indoor_humidity=None, operate_ipaddress=None,
                 user_id=None):

        self.timestamp = dt.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
        self.on_off = str(on_off) if on_off else on_off
        self.operating = str(operating) if operating else operating
        self.set_temperature = int(set_temperature) \
            if set_temperature else set_temperature
        self.wind = str(wind) if wind else wind
        self.indoor_temperature = float(indoor_temperature) \
            if indoor_temperature else wind
        self.indoor_pressure = float(indoor_pressure) \
            if indoor_pressure else indoor_pressure
        self.indoor_humidity = float(indoor_humidity) \
            if indoor_humidity else indoor_humidity
        self.operate_ipaddress = str(operate_ipaddress) \
            if operate_ipaddress else operate_ipaddress
        self.user_id = int(user_id) \
            if user_id else user_id


class RecommnedationDecisionTreeTestCase(unittest.TestCase):
    def setUp(self):
        # prepare start_train_dt
        start_train_dt = dt(2016, 8, 2)
        # prepare end_train_dt
        end_train_dt = dt(2016, 9, 18)
        # define data_list_num
        self.data_list_num = 48  # 2016-08-02 -> 2016-09-18 kikan

        # prepare ac_logs_list
        ac_logs_list = []
        # 本来はstart_train_dt, end_train_dtの条件でデータのクエリゲット
        with open(CSVFILE_PATH) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                ac_logs_list.append(
                    RowData(
                        timestamp=row['timestamp'],
                        on_off=row['on_off'],
                        operating=row['operating'],
                        set_temperature=row['set_temperature'],
                        wind=row['wind'],
                        indoor_temperature=row['indoor_temperature'],
                        indoor_pressure=row['indoor_temperature'],
                        indoor_humidity=row['indoor_humidity'],
                        operate_ipaddress=row['operate_ipaddress'],
                        user_id=row['user_id'],
                    )
                )

        # prepare target_hour
        target_hour = 10

        # Instanciate RecommnedationDecisionTree
        self.rDT = RecommnedationDecisionTree(
            start_train_dt=start_train_dt,
            end_train_dt=end_train_dt,
            ac_logs_list=ac_logs_list,
            target_hour=target_hour,
        )

    def test_basic_instanciation(self):
        self.assertEqual(self.rDT.start_train_dt, dt(2016, 8, 2))
        self.assertEqual(self.rDT.end_train_dt, dt(2016, 9, 18))
        self.assertEqual(self.rDT.target_hour, 10)

    def test_X_data_list(self):
        dlist = self.rDT.train_X_list

        # length
        self.assertEqual(len(dlist), self.data_list_num)

        # weekday or holiday
        self.assertEqual(dlist[0][1], 0.0)
        self.assertEqual(dlist[4][1], 1.0)

        # max_temperature
        self.assertEqual(dlist[0][2], 29.4)
        self.assertEqual(dlist[4][2], 34.2)

    def test_Y_data_list(self):
        dlist = self.rDT.train_Y_list

        # length
        self.assertEqual(len(dlist), self.data_list_num)

        # is_done
        self.assertEqual(dlist[0][1], 0)
        self.assertEqual(dlist[1][1], 0)
        self.assertEqual(dlist[2][1], 1)
        self.assertEqual(dlist[3][1], 0)

    def test__ret_decision_table(self):
        x, y = self.rDT._ret_decision_table()

        # length
        self.assertEqual(len(x), self.data_list_num)
        self.assertEqual(len(y), self.data_list_num)

        # x
        self.assertEqual(x[0][0], 0.0)
        self.assertEqual(x[4][0], 1.0)

        # y
        self.assertEqual(y[0], 0)
        self.assertEqual(y[1], 0)
        self.assertEqual(y[2], 1)
        self.assertEqual(y[3], 0)

    def test_get_test_X_list(self):
        OWM_API_KEY = os.getenv('OWM_API_KEY')
        self.rDT.get_test_X_list(OWM_API_KEY)
        dlist = self.rDT.test_X_list
        self.assertEqual(len(dlist), 5)
