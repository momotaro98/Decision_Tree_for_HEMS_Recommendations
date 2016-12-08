from datetime import datetime as dt
from datetime import timedelta as delta

import numpy as np
from sklearn.tree.tree import DecisionTreeClassifier

import pyowm

from tenkishocho import DayPerMonthTenki


def is_rain_or_not(char):
    '''
    >>> is_rain_or_not('晴時々曇')
    0.0
    >>> is_rain_or_not('曇一時雨')
    1.0
    '''
    if '雨' in char:
        return 1.0
    elif 'みぞれ' in char:
        return 1.0
    elif '雪' in char:
        return 1.0
    return 0.0


def ret_outer_data_list(start_dt, end_dt):
    '''
    Tenki data

    example list to make
    [
        [datetime(2016, 7, 1) 1.0, 31.0, 25.0, 77.2, 0.0],
        [datetime(2016, 7, 2) 1.0, 29.8, 24.8, 70.2, 0.0],
        .
        .
        .
        [datetime(2016, 8, 15) 1.0, 31, 25, 73.2, 0.0],
    ]
    date_list, weekday_list, max_temperature_list, min_temperature_list, ave_humidity_list, day_tenki_list

    >>> from datetime import datetime as df
    >>> start_dt = dt(2016, 7, 31)
    >>> end_dt = dt(2016, 8, 1)
    >>> ret_outer_data_list(start_dt, end_dt)
    [[datetime.date(2016, 7, 31), 1.0, 30.8, 24.4, 60.0, 1.0], [datetime.date(2016, 8, 1), 0.0, 31.5, 24.6, 60.0, 1.0]]
    '''

    """
    if start_dt.year != end_dt.year:
        raise Exception('start_dt year and end_dt year must be same.')
    """
    # stat_dt = dt(year=year, month=month, day=1)
    stat_dt = start_dt
    date_list = []
    weekday_list = []
    while stat_dt <= end_dt:
        # 日付リスト作成
        date_list.append(stat_dt.date())
        # 平日休日リスト作成
        # 平日:'w', 休日:'h'
        wd = stat_dt.weekday()  # 曜日取得
        if 0 <= wd <= 4:
            # weekday_list.append('w')
            weekday_list.append(0.0)
        elif 5 <= wd <= 6:
            # weekday_list.append('h')
            weekday_list.append(1.0)
        stat_dt += delta(days=1)

    # tenkishocho モジュールを取得
    dpmt_list = [DayPerMonthTenki(start_dt.year, month) \
        for month in range(start_dt.month, end_dt.month + 1)]
    # Causion: ↑は年越しに対応していない

    max_temperature_list = []
    min_temperature_list = []
    ave_humidity_list = []
    day_tenki_list = []
    for index, dpmt in enumerate(dpmt_list):
        if index == 0:
            first_month_flag = True
        else:
            first_month_flag = False

        if index == len(dpmt_list) - 1:
            end_month_flag = True
        else:
            end_month_flag = False

        # 最高気温
        for day, v in dpmt.get_max_temperature().items():
            if first_month_flag and day < start_dt.day:
                continue
            if end_month_flag and day > end_dt.day:
                break
            max_temperature_list.append(v)

        # 最低気温
        for day, v in dpmt.get_min_temperature().items():
            if first_month_flag and day < start_dt.day:
                continue
            if end_month_flag and day > end_dt.day:
                break
            min_temperature_list.append(v)

        # 平均湿度
        for day, v in dpmt.get_ave_humidity().items():
            if first_month_flag and day < start_dt.day:
                continue
            if end_month_flag and day > end_dt.day:
                break
            ave_humidity_list.append(v)

        # 日中天候
        for day, v in dpmt.get_day_tenki().items():
            if first_month_flag and day < start_dt.day:
                continue
            if end_month_flag and day > end_dt.day:
                break
            day_tenki_list.append(is_rain_or_not(v))

    # check the length
    if len(date_list) != len(max_temperature_list):
        print('len(date_list)', len(date_list))
        print('len(max_temperature_list)', len(max_temperature_list))
        raise Exception('これからzipしていくリストの長さが違うでよ')

    ret_list = [[c1, c2, c3, c4, c5, c6] for c1, c2, c3, c4, c5, c6 in zip(
        date_list,
        weekday_list,
        max_temperature_list,
        min_temperature_list,
        ave_humidity_list,
        day_tenki_list
    )]

    return ret_list


def ret_date_list(start_dt, end_dt):
    stat_dt = start_dt
    ret_list = []
    while stat_dt <= end_dt:
        # 日付リスト作成
        ret_list.append(stat_dt.date())
        stat_dt += delta(days=1)
    return ret_list


def be_ndarray(x):
    return np.array(x)


def ret_trained_DT_clf(X, Y):
    clf = DecisionTreeClassifier(max_depth=3)
    clf.fit(X, Y)
    return clf


def ret_predicted_outer_data_list(OWM_API_KEY, target_date=dt.now().date()):
    '''
    Tenki data

    example list to make
    [1.0, 31.0, 25.0, 77.2, 0.0],
    weekday_list, max_temperature_list, min_temperature_list, ave_humidity_list, day_tenki_list
    '''

    # 平日休日 weekday
    wd = target_date.weekday()  # 曜日取得
    '''
    if 0 <= wd <= 4:
        # weekday = 'w'
        weekday = 0.0
    elif 5 <= wd <= 6:
        # weekday = 'h'
        weekday = 1.0
    '''
    weekday = 0.0 if 0 <= wd <= 4 else 1.0

    # Instanciate owm and weather
    owm = pyowm.OWM(OWM_API_KEY)
    observation = owm.weather_at_place('Tokoyo,jp')
    weather = observation.get_weather()

    # 最大気温 temp_max
    temp_max = weather.get_temperature('celsius')['temp_max']

    # 最低気温 temp_min
    temp_min = weather.get_temperature('celsius')['temp_min']

    # 平均湿度 humidity_ave
    humidity_ave = weather.get_humidity()

    # 日中天候 tenki
    w_icon = weather.get_weather_icon_name()
    sunnuy_icon_tupple = (
        '01d', '01n',
        '02d', '02n',
        '03d', '03n',
        '04d', '04n',
    )
    rainy_icon_tupple = (
        '09d', '09n',
        '10d', '10n',
        '11d', '11n',
        '12d', '12n',
        '13d', '13n',
        '50d', '50n',
    )
    tenki = 0.0 if w_icon in sunnuy_icon_tupple else 1.0

    # make ret_list
    ret_list = [weekday, temp_max, temp_min, humidity_ave, tenki]

    return ret_list
