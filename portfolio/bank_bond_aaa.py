import pandas as pd
from datetime import datetime, date
from src.helper.bond import hpr_received_coupons, hpr_coupon_amounts, hpr_coupon_horizon_value, hpr_horizon_bond_price, \
    hpr_total_future_value, hpr_return, time_factors, bond_price, present_value, cash_flows, discount_factors


def date_manipulate(x):
    x = datetime.strptime(x, '%m月%d日')
    return x

if __name__ == '__main__':
    """
    Assumption: Yield Curve do not change during holding period.
    """

    commercial_bank_chinabond = pd.read_csv('../resource/商业银行债券0128.CSV',
                                            parse_dates=['Coupon Date (Y)\r\n[N] 1'],
                                            date_parser=date_manipulate,
                                            )
    bond_icbc = commercial_bank_chinabond.iloc[0]
    """
    INFORMATION
            Symbol                                                                            1105001.IB
            Short Name                                                                ICBC 5.56% B310630
            Close (D)\r\n[Trade Date] Last Closing Day\r\n[Price Type] Dirty Price              103.1889
            Bid Yield (Optimal)\r\n[Trade Date] Last Closing Day\r\n[Unit] %                         NaN
            Initial Face Value                                                                     100.0
            Latest Bond Rating                                                                       AAA
            Maturity Date                                                                     2031-06-30
            Coupon Type                                                            Fixed Interest Rate
            Interest Accrual Method                                                 Simple interest
            Coupon Description                                                    5.56%
            Coupon Frequency                                                        1
            Coupon Date (Y)\r\n[N] 1                                             6月30日
            Bond Term (Year)\r\n[Unit] Yearly                                    20.0
            Maturities (Text)                                                     15+5
            Interest Reference                                                     ACT/ACT
            Coupon Date Description           Pay interest on June 30 every year, and postpo...
            Bond Term (Year)\r\n[Unit] Yearly.1                                     20.0
            Issue Amount\r\n[Unit] (100M)                                           380.0
            Remaing Maturity                                                         9.41
    """

    # today = date.today()
    # coupon_date = bond_icbc['Coupon Date (Y)\r\n[N] 1']
    # maturity_date = bond_icbc['Maturity Date']
    # bond_b_coupon_schedule = pd.date_range(start=settlement_date, end=maturity_date, freq='y')
    settlement_date = (2022, 1, 27)
    horizon_date = (2023, 1, 27)
    coupon_rate = 0.0556
    coupon_freq = 1
    prev_coupon = (2021, 6, 30)
    reinvestment_rate = 0.024666    # forward raet (1, 8)
    bond_horizon_yld = 0.055584     # assumption
    bond_settle_yld = 0.055584
    yield_curve = []
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

    bond_b = (bond_b_coupon_schedule, coupon_rate, coupon_freq, 100, prev_coupon)
    print(hpr_received_coupons(settlement_date, bond_b_coupon_schedule, horizon_date))   # [(2022, 6, 30), (2023, 6, 30), (2024, 6, 30)]
    print(hpr_coupon_amounts(settlement_date, bond_b_coupon_schedule, horizon_date, coupon_rate, 1, 100)) # [6.0, 6.0, 6.0]
    print(hpr_coupon_horizon_value(settlement_date, bond_b_coupon_schedule, horizon_date, coupon_rate, 1, 100, reinvestment_rate)) # 8 year yield.
    print(hpr_horizon_bond_price(settlement_date, horizon_date, *bond_b, 0.0556)) # 100
    print(hpr_total_future_value(settlement_date, horizon_date, *bond_b, 0.06, 0.05)) # 115.071652
    print(hpr_return(settlement_date, horizon_date, *bond_b, bond_settle_yld, bond_horizon_yld, reinvestment_rate)) # 0.07947168342801092

