from src.helper.bond import time_factors


def test_d30360e():
    settlement_date = (2018, 12, 15)
    coupon_schedule = [(2019,3,1),
                       (2020,3,1),
                       (2021,3,1),
                       (2022,3,1),
                       (2023,3,1)]
    coupon_freq = 1
    time_factors0 = time_factors(settlement_date,
                                     coupon_schedule,
                                     coupon_freq, convention='d30360e')
    print(time_factors0)   # 0.2111111111111111
    assert  time_factors0[0] == 0.2111111111111111

def test_act_isda():
    settlement_date = (2018, 12, 15)
    coupon_schedule = [(2019,3,1),
                       (2020,3,1),
                       (2021,3,1),
                       (2022,3,1),
                       (2023,3,1)]
    coupon_freq = 1
    time_factors0 = time_factors(settlement_date,
                                     coupon_schedule,
                                     coupon_freq, convention='act_isda')
    print(time_factors0)   # 0.2054794520547945
    assert time_factors0[0] == 0.2054794520547945

def test_act_afb():
    settlement_date = (2018, 12, 15)
    coupon_schedule = [(2019,3,1),
                       (2020,3,1),
                       (2021,3,1),
                       (2022,3,1),
                       (2023,3,1)]
    coupon_freq = 1
    time_factors0 = time_factors(settlement_date,
                                     coupon_schedule,
                                     coupon_freq, convention='act_afb')  #  unexpected keyword argument 'matu'
    print(time_factors0)   # 0.2054794520547945
    assert time_factors0[0] == 0.2054794520547945

def test_30365():
    settlement_date = (2018, 12, 15)
    coupon_schedule = [(2019,3,1),
                       (2020,3,1),
                       (2021,3,1),
                       (2022,3,1),
                       (2023,3,1)]
    coupon_freq = 1
    time_factors0 = time_factors(settlement_date,
                                     coupon_schedule,
                                     coupon_freq, convention='30365')  #  unexpected keyword argument 'matu'
    print(time_factors0)   # 0.20821917808219179
    assert time_factors0[0] == 0.20821917808219179

def test_default():
    settlement_date = (2018, 12, 15)
    coupon_schedule = [(2019,3,1),
                       (2020,3,1),
                       (2021,3,1),
                       (2022,3,1),
                       (2023,3,1)]
    coupon_freq = 1
    time_factors0 = time_factors(settlement_date,
                                     coupon_schedule,
                                     coupon_freq)
    print(time_factors0)   # 0.2111111111111111
    assert  time_factors0[0] == 0.2111111111111111