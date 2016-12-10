# coding: utf-8

import unittest

import csv
from datetime import datetime
from datetime import date

from decision_tree_for_hems_recommendations import (
    utils,
    RecommnedationDecisionTree,
    SettingTempDT, TotalUsageDT, ChangeUsageDT,
)

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

        self.timestamp = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
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


def ret_start_train_dt():
    start_train_dt =  datetime(2016, 8, 2)
    return start_train_dt


def ret_end_train_dt():
    end_train_dt =  datetime(2016, 9, 18)
    return end_train_dt


def ret_ac_logs_list():
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
    return ac_logs_list


def ret_target_season():
    # target_season = 'spr'
    # target_season = 'sum'
    # target_season = 'fal'
    target_season = 'win'
    return target_season


def ret_target_hour():
    target_hour = 10
    return target_hour


class RecommnedationDecisionTreeTestCase(unittest.TestCase):
    def setUp(self):
        # *** Prepare Input Variables ***
        # prepare start_train_dt
        start_train_dt = ret_start_train_dt()

        # prepare end_train_dt
        end_train_dt = ret_end_train_dt()

        # prepare ac_logs_list
        ac_logs_list = ret_ac_logs_list()

        # prepare target_season
        target_season = ret_target_season()

        # prepare target_hour
        target_hour = ret_target_hour()

        # *** Set Test Case Class Instance variables ***
        self.data_list_num = 48  # 2016-08-02 -> 2016-09-18 kikan
        # Instanciate RecommnedationDecisionTree
        self.rDT = RecommnedationDecisionTree(
            start_train_dt=start_train_dt,
            end_train_dt=end_train_dt,
            ac_logs_list=ac_logs_list,
            target_season=target_season,
            target_hour=target_hour,
        )

    def test_basic_instanciation(self):
        self.assertEqual(self.rDT.start_train_dt, datetime(2016, 8, 2))
        self.assertEqual(self.rDT.end_train_dt, datetime(2016, 9, 18))
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
        '''
        Each Test Class must implement this 'test_Y_data_list' method
        '''
        dlist = self.rDT.train_Y_list

        # length
        self.assertEqual(len(dlist), self.data_list_num)

        # is_done
        self.assertEqual(dlist[0][1], 0)
        self.assertEqual(dlist[1][1], 0)
        self.assertEqual(dlist[2][1], 0)
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
        self.assertEqual(y[2], 0)
        self.assertEqual(y[3], 0)

    def test_get_test_X_list(self):
        OWM_API_KEY = utils.ret_OWM_API_KEY()
        self.rDT.get_test_X_list(OWM_API_KEY)
        dlist = self.rDT.test_X_list
        self.assertEqual(len(dlist), 5)

    def test_ret_predicted_Y_int(self):
        pred_y = self.rDT.ret_predicted_Y_int()
        self.assertIn(pred_y, [0, 1])  # 予測値pred_yが0または1であるかを確認


class SettingTempDTTestCase(unittest.TestCase):
    def test_Y_data_list(self):
        '''
        dlist = self.rDT.train_Y_list

        # length
        self.assertEqual(len(dlist), self.data_list_num)

        # is_done
        self.assertEqual(dlist[0][1], 0)
        self.assertEqual(dlist[1][1], 1)
        self.assertEqual(dlist[2][1], 1)
        self.assertEqual(dlist[3][1], 1)
        '''
        pass


class TotalUsageDTTestCase(unittest.TestCase):
    def setUp(self):
        # *** Prepare Input Variables ***
        # prepare start_train_dt
        start_train_dt = ret_start_train_dt()

        # prepare end_train_dt
        end_train_dt = ret_end_train_dt()

        # prepare ac_logs_list
        ac_logs_list = ret_ac_logs_list()

        # prepare target_season
        target_season = ret_target_season()

        # prepare target_hour
        target_hour = ret_target_hour()

        # *** Set Test Case Class Instance variables ***
        self.data_list_num = 48  # 2016-08-02 -> 2016-09-18 kikan
        # Instanciate RecommnedationDecisionTree
        self.rDT = TotalUsageDT(
            start_train_dt=start_train_dt,
            end_train_dt=end_train_dt,
            ac_logs_list=ac_logs_list,
            target_season=target_season,
            target_hour=target_hour,
        )

    def test__ret_target_usage_hour(self):
        target_usage_hour = self.rDT._ret_target_usage_hour()
        self.assertIsInstance(target_usage_hour, float)

    def test__ret_datetime_value_list(self):
        datetime_value_list = self.rDT._ret_datetime_value_list()

        # length
        self.assertEqual(len(datetime_value_list), self.data_list_num)
        self.assertEqual(len(datetime_value_list[0]), 2)

        # value
        self.assertEqual(datetime_value_list[0][0], date(2016, 8, 2))
        self.assertEqual(datetime_value_list[1][0], date(2016, 8, 3))

    def test_Y_data_list(self):
        dlist = self.rDT.train_Y_list

        # length
        self.assertEqual(len(dlist), self.data_list_num)

        # is_done
        self.assertEqual(dlist[0][1], 0)
        self.assertEqual(dlist[1][1], 1)
        self.assertEqual(dlist[2][1], 1)
        self.assertEqual(dlist[3][1], 1)


class ChangeUsageDTTestCase(unittest.TestCase):
    def setUp(self):
        # *** Prepare Input Variables ***
        # prepare start_train_dt
        start_train_dt = ret_start_train_dt()

        # prepare end_train_dt
        end_train_dt = ret_end_train_dt()

        # prepare ac_logs_list
        ac_logs_list = ret_ac_logs_list()

        # prepare target_season
        target_season = ret_target_season()

        # prepare target_hour
        target_hour = ret_target_hour()

        # *** Set Test Case Class Instance variables ***
        self.data_list_num = 48  # 2016-08-02 -> 2016-09-18 kikan
        # Instanciate RecommnedationDecisionTree
        self.rDT = ChangeUsageDT(
            start_train_dt=start_train_dt,
            end_train_dt=end_train_dt,
            ac_logs_list=ac_logs_list,
            target_season=target_season,
            target_hour=target_hour,
        )

    def test_Y_data_list(self):
        dlist = self.rDT.train_Y_list

        # length
        self.assertEqual(len(dlist), self.data_list_num)

        # is_done
        self.assertEqual(dlist[0][1], 0)
        self.assertEqual(dlist[1][1], 0)
        self.assertEqual(dlist[2][1], 1)
        self.assertEqual(dlist[3][1], 0)
