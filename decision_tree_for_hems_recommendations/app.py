# coding: utf-8

'''
1. [] Building Decision Tree (DT) Model from past Tenki and HEMS data
  1. [] Make Decision Table
  2. [] Make Decision Tree

2. Decide to deliver the contents using the DT Model and the today's Tenki data
  1. [] Get the today's Tenki data
  1. [] Give the decision flags
'''

from . import utils


class RecommnedationDecisionTree:
    def __init__(self, start_train_dt, end_train_dt):
        self.start_train_dt = start_train_dt
        self.end_train_dt = end_train_dt
        self.X_data_list = self._ret_X_data_list()

    def _ret_X_data_list(self):
        '''
        Tenki data

        list to make
	[
	    [datetime(2016, 7, 1) 1.0, 31.0, 25.0, 77.2, 0.0],
	    [datetime(2016, 7, 2) 1.0, 29.8, 24.8, 70.2, 0.0],
	    .
	    .
	    .
	    [datetime(2016, 8, 15) 1.0, 31, 25, 73.2, 0.0],
	]
        date_list, weekday_list, max_temperature_list, min_temperature_list, ave_humidity_list, day_tenki_list

        '''
        X_data_list = utils.ret_outer_data_list(
            start_dt=self.start_train_dt,
            end_dt=self.end_train_dt
        )
        return X_data_list

    def _make_Y_data(self):
        '''
        HEMS data
        '''
        pass

    def make_decision_table(self):
        '''
        X_data
        [
          [],
          [],
          [],
          [],
        ]

        Y_data
        [
          0,
          0,
          0,
          0,
        ]
        '''
        pass

    def make_decision_tree(self):
        pass

    def get_the_predicted_tenki_data(self):
        pass

    def ret_the_decision_flags(self):
        pass
