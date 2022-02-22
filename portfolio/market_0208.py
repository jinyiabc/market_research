from time import time

import math

import os

import pandas as pd
from datetime import datetime, date
import QuantLib as ql


def date_manipulate(x):
    x = datetime.strptime(x, '%m月%d日')
    return x


def p2f(x):
    return float(x.strip('%')) / 100


def d2q(x):
    day = int(x.split('/')[1])
    year = int(x.split('/')[2])
    month = int(x.split('/')[0])
    return ql.Date(day, month, year)


if __name__ == '__main__':

    """
    GLOBAL SETTINGS
    """
    calculation_date = ql.Date(8, 2, 2022)
    ql.Settings.instance().evaluationDate = calculation_date
    # # 上海清算所商业银行债收益率曲线(AAA) latest
    spot_dates = [ql.Date(27, 1, 2022),
                  ql.Date(27, 2, 2022),
                  ql.Date(27, 4, 2022),
                  ql.Date(27, 7, 2022),
                  ql.Date(27, 10, 2022),
                  ql.Date(27, 1, 2023),
                  ql.Date(27, 1, 2024),
                  ql.Date(27, 1, 2025),
                  ql.Date(27, 1, 2026),
                  ql.Date(27, 1, 2027),
                  ql.Date(27, 1, 2028),
                  ql.Date(27, 1, 2029),
                  ql.Date(27, 1, 2030),
                  ql.Date(27, 1, 2031),
                  ql.Date(27, 1, 2032),
                  ]
    spot_rates = [
        # 上海清算所商业银行债收益率曲线(AAA) 1-27
        1.856 / 100,
        2.1 / 100,
        2.28 / 100,
        2.33 / 100,
        2.3938 / 100,
        2.43 / 100,
        2.6169 / 100,
        2.7137 / 100,
        2.8233 / 100,
        3.0527 / 100,
        3.2245 / 100,
        3.335 / 100,
        3.4266 / 100,
        3.4674 / 100,
        3.5211 / 100,
    ]
    # spread = 0.0  # 0.6/ 100
    # spot_rates = [x + spread for x in spot_rates]
    # risk_free_rate = 0.01
    # day_count = ql.Actual365Fixed()
    #
    # discount_curve = ql.YieldTermStructureHandle(
    #     ql.FlatForward(calculation_date, risk_free_rate, day_count)
    # )

    """
    Assumption: Yield Curve do not change during holding period.
    """
    commercial_bank_chinabond = pd.read_csv(f'../resource/SSE-TRADED-BONDS0209.CSV',
                                            parse_dates=['COUPON_DATE'],
                                            date_parser=date_manipulate,
                                            )
    length = len(commercial_bank_chinabond)
    calculated_dirty_price = []
    fv_bond = []
    pv_bond = []
    for i in range(length):
        ticker = commercial_bank_chinabond.iloc[i]
        coupon_rate = p2f(ticker['Coupon Description'])  # 0.0556

        # generate schedule

        issue_date = d2q(ticker['Dated Date'])  # ql.Date(30, 6, 2011)
        maturity_date = d2q(ticker['Maturity Date'])  # ql.Date(30, 6, 2031)
        tenor = ql.Period(ql.Annual)
        calendar = ql.China()
        convention = ql.Following
        terminationDateConvention = ql.Following
        rule = ql.DateGeneration.Forward
        month_end = False
        schedule = ql.Schedule(issue_date, maturity_date, tenor,
                               calendar, convention,
                               terminationDateConvention, rule,
                               month_end)
        settlementDays = 1
        dc = ql.ActualActual()
        fixed_leg = ql.FixedRateLeg(schedule, dc, [100], [coupon_rate])
        bond = ql.Bond(settlementDays, ql.TARGET(), issue_date, fixed_leg)


        # day_count = ql.ActualActual()
        # interpolation = ql.Linear()
        compounding = ql.Compounded
        compounding_frequency = ql.Annual

        spot_curve = ql.NaturalCubicZeroCurve(spot_dates, spot_rates, dc, calendar, )   # 116.63027293435499
        spot_curve_handle = ql.YieldTermStructureHandle(spot_curve)
        bond_engine = ql.DiscountingBondEngine(spot_curve_handle)
        bond.setPricingEngine(bond_engine)
        # print(bond.cleanPrice())
        # print(bond.NPV())
        # print(bond.dirtyPrice())
        leg = ql.Leg(bond.cashflows())
        # print([(x.date(), x.amount()) for x in leg.iterator()])
        yts = spot_curve_handle
        # for date in [x.date() for x in bond.cashflows()]:
        #     if date > today and date < today + ql.Period(1, ql.Years):
        #         settlementDate = date
        #         break;
        # if settlementDate < today or settlementDate >= today + ql.Period(1, ql.Years):
        #     settlementDate = today
        # while settlementDate is None:
        #     time(5)
        settlement_date = calculation_date
        npvDate = calculation_date + ql.Period(1, ql.Years)
        # print(settelmentDate)
        fv_bond.append(ql.CashFlows.npv(leg, yts, True, settlement_date, npvDate))
        pv_bond.append(ql.CashFlows.npv(leg, yts, True, settlement_date, calculation_date))
        calculated_dirty_price.append(bond.dirtyPrice())

    commercial_bank_chinabond['fv_bond'] = pd.Series(fv_bond)
    commercial_bank_chinabond['pv_bond'] = pd.Series(pv_bond)
    commercial_bank_chinabond['calculated_dirty_price'] = pd.Series(calculated_dirty_price)
    # commercial_bank_chinabond['zero_curve_clean_price'] = pd.Series(zero_curve_clean_price)
    # commercial_bank_chinabond['log_linear_clean_price'] = pd.Series(log_linear_clean_price)

    df2 = commercial_bank_chinabond.loc[:,
          ['Symbol', 'Latest Bond Rating', 'Coupon Description', \
           'calculated_dirty_price','FULL','fv_bond' \
           ]].to_csv(f'../resource/SSE-TRADED-BONDS0209_valuation.csv')

    # Result: Three valuation method calculate closely with value from SHCH: Shanghai Clearing House.
    # zero_curve_clean_price, cubic_zero_curve_clean_price,natural_cubic_curve_clean_price
