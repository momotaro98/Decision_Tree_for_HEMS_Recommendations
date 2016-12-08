# coding: utf-8

'''
1. [] Building Decision Tree (DT) Model from past Tenki and HEMS data
  1. [X] Make Decision Table
  2. [X] Make Decision Tree

2. Decide to deliver the contents using the DT Model and the today's Tenki data
  1. [] Get the today's Tenki data
  1. [] Give the decision flags
'''

from . import utils


class RecommnedationDecisionTree:
    def __init__(self, start_train_dt, end_train_dt, ac_logs_list, target_hour):
        # get args
        self.start_train_dt = start_train_dt
        self.end_train_dt = end_train_dt
        self.ac_logs_list = ac_logs_list
        self.target_hour = target_hour

        # TODO: インスタンス化でどこまでデータを整えるか

        # process making lists
        self.X_data_list = self._ret_X_data_list()
        self.Y_data_list = self._ret_Y_data_list()

        # get Decision Tree
        self.clf = self._ret_trained_DT_clf()

    def _ret_X_data_list(self):
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
        X_data_list = utils.ret_outer_data_list(
            start_dt=self.start_train_dt,
            end_dt=self.end_train_dt
        )
        return X_data_list

    def _ret_Y_data_list(self):
        '''
        Y data (label data) is HEMS data

        example list to make
        [
          [datetime(2016, 7, 1), 0]
          [datetime(2016, 7, 2), 1]
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
                    ret_list[last_1label_index][1] = 1
        # 最終日の日付越えてもonであったとき
        if on_operationg_flag:
            if on_timestamp.hour <= self.target_hour <= 23:
                # Get the list index
                last_1label_index = date_list.index(on_timestamp.date())
                # 対象時刻にonであった日付インデックスを1にする
                ret_list[last_1label_index][1] = 1
        return ret_list

    def _ret_decision_table(self):
        """
        学習用の訓練データ、訓練ラベルのリストを返す
        そのとき、学習用のx，yの長さが同じであるか
        スタートの日付が同じであるかを確認する
        """
        # check if the start date is same
        if not self.X_data_list[0][0] == self.Y_data_list[0][0]:
            raise Exception('X list Y list start_date Different Error!')

        # slice except datetime
        x = [row[1:] for row in self.X_data_list]
        y = [row[1] for row in self.Y_data_list]

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

    def get_pred_X(self):
        """
        翌日の天気情報を取得する

        make self.pred_X (ndarray)

        self.pred_X
        [
            [datetime(2016, 12, 24), 1.0, 14.2, 4.2, 35.2, 0.0],
        ]
        convert ndarray
        """
        pred_X = [datetime(2016, 12, 24), 1.0, 14.2, 4.2, 35.2, 0.0]
        pass

    def ret_decision_flags(self):
        """
        self.clf.predict(self.pred_X)
        """
        pass
