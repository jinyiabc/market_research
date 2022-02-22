import pandas as pd

from src.helper.bond import bond_yield, bond_price, hpr_received_coupons, hpr_coupon_amounts, hpr_coupon_horizon_value, \
    hpr_horizon_bond_price, hpr_total_future_value, hpr_return, time_factors, present_value
from collections import namedtuple


def test0():
    bond_b_coupon_schedule = [(2022, 6, 30),
                              (2023, 6, 30),
                              (2024, 6, 30),
                              (2025, 6, 30),
                              (2026, 6, 30),
                              (2027, 6, 30),
                              (2028, 6, 30),
                              (2029, 6, 30),
                              (2030, 6, 30),
                              (2031, 6, 30)]

    current_bond_price = bond_price((2022, 1, 28),
                                    bond_b_coupon_schedule,
                                    0.0556,
                                    1,
                                    100,
                                    (2021, 6, 30),
                                    0.055584,clean=True)
    print(current_bond_price)  # 99.9748

    bond_present_value = present_value((2022, 1, 27), bond_b_coupon_schedule, 0.0556,
                  1, 100, 0.055584,)
    print(bond_present_value)

    time_factors0 = time_factors((2022, 1, 27),
                                 bond_b_coupon_schedule,
                                 1, convention='act_isda')
    print( [round(x, 5) for x in time_factors0])
    time_factors0 = time_factors((2022, 1, 27),
                                 bond_b_coupon_schedule,
                                 1, convention='d30360e')
    print( [round(x, 5) for x in time_factors0])

    pass
def test1():
    # The observed market value of the bond that we are calculating the yield for
    price = 112.637

    # NOTICE: Bond yield and name is no longer an entry.
    Bond_Data = namedtuple("Bond_Data",
                           """ 
                           coupon_schedule, 
                           coupon_rate, 
                           coupon_freq, 
                           face,  
                           prev_coupon""")

    corp_5_2026_coupon_schedule = [(2022, 9, 1),
                                   (2023, 9, 1),
                                   (2024, 9, 1),
                                   (2025, 9, 1),
                                   (2026, 9, 1)]

    corp_5_2026 = Bond_Data(corp_5_2026_coupon_schedule,
                            0.05,
                            1,
                            100,
                            (2021, 9, 1))

    settlement_date = (2021, 9, 1)

    bond_yield(settlement_date, *corp_5_2026, price, precision=12, show_stats=True)



def test2():
    settlement_date = (2021, 9, 1)

    horizon_date = (2022, 9, 1)

    bond_a_coupon_schedule_at_settle = [(2022, 9, 1),
                                        (2023, 9, 1),
                                        (2024, 9, 1)]

    bond_a_at_settle = (bond_a_coupon_schedule_at_settle, 0.06, 1, 100, (2021, 9, 1))

    bond_a_settle_px = bond_price(settlement_date, *bond_a_at_settle, 0.0625)

    # bond_a_settle_px

    bond_a_coupon_schedule_at_horizon = [(2023, 9, 1), (2024, 9, 1)]

    bond_a_at_horizon = (bond_a_coupon_schedule_at_horizon, 0.06, 1, 100, (2022, 9, 1))

    bond_a_horizon_px = bond_price(horizon_date, *bond_a_at_horizon, 0.05375)  # 2-year yield

    # bond_a_horizon_px

    bond_b_coupon_schedule_at_settle = [(2022, 9, 1),
                                        (2023, 9, 1),
                                        (2024, 9, 1),
                                        (2025, 9, 1),
                                        (2026, 9, 1),
                                        (2027, 9, 1),
                                        (2028, 9, 1)]

    bond_b_at_settle = (bond_b_coupon_schedule_at_settle, 0.06, 1, 100, (2021, 9, 1))

    bond_b_settle_px = bond_price(settlement_date, *bond_b_at_settle, 0.0652)

    # bond_b_settle_px

    bond_b_coupon_schedule_at_horizon = [(2023, 9, 1),
                                         (2024, 9, 1),
                                         (2025, 9, 1),
                                         (2026, 9, 1),
                                         (2027, 9, 1),
                                         (2028, 9, 1)]

    bond_b_at_horizon = (bond_b_coupon_schedule_at_horizon, 0.06, 1, 100, (2022, 9, 1))

    bond_b_horizon_px = bond_price(horizon_date, *bond_b_at_horizon, 0.0651)  # 6-year yield

    # bond_b_horizon_px

    bond_a_price_return = bond_a_horizon_px / bond_a_settle_px - 1
    bond_b_price_return = bond_b_horizon_px / bond_b_settle_px - 1

    print(f'Bond A Price Return: {round(bond_a_price_return, 6) * 100}%')
    print(f'Bond B Price Return: {round(bond_b_price_return, 6) * 100}%')

