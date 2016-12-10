# coding: utf-8

'''
1. Building Decision Tree (DT) Model from past Tenki and HEMS data
  1. [X] Make Decision Table
    * [] SettingTemp
    * [X] TotalUsage
    * [X] ChangeUsage
  2. [X] Make Decision Tree

2. Decide to deliver the contents using the DT Model and the today's Tenki data
  1. [X] Get the today's Tenki data
  2. [] Give the decision flags
    * [] SettingTemp
    * [X] TotalUsage
    * [X] ChangeUsage
'''

from . import utils


class RecommnedationDecisionTree:
    def __init__(self, start_train_dt, end_train_dt, ac_logs_list, target_season, target_hour):
        # get args
        self.start_train_dt = start_train_dt
        self.end_train_dt = end_train_dt
        self.ac_logs_list = ac_logs_list
        self.target_hour = target_hour

        # TODO: インスタンス化でどこまでデータを整えるか

        # process making lists
        self.train_X_list = self._ret_train_X_list()
        self.train_Y_list = self._ret_train_Y_list()

        # get Decision Tree
        self.clf = self._ret_trained_DT_clf()

    def _ret_train_X_list(self):
        '''
        X data is Tenki data

        example list to make
	[
	    [datetime(2016, 7, 1), 1.0, 31.0, 25.0, 77.2, 0.0],
	    [datetime(2016, 7, 2), 1.0, 29.8, 24.8, 70.2, 0.0],
	    .
	    .
	    .
	    [datetime(2016, 8, 15), 1.0, 31, 25, 73.2, 0.0],
	]

        columns
        [date_list, weekday_list, max_temperature_list, min_temperature_list, ave_humidity_list, day_tenki_list]

        '''
        train_X_list = utils.ret_outer_data_list(
            start_dt=self.start_train_dt,
            end_dt=self.end_train_dt
        )
        return train_X_list

    def _ret_train_Y_list(self):
        '''
        Abstract Method
        Each Children Class must implement this method.

        Y data (label data) is HEMS data

        example list to make
        [
          [datetime(2016, 7, 1), 0],
          [datetime(2016, 7, 2), 1],
          .
          .
          .
          [datetime(2016, 8, 15), 1]
        ]

        columns
        [date_list, is_done_list]
        '''
        date_list = utils.ret_date_list(self.start_train_dt, self.end_train_dt)
        ret_list = [[dt, 0] for dt in date_list]
        return ret_list

    def _ret_decision_table(self):
        """
        学習用の訓練データ、訓練ラベルのリストを返す
        そのとき、学習用のx，yの長さが同じであるか
        スタートの日付が同じであるかを確認する
        """
        # check if the start date is same
        if not self.train_X_list[0][0] == self.train_Y_list[0][0]:
            raise Exception('X list Y list start_date Different Error!')

        # slice except datetime
        x = [row[1:] for row in self.train_X_list]
        y = [row[1] for row in self.train_Y_list]

        # check if the lists length is same
        if not len(x) == len(y):
            raise Exception('X list and Y list Different length Error!')

        return x, y

    def _ret_trained_DT_clf(self):
        x, y = self._ret_decision_table()
        X = utils.be_ndarray(x)
        Y = utils.be_ndarray(y)
        clf = utils.ret_trained_DT_clf(X, Y)
        return clf

    def get_test_X_list(self, OWM_API_KEY):
        """
        '現在'の天気情報を取得する

        self.test_X_list example
        [1.0, 34.2, 25.8, 50.0, 0.0]
        """
        self.test_X_list = utils.ret_predicted_outer_data_list(OWM_API_KEY)

    def ret_predicted_Y_int(self):
        # set self.test_X_list
        OWM_API_KEY = utils.ret_OWM_API_KEY()
        self.get_test_X_list(OWM_API_KEY)

        # convert ndarray
        test_x = [self.test_X_list]
        test_X = utils.be_ndarray(test_x)

        # Predict the Y label
        pred_Y = self.clf.predict(test_X)

        # convert pred_Y to int type
        pred_y = int(pred_Y[0])

        return pred_y


class SettingTempDT(RecommnedationDecisionTree):
    def _ret_target_settemp(self):
        '''
        (全ての行分の設定温度)
        '''

    def _ret_datetime_settemp_list(self):
        pass

    def _ret_train_Y_list(self):
        '''
        Y data (label data) is HEMS data

        example list to make
        [
          [datetime(2016, 7, 1), 0],
          [datetime(2016, 7, 2), 1],
          .
          .
          .
          [datetime(2016, 8, 15), 1]
        ]

        columns
        [date_list, is_done_list]
        '''
        pass


class TotalUsageDT(RecommnedationDecisionTree):
    def _ret_target_usage_hour(self):
        '''
        (全期間合計エアコン利用時間 / 総日数) - 2
        を目標値とする
        '''
        # 総日数 total_days
        total_days = (self.end_train_dt - self.start_train_dt).days + 1

        # 全期間合計エアコン利用時間 total_usage_hour
        total_usage_hour = 0
        on_operationg_flag = False
        for row in self.ac_logs_list:
            if row.on_off == "on" and not on_operationg_flag:
                on_operationg_flag = True
                on_timestamp = row.timestamp
            elif row.on_off == "off" and on_operationg_flag:
                on_operationg_flag = False
                off_timestamp = row.timestamp
                # Event happens when switching on->off
                total_usage_hour += utils.make_delta_hour(
                    on_timestamp, off_timestamp)
        # 最終日の日付越えてもonであったとき
        if on_operationg_flag:
            days_last_timestamp = utils.make_days_last_timestamp(on_timestamp)
            total_usage_hour += utils.make_delta_hour(
                on_timestamp, days_last_timestamp)

        # 目標値 target_usage_hour
        target_usage_hour = (total_usage_hour / total_days) - 2.0

        return target_usage_hour

    def _ret_datetime_value_list(self):
        '''
        ret_list
        [
            [datetime(2016, 7, 1), 3.2],
            [datetime(2016, 7, 2), 2.4],
            .
            .
            .
            [datetime(2016, 8, 15), 4.5]
        ]
        '''
        date_list = utils.ret_date_list(self.start_train_dt, self.end_train_dt)
        dt_value_dict = {d: 0 for d in date_list}
        # ac_logs_list foreach start
        on_operationg_flag = False
        for row in self.ac_logs_list:
            if row.on_off == "on" and not on_operationg_flag:
                on_operationg_flag = True
                on_timestamp = row.timestamp
            elif row.on_off == "off" and on_operationg_flag:
                on_operationg_flag = False
                off_timestamp = row.timestamp
                # Event happens when switching on->off
                dt_value_dict[on_timestamp.date()] += \
                    utils.make_delta_hour(on_timestamp, off_timestamp)
        # 最終日の日付越えてもonであったとき
        if on_operationg_flag:
            days_last_timestamp = utils.make_days_last_timestamp(on_timestamp)
            dt_value_dict[on_timestamp.date()] += \
                utils.make_delta_hour(on_timestamp, days_last_timestamp)
        ret_list = [
            [d, v] for d, v in sorted(dt_value_dict.items(), key=lambda x:x[0])
        ]
        return ret_list

    def _ret_train_Y_list(self):
        '''
        Y data (label data) is HEMS data

        example list to make
        [
          [datetime(2016, 7, 1), 0],
          [datetime(2016, 7, 2), 1],
          .
          .
          .
          [datetime(2016, 8, 15), 1]
        ]

        columns
        [date_list, is_done_list]
        '''

        # *** 目標値設定 ***
        # target_usage_hour を決定する
        target_usage_hour = self._ret_target_usage_hour()

        # &&& 日付・値 辞書取得 &&&
        datetime_value_list = self._ret_datetime_value_list()

        # ^^^ 返すラベル生成 ^^^
        ret_list = []
        for d_v_list in datetime_value_list:
            dt = d_v_list[0]
            value = d_v_list[1]
            # "レコメンドを送る必要がある日"を1にする
            # 目標値より大きい値のとき1にする
            if value > target_usage_hour:
                ret_list.append([dt, 1])
                continue
            ret_list.append([dt, 0])
        return ret_list


class ChangeUsageDT(RecommnedationDecisionTree):
    def _ret_train_Y_list(self):
        '''
        Y data (label data) is HEMS data

        example list to make
        [
          [datetime(2016, 7, 1), 0],
          [datetime(2016, 7, 2), 1],
          .
          .
          .
          [datetime(2016, 8, 15), 1]
        ]

        columns
        [date_list, is_done_list]
        '''
        date_list = utils.ret_date_list(self.start_train_dt, self.end_train_dt)
        ret_list = [[dt, 0] for dt in date_list]

        last_1label_index = 0
        on_operationg_flag = False
        for row in self.ac_logs_list:
            if row.on_off == "on" and not on_operationg_flag:
                on_operationg_flag = True
                on_timestamp = row.timestamp
            elif row.on_off == "off" and on_operationg_flag:
                on_operationg_flag = False
                off_timestamp = row.timestamp
                # Event happens when switching on->off
                if on_timestamp.hour <= self.target_hour <= off_timestamp.hour:
                    # Get the list index
                    last_1label_index = date_list.index(on_timestamp.date())
                    # 対象時刻にonであった日付インデックスを1にする
                    # つまり、"レコメンドを送る必要がある日"を1にする
                    ret_list[last_1label_index][1] = 1
        # 最終日の日付越えてもonであったとき
        if on_operationg_flag:
            if on_timestamp.hour <= self.target_hour <= 23:
                # Get the list index
                last_1label_index = date_list.index(on_timestamp.date())
                # 対象時刻にonであった日付インデックスを1にする
                ret_list[last_1label_index][1] = 1
        return ret_list