def test3():
    settlement_date = (2021, 9, 1)
    horizon_date = (2023, 9, 1)

    bond_b_coupon_schedule = [(2022, 9, 1),
                              (2023, 9, 1),
                              (2024, 9, 1),
                              (2025, 9, 1),
                              (2026, 9, 1),
                              (2027, 9, 1),
                              (2028, 9, 1)]

    bond_b = (bond_b_coupon_schedule, 0.06, 1, 100, (2021, 9, 1))
    print(hpr_received_coupons(settlement_date, bond_b_coupon_schedule, horizon_date))
    print(hpr_coupon_amounts(settlement_date, bond_b_coupon_schedule, horizon_date, 0.06, 1, 100))
    print(hpr_coupon_horizon_value(settlement_date, bond_b_coupon_schedule, horizon_date, 0.06, 1, 100, 0.09))
    print(hpr_horizon_bond_price(settlement_date, horizon_date, *bond_b, 0.06))
    print(hpr_total_future_value(settlement_date, horizon_date, *bond_b, 0.06, 0.05))
    print(hpr_return(settlement_date, horizon_date, *bond_b, 0.0652, 0.065, 0.05))
    pass

def test4():
    settlement_date = (2021, 9, 1)
    horizon_date = (2023, 9, 1)

    bond_b_coupon_schedule = [(2022, 9, 1),
                              (2023, 9, 1),
                              (2024, 9, 1),
                              (2025, 9, 1),
                              (2026, 9, 1),
                              (2027, 9, 1),
                              (2028, 9, 1)]

    # coupon dates, coupon rate, coupon freq, face, previous coupon
    bond_b = (bond_b_coupon_schedule, 0.06, 1, 100, (2021, 9, 1))
    index = ['3%', '4%', '5%', '6%', '7%', '8%', '9%']
    columns = ['3%', '4%', '5%', '6%', '7%', '8%', '9%']

    scenario_inputs = pd.DataFrame([
        [(0.03, 0.03), (0.03, 0.04), (0.03, 0.05), (0.03, 0.06), (0.03, 0.07), (0.03, 0.08), (0.03, 0.09)],
        [(0.04, 0.03), (0.04, 0.04), (0.04, 0.05), (0.04, 0.06), (0.04, 0.07), (0.04, 0.08), (0.04, 0.09)],
        [(0.05, 0.03), (0.05, 0.04), (0.05, 0.05), (0.05, 0.06), (0.05, 0.07), (0.05, 0.08), (0.05, 0.09)],
        [(0.06, 0.03), (0.06, 0.04), (0.06, 0.05), (0.06, 0.06), (0.06, 0.07), (0.06, 0.08), (0.06, 0.09)],
        [(0.07, 0.03), (0.07, 0.04), (0.07, 0.05), (0.07, 0.06), (0.07, 0.07), (0.07, 0.08), (0.07, 0.09)],
        [(0.08, 0.03), (0.08, 0.04), (0.08, 0.05), (0.08, 0.06), (0.08, 0.07), (0.08, 0.08), (0.08, 0.09)],
        [(0.09, 0.03), (0.09, 0.04), (0.09, 0.05), (0.09, 0.06), (0.09, 0.07), (0.09, 0.08), (0.09, 0.09)]
    ], columns=columns, index=index)

    scenario_fv = scenario_inputs.applymap(lambda x: round(hpr_total_future_value(settlement_date,
                                                                            horizon_date,
                                                                            *bond_b,
                                                                            x[1], # horizon yield
                                                                            x[0] # re-investment rate
                                                                           ),4)) #rounded to 4 dp

    print(scenario_fv)

    scenario_returns = scenario_inputs.applymap(lambda x: str(round(100 * hpr_return(settlement_date,
                                                                                     horizon_date,
                                                                                     *bond_b,
                                                                                     0.0652,
                                                                                     x[1],  # horizon yield
                                                                                     x[0]  # re-investment rate
                                                                                     ), 2)) + "%")

    print(scenario_returns)
